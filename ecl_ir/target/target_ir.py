from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
import re
from typing import Any

from ..analysis.bullet_ir import active_difficulty_lanes, analyze_bullet_module
from ..dialects.game_profile import (
    CAP_BULLET_MANAGER,
    CAP_TRANSFORM_APPEND,
    CAP_TRANSFORM_INDEXED_REPLACE,
    MACRO_MODES,
    profile_for_game,
)
from .lowering import (
    BackendEmission,
    CapabilityDecision,
    DiagnosticSeverity,
    LoweringDiagnostic,
    LoweringPlanner,
    LoweringResult,
    LoweringStrategy,
    identity_instruction_text,
)
from ..canonical.semantic_ir import DIFFICULTY_LANES, DifficultyGuard, SemanticModule, SemanticNode
from ..canonical.semantic_ir import SemanticOperation
from ..dialects.semantics import (
    bullet_shape_can_encode,
    bullet_shape_is_lossy,
    bullet_shape_semantic,
    encode_bullet_shape,
)
from ..analysis.spread_ir import format_float_literal, parse_float_literal
from ..analysis.transform_ir import BulletTransformIR


@dataclass(frozen=True)
class TargetStatement:
    source_node_id: str
    strategy: LoweringStrategy
    lines: tuple[str, ...]
    guard: DifficultyGuard
    diagnostics: tuple[LoweringDiagnostic, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_node_id": self.source_node_id,
            "strategy": self.strategy.value,
            "lines": list(self.lines),
            "guard": self.guard.to_dict(),
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class TargetRoutine:
    name: str
    params: str
    body: tuple[TargetStatement, ...]
    params_inferred: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "params": self.params,
            "params_inferred": self.params_inferred,
            "body": [statement.to_dict() for statement in self.body],
        }


def reconcile_inferred_parameter_declarations(
    body: tuple[TargetStatement, ...],
    params: str,
) -> tuple[TargetStatement, ...]:
    """Remove source `var` aliases that an inferred signature promotes to parameters."""

    param_names = {
        part.strip().split()[-1]
        for part in params.split(",")
        if part.strip()
    }
    if not param_names:
        return body

    var_re = re.compile(r"^(\s*)var\s+(.+?)\s*;\s*$")
    reconciled: list[TargetStatement] = []
    for statement in body:
        lines: list[str] = []
        for line in statement.lines:
            match = var_re.match(line)
            if match is None:
                lines.append(line)
                continue
            kept = [
                item.strip()
                for item in match.group(2).split(",")
                if item.strip() and item.strip().split()[-1] not in param_names
            ]
            if kept:
                lines.append(f"{match.group(1)}var {', '.join(kept)};")
        reconciled.append(replace(statement, lines=tuple(lines)))
    return tuple(reconciled)


@dataclass(frozen=True)
class TargetModule:
    source: str
    source_game: str
    target_game: str
    target_generation: str
    resources: dict[str, list[str]]
    top_level: tuple[TargetStatement, ...]
    routines: tuple[TargetRoutine, ...]
    diagnostics: tuple[LoweringDiagnostic, ...]

    def strategy_counts(self) -> dict[str, int]:
        statements = [
            *self.top_level,
            *(statement for routine in self.routines for statement in routine.body),
        ]
        counts = Counter(statement.strategy.value for statement in statements)
        return {strategy.value: counts.get(strategy.value, 0) for strategy in LoweringStrategy}

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "th062.target-ir",
            "schema_version": 1,
            "source": self.source,
            "source_game": self.source_game,
            "target_game": self.target_game,
            "target_generation": self.target_generation,
            "resources": self.resources,
            "top_level": [statement.to_dict() for statement in self.top_level],
            "routines": [routine.to_dict() for routine in self.routines],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "strategy_counts": self.strategy_counts(),
        }

    def render_decl(self) -> str:
        counts = self.strategy_counts()
        rendered_counts = ", ".join(f"{name}={count}" for name, count in counts.items())
        lines = [
            f"// source: {self.source}",
            f"// source game: {self.source_game}",
            f"// target: {self.target_game}",
            f"// canonical lowering plan: {rendered_counts}; diagnostics={len(self.diagnostics)}",
        ]
        lines.extend(
            (
                f"// [{diagnostic.code}] routine={diagnostic.routine or '<module>'}: "
                f"{diagnostic.message}"
            )
            for diagnostic in self.diagnostics
            if diagnostic.node_id is None
        )
        for resource, entries in self.resources.items():
            quoted = "; ".join(f'"{entry}"' for entry in entries)
            lines.append(f"{resource} {{ {quoted}; }}")
        lines.extend(render_target_statements(self.top_level, indent=""))
        for routine in self.routines:
            lines.append("")
            header = (
                f"sub {routine.name}()"
                if self.target_generation == "first"
                else f"void {routine.name}({routine.params})"
            )
            lines.extend([header, "{"])
            lines.extend(render_target_statements(routine.body, indent="    "))
            lines.append("}")
        return "\n".join(lines) + "\n"


@dataclass(frozen=True, slots=True)
class LegacyMacroRandomRanges:
    """Canonical ranges decoded from legacy macro endpoint operands."""

    angle_center: str | None = None
    angle_half_span: str | None = None
    speed_minimum: str | None = None
    speed_span: str | None = None

    def to_dict(self) -> dict[str, str]:
        return {
            name: value
            for name, value in (
                ("angle_center", self.angle_center),
                ("angle_half_span", self.angle_half_span),
                ("speed_minimum", self.speed_minimum),
                ("speed_span", self.speed_span),
            )
            if value is not None
        }


RANDOM_ANGLE_MACRO_MODES = frozenset({"random_angle", "random_angle_speed"})
RANDOM_SPEED_MACRO_MODES = frozenset({"random_speed", "random_angle_speed"})


def decode_legacy_macro_random_ranges(
    mode_semantic: str,
    encoded_args: list[str],
) -> LegacyMacroRandomRanges | None:
    """Decode literal legacy endpoints into target-independent random ranges.

    Legacy modes 6/8 store two angle endpoints, while manager modes 6/8
    consume a center and half-span.  Legacy modes 7/8 store two speed
    endpoints, while manager modes 7/8 consume a minimum/base and a positive
    span.  Dynamic endpoints need typed expression lowering and are rejected.
    """

    if len(encoded_args) != 9 or mode_semantic not in (
        RANDOM_ANGLE_MACRO_MODES | RANDOM_SPEED_MACRO_MODES
    ):
        return None

    angle_center: str | None = None
    angle_half_span: str | None = None
    speed_minimum: str | None = None
    speed_span: str | None = None
    if mode_semantic in RANDOM_ANGLE_MACRO_MODES:
        first_angle = parse_float_literal(encoded_args[6])
        second_angle = parse_float_literal(encoded_args[7])
        if first_angle is None or second_angle is None:
            return None
        angle_center = format_float_literal((first_angle + second_angle) / 2.0)
        angle_half_span = format_float_literal(abs(first_angle - second_angle) / 2.0)
    if mode_semantic in RANDOM_SPEED_MACRO_MODES:
        first_speed = parse_float_literal(encoded_args[4])
        second_speed = parse_float_literal(encoded_args[5])
        if first_speed is None or second_speed is None:
            return None
        speed_minimum = format_float_literal(min(first_speed, second_speed))
        speed_span = format_float_literal(abs(first_speed - second_speed))
    return LegacyMacroRandomRanges(
        angle_center=angle_center,
        angle_half_span=angle_half_span,
        speed_minimum=speed_minimum,
        speed_span=speed_span,
    )


def parse_integer_literal(value: object) -> int | None:
    text = str(value).strip()
    if not re.fullmatch(r"[-+]?(?:0[xX][0-9a-fA-F]+|\d+)", text):
        return None
    try:
        unsigned = text.lstrip("+-")
        return int(text, 16 if unsigned.lower().startswith("0x") else 10)
    except ValueError:
        return None


class TargetAstBuilder:
    def __init__(self, planner: LoweringPlanner) -> None:
        self.planner = planner

    def build(self, module: SemanticModule) -> TargetModule:
        result = self.planner.plan_module(module)
        signatures = {signature.name: signature.params for signature in module.routine_signatures}
        source_profile = profile_for_game(module.source_game)
        parameter_abi_compatible = (
            result.target_profile.routine_dialect.accepts_parameters_from(
                source_profile.routine_dialect
            )
        )
        top_level, syntax_diagnostics = target_top_level_statements(
            module,
            result,
            result.target_profile.generation,
        )
        routines: list[TargetRoutine] = []
        for source_routine, lowered_routine in zip(module.routines, result.routines):
            body = tuple(
                target_statement(
                    node,
                    decision,
                    result.target_profile.generation,
                    result.target_profile.game,
                )
                for node, decision in zip(source_routine.body, lowered_routine.decisions)
            )
            inferred_params = (
                signatures.get(source_routine.name, "")
                if not source_routine.params
                else ""
            )
            params = source_routine.params or inferred_params
            if inferred_params and parameter_abi_compatible:
                body = reconcile_inferred_parameter_declarations(body, inferred_params)
            routines.append(
                TargetRoutine(
                    name=source_routine.name,
                    params=params,
                    body=body,
                    params_inferred=bool(inferred_params),
                )
            )
        return TargetModule(
            source=module.source,
            source_game=module.source_game,
            target_game=result.target_profile.game,
            target_generation=result.target_profile.generation,
            resources={name: list(entries) for name, entries in module.resources.items()},
            top_level=tuple(top_level),
            routines=tuple(routines),
            diagnostics=(*result.diagnostics, *syntax_diagnostics),
        )


class CanonicalBackendEmitter:
    """State-aware adapter from canonical operations to the legacy text backend."""

    def __init__(self, module: SemanticModule, target_game: str) -> None:
        analysis = analyze_bullet_module(module)
        self.target_profile = profile_for_game(target_game)
        self.transform_indices = {
            node_id: lanes
            for routine in analysis.routines
            for node_id, lanes in routine.resolved_transform_indices.items()
        }
        self.initialized_implicit_manager_lanes: dict[str, set[str]] = {}

    def begin_module(self, _module: SemanticModule) -> None:
        self.initialized_implicit_manager_lanes.clear()

    def __call__(self, node: SemanticOperation, target_game: str) -> BackendEmission | str | None:
        from ..compat.backend import compile_ir_op_emission

        if target_game == node.provenance.game and node.provenance.opcode is not None:
            return BackendEmission(
                identity_instruction_text(
                    node.provenance.opcode,
                    node.encoded_args(),
                    node.selected_values,
                )
            )
        from ..canonical.variable_ir import project_semantic_operation

        projected, variable_issues = project_semantic_operation(node, target_game)
        if projected is None:
            issue = variable_issues[0]
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code=issue.code,
                reason=issue.message,
                details={
                    **issue.details(),
                    "issue_count": len(variable_issues),
                },
            )
        node = projected
        prefix, initialized_lanes, initialization_error = self.implicit_manager_initialization(node)
        if initialization_error is not None:
            return initialization_error
        if node.operation == "bullet.macro.configure":
            lowered = self.lower_macro(node)
            return self.finish_implicit_manager_initialization(node, prefix, initialized_lanes, lowered)
        if node.operation == "bullet.visual.set":
            lowered = self.lower_bullet_visual(node)
            return self.finish_implicit_manager_initialization(node, prefix, initialized_lanes, lowered)
        if node.operation == "bullet.fire.defer" and self.target_profile.supports(CAP_BULLET_MANAGER):
            return self.finish_implicit_manager_initialization(
                node,
                prefix,
                initialized_lanes,
                f"// folded legacy fire defer state at canonical node {node.node_id}",
            )
        if node.operation in {"bullet.fire.enable", "bullet.fire.immediate"} and self.target_profile.supports(CAP_BULLET_MANAGER):
            fire_opcode = self.target_opcode("bullet.fire")
            lowered = f"ins_{fire_opcode}(0);" if fire_opcode is not None else None
            return self.finish_implicit_manager_initialization(node, prefix, initialized_lanes, lowered)
        if node.operation in {"bullet.transform.replace", "bullet.transform.append"}:
            return self.finish_implicit_manager_initialization(
                node,
                prefix,
                initialized_lanes,
                self.lower_transform(node, target_game),
            )
        target_has_append = self.target_profile.supports(CAP_TRANSFORM_APPEND)
        target_has_replace = self.target_profile.supports(CAP_TRANSFORM_INDEXED_REPLACE)
        if (
            node.operation == "bullet.transform.append_cursor.decrement"
            and not target_has_append
            and target_has_replace
        ):
            return self.finish_implicit_manager_initialization(
                node,
                prefix,
                initialized_lanes,
                f"// folded append cursor decrement at canonical node {node.node_id} into later explicit indices",
            )
        return self.finish_implicit_manager_initialization(
            node,
            prefix,
            initialized_lanes,
            compile_ir_op_emission(node, target_game),
        )

    def implicit_manager_initialization(
        self,
        node: SemanticOperation,
    ) -> tuple[str | None, tuple[str, ...], BackendEmission | None]:
        source_profile = profile_for_game(node.provenance.game)
        initializable_operations = {
            "bullet.macro.configure",
            "bullet.fire.defer",
            "bullet.fire.enable",
            "bullet.fire.immediate",
            "bullet.transform.replace",
        }
        if node.operation == "bullet.origin.offset.set" and len(node.operands) == 2:
            initializable_operations.add(node.operation)
        if node.operation == "bullet.sounds.set" and len(node.operands) >= 2:
            initializable_operations.add(node.operation)
        if (
            not source_profile.bullet_dialect.implicit_manager
            or not node.operation.startswith("bullet.")
            or node.operation not in initializable_operations
            or node.operation in {"bullet.clear_all", "bullet.cancel_radius", "bullet.clear_radius"}
            or not self.target_profile.supports(CAP_BULLET_MANAGER)
        ):
            return None, (), None
        routine = node.provenance.routine
        active_lanes = set(active_difficulty_lanes(node.guard))
        initialized = self.initialized_implicit_manager_lanes.setdefault(routine, set())
        missing_lanes = active_lanes - initialized
        if not missing_lanes:
            return None, (), None
        if active_lanes & initialized:
            return (
                None,
                (),
                BackendEmission(
                    text="",
                    strategy=LoweringStrategy.UNSUPPORTED,
                    code="backend.implicit_manager_lane_join",
                    reason=(
                        "implicit source manager reaches target lanes with mixed initialization state; "
                        "lane splitting or a CFG state join is required"
                    ),
                    details={
                        "active_lanes": sorted(active_lanes),
                        "initialized_lanes": sorted(initialized),
                        "missing_lanes": sorted(missing_lanes),
                    },
                ),
            )
        reset_opcode = self.target_opcode("bullet.manager.reset")
        prefix = f"ins_{reset_opcode}(0);" if reset_opcode is not None else None
        return prefix, tuple(sorted(missing_lanes)), None

    def finish_implicit_manager_initialization(
        self,
        node: SemanticOperation,
        prefix: str | None,
        initialized_lanes: tuple[str, ...],
        lowered: BackendEmission | str | None,
    ) -> BackendEmission | str | None:
        joined = join_lowered(prefix, lowered)
        if joined is None or (
            isinstance(joined, BackendEmission)
            and joined.strategy is LoweringStrategy.UNSUPPORTED
        ):
            return joined
        if initialized_lanes:
            self.initialized_implicit_manager_lanes.setdefault(
                node.provenance.routine,
                set(),
            ).update(initialized_lanes)
        return joined

    def target_opcode(self, operation: str) -> int | None:
        candidates = self.target_profile.bullet_dialect.opcodes_for_operation(operation)
        return candidates[0] if candidates else None

    def lower_transform(self, node: SemanticOperation, target_game: str) -> BackendEmission:
        transform = BulletTransformIR.from_semantic_operation(node)
        if transform is None:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.transform.invalid_canonical_form",
                reason="canonical transform operands do not describe a supported transform write",
            )

        resolved_index: int | None = None
        if (
            transform.write_kind == "append"
            and not self.target_profile.supports(CAP_TRANSFORM_APPEND)
            and self.target_profile.supports(CAP_TRANSFORM_INDEXED_REPLACE)
        ):
            lane_indices = self.transform_indices.get(str(node.node_id), {})
            indices = {index for index in lane_indices.values() if index is not None}
            if len(indices) != 1 or any(index is None for index in lane_indices.values()):
                return BackendEmission(
                    text="",
                    strategy=LoweringStrategy.UNSUPPORTED,
                    code="backend.transform_append_index_join",
                    reason=(
                        "append cursor does not resolve to one explicit transform index "
                        "across all active difficulty lanes"
                    ),
                    details={"resolved_indices": dict(lane_indices)},
                )
            resolved_index = next(iter(indices))

        reason = transform.unsupported_reason(target_game, resolved_index)
        lowered = transform.lower_to(target_game, resolved_index)
        if lowered is None:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.transform.unsupported",
                reason=reason or "canonical transform has no verified target encoding",
                details={
                    "source_opcode": transform.source_opcode,
                    "write_kind": transform.write_kind,
                    "parameter_set": transform.parameter_set,
                    "mode_semantic": transform.mode_semantic,
                },
            )
        args = ", ".join(lowered.args)
        lossy_reason = transform.lossy_reason(target_game)
        return BackendEmission(
            text=f"ins_{lowered.opcode}({args});" if lowered.args else f"ins_{lowered.opcode}();",
            strategy=LoweringStrategy.LOSSY if lossy_reason else LoweringStrategy.DIRECT,
            code="backend.transform.lossy_semantics" if lossy_reason else "",
            reason=lossy_reason or "",
        )

    def lower_bullet_visual(self, node: SemanticOperation) -> BackendEmission:
        values = {operand.name: operand.value for operand in node.operands}

        def raw(name: str, default: str) -> str:
            value = values.get(name)
            if value is None:
                return default
            return value.source_text or (value.expression.text if value.expression else default)

        opcode = self.target_opcode("bullet.visual.set")
        if opcode is None:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.bullet_visual.unsupported",
                reason="the target bullet dialect has no standalone visual configuration operation",
            )
        source_shape = raw("bullet_type", "")
        shape_semantic = str(
            node.annotations.get("bullet_shape")
            or bullet_shape_semantic(node.provenance.game, source_shape)
        )
        if not bullet_shape_can_encode(shape_semantic, self.target_profile.game):
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.bullet_shape.unsupported",
                reason=f"bullet shape {shape_semantic} has no verified target catalog entry",
                details={"source_shape": source_shape, "shape_semantic": shape_semantic},
            )
        encoded_shape = encode_bullet_shape(
            shape_semantic,
            self.target_profile.game,
            source_shape,
        )
        args = [raw("manager", "0"), encoded_shape, raw("color", "0")]
        lossy = bullet_shape_is_lossy(shape_semantic, self.target_profile.game)
        reason = "target bullet catalog merges this source shape with another visual" if lossy else ""
        return BackendEmission(
            text=f"ins_{opcode}({', '.join(args)});",
            strategy=LoweringStrategy.LOSSY if lossy else LoweringStrategy.DIRECT,
            code="backend.bullet_shape.lossy_catalog" if lossy else "",
            reason=reason,
            details={"shape_semantic": shape_semantic, "target_shape": encoded_shape},
        )

    def lower_macro(self, node: SemanticOperation) -> BackendEmission:
        args = node.encoded_args()
        if len(args) != 9:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.invalid_form",
                reason="legacy bullet macro does not have the canonical nine-operand form",
                details={"operand_count": len(args)},
            )

        source_profile = profile_for_game(node.provenance.game)
        if source_profile.transform_dialect.mode_encoding == "opaque":
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.opaque_runtime",
                reason=(
                    "the source macro uses an opaque transform/priority runtime; "
                    "expanding it into persistent manager mutations is not verified"
                ),
                details={"source_dialect": source_profile.bullet_dialect.name},
            )

        mode = str(node.annotations.get("macro_mode") or "")
        if mode not in MACRO_MODES:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.unknown_mode",
                reason="legacy bullet macro has no canonical formation mode",
                details={"macro_mode": mode},
            )

        flags = parse_integer_literal(args[8])
        if flags is None:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.dynamic_flags",
                reason="dynamic legacy transform flags cannot be expanded at compile time",
                details={"flags": args[8]},
            )
        if flags != 0:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.transform_flags",
                reason=(
                    "legacy transform flags select configured transforms at fire time; "
                    "they are executable semantics, not disposable metadata"
                ),
                details={"flags": flags},
            )

        if parse_integer_literal(args[0]) is None:
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.dynamic_shape",
                reason="dynamic legacy bullet shape cannot be resolved through the target shape catalog",
                details={"source_shape": args[0]},
            )
        shape_semantic = str(
            node.annotations.get("bullet_shape")
            or bullet_shape_semantic(node.provenance.game, args[0])
        )
        if not bullet_shape_can_encode(shape_semantic, self.target_profile.game):
            return BackendEmission(
                text="",
                strategy=LoweringStrategy.UNSUPPORTED,
                code="backend.legacy_macro.shape_catalog",
                reason=f"legacy bullet shape {shape_semantic} has no verified target catalog entry",
                details={"source_shape": args[0], "shape_semantic": shape_semantic},
            )
        target_shape = encode_bullet_shape(
            shape_semantic,
            self.target_profile.game,
            args[0],
        )

        random_ranges: LegacyMacroRandomRanges | None = None
        if mode in RANDOM_ANGLE_MACRO_MODES or mode in RANDOM_SPEED_MACRO_MODES:
            random_ranges = decode_legacy_macro_random_ranges(mode, args)
            if random_ranges is None:
                return BackendEmission(
                    text="",
                    strategy=LoweringStrategy.UNSUPPORTED,
                    code="backend.legacy_macro.dynamic_random_range",
                    reason=(
                        "legacy random macro endpoints require typed arithmetic before they can be "
                        "encoded as center/span or base/delta operands"
                    ),
                    details={
                        "macro_mode": mode,
                        "speed_endpoints": args[4:6],
                        "angle_endpoints": args[6:8],
                    },
                )

        details: dict[str, object] = {
            "source_shape": args[0],
            "shape_semantic": shape_semantic,
            "target_shape": target_shape,
            "source_color": args[1],
            "macro_mode": mode,
        }
        if random_ranges is not None:
            details["random_ranges"] = random_ranges.to_dict()
        return BackendEmission(
            text="",
            strategy=LoweringStrategy.UNSUPPORTED,
            code="backend.legacy_macro.color_catalog",
            reason=(
                "legacy macro color is a shape- and game-specific sprite offset; "
                "no verified cross-game color catalog is available"
            ),
            details=details,
        )


def join_lowered(
    prefix: str | None,
    lowered: BackendEmission | str | None,
) -> BackendEmission | str | None:
    if lowered is None:
        return None
    if isinstance(lowered, BackendEmission):
        if lowered.strategy is LoweringStrategy.UNSUPPORTED or not prefix:
            return lowered
        return BackendEmission(
            text=f"{prefix}\n{lowered.text}",
            strategy=lowered.strategy,
            code=lowered.code,
            reason=lowered.reason,
            details=lowered.details,
        )
    if lowered.lstrip().startswith("// unsupported semantic op"):
        return lowered
    if prefix and lowered:
        return f"{prefix}\n{lowered}"
    return lowered


def target_statement(
    node: SemanticNode,
    decision: CapabilityDecision,
    target_generation: str = "unknown",
    target_game: str = "",
) -> TargetStatement:
    if decision.target_text:
        diagnostic_lines = tuple(
            (
                f"// [{diagnostic.code}] node={decision.node_id} "
                f"strategy={diagnostic.strategy.value}: {diagnostic.message}"
            )
            for diagnostic in decision.diagnostics
        )
        target_lines = decision.target_text.split("\n")
        if target_lines and target_lines[-1] == "":
            target_lines.pop()
        lines = (*diagnostic_lines, *target_lines)
    else:
        diagnostics = decision.diagnostics
        code = diagnostics[-1].code if diagnostics else "lowering.unsupported"
        lines = (
            f"// [{code}] node={decision.node_id} operation={decision.operation}: {decision.reason}",
            f"// source: {node.provenance.raw.strip() or getattr(node, 'text', '')}",
        )
    return TargetStatement(
        source_node_id=str(decision.node_id),
        strategy=decision.strategy,
        lines=lines,
        guard=target_difficulty_guard(node.guard, target_generation, target_game),
        diagnostics=decision.diagnostics,
    )


def target_top_level_statements(
    module: SemanticModule,
    result: LoweringResult,
    target_generation: str,
) -> tuple[list[TargetStatement], tuple[LoweringDiagnostic, ...]]:
    statements: list[TargetStatement] = []
    diagnostics: list[LoweringDiagnostic] = []
    index = 0
    while index < len(module.top_level):
        node = module.top_level[index]
        decision = result.top_level[index]
        text = node.text.strip()
        if (
            result.target_profile.game != module.source_game
            and node.dialect_region is None
            and text.startswith("timeline ")
        ):
            block_start = index
            depth = text.count("{") - text.count("}")
            saw_open = depth > 0
            index += 1
            while index < len(module.top_level):
                current = module.top_level[index].text
                depth += current.count("{") - current.count("}")
                saw_open = saw_open or "{" in current
                index += 1
                if saw_open and depth <= 0:
                    break
            block_end = max(block_start, index - 1)
            for block_index in range(block_start, block_end + 1):
                block_node = module.top_level[block_index]
                diagnostic = LoweringDiagnostic(
                    code="syntax.timeline.cross_game_unsupported",
                    severity=DiagnosticSeverity.ERROR,
                    message=(
                        "legacy timeline blocks use a game-specific opcode dialect and require "
                        "typed cross-game lowering"
                    ),
                    target_game=result.target_profile.game,
                    node_id=block_node.node_id,
                    source_game=module.source_game,
                    operation="syntax.timeline",
                    strategy=LoweringStrategy.UNSUPPORTED,
                    details={
                        "start_node_id": str(node.node_id),
                        "end_node_id": str(module.top_level[block_end].node_id),
                        "node_count": block_end - block_start + 1,
                        "block_offset": block_index - block_start,
                    },
                )
                diagnostics.append(diagnostic)
                statements.append(
                    TargetStatement(
                        source_node_id=str(block_node.node_id),
                        strategy=LoweringStrategy.UNSUPPORTED,
                        lines=(
                            f"// [{diagnostic.code}] node={block_node.node_id}: {diagnostic.message}",
                            f"// timeline block member {block_index - block_start + 1}/{block_end - block_start + 1} preserved in canonical IR",
                        ),
                        guard=DifficultyGuard(),
                        diagnostics=(diagnostic,),
                    )
                )
            continue
        statements.append(
            target_statement(
                node,
                decision,
                target_generation,
                result.target_profile.game,
            )
        )
        index += 1
    return statements, tuple(diagnostics)


def target_difficulty_guard(
    guard: DifficultyGuard,
    target_generation: str,
    target_game: str = "",
) -> DifficultyGuard:
    if guard.is_unconditional or guard.raw == "-" or not guard.mask:
        return guard
    if target_game == "th185":
        spelling = dict(zip(DIFFICULTY_LANES, "01234567"))
    elif target_generation == "fourth":
        spelling = {lane: lane for lane in DIFFICULTY_LANES}
    elif target_generation in {"first", "second", "third"}:
        spelling = {
            "E": "E",
            "N": "N",
            "H": "H",
            "L": "L",
            "X": "4",
            "O": "5",
            "6": "6",
            "7": "7",
        }
    else:
        return guard
    return DifficultyGuard.from_marker("".join(spelling[lane] for lane in guard.mask))


def render_target_statement(statement: TargetStatement, indent: str) -> list[str]:
    return render_target_statements((statement,), indent)


def render_target_statements(
    statements: tuple[TargetStatement, ...] | list[TargetStatement],
    indent: str,
) -> list[str]:
    lines: list[str] = []
    active_marker = ""
    for statement in statements:
        marker = statement.guard.raw
        marker = marker if marker and marker != "*" else ""
        if marker != active_marker:
            if marker:
                lines.append(f"{indent}!{marker}")
            elif active_marker:
                lines.append(f"{indent}!*")
            active_marker = marker
        lines.extend(f"{indent}{line}" if line else "" for line in statement.lines)
    if active_marker:
        lines.append(f"{indent}!*")
    return lines
