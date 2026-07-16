"""Capability-driven planning for lowering ordered semantic IR.

This module deliberately stops short of owning opcode selection.  It decides
whether a canonical node can be represented by a target profile, while an
optional emitter implements the compatibility boundary to a target AST or the
legacy text backend.  Keeping those concerns separate prevents target policy
from leaking back into :mod:`semantic_ir`.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
import re
from typing import Callable, Iterable, Mapping, Sequence

from ..dialects.anm_catalog import operation_uses_anm_resource
from ..dialects.game_profile import (
    CAP_BULLET_MACRO,
    CAP_BULLET_MANAGER,
    CAP_BULLET_TRANSFORM,
    CAP_ENEMY_INTERACTION,
    CAP_LASER_BASIC,
    CAP_LASER_CURVE,
    CAP_LASER_INFINITE,
    CAP_RECT_COLLISION,
    CAP_RELATIVE_MOTION,
    CAP_TRANSFORM_APPEND,
    CAP_TRANSFORM_APPEND_CURSOR,
    CAP_TRANSFORM_CHANNELS,
    CAP_TRANSFORM_CURSOR_DECREMENT,
    CAP_TRANSFORM_INDEXED_REPLACE,
    GameProfile,
    profile_for_game,
)
from ..canonical.semantic_ir import (
    DIFFICULTY_LANES,
    DialectRegionKind,
    DifficultyGuard,
    LoweringOwner,
    NodeId,
    RawInstructionOp,
    SelectedValue,
    SelectionKind,
    SemanticModule,
    SemanticNode,
    SemanticOperation,
    SyntaxStatement,
)


class LoweringStrategy(str, Enum):
    """The four outcomes understood by the lowering pipeline."""

    DIRECT = "direct"
    LOSSY = "lossy"
    RAW = "raw"
    UNSUPPORTED = "unsupported"


class DiagnosticSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class CapabilityAlternative:
    """A capability set that can approximate a rule's native semantics."""

    capabilities: frozenset[str]
    reason: str
    strategy: LoweringStrategy = LoweringStrategy.LOSSY


@dataclass(frozen=True, slots=True)
class CapabilityRule:
    """Declarative capability requirements for a family of semantic ops.

    Rules are ordered and the first match wins.  Selectors describe semantic
    operation names, never source opcodes or individual games.
    """

    name: str
    native_capabilities: frozenset[str]
    operations: frozenset[str] = frozenset()
    prefixes: tuple[str, ...] = ()
    domains: frozenset[str] = frozenset()
    alternatives: tuple[CapabilityAlternative, ...] = ()

    def matches(self, node: SemanticOperation) -> bool:
        if self.operations and node.operation in self.operations:
            return True
        if self.prefixes and any(node.operation.startswith(prefix) for prefix in self.prefixes):
            return True
        return bool(self.domains and node.domain in self.domains)


def _caps(*values: str) -> frozenset[str]:
    return frozenset(values)


# Specific semantic features precede their broader domains.  This is the only
# built-in lowering table: it maps semantic features to capabilities and does
# not duplicate any per-game opcode catalog.
DEFAULT_CAPABILITY_RULES: tuple[CapabilityRule, ...] = (
    CapabilityRule(
        "bullet.transform.append_cursor.decrement",
        _caps(CAP_BULLET_TRANSFORM, CAP_TRANSFORM_APPEND_CURSOR, CAP_TRANSFORM_CURSOR_DECREMENT),
        operations=_caps("bullet.transform.append_cursor.decrement"),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_BULLET_TRANSFORM, CAP_TRANSFORM_INDEXED_REPLACE),
                "append cursor changes are folded into later explicit transform indices",
            ),
        ),
    ),
    CapabilityRule(
        "bullet.transform.append",
        _caps(
            CAP_BULLET_TRANSFORM,
            CAP_TRANSFORM_APPEND,
            CAP_TRANSFORM_APPEND_CURSOR,
            CAP_TRANSFORM_CHANNELS,
        ),
        operations=_caps("bullet.transform.append"),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_BULLET_TRANSFORM, CAP_TRANSFORM_INDEXED_REPLACE, CAP_TRANSFORM_CHANNELS),
                "append order must be materialized as explicit transform indices",
            ),
        ),
    ),
    CapabilityRule(
        "bullet.transform.replace",
        _caps(CAP_BULLET_TRANSFORM, CAP_TRANSFORM_INDEXED_REPLACE, CAP_TRANSFORM_CHANNELS),
        operations=_caps("bullet.transform.replace"),
        alternatives=(
            CapabilityAlternative(
                _caps(
                    CAP_BULLET_TRANSFORM,
                    CAP_TRANSFORM_APPEND,
                    CAP_TRANSFORM_APPEND_CURSOR,
                    CAP_TRANSFORM_CHANNELS,
                ),
                "indexed replacement is representable only when append order is reconstructed",
            ),
        ),
    ),
    CapabilityRule(
        "bullet.transform.channels",
        _caps(CAP_BULLET_TRANSFORM, CAP_TRANSFORM_CHANNELS),
        prefixes=("bullet.transform.channel",),
    ),
    CapabilityRule(
        "bullet.transform",
        _caps(CAP_BULLET_TRANSFORM),
        prefixes=("bullet.transform.",),
    ),
    CapabilityRule(
        "bullet.macro",
        _caps(CAP_BULLET_MACRO),
        prefixes=("bullet.macro.", "bullet.auto_fire.", "bullet.fire.defer", "bullet.fire.enable", "bullet.fire.immediate"),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_BULLET_MANAGER),
                "macro fire semantics must be expanded into manager mutations and a fire operation",
            ),
        ),
    ),
    CapabilityRule(
        "bullet.manager",
        _caps(CAP_BULLET_MANAGER),
        prefixes=("bullet.",),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_BULLET_MACRO),
                "persistent manager state must be folded into a target bullet macro",
            ),
        ),
    ),
    CapabilityRule(
        "laser.curve",
        _caps(CAP_LASER_CURVE),
        operations=_caps("laser.activate_curve"),
        prefixes=("laser.curve.",),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_LASER_BASIC),
                "curve geometry must be approximated by a basic laser",
            ),
        ),
    ),
    CapabilityRule(
        "laser.infinite",
        _caps(CAP_LASER_INFINITE),
        prefixes=("laser.infinite.",),
        alternatives=(
            CapabilityAlternative(
                _caps(CAP_LASER_BASIC),
                "infinite laser lifetime must be approximated by a finite basic laser",
            ),
        ),
    ),
    CapabilityRule(
        "laser.basic",
        _caps(CAP_LASER_BASIC),
        prefixes=("laser.",),
    ),
    CapabilityRule(
        "movement.relative",
        _caps(CAP_RELATIVE_MOTION),
        prefixes=("movement.position_rel", "movement.velocity_rel", "movement.relative."),
    ),
    CapabilityRule(
        "enemy.interaction",
        _caps(CAP_ENEMY_INTERACTION),
        prefixes=("enemy.interaction.",),
    ),
    CapabilityRule(
        "collision.rectangle",
        _caps(CAP_RECT_COLLISION),
        prefixes=("collision.rectangle.", "collision.rect."),
    ),
)


@dataclass(frozen=True, slots=True)
class LoweringPolicy:
    """Compiler policy kept outside canonical semantic nodes."""

    allow_lossy: bool = False
    preserve_syntax: bool = True
    preserve_raw_same_family: bool = False
    preserve_raw_cross_family: bool = False


@dataclass(frozen=True, slots=True)
class LoweringDiagnostic:
    code: str
    severity: DiagnosticSeverity
    message: str
    target_game: str
    node_id: NodeId | None = None
    source_game: str = ""
    routine: str = ""
    operation: str = ""
    strategy: LoweringStrategy = LoweringStrategy.UNSUPPORTED
    required_capabilities: tuple[str, ...] = ()
    missing_capabilities: tuple[str, ...] = ()
    details: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "target_game": self.target_game,
            "node_id": str(self.node_id) if self.node_id is not None else None,
            "source_game": self.source_game,
            "routine": self.routine,
            "operation": self.operation,
            "strategy": self.strategy.value,
            "required_capabilities": list(self.required_capabilities),
            "missing_capabilities": list(self.missing_capabilities),
            "details": dict(self.details),
        }


@dataclass(frozen=True, slots=True)
class BackendEmission:
    """Typed result returned by a target encoder at the compatibility boundary."""

    text: str
    strategy: LoweringStrategy = LoweringStrategy.DIRECT
    code: str = ""
    reason: str = ""
    details: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CapabilityDecision:
    """A target decision for one canonical node."""

    node_id: NodeId
    node_kind: str
    operation: str
    routine: str
    strategy: LoweringStrategy
    target_game: str
    source_game: str
    rule: str = ""
    required_capabilities: tuple[str, ...] = ()
    selected_capabilities: tuple[str, ...] = ()
    missing_capabilities: tuple[str, ...] = ()
    reason: str = ""
    target_text: str | None = None
    diagnostics: tuple[LoweringDiagnostic, ...] = ()

    @property
    def supported(self) -> bool:
        return self.strategy is not LoweringStrategy.UNSUPPORTED

    @property
    def is_lossless(self) -> bool:
        return self.strategy is LoweringStrategy.DIRECT or (
            self.strategy is LoweringStrategy.RAW
            and not any(item.severity is DiagnosticSeverity.WARNING for item in self.diagnostics)
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "node_id": str(self.node_id),
            "node_kind": self.node_kind,
            "operation": self.operation,
            "routine": self.routine,
            "strategy": self.strategy.value,
            "target_game": self.target_game,
            "source_game": self.source_game,
            "rule": self.rule,
            "required_capabilities": list(self.required_capabilities),
            "selected_capabilities": list(self.selected_capabilities),
            "missing_capabilities": list(self.missing_capabilities),
            "reason": self.reason,
            "target_text": self.target_text,
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True, slots=True)
class LoweredRoutine:
    name: str
    params: str
    decisions: tuple[CapabilityDecision, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "params": self.params,
            "decisions": [decision.to_dict() for decision in self.decisions],
        }


@dataclass(frozen=True, slots=True)
class LoweringResult:
    source_game: str
    target_profile: GameProfile
    top_level: tuple[CapabilityDecision, ...]
    routines: tuple[LoweredRoutine, ...]
    diagnostics: tuple[LoweringDiagnostic, ...]

    @property
    def decisions(self) -> tuple[CapabilityDecision, ...]:
        return self.top_level + tuple(
            decision
            for routine in self.routines
            for decision in routine.decisions
        )

    @property
    def successful(self) -> bool:
        return all(decision.supported for decision in self.decisions) and not any(
            diagnostic.severity is DiagnosticSeverity.ERROR for diagnostic in self.diagnostics
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "source_game": self.source_game,
            "target_game": self.target_profile.game,
            "target_generation": self.target_profile.generation,
            "top_level": [decision.to_dict() for decision in self.top_level],
            "routines": [routine.to_dict() for routine in self.routines],
            "diagnostics": [diagnostic.to_dict() for diagnostic in self.diagnostics],
            "successful": self.successful,
        }


BackendEmitter = Callable[[SemanticOperation, str], BackendEmission | str | None]


def target_difficulty_guard(
    guard: DifficultyGuard,
    target_generation: str,
    target_game: str = "",
) -> DifficultyGuard:
    """Render one semantic difficulty mask in the target dialect spelling."""

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


def evaluation_stack_offsets(
    selected_values: Sequence[SelectedValue],
) -> frozenset[int]:
    """Return the evaluation slots produced by ordered selection tables.

    Each table pushes one value. Therefore N source tables are consumed as
    ``[-N]`` through ``[-1]`` in the following target expression.
    """

    return frozenset(range(-len(selected_values), 0))


_NON_CODE_TOKEN_RE = re.compile(
    r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
    re.DOTALL,
)
_EVALUATION_PLACEHOLDER_RE = re.compile(r"\[\s*(-\d+)(?:\.0f)?\s*\]")


def executable_evaluation_stack_offsets(text: str) -> frozenset[int]:
    """Find evaluation placeholders outside comments and quoted strings."""

    code = _NON_CODE_TOKEN_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"),
        text,
    )
    return frozenset(
        int(match.group(1)) for match in _EVALUATION_PLACEHOLDER_RE.finditer(code)
    )


def first_executable_statement_stack_offsets(text: str) -> frozenset[int]:
    """Return placeholders in the first emitted non-marker statement."""

    code = _NON_CODE_TOKEN_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"),
        text,
    )
    for line in code.splitlines():
        statement = line.strip()
        if not statement or statement in {"{", "}"}:
            continue
        if re.fullmatch(r"![ENHLXO0-7*:-]+", statement, re.IGNORECASE):
            continue
        if re.fullmatch(r"(?:[A-Za-z_]\w*|\d+):", statement):
            continue
        return frozenset(
            int(match.group(1))
            for match in _EVALUATION_PLACEHOLDER_RE.finditer(statement)
        )
    return frozenset()


def _selected_value_source_text(node: SemanticNode) -> str:
    if isinstance(node, SemanticOperation):
        return ", ".join(node.encoded_args())
    if isinstance(node, RawInstructionOp):
        return ", ".join(node.args)
    return node.text


def lower_selected_values_for_target(
    node: SemanticNode,
    target_text: str,
    target_profile: GameProfile,
) -> tuple[str | None, str, Mapping[str, object]]:
    """Prefix proven cross-game evaluation tables or return a safe failure."""

    selected_values = node.selected_values
    if not selected_values:
        return target_text, "", {}
    source_profile = profile_for_game(node.provenance.game)
    source_syntax = source_profile.routine_dialect
    target_syntax = target_profile.routine_dialect
    if not (
        source_syntax.supports_structured_syntax
        and target_syntax.supports_structured_syntax
    ):
        return None, (
            "difficulty-selected evaluation values require stack-expression syntax "
            "in both the source and target routine dialects"
        ), {
            "source_routine_dialect": source_syntax.name,
            "target_routine_dialect": target_syntax.name,
            "source_syntax_encoding": source_syntax.syntax_encoding.value,
            "target_syntax_encoding": target_syntax.syntax_encoding.value,
        }
    expected = evaluation_stack_offsets(selected_values)
    source_offsets = executable_evaluation_stack_offsets(
        _selected_value_source_text(node)
    )
    missing_source = expected - source_offsets
    if missing_source:
        return None, (
            "canonical selected values have no corresponding evaluation placeholder "
            "in the source consumer"
        ), {
            "expected_placeholders": sorted(expected),
            "source_placeholders": sorted(source_offsets),
            "missing_source_placeholders": sorted(missing_source),
        }
    target_offsets = executable_evaluation_stack_offsets(target_text)
    missing_target = expected - target_offsets
    if missing_target:
        return None, (
            "target argument or syntax adaptation removed an evaluation placeholder "
            "required by a difficulty-selected value"
        ), {
            "expected_placeholders": sorted(expected),
            "target_placeholders": sorted(target_offsets),
            "missing_target_placeholders": sorted(missing_target),
        }
    first_statement_offsets = first_executable_statement_stack_offsets(target_text)
    missing_first_statement = expected - first_statement_offsets
    if missing_first_statement:
        return None, (
            "the first emitted executable statement is not the selected-value consumer; "
            "intervening instructions could invalidate the evaluation stack"
        ), {
            "expected_placeholders": sorted(expected),
            "target_placeholders": sorted(target_offsets),
            "first_statement_placeholders": sorted(first_statement_offsets),
            "missing_first_statement_placeholders": sorted(missing_first_statement),
        }

    from ..canonical.variable_ir import project_expression

    lines: list[str] = []
    for selection_index, selected in enumerate(selected_values):
        if selected.selector is not SelectionKind.DIFFICULTY or not selected.cases:
            return None, "selected value has no supported non-empty difficulty table", {
                "selection_index": selection_index,
                "selector": selected.selector.value,
            }
        for case_index, case in enumerate(selected.cases):
            projected = project_expression(case.value, target_profile.game)
            if projected.expression is None:
                issue = projected.issues[0]
                return None, (
                    "difficulty-selected case value cannot be projected to the target "
                    "variable dialect"
                ), {
                    "selection_index": selection_index,
                    "case_index": case_index,
                    **issue.details(),
                }
            marker = target_difficulty_guard(
                case.guard,
                target_profile.generation,
                target_profile.game,
            ).raw or "*"
            lines.extend((f"!{marker}", f"{projected.expression.text};"))
        lines.append("!*")
    return "\n".join((*lines, target_text)), "", {
        "evaluation_placeholders": sorted(expected),
    }


def identity_selected_value_lines(selected_values: Sequence[object]) -> list[str]:
    lines: list[str] = []
    for selected in selected_values:
        for case in getattr(selected, "cases", ()):
            marker = case.guard.raw or "*"
            lines.extend((f"!{marker}", f"{case.value.text};"))
        lines.append("!*")
    return lines


def identity_instruction_text(
    opcode: int,
    args: Sequence[str],
    selected_values: Sequence[object] = (),
) -> str:
    """Render a native instruction and its ordered source value selections."""

    lines = identity_selected_value_lines(selected_values)
    rendered_args = ", ".join(str(arg) for arg in args)
    lines.append(f"ins_{opcode}({rendered_args});" if args else f"ins_{opcode}();")
    return "\n".join(lines)


def identity_syntax_text(text: str, selected_values: Sequence[object] = ()) -> str:
    lines = identity_selected_value_lines(selected_values)
    lines.append(text)
    return "\n".join(lines)


def requires_structured_routine_syntax(node: SyntaxStatement) -> bool:
    if node.statement_kind in {
        "goto",
        "conditional_goto",
        "return",
        "assign",
        "function_decl",
    }:
        return True
    return node.statement_kind == "raw" and node.text.rstrip().endswith(";")


def compatibility_backend_emitter(
    node: SemanticOperation,
    target_game: str,
) -> BackendEmission | None:
    """Call the existing text backend without making it a planner dependency."""

    if target_game == node.provenance.game and node.provenance.opcode is not None:
        return BackendEmission(
            identity_instruction_text(
                node.provenance.opcode,
                node.encoded_args(),
                node.selected_values,
            )
        )
    from ..canonical.variable_ir import project_semantic_operation

    projected, issues = project_semantic_operation(
        node,
        target_game,
        evaluation_stack_offsets=evaluation_stack_offsets(node.selected_values),
    )
    if projected is None:
        issue = issues[0]
        return BackendEmission(
            text="",
            strategy=LoweringStrategy.UNSUPPORTED,
            code=issue.code,
            reason=issue.message,
            details=issue.details(),
        )
    from ..compat.backend import compile_ir_op_emission

    return compile_ir_op_emission(projected, target_game)


class LoweringPlanner:
    """Plan lowering using semantic capabilities and an optional emitter."""

    def __init__(
        self,
        target_profile: GameProfile,
        *,
        policy: LoweringPolicy | None = None,
        rules: Sequence[CapabilityRule] = DEFAULT_CAPABILITY_RULES,
        backend_emitter: BackendEmitter | None = None,
    ) -> None:
        self.target_profile = target_profile
        self.policy = policy or LoweringPolicy()
        self.rules = tuple(rules)
        self.backend_emitter = backend_emitter

    @classmethod
    def for_game(
        cls,
        target_game: str,
        *,
        policy: LoweringPolicy | None = None,
        rules: Sequence[CapabilityRule] = DEFAULT_CAPABILITY_RULES,
        backend_emitter: BackendEmitter | None = None,
    ) -> LoweringPlanner:
        return cls(
            profile_for_game(target_game),
            policy=policy,
            rules=rules,
            backend_emitter=backend_emitter,
        )

    @classmethod
    def with_compat_backend(
        cls,
        target_game: str,
        *,
        policy: LoweringPolicy | None = None,
        rules: Sequence[CapabilityRule] = DEFAULT_CAPABILITY_RULES,
    ) -> LoweringPlanner:
        return cls.for_game(
            target_game,
            policy=policy,
            rules=rules,
            backend_emitter=compatibility_backend_emitter,
        )

    def plan(self, value: SemanticModule | SemanticNode) -> LoweringResult | CapabilityDecision:
        if isinstance(value, SemanticModule):
            return self.plan_module(value)
        return self.plan_node(value)

    def plan_node(self, node: SemanticNode, routine: str = "") -> CapabilityDecision:
        ownership_error = self._ownership_error(node, routine)
        if ownership_error is not None:
            return ownership_error
        if isinstance(node, SemanticOperation):
            return self._plan_semantic_operation(node, routine)
        if isinstance(node, RawInstructionOp):
            return self._plan_raw_instruction(node, routine)
        if isinstance(node, SyntaxStatement):
            return self._plan_syntax(node, routine)
        raise TypeError(f"unsupported semantic node: {type(node).__name__}")

    def plan_module(self, module: SemanticModule) -> LoweringResult:
        begin_module = getattr(self.backend_emitter, "begin_module", None)
        if callable(begin_module):
            begin_module(module)
        seen: dict[str, tuple[str, CapabilityDecision]] = {}
        module_diagnostics: list[LoweringDiagnostic] = []

        top_level = tuple(
            self._register_decision(self.plan_node(node), "<module>", seen, module_diagnostics)
            for node in module.top_level
        )
        routines: list[LoweredRoutine] = []
        for routine in module.routines:
            decisions = tuple(
                self._register_decision(
                    self.plan_node(node, routine.name),
                    routine.name,
                    seen,
                    module_diagnostics,
                )
                for node in routine.body
            )
            routines.append(LoweredRoutine(routine.name, routine.params, decisions))

        all_decisions = top_level + tuple(
            decision for routine in routines for decision in routine.decisions
        )
        signature_diagnostics: list[LoweringDiagnostic] = []
        source_profile = profile_for_game(module.source_game)
        if (
            self.target_profile.game != source_profile.game
            and not self.target_profile.routine_dialect.accepts_parameters_from(
                source_profile.routine_dialect
            )
        ):
            external_params = {
                signature.name: signature.params for signature in module.routine_signatures
            }
            for routine in module.routines:
                params = routine.params or external_params.get(routine.name, "")
                if not params:
                    continue
                signature_diagnostics.append(
                    LoweringDiagnostic(
                        code="syntax.routine_parameters.unsupported",
                        severity=DiagnosticSeverity.ERROR,
                        message=(
                            "source and target routines do not share a compatible parameter/local "
                            "storage ABI; explicit parameter allocation is required"
                        ),
                        target_game=self.target_profile.game,
                        source_game=module.source_game,
                        routine=routine.name,
                        operation="syntax.routine_parameters",
                        strategy=LoweringStrategy.UNSUPPORTED,
                        details={
                            "source_params": params,
                            "source_routine_dialect": source_profile.routine_dialect.name,
                            "target_routine_dialect": self.target_profile.routine_dialect.name,
                        },
                    )
                )
        diagnostics = tuple(module_diagnostics) + tuple(signature_diagnostics) + tuple(
            diagnostic
            for decision in all_decisions
            for diagnostic in decision.diagnostics
        )
        if self.target_profile.game == "unknown":
            diagnostics = (
                LoweringDiagnostic(
                    code="target.unknown_profile",
                    severity=DiagnosticSeverity.ERROR,
                    message="target game has no registered capability profile",
                    target_game=self.target_profile.game,
                ),
                *diagnostics,
            )
        return LoweringResult(
            source_game=module.source_game,
            target_profile=self.target_profile,
            top_level=top_level,
            routines=tuple(routines),
            diagnostics=diagnostics,
        )

    def _plan_semantic_operation(self, node: SemanticOperation, routine: str) -> CapabilityDecision:
        if self.target_profile.game == node.provenance.game and node.provenance.opcode is not None:
            return self._emit(
                node,
                self._decision(
                    node,
                    routine,
                    strategy=LoweringStrategy.DIRECT,
                    rule="identity.same_game",
                    reason="canonical operands use the source game's native instruction form",
                ),
            )
        if selection_error := self._selection_syntax_error(node, routine):
            return selection_error
        candidate_resolver = getattr(self.backend_emitter, "has_anm_candidate", None)
        has_anm_candidate = (
            callable(candidate_resolver)
            and bool(candidate_resolver(node))
        )
        if operation_uses_anm_resource(node.operation) and not has_anm_candidate:
            return self._unsupported(
                node,
                routine,
                code="anm.resource_context_unresolved",
                message=(
                    "cross-game ANM bank/script IDs require either a manifest-scoped target "
                    "candidate or a typed resource reference"
                ),
                details={
                    "resource_operation": node.operation,
                    "required_ir": "AnmResourceRef|AnmCandidateSelection",
                },
            )
        from ..canonical.variable_ir import project_semantic_operation

        _projected, variable_issues = project_semantic_operation(
            node,
            self.target_profile.game,
            evaluation_stack_offsets=evaluation_stack_offsets(node.selected_values),
        )
        if variable_issues:
            issue = variable_issues[0]
            return self._unsupported(
                node,
                routine,
                code=issue.code,
                message=issue.message,
                details={
                    **issue.details(),
                    "issue_count": len(variable_issues),
                },
            )
        if self.target_profile.game == "unknown":
            return self._unsupported(
                node,
                routine,
                code="target.unknown_profile",
                message="cannot lower semantic operations without a target capability profile",
            )

        rule = next((candidate for candidate in self.rules if candidate.matches(node)), None)
        if rule is None:
            decision = self._decision(
                node,
                routine,
                strategy=LoweringStrategy.DIRECT,
                reason="operation does not require a target-specific advertised capability",
            )
            return self._emit(node, decision)

        native = tuple(sorted(rule.native_capabilities))
        native_missing = tuple(sorted(rule.native_capabilities - self.target_profile.capabilities))
        if not native_missing:
            decision = self._decision(
                node,
                routine,
                strategy=LoweringStrategy.DIRECT,
                rule=rule.name,
                required=native,
                selected=native,
                reason="target provides the native semantic capability set",
            )
            return self._emit(node, decision)

        for alternative in rule.alternatives:
            missing = alternative.capabilities - self.target_profile.capabilities
            if missing or not self.policy.allow_lossy:
                continue
            selected = tuple(sorted(alternative.capabilities))
            diagnostic = LoweringDiagnostic(
                code="capability.lossy_fallback",
                severity=DiagnosticSeverity.WARNING,
                message=alternative.reason,
                target_game=self.target_profile.game,
                node_id=node.node_id,
                source_game=node.provenance.game,
                routine=routine,
                operation=node.operation,
                strategy=alternative.strategy,
                required_capabilities=native,
                missing_capabilities=native_missing,
                details={"selected_capabilities": list(selected), "rule": rule.name},
            )
            decision = self._decision(
                node,
                routine,
                strategy=alternative.strategy,
                rule=rule.name,
                required=native,
                selected=selected,
                missing=native_missing,
                reason=alternative.reason,
                diagnostics=(diagnostic,),
            )
            return self._emit(node, decision)

        message = (
            f"target lacks capabilities required by semantic feature {rule.name}: "
            + ", ".join(native_missing)
        )
        if not self.policy.allow_lossy and rule.alternatives:
            message += "; lossy fallbacks are disabled"
        return self._unsupported(
            node,
            routine,
            code="capability.unsupported",
            message=message,
            rule=rule.name,
            required=native,
            missing=native_missing,
        )

    def _plan_raw_instruction(self, node: RawInstructionOp, routine: str) -> CapabilityDecision:
        source_profile = profile_for_game(node.provenance.game)
        same_game = source_profile.game == self.target_profile.game and source_profile.game != "unknown"
        same_family = (
            source_profile.opcode_family == self.target_profile.opcode_family
            and source_profile.opcode_family != "unknown"
        )
        allowed = same_game or (same_family and self.policy.preserve_raw_same_family)
        allowed = allowed or self.policy.preserve_raw_cross_family
        if not allowed:
            return self._unsupported(
                node,
                routine,
                code="raw.incompatible_dialect",
                message=(
                    f"raw instruction from {source_profile.opcode_family} cannot be emitted safely "
                    f"for {self.target_profile.opcode_family}"
                ),
            )
        if selection_error := self._selection_syntax_error(node, routine):
            return selection_error

        target_args = list(node.args)
        if not same_game:
            from ..canonical.semantic_ir import VariableUseKind
            from ..canonical.variable_ir import rewrite_argument_variables

            projected_args, variable_issues = rewrite_argument_variables(
                node.provenance.game,
                self.target_profile.game,
                node.args,
                use_kind=VariableUseKind.UNKNOWN,
                evaluation_stack_offsets=evaluation_stack_offsets(node.selected_values),
            )
            if projected_args is None:
                issue = variable_issues[0]
                return self._unsupported(
                    node,
                    routine,
                    code=issue.code,
                    message=issue.message,
                    details={
                        **issue.details(),
                        "issue_count": len(variable_issues),
                        "raw_operand_access": "unknown",
                    },
                )
            target_args = projected_args

        target_text = identity_instruction_text(
            node.opcode,
            target_args,
            node.selected_values if same_game else (),
        )
        if node.selected_values and not same_game:
            target_text, reason, details = lower_selected_values_for_target(
                node,
                target_text,
                self.target_profile,
            )
            if target_text is None:
                return self._unsupported(
                    node,
                    routine,
                    code="value_selection.unsupported",
                    message=reason,
                    details=details,
                )
        diagnostics: tuple[LoweringDiagnostic, ...] = ()
        if not same_game:
            code = "raw.same_family_passthrough" if same_family else "raw.cross_family_passthrough"
            diagnostic = LoweringDiagnostic(
                code=code,
                severity=DiagnosticSeverity.WARNING,
                message="raw opcode compatibility is assumed and has not been semantically verified",
                target_game=self.target_profile.game,
                node_id=node.node_id,
                source_game=node.provenance.game,
                routine=routine,
                operation=f"ins_{node.opcode}",
                strategy=LoweringStrategy.RAW,
                details={
                    "source_opcode_family": source_profile.opcode_family,
                    "target_opcode_family": self.target_profile.opcode_family,
                },
            )
            diagnostics = (diagnostic,)
        return self._decision(
            node,
            routine,
            strategy=LoweringStrategy.RAW,
            reason=node.reason,
            target_text=target_text,
            diagnostics=diagnostics,
        )

    def _plan_syntax(self, node: SyntaxStatement, routine: str) -> CapabilityDecision:
        if not self.policy.preserve_syntax:
            return self._unsupported(
                node,
                routine,
                code="syntax.passthrough_disabled",
                message="target policy disables preservation of dialect syntax statements",
            )
        same_game = self.target_profile.game == node.provenance.game
        source_profile = profile_for_game(node.provenance.game)
        if selection_error := self._selection_syntax_error(node, routine):
            return selection_error
        if (
            not same_game
            and node.dialect_region is not None
            and node.dialect_region.kind is DialectRegionKind.TIMELINE
        ):
            return self._unsupported(
                node,
                routine,
                code="syntax.timeline.cross_game_unsupported",
                message=(
                    "legacy timeline instructions use a game-specific opcode dialect; "
                    "a typed timeline lowerer is required for cross-game emission"
                ),
                details=node.dialect_region.to_dict(),
            )
        if (
            not same_game
            and node.statement_kind in {"call", "async_call"}
            and not self.target_profile.routine_dialect.accepts_call_syntax_from(
                source_profile.routine_dialect
            )
        ):
            return self._unsupported(
                node,
                routine,
                code="routine.call_abi_unsupported",
                message=(
                    "source and target routine call encodings differ; explicit callee identity "
                    "and argument allocation lowering is required"
                ),
                details={
                    "source_routine_dialect": source_profile.routine_dialect.name,
                    "target_routine_dialect": self.target_profile.routine_dialect.name,
                    "source_call_encoding": source_profile.routine_dialect.call_encoding.value,
                    "target_call_encoding": self.target_profile.routine_dialect.call_encoding.value,
                },
            )
        if (
            not same_game
            and requires_structured_routine_syntax(node)
            and not self.target_profile.routine_dialect.supports_structured_syntax
        ):
            return self._unsupported(
                node,
                routine,
                code="routine.structured_syntax_abi_unsupported",
                message=(
                    "the target routine ABI has no structured stack-expression encoding for "
                    f"{node.statement_kind}; explicit instruction lowering is required"
                ),
                details={
                    "statement_kind": node.statement_kind,
                    "source_routine_dialect": source_profile.routine_dialect.name,
                    "target_routine_dialect": self.target_profile.routine_dialect.name,
                    "source_syntax_encoding": source_profile.routine_dialect.syntax_encoding.value,
                    "target_syntax_encoding": self.target_profile.routine_dialect.syntax_encoding.value,
                },
            )
        target_text = identity_syntax_text(node.text, node.selected_values) if same_game else node.text
        if not same_game:
            from ..canonical.variable_ir import project_syntax_statement

            projected_text, variable_issues = project_syntax_statement(
                node,
                self.target_profile.game,
                evaluation_stack_offsets=evaluation_stack_offsets(node.selected_values),
            )
            if projected_text is None:
                issue = variable_issues[0]
                return self._unsupported(
                    node,
                    routine,
                    code=issue.code,
                    message=issue.message,
                    details={
                        **issue.details(),
                        "issue_count": len(variable_issues),
                    },
                )
            target_text = projected_text
        syntax_emitter = getattr(self.backend_emitter, "emit_syntax", None)
        if callable(syntax_emitter):
            try:
                emitted_text = syntax_emitter(
                    node,
                    target_text,
                    self.target_profile.game,
                )
            except Exception as exc:
                return self._unsupported(
                    node,
                    routine,
                    code="backend.syntax_exception",
                    message=str(exc),
                )
            if emitted_text is not None:
                target_text = str(emitted_text)
        if node.selected_values and not same_game:
            selected_text, reason, details = lower_selected_values_for_target(
                node,
                target_text,
                self.target_profile,
            )
            if selected_text is None:
                return self._unsupported(
                    node,
                    routine,
                    code="value_selection.unsupported",
                    message=reason,
                    details=details,
                )
            target_text = selected_text
        return self._decision(
            node,
            routine,
            strategy=LoweringStrategy.RAW,
            reason=(
                "typed syntax expression projected to the target variable dialect"
                if target_text != node.text
                else "lossless syntax statement passthrough"
            ),
            target_text=target_text,
        )

    def _emit(self, node: SemanticOperation, decision: CapabilityDecision) -> CapabilityDecision:
        if decision.strategy is LoweringStrategy.UNSUPPORTED:
            return decision
        if self.backend_emitter is None:
            if node.selected_values and self.target_profile.game != node.provenance.game:
                return self._backend_failure(
                    node,
                    decision,
                    "value_selection.unsupported",
                    "target emission is required to prove that selected-value placeholders survive",
                    {
                        "expected_placeholders": sorted(
                            evaluation_stack_offsets(node.selected_values)
                        ),
                    },
                )
            return decision
        try:
            emitted = self.backend_emitter(node, self.target_profile.game)
        except Exception as exc:  # The compatibility boundary must become a diagnostic.
            return self._backend_failure(node, decision, "backend.exception", str(exc))
        if not emitted:
            return self._backend_failure(
                node,
                decision,
                "backend.no_lowering",
                "target backend returned no lowering",
            )
        emission = emitted if isinstance(emitted, BackendEmission) else BackendEmission(str(emitted))
        if emission.strategy is LoweringStrategy.UNSUPPORTED:
            return self._backend_failure(
                node,
                decision,
                emission.code or "backend.unsupported",
                emission.reason or "target backend reported that no lowering is implemented",
                emission.details,
            )
        if node.selected_values and self.target_profile.game != node.provenance.game:
            selected_text, reason, details = lower_selected_values_for_target(
                node,
                emission.text,
                self.target_profile,
            )
            if selected_text is None:
                return self._backend_failure(
                    node,
                    decision,
                    "value_selection.unsupported",
                    reason,
                    details,
                )
            emission = replace(emission, text=selected_text)
        if emission.strategy is LoweringStrategy.LOSSY:
            reason = emission.reason or "target backend selected a lossy compatibility lowering"
            if not self.policy.allow_lossy:
                return self._backend_failure(
                    node,
                    decision,
                    "backend.lossy_forbidden",
                    f"{reason}; lossy fallbacks are disabled",
                    emission.details,
                )
            if decision.strategy is not LoweringStrategy.LOSSY:
                diagnostic = LoweringDiagnostic(
                    code=emission.code or "backend.lossy_fallback",
                    severity=DiagnosticSeverity.WARNING,
                    message=reason,
                    target_game=self.target_profile.game,
                    node_id=node.node_id,
                    source_game=node.provenance.game,
                    routine=decision.routine,
                    operation=node.operation,
                    strategy=LoweringStrategy.LOSSY,
                    details=dict(emission.details),
                )
                decision = replace(
                    decision,
                    strategy=LoweringStrategy.LOSSY,
                    reason=reason,
                    diagnostics=(*decision.diagnostics, diagnostic),
                )
        return replace(decision, target_text=emission.text)

    def _selection_syntax_error(
        self,
        node: SemanticNode,
        routine: str,
    ) -> CapabilityDecision | None:
        if (
            not node.selected_values
            or self.target_profile.game == node.provenance.game
        ):
            return None
        source_profile = profile_for_game(node.provenance.game)
        source_syntax = source_profile.routine_dialect
        target_syntax = self.target_profile.routine_dialect
        if (
            source_syntax.supports_structured_syntax
            and target_syntax.supports_structured_syntax
        ):
            return None
        return self._unsupported(
            node,
            routine,
            code="value_selection.unsupported",
            message=(
                "difficulty-selected evaluation values require stack-expression syntax "
                "in both the source and target routine dialects"
            ),
            details={
                "source_routine_dialect": source_syntax.name,
                "target_routine_dialect": target_syntax.name,
                "source_syntax_encoding": source_syntax.syntax_encoding.value,
                "target_syntax_encoding": target_syntax.syntax_encoding.value,
            },
        )

    def _backend_failure(
        self,
        node: SemanticOperation,
        decision: CapabilityDecision,
        code: str,
        message: str,
        details: Mapping[str, object] | None = None,
    ) -> CapabilityDecision:
        diagnostic = LoweringDiagnostic(
            code=code,
            severity=DiagnosticSeverity.ERROR,
            message=message,
            target_game=self.target_profile.game,
            node_id=node.node_id,
            source_game=node.provenance.game,
            routine=decision.routine,
            operation=node.operation,
            strategy=LoweringStrategy.UNSUPPORTED,
            required_capabilities=decision.required_capabilities,
            missing_capabilities=decision.missing_capabilities,
            details={"planned_strategy": decision.strategy.value, **dict(details or {})},
        )
        return replace(
            decision,
            strategy=LoweringStrategy.UNSUPPORTED,
            reason=message,
            target_text=None,
            diagnostics=(*decision.diagnostics, diagnostic),
        )

    def _ownership_error(self, node: SemanticNode, routine: str) -> CapabilityDecision | None:
        expected = {
            SemanticOperation: LoweringOwner.SEMANTIC,
            RawInstructionOp: LoweringOwner.RAW,
            SyntaxStatement: LoweringOwner.SYNTAX,
        }[type(node)]
        if node.ownership.owner is expected:
            return None
        return self._unsupported(
            node,
            routine,
            code="ownership.wrong_lowerer",
            message=(
                f"node is owned by {node.ownership.owner.value}, not the "
                f"{expected.value} lowerer"
            ),
        )

    def _register_decision(
        self,
        decision: CapabilityDecision,
        scope: str,
        seen: dict[str, tuple[str, CapabilityDecision]],
        diagnostics: list[LoweringDiagnostic],
    ) -> CapabilityDecision:
        key = str(decision.node_id)
        previous = seen.get(key)
        if previous is None and key:
            seen[key] = (scope, decision)
            return decision

        if previous is None:
            message = "canonical node has an empty NodeId"
            code = "identity.empty_node_id"
            details: dict[str, object] = {"scope": scope}
        else:
            message = f"NodeId {key!r} is already owned by scope {previous[0]!r}"
            code = "identity.duplicate_node_id"
            details = {"scope": scope, "previous_scope": previous[0]}
        diagnostic = LoweringDiagnostic(
            code=code,
            severity=DiagnosticSeverity.ERROR,
            message=message,
            target_game=self.target_profile.game,
            node_id=decision.node_id,
            source_game=decision.source_game,
            routine=decision.routine,
            operation=decision.operation,
            strategy=LoweringStrategy.UNSUPPORTED,
            details=details,
        )
        diagnostics.append(diagnostic)
        return replace(
            decision,
            strategy=LoweringStrategy.UNSUPPORTED,
            reason=message,
            target_text=None,
        )

    def _unsupported(
        self,
        node: SemanticNode,
        routine: str,
        *,
        code: str,
        message: str,
        rule: str = "",
        required: Iterable[str] = (),
        missing: Iterable[str] = (),
        details: Mapping[str, object] | None = None,
    ) -> CapabilityDecision:
        required_tuple = tuple(sorted(required))
        missing_tuple = tuple(sorted(missing))
        operation = self._operation_name(node)
        source_game = node.provenance.game
        diagnostic = LoweringDiagnostic(
            code=code,
            severity=DiagnosticSeverity.ERROR,
            message=message,
            target_game=self.target_profile.game,
            node_id=node.node_id,
            source_game=source_game,
            routine=routine,
            operation=operation,
            strategy=LoweringStrategy.UNSUPPORTED,
            required_capabilities=required_tuple,
            missing_capabilities=missing_tuple,
            details={**({"rule": rule} if rule else {}), **dict(details or {})},
        )
        return self._decision(
            node,
            routine,
            strategy=LoweringStrategy.UNSUPPORTED,
            rule=rule,
            required=required_tuple,
            missing=missing_tuple,
            reason=message,
            diagnostics=(diagnostic,),
        )

    def _decision(
        self,
        node: SemanticNode,
        routine: str,
        *,
        strategy: LoweringStrategy,
        rule: str = "",
        required: Iterable[str] = (),
        selected: Iterable[str] = (),
        missing: Iterable[str] = (),
        reason: str = "",
        target_text: str | None = None,
        diagnostics: tuple[LoweringDiagnostic, ...] = (),
    ) -> CapabilityDecision:
        return CapabilityDecision(
            node_id=node.node_id,
            node_kind=node.node,
            operation=self._operation_name(node),
            routine=routine,
            strategy=strategy,
            target_game=self.target_profile.game,
            source_game=node.provenance.game,
            rule=rule,
            required_capabilities=tuple(sorted(required)),
            selected_capabilities=tuple(sorted(selected)),
            missing_capabilities=tuple(sorted(missing)),
            reason=reason,
            target_text=target_text,
            diagnostics=diagnostics,
        )

    @staticmethod
    def _operation_name(node: SemanticNode) -> str:
        if isinstance(node, SemanticOperation):
            return node.operation
        if isinstance(node, RawInstructionOp):
            return f"ins_{node.opcode}"
        return node.statement_kind


__all__ = [
    "BackendEmission",
    "BackendEmitter",
    "CapabilityAlternative",
    "CapabilityDecision",
    "CapabilityRule",
    "DEFAULT_CAPABILITY_RULES",
    "DiagnosticSeverity",
    "LoweredRoutine",
    "LoweringDiagnostic",
    "LoweringPlanner",
    "LoweringPolicy",
    "LoweringResult",
    "LoweringStrategy",
    "compatibility_backend_emitter",
]
