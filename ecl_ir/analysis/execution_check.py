from __future__ import annotations

import ast
import re
from collections import Counter, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from .anm_resources import (
    AnmActionCandidate,
    AnmCandidatePool,
    build_anm_lowering_plan,
    candidate_pool_for_stage,
    stage_id_from_source,
)
from ..canonical.semantic_ir import (
    SemanticModule,
    SemanticNode,
    SemanticOperation,
    SemanticRoutine,
    SyntaxStatement,
    RawInstructionOp,
    VariableEncodingKind,
    VariableUseKind,
)
from ..canonical.semantic_lifter import build_semantic_module
from ..canonical.variable_ir import parse_expression
from ..dialects.anm_catalog import target_bank_for_role
from ..dialects.game_ids import KNOWN_GAME_IDS, normalize_game_id
from ..dialects.reference import opcode_info, validate_opcode_args
from ..source.model import Program
from ..source.parser import FUNC_RE, infer_game, parse_decl, parse_decl_text


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIFFICULTIES = ("E", "N", "H", "L")
ANM_SET_OPERATIONS = frozenset({"anm.set_main", "anm.set_sprite"})
ANM_EXPLICIT_PLAY_OPERATIONS = frozenset(
    {"anm.play", "anm.play_abs", "anm.play_high", "anm.play_pos", "anm.play_rotate"}
)
ANM_PLAY_OPERATIONS = frozenset({*ANM_EXPLICIT_PLAY_OPERATIONS, "anm.selected_play"})
ANM_RESOURCE_OPERATIONS = frozenset(
    {"anm.select", *ANM_SET_OPERATIONS, *ANM_PLAY_OPERATIONS, "enemy.death_anm"}
)
ANM_SLOT_CONSUMERS = frozenset(
    {
        "anm.switch",
        "anm.rotate",
        "anm.move",
        "anm.color",
        "anm.color_time",
        "anm.alpha",
        "anm.alpha_time",
        "anm.alpha2",
        "anm.alpha2_time",
        "anm.scale",
        "anm.scale_time",
        "anm.scale2",
        "anm.layer",
        "anm.blend_mode",
        "anm.on_et",
    }
)
LOWERING_COMMENT_RE = re.compile(
    r"^\s*//\s*\[([^\]]+)\]\s+node=(\S+)"
    r"(?:\s+operation=([^\s:]+))?"
    r"(?:\s+strategy=(direct|raw|lossy|unsupported))?\s*:\s*(.*)$"
)
GENERATED_HEADER_RE = re.compile(
    r"^\s*//\s*(source|source game|target)\s*:\s*(.*?)\s*$",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class EclExecutionDiagnostic:
    severity: str
    code: str
    game: str
    difficulty: str = ""
    module: str = ""
    routine: str = ""
    line: int | None = None
    node_id: str = ""
    message: str = ""
    path: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "game": self.game,
            "difficulty": self.difficulty,
            "module": self.module,
            "routine": self.routine,
            "line": self.line,
            "node_id": self.node_id,
            "message": self.message,
            "path": list(self.path),
            "details": dict(self.details),
        }


@dataclass(slots=True)
class EclExecutionReport:
    source: str
    game: str
    entry: str
    difficulties: tuple[str, ...]
    modules: tuple[str, ...] = ()
    entries: tuple[str, ...] = ()
    diagnostics: list[EclExecutionDiagnostic] = field(default_factory=list)
    states_explored: int = 0
    analysis_complete: bool = True

    @property
    def errors(self) -> tuple[EclExecutionDiagnostic, ...]:
        return tuple(item for item in self.diagnostics if item.severity == "error")

    @property
    def warnings(self) -> tuple[EclExecutionDiagnostic, ...]:
        return tuple(item for item in self.diagnostics if item.severity == "warning")

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def to_dict(self) -> dict[str, Any]:
        errors = len(self.errors)
        warnings = len(self.warnings)
        return {
            "schema": "th062.ecl-execution-check",
            "schema_version": 1,
            "source": self.source,
            "game": self.game,
            "entry": self.entry,
            "difficulties": list(self.difficulties),
            "modules": list(self.modules),
            "entries": list(self.entries),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "errors": errors,
            "warnings": warnings,
            "states_explored": self.states_explored,
            "analysis_complete": self.analysis_complete,
            "summary": {
                "diagnostics": len(self.diagnostics),
                "errors": errors,
                "warnings": warnings,
                "states_explored": self.states_explored,
                "analysis_complete": self.analysis_complete,
            },
        }


@dataclass(slots=True)
class _ModuleUnit:
    key: str
    path: Path | None
    program: Program
    module: SemanticModule
    text: str
    role: str


@dataclass(slots=True)
class _RoutineRef:
    unit: _ModuleUnit
    routine: SemanticRoutine

    @property
    def key(self) -> str:
        return f"{self.unit.key}:{self.routine.name}"


@dataclass(slots=True)
class _Package:
    game: str
    root: _ModuleUnit
    units: list[_ModuleUnit]
    routines: dict[str, list[_RoutineRef]]
    signatures: dict[str, str]
    pool: AnmCandidatePool
    stage_id: str | None
    reference_root: Path | None
    unresolved_ecli: tuple[tuple[str, str], ...]


@dataclass(slots=True)
class _AnmUnitState:
    selected_bank: int | None = None
    bank_unknown: bool = False
    slot_bindings: dict[int, int | None] = field(default_factory=dict)
    slots_unknown: bool = False
    pending_bank: int | None = None
    pending_actions: list[AnmActionCandidate] = field(default_factory=list)
    pending_dynamic: bool = False
    configured: bool = False
    setup_checked: bool = False

    def clone(self) -> _AnmUnitState:
        return _AnmUnitState(
            selected_bank=self.selected_bank,
            bank_unknown=self.bank_unknown,
            slot_bindings=dict(self.slot_bindings),
            slots_unknown=self.slots_unknown,
            pending_bank=self.pending_bank,
            pending_actions=list(self.pending_actions),
            pending_dynamic=self.pending_dynamic,
            configured=self.configured,
            setup_checked=self.setup_checked,
        )

    def fingerprint(self) -> tuple[Any, ...]:
        return (
            self.selected_bank,
            self.bank_unknown,
            tuple(sorted(self.slot_bindings.items())),
            self.slots_unknown,
            self.pending_bank,
            tuple(self.pending_actions),
            self.pending_dynamic,
            self.configured,
            self.setup_checked,
        )


@dataclass(frozen=True, slots=True)
class _ReturnFrame:
    routine_key: str
    pc: int
    initialized: frozenset[str]
    values: tuple[tuple[str, int | float | None], ...]


@dataclass(slots=True)
class _ExecutionState:
    routine_ref: _RoutineRef
    pc: int
    initialized: set[str]
    values: dict[str, int | float | None]
    anm: _AnmUnitState
    stack: tuple[_ReturnFrame, ...] = ()
    path: tuple[str, ...] = ()
    spawned: bool = False
    entity_root: str = ""
    entity_role: str = "stage"

    def clone(self) -> _ExecutionState:
        return _ExecutionState(
            routine_ref=self.routine_ref,
            pc=self.pc,
            initialized=set(self.initialized),
            values=dict(self.values),
            anm=self.anm.clone(),
            stack=self.stack,
            path=self.path,
            spawned=self.spawned,
            entity_root=self.entity_root,
            entity_role=self.entity_role,
        )

    def fingerprint(self) -> tuple[Any, ...]:
        return (
            self.routine_ref.key,
            self.pc,
            tuple(sorted(self.initialized)),
            tuple(sorted(self.values.items())),
            self.anm.fingerprint(),
            self.stack,
            self.spawned,
            self.entity_root,
            self.entity_role,
        )


def check_ecl_file(
    path: str | Path,
    *,
    game: str | None = None,
    reference_package: str | Path | None = None,
    entry: str = "main",
    difficulties: Sequence[str] = DEFAULT_DIFFICULTIES,
    all_routines: bool = False,
    state_budget: int = 200000,
) -> EclExecutionReport:
    input_path = Path(path)
    text = input_path.read_bytes()
    from ..source.parser import SourceDocument

    document = SourceDocument.from_bytes(text)
    return _check_ecl(
        document.text,
        source_name=str(input_path),
        game=game,
        reference_package=reference_package,
        entry=entry,
        difficulties=difficulties,
        all_routines=all_routines,
        state_budget=state_budget,
        input_path=input_path,
    )


def check_ecl_text(
    text: str,
    *,
    source_name: str,
    game: str,
    reference_package: str | Path | None = None,
    entry: str = "main",
    difficulties: Sequence[str] = DEFAULT_DIFFICULTIES,
    all_routines: bool = False,
    state_budget: int = 200000,
) -> EclExecutionReport:
    return _check_ecl(
        text,
        source_name=source_name,
        game=game,
        reference_package=reference_package,
        entry=entry,
        difficulties=difficulties,
        all_routines=all_routines,
        state_budget=state_budget,
        input_path=None,
    )


def _check_ecl(
    text: str,
    *,
    source_name: str,
    game: str | None,
    reference_package: str | Path | None,
    entry: str,
    difficulties: Sequence[str],
    all_routines: bool,
    state_budget: int,
    input_path: Path | None,
) -> EclExecutionReport:
    if state_budget <= 0:
        raise ValueError("state_budget must be greater than zero")
    lanes = _normalize_difficulties(difficulties)
    headers = _generated_headers(text)
    selected_game = _select_game(game, source_name, headers, reference_package)
    package = _load_package(
        text,
        source_name,
        selected_game,
        input_path,
        reference_package,
        headers,
    )
    report = EclExecutionReport(
        source=source_name,
        game=selected_game,
        entry=entry,
        difficulties=lanes,
        modules=tuple(unit.key for unit in package.units),
    )
    checker = _ExecutionChecker(package, report, state_budget)
    checker.scan_lowering_comments()
    checker.static_preflight()
    checker.check_manifest()
    entries = checker.resolve_entries(entry)
    possible_audit_entries = (
        [
            ref
            for refs in package.routines.values()
            for ref in refs
            if ref.key not in {item.key for item in entries}
        ]
        if all_routines
        else []
    )
    report.entries = tuple(item.key for item in (*entries, *possible_audit_entries))
    for lane in lanes:
        lane_start = report.states_explored
        reached, lane_complete = checker.execute_lane(lane, entries, False)
        audit_entries = [
            ref for ref in possible_audit_entries if ref.key not in reached
        ]
        if lane_complete and audit_entries:
            used = report.states_explored - lane_start
            _audit_reached, lane_complete = checker.execute_lane(
                lane,
                audit_entries,
                True,
                budget=max(0, state_budget - used),
            )
    checker.check_source_target_trace()
    return report


def _normalize_difficulties(values: Sequence[str]) -> tuple[str, ...]:
    lanes: list[str] = []
    for raw in values:
        for lane in str(raw).upper():
            if lane not in DEFAULT_DIFFICULTIES:
                raise ValueError(f"unsupported checker difficulty lane: {lane!r}")
            if lane not in lanes:
                lanes.append(lane)
    if not lanes:
        raise ValueError("at least one E/N/H/L difficulty lane is required")
    return tuple(lanes)


def _generated_headers(text: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in text.splitlines()[:32]:
        match = GENERATED_HEADER_RE.match(line)
        if match:
            headers[match.group(1).lower()] = match.group(2).strip()
    return headers


def _select_game(
    explicit: str | None,
    source_name: str,
    headers: dict[str, str],
    reference_package: str | Path | None,
) -> str:
    candidates = [explicit, headers.get("target"), infer_game(source_name)]
    if reference_package is not None:
        candidates.append(infer_game(reference_package))
    for candidate in candidates:
        normalized = normalize_game_id(str(candidate or ""))
        if normalized in KNOWN_GAME_IDS:
            return normalized
    raise ValueError(
        "target game is unknown; pass game=... or place the input under a game directory"
    )


def _artifact_role(path: str | Path) -> str:
    name = Path(path).name.lower()
    match = re.match(r"^(?:stage|st)\d{2}(.*?)\.decl$", name)
    suffix = match.group(1) if match else ""
    if "mboss" in suffix or re.fullmatch(r"mbs\d*", suffix):
        return "midboss"
    if "boss" in suffix or re.fullmatch(r"bs\d*", suffix):
        return "boss"
    if name == "default.decl":
        return "global"
    return "stage"


def _make_unit(
    text: str,
    source_name: str,
    game: str,
    path: Path | None,
) -> _ModuleUnit:
    if path is not None and path.is_file():
        program = parse_decl(path)
        if Path(program.source) != path:
            program.source = str(path)
    else:
        program = parse_decl_text(text, source_name)
    program.game = game
    module = build_semantic_module(program)
    key = str(path if path is not None else source_name)
    return _ModuleUnit(key, path, program, module, text, _artifact_role(source_name))


def _semantic_module_from_path(path: Path, game: str | None = None) -> SemanticModule:
    program = parse_decl(path)
    selected_game = normalize_game_id(str(game or ""))
    if selected_game in KNOWN_GAME_IDS:
        program.game = selected_game
    return build_semantic_module(program)


def _reference_root(
    value: str | Path | None,
    game: str,
    stage_id: str | None,
) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    if path.is_file():
        return path
    if path.is_dir() and stage_id:
        for name in (f"st{stage_id}.decl", f"stage{stage_id}.decl"):
            candidate = path / name
            if candidate.is_file():
                return candidate
    if not path.is_absolute():
        candidate = ROOT / path
        if candidate.is_file():
            return candidate
        if candidate.is_dir() and stage_id:
            for name in (f"st{stage_id}.decl", f"stage{stage_id}.decl"):
                root = candidate / name
                if root.is_file():
                    return root
    return None


def _header_stage_id(headers: dict[str, str]) -> str | None:
    source = headers.get("source", "")
    return stage_id_from_source(source) if source else None


def _resolve_ecli(
    entry: str,
    search_dirs: Iterable[Path],
) -> Path | None:
    relative = Path(str(entry).replace("\\", "/")).with_suffix(".decl")
    if relative.is_absolute():
        return relative if relative.is_file() else None
    for directory in search_dirs:
        candidate = directory / relative
        if candidate.is_file():
            return candidate
    return None


def _load_package(
    text: str,
    source_name: str,
    game: str,
    input_path: Path | None,
    reference_package: str | Path | None,
    headers: dict[str, str],
) -> _Package:
    source_path = input_path if input_path is not None else None
    root = _make_unit(text, source_name, game, source_path)
    stage_id = (
        stage_id_from_source(str(reference_package or ""))
        or stage_id_from_source(source_name)
        or _header_stage_id(headers)
    )
    reference_root = _reference_root(reference_package, game, stage_id)
    if reference_package is not None and reference_root is None:
        raise ValueError(f"reference package does not exist: {reference_package}")
    if stage_id is None and reference_root is not None:
        stage_id = stage_id_from_source(str(reference_root))

    target_search_dirs: list[Path] = []
    if input_path is not None:
        target_search_dirs.append(input_path.parent)
    else:
        source_parent = Path(source_name).parent
        if source_parent != Path("."):
            target_search_dirs.append(source_parent)
    reference_search_dirs: list[Path] = []
    if reference_root is not None:
        reference_search_dirs.append(reference_root.parent)
    reference_search_dirs.append(ROOT / game)
    target_search_dirs = list(dict.fromkeys(target_search_dirs))
    reference_search_dirs = list(dict.fromkeys(reference_search_dirs))

    units = [root]
    seen_paths: set[Path] = set()
    unresolved_ecli: list[tuple[str, str]] = []
    pending = deque((root, entry) for entry in root.program.resources.get("ecli", []))
    while pending:
        owner, entry = pending.popleft()
        owner_dirs = [owner.path.parent] if owner.path is not None else []
        dependency = _resolve_ecli(
            entry,
            list(dict.fromkeys((*owner_dirs, *target_search_dirs))),
        )
        normalized_entry = str(entry).replace("\\", "/").rsplit("/", 1)[-1].lower()
        if dependency is None and normalized_entry == "default.ecl":
            dependency = _resolve_ecli(entry, reference_search_dirs)
        if dependency is None:
            unresolved_ecli.append((owner.key, str(entry)))
            continue
        resolved = dependency.resolve()
        if resolved in seen_paths or (input_path is not None and resolved == input_path.resolve()):
            continue
        seen_paths.add(resolved)
        dependency_text = dependency.read_text(encoding="utf-8", errors="replace")
        unit = _make_unit(dependency_text, str(dependency), game, dependency)
        units.append(unit)
        pending.extend((unit, entry) for entry in unit.program.resources.get("ecli", []))

    routines: dict[str, list[_RoutineRef]] = {}
    signatures: dict[str, str] = {}
    for unit in units:
        for signature in unit.module.routine_signatures:
            signatures.setdefault(signature.name, signature.params)
        for declaration in unit.module.top_level:
            if declaration.statement_kind == "function_decl":
                name = str(declaration.attributes.get("function", ""))
                if name:
                    signatures.setdefault(name, str(declaration.attributes.get("params", "")))
        for routine in unit.module.routines:
            ref = _RoutineRef(unit, routine)
            routines.setdefault(routine.name, []).append(ref)
            signatures.setdefault(routine.name, routine.params)

    pool = candidate_pool_for_stage(game, stage_id, reference_root)
    return _Package(
        game,
        root,
        units,
        routines,
        signatures,
        pool,
        stage_id,
        reference_root,
        tuple(dict.fromkeys(unresolved_ecli)),
    )


def _parameter_names(params: str) -> tuple[str, ...]:
    names: list[str] = []
    for part in params.split(","):
        tokens = re.findall(r"[A-Za-z_]\w*", part)
        if tokens:
            names.append(tokens[-1])
    return tuple(names)


def _literal_number(value: object) -> int | float | None:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return int(text)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:f)?", text):
        return float(text.rstrip("f"))
    return None


def _operand_text(node: SemanticOperation, name: str, fallback: int) -> str:
    operand = next((item for item in node.operands if item.name == name), None)
    if operand is None and fallback < len(node.operands):
        operand = node.operands[fallback]
    if operand is None:
        return ""
    return operand.value.source_text or (
        operand.value.expression.text if operand.value.expression is not None else ""
    )


class _ExecutionChecker:
    def __init__(
        self,
        package: _Package,
        report: EclExecutionReport,
        state_budget: int,
    ) -> None:
        self.package = package
        self.report = report
        self.state_budget = state_budget
        self._diagnostic_keys: set[tuple[Any, ...]] = set()
        self._source_module_cache: dict[str, SemanticModule | None] = {}

    def add(
        self,
        severity: str,
        code: str,
        *,
        difficulty: str = "",
        unit: _ModuleUnit | None = None,
        routine: str = "",
        node: SemanticNode | None = None,
        line: int | None = None,
        message: str,
        path: tuple[str, ...] = (),
        details: dict[str, Any] | None = None,
    ) -> None:
        module = unit.key if unit is not None else self.package.root.key
        node_id = str(node.node_id) if node is not None else ""
        if line is None and node is not None:
            line = node.provenance.span.start_line
        payload = dict(details or {})
        key = (
            severity,
            code,
            difficulty,
            module,
            routine,
            line,
            node_id,
            repr(sorted(payload.items())),
        )
        if key in self._diagnostic_keys:
            return
        self._diagnostic_keys.add(key)
        self.report.diagnostics.append(
            EclExecutionDiagnostic(
                severity=severity,
                code=code,
                game=self.package.game,
                difficulty=difficulty,
                module=module,
                routine=routine,
                line=line,
                node_id=node_id,
                message=message,
                path=path,
                details=payload,
            )
        )

    def scan_lowering_comments(self) -> None:
        for unit in self.package.units:
            routine = ""
            for line_no, line in enumerate(unit.text.splitlines(), 1):
                function = FUNC_RE.match(line)
                if function:
                    routine = function.group(1)
                match = LOWERING_COMMENT_RE.match(line)
                if not match:
                    continue
                code, node_id, operation, strategy, message = match.groups()
                severity = "warning" if strategy in {"raw", "lossy"} else "error"
                self.add(
                    severity,
                    code,
                    unit=unit,
                    routine=routine,
                    line=line_no,
                    message=message,
                    details={
                        "origin": "lowering_comment",
                        "strategy": strategy or "unsupported",
                        "operation": operation or "",
                        "source_node_id": node_id,
                    },
                )

    def static_preflight(self) -> None:
        units_by_key = {unit.key: unit for unit in self.package.units}
        for module, entry in self.package.unresolved_ecli:
            self.add(
                "error",
                "package.ecli_unresolved",
                unit=units_by_key.get(module),
                message=f"ECL dependency {entry} is not available for package analysis",
                details={"entry": entry, "owner": module},
            )
        for name, refs in self.package.routines.items():
            definitions_by_unit: dict[str, list[_RoutineRef]] = {}
            for ref in refs:
                definitions_by_unit.setdefault(ref.unit.key, []).append(ref)
            duplicates = [items for items in definitions_by_unit.values() if len(items) > 1]
            if duplicates:
                self.add(
                    "error",
                    "routine.duplicate_definition",
                    unit=duplicates[0][0].unit,
                    routine=name,
                    message="routine has multiple bodies in one ECL module",
                    details={"definitions": [item.unit.key for item in duplicates[0]]},
                )
        for unit in self.package.units:
            for routine in unit.module.routines:
                self._check_routine_static(unit, routine)

    def _check_routine_static(self, unit: _ModuleUnit, routine: SemanticRoutine) -> None:
        declarations: dict[str, int] = {name: 0 for name in _parameter_names(routine.params)}
        for name in _parameter_names(routine.params):
            if list(_parameter_names(routine.params)).count(name) > 1:
                self.add(
                    "error",
                    "symbol.duplicate_local",
                    unit=unit,
                    routine=routine.name,
                    line=0,
                    message=f"routine parameter {name} is declared more than once",
                    details={"name": name},
                )
        labels: dict[str, int] = {}
        gotos: list[SyntaxStatement] = []
        for node in routine.body:
            if isinstance(node, SyntaxStatement) and node.statement_kind == "var":
                values = node.attributes.get("vars", [])
                for raw in values if isinstance(values, list) else []:
                    tokens = re.findall(r"[A-Za-z_]\w*", str(raw))
                    if not tokens:
                        continue
                    name = tokens[-1]
                    if name in declarations:
                        self.add(
                            "error",
                            "symbol.duplicate_local",
                            unit=unit,
                            routine=routine.name,
                            node=node,
                            message=f"local {name} is declared more than once",
                            details={"name": name, "first_line": declarations[name]},
                        )
                    else:
                        declarations[name] = node.provenance.span.start_line
            if isinstance(node, SyntaxStatement) and node.statement_kind == "label":
                label = str(node.attributes.get("name", ""))
                if label:
                    labels[label] = node.provenance.span.start_line
            if isinstance(node, SyntaxStatement) and node.statement_kind in {"goto", "conditional_goto"}:
                gotos.append(node)

        for node in routine.body:
            self._check_node_variables(unit, routine, node, declarations)
            self._check_instruction(unit, routine, node)
            if isinstance(node, SyntaxStatement) and node.statement_kind in {"call", "async_call"}:
                self._check_call_static(unit, routine, node)
        for node in gotos:
            label = str(node.attributes.get("label", ""))
            if label and label not in labels:
                self.add(
                    "error",
                    "control_flow.unresolved_target",
                    unit=unit,
                    routine=routine.name,
                    node=node,
                    message=f"goto target {label} is not defined in this routine",
                    details={"label": label},
                )

    def _node_primary_expressions(self, node: SemanticNode) -> list[Any]:
        expressions = []
        if isinstance(node, SemanticOperation):
            expressions.extend(
                operand.value.expression
                for operand in node.operands
                if operand.value.expression is not None
            )
        elif isinstance(node, SyntaxStatement):
            expressions.extend(binding.expression for binding in node.expressions)
        elif isinstance(node, RawInstructionOp):
            expressions.extend(parse_expression(self.package.game, arg) for arg in node.args)
        return expressions

    def _node_variable_uses(self, node: SemanticNode) -> list[Any]:
        expressions = self._node_primary_expressions(node)
        for selected in node.selected_values:
            expressions.extend(case.value for case in selected.cases)
        return [use for expression in expressions for use in expression.variable_uses]

    def _check_node_variables(
        self,
        unit: _ModuleUnit,
        routine: SemanticRoutine,
        node: SemanticNode,
        declarations: dict[str, int],
    ) -> None:
        line = node.provenance.span.start_line
        for expression_index, expression in enumerate(
            self._node_primary_expressions(node)
        ):
            for use in expression.stack_uses:
                for lane in self.report.difficulties:
                    if not _guard_active(node, lane):
                        continue
                    selected_depth = sum(
                        1
                        for selected in node.selected_values
                        if any(
                            case.guard.is_unconditional or lane in case.guard.mask
                            for case in selected.cases
                        )
                    )
                    available_depth = selected_depth + expression_index
                    if -use.reference.offset <= available_depth:
                        continue
                    self.add(
                        "error",
                        "stack.relative_reference_unbound",
                        difficulty=lane,
                        unit=unit,
                        routine=routine.name,
                        node=node,
                        message=(
                            f"relative stack reference {use.reference.source_encoding} "
                            "has no preceding expression or selected value"
                        ),
                        details={
                            "offset": use.reference.offset,
                            "available_depth": available_depth,
                            "expression_index": expression_index,
                            "use_kind": use.kind.value,
                        },
                    )
        for use in self._node_variable_uses(node):
            encoding = use.reference.source_encoding
            if encoding.kind is VariableEncodingKind.UNKNOWN:
                self.add(
                    "error",
                    "variable.numeric_reference_unsupported",
                    unit=unit,
                    routine=routine.name,
                    node=node,
                    message=(
                        f"numeric variable reference {encoding.raw} is outside the target "
                        "game's supported variable dialect"
                    ),
                    details={
                        "raw": encoding.raw,
                        "numeric_id": encoding.numeric_id,
                        "use_kind": use.kind.value,
                    },
                )
                continue
            if encoding.kind is VariableEncodingKind.NAMED_LOCAL:
                name = encoding.name
                declaration = declarations.get(name)
                if declaration is None:
                    self.add(
                        "error",
                        "symbol.undeclared_local",
                        unit=unit,
                        routine=routine.name,
                        node=node,
                        message=f"named local {name} is used but never declared",
                        details={"name": name, "use_kind": use.kind.value},
                    )
                elif declaration > line:
                    self.add(
                        "error",
                        "symbol.use_before_declaration",
                        unit=unit,
                        routine=routine.name,
                        node=node,
                        message=f"named local {name} is used before its declaration",
                        details={"name": name, "declaration_line": declaration},
                    )
                continue

            requires_read = use.kind in {VariableUseKind.READ, VariableUseKind.READ_WRITE}
            requires_write = use.kind in {VariableUseKind.WRITE, VariableUseKind.READ_WRITE}
            access = use.reference.access
            if use.kind is VariableUseKind.UNKNOWN:
                continue
            if (requires_read and not access.readable) or (
                requires_write and not access.writable
            ):
                severity = "warning" if access.value == "unknown" else "error"
                self.add(
                    severity,
                    (
                        "variable.access_unproven"
                        if severity == "warning"
                        else "variable.access_violation"
                    ),
                    unit=unit,
                    routine=routine.name,
                    node=node,
                    message=(
                        f"variable {encoding.raw} has undocumented access semantics"
                        if severity == "warning"
                        else f"variable {encoding.raw} does not permit {use.kind.value} access"
                    ),
                    details={
                        "raw": encoding.raw,
                        "semantic_id": use.reference.semantic_id,
                        "access": access.value,
                        "use_kind": use.kind.value,
                    },
                )

    def _check_instruction(
        self,
        unit: _ModuleUnit,
        routine: SemanticRoutine,
        node: SemanticNode,
    ) -> None:
        if isinstance(node, SemanticOperation):
            opcode = node.provenance.opcode
            args = node.encoded_args()
        elif isinstance(node, RawInstructionOp):
            opcode = node.opcode
            args = node.args
        else:
            return
        if opcode is None:
            return
        error = validate_opcode_args(self.package.game, opcode, list(args))
        if error:
            documented_format_gap = (
                "not in thecl format table" in error
                and opcode_info(self.package.game, opcode) is not None
            )
            self.add(
                "warning" if documented_format_gap else "error",
                (
                    "instruction.format_table_evidence_gap"
                    if documented_format_gap
                    else "instruction.invalid_arguments"
                ),
                unit=unit,
                routine=routine.name,
                node=node,
                message=(
                    f"{error}; an ECL map or game reference still documents this opcode"
                    if documented_format_gap
                    else error
                ),
                details={
                    "kind": (
                        "unsupported_opcode"
                        if "not in thecl format table" in error
                        else "arity_or_type"
                    ),
                    "opcode": opcode,
                    "args": list(args),
                },
            )
        if isinstance(node, SemanticOperation):
            self._check_literal_constraints(unit, routine, node)

    def _check_literal_constraints(
        self,
        unit: _ModuleUnit,
        routine: SemanticRoutine,
        node: SemanticOperation,
    ) -> None:
        byte_operands = {
            "anm.color": (("red", 1), ("green", 2), ("blue", 3)),
            "anm.color_time": (("red", 3), ("green", 4), ("blue", 5)),
            "anm.alpha": (("alpha", 1),),
            "anm.alpha_time": (("alpha", 3),),
            "anm.alpha2": (("alpha", 1),),
            "anm.alpha2_time": (("alpha", 3),),
        }.get(node.operation)
        if byte_operands is None:
            return
        for name, index in byte_operands:
            text = _operand_text(node, name, index)
            value = _literal_number(text)
            if value is None:
                self.add(
                    "warning",
                    "anm.dynamic_operand_unproven",
                    unit=unit,
                    routine=routine.name,
                    node=node,
                    message=f"dynamic {node.operation} {name} cannot be range-checked",
                    details={
                        "operation": node.operation,
                        "operand": name,
                        "operand_index": index,
                        "value": text,
                    },
                )
            elif not 0 <= value <= 255:
                self.add(
                    "error",
                    "instruction.parameter_value_out_of_range",
                    unit=unit,
                    routine=routine.name,
                    node=node,
                    message=f"{node.operation} {name} must be in 0..255",
                    details={
                        "operation": node.operation,
                        "operand": name,
                        "operand_index": index,
                        "value": value,
                        "min": 0,
                        "max": 255,
                    },
                )

    def _check_call_static(
        self,
        unit: _ModuleUnit,
        routine: SemanticRoutine,
        node: SyntaxStatement,
    ) -> None:
        callee = str(node.attributes.get("function", ""))
        args = node.attributes.get("args", [])
        raw_args = args if isinstance(args, list) else []
        local_definition = next(
            (
                ref.routine.params
                for ref in self.package.routines.get(callee, [])
                if ref.unit.key == unit.key
            ),
            None,
        )
        local_declaration = next(
            (
                str(statement.attributes.get("params", ""))
                for statement in unit.module.top_level
                if statement.statement_kind == "function_decl"
                and str(statement.attributes.get("function", "")) == callee
            ),
            None,
        )
        params = (
            local_definition
            if local_definition is not None
            else local_declaration
            if local_declaration is not None
            else self.package.signatures.get(callee)
        )
        if params is None:
            self.add(
                "warning",
                "routine.unresolved_target",
                unit=unit,
                routine=routine.name,
                node=node,
                message=f"routine target {callee} is not present in the loaded package",
                details={"callee": callee},
            )
            return
        expected = len(_parameter_names(params))
        if expected != len(raw_args):
            self.add(
                "error",
                "routine.call_arity_mismatch",
                unit=unit,
                routine=routine.name,
                node=node,
                message=f"call to {callee} expects {expected} args, got {len(raw_args)}",
                details={"callee": callee, "expected": expected, "actual": len(raw_args)},
            )

    def check_manifest(self) -> None:
        expected = self.package.pool.resources.get("anim")
        if not expected:
            return
        actual = self.package.root.program.resources.get("anim", [])
        if tuple(actual) != tuple(expected):
            self.add(
                "error",
                "resource.anim_manifest_mismatch",
                unit=self.package.root,
                message="target anim manifest differs from the corresponding original package",
                details={"expected": list(expected), "actual": list(actual)},
            )

    def resolve_entries(self, entry: str) -> list[_RoutineRef]:
        refs = self.package.routines.get(entry, [])
        if not refs:
            self.add(
                "error",
                "execution.entry_not_found",
                unit=self.package.root,
                routine=entry,
                message=f"entry routine {entry} is not defined in the loaded package",
                details={"entry": entry},
            )
            return []
        return [refs[0]]

    def _resolve_routine(
        self,
        name: str,
        current_unit: _ModuleUnit,
    ) -> _RoutineRef | None:
        refs = self.package.routines.get(name, [])
        if not refs:
            return None
        local = next((ref for ref in refs if ref.unit.key == current_unit.key), None)
        return local or refs[0]

    def _routine_for_key(self, key: str) -> _RoutineRef | None:
        return next(
            (
                ref
                for refs in self.package.routines.values()
                for ref in refs
                if ref.key == key
            ),
            None,
        )

    def _initial_anm(self, ref: _RoutineRef) -> _AnmUnitState:
        role = _routine_role(ref.unit.role, ref.routine.name)
        bank_role = "boss" if role == "midboss" else role
        return _AnmUnitState(selected_bank=target_bank_for_role(self.package.game, bank_role))

    def _initial_state(
        self,
        ref: _RoutineRef,
        *,
        anm: _AnmUnitState | None = None,
        values: dict[str, int | float | None] | None = None,
        stack: tuple[_ReturnFrame, ...] = (),
        path: tuple[str, ...] = (),
        spawned: bool = False,
        entity_root: str = "",
        entity_role: str | None = None,
    ) -> _ExecutionState:
        supplied = values or {}
        params = tuple(
            dict.fromkeys((*_parameter_names(ref.routine.params), *supplied.keys()))
        )
        return _ExecutionState(
            routine_ref=ref,
            pc=0,
            initialized=set(params),
            values={name: supplied.get(name) for name in params},
            anm=anm.clone() if anm is not None else self._initial_anm(ref),
            stack=stack,
            path=path,
            spawned=spawned,
            entity_root=entity_root or ref.key,
            entity_role=entity_role or _routine_role(ref.unit.role, ref.routine.name),
        )

    def execute_lane(
        self,
        lane: str,
        entries: Sequence[_RoutineRef],
        all_routines: bool,
        *,
        budget: int | None = None,
    ) -> tuple[set[str], bool]:
        queue: deque[_ExecutionState] = deque()
        for ref in entries:
            unknown_entry = all_routines
            queue.append(
                self._initial_state(
                    ref,
                    anm=(
                        _AnmUnitState(bank_unknown=True, slots_unknown=True)
                        if unknown_entry
                        else None
                    ),
                    path=(ref.key,),
                )
            )
        visited: set[tuple[Any, ...]] = set()
        reached: set[str] = set()
        labels: dict[str, dict[str, int]] = {}
        lane_states = 0
        lane_budget = self.state_budget if budget is None else budget

        while queue:
            state = queue.popleft()
            fingerprint = state.fingerprint()
            if fingerprint in visited:
                continue
            if lane_states >= lane_budget:
                self.report.analysis_complete = False
                self.add(
                    "error",
                    "execution.state_budget_exceeded",
                    difficulty=lane,
                    unit=self.package.root,
                    message=(
                        f"abstract execution exceeded the {self.state_budget} per-difficulty "
                        "state budget; "
                        "the report is incomplete"
                    ),
                    details={"state_budget": self.state_budget},
                )
                return reached, False
            visited.add(fingerprint)
            lane_states += 1
            self.report.states_explored += 1
            ref = state.routine_ref
            reached.add(ref.key)
            body = ref.routine.body
            if state.pc >= len(body):
                self._flush_anm_group(state, lane, None)
                if not state.stack:
                    self._check_entity_anm_setup(state, lane, None)
                returned = self._return_state(state)
                if returned is not None:
                    queue.append(returned)
                continue

            node = body[state.pc]
            if not _guard_active(node, lane):
                state.pc += 1
                queue.append(state)
                continue
            state.path = _extend_path(state.path, str(node.node_id))

            if isinstance(node, SyntaxStatement):
                self._flush_anm_group(state, lane, node)
                kind = node.statement_kind
                if kind == "assign":
                    self._apply_assignment(state, node)
                    state.pc += 1
                    queue.append(state)
                    continue
                if kind == "goto":
                    target = self._label_target(ref, node, labels)
                    if target is not None:
                        state.pc = target
                        queue.append(state)
                    continue
                if kind == "conditional_goto":
                    self._enqueue_conditional(state, node, lane, queue, labels)
                    continue
                if kind == "return":
                    if not state.stack:
                        self._check_entity_anm_setup(state, lane, node)
                    returned = self._return_state(state)
                    if returned is not None:
                        queue.append(returned)
                    continue
                if kind in {"call", "async_call"}:
                    if all_routines:
                        self._audit_call_without_expansion(state, node, lane)
                        state.pc += 1
                        queue.append(state)
                        continue
                    self._enqueue_call(state, node, lane, queue)
                    continue
                state.pc += 1
                queue.append(state)
                continue

            if isinstance(node, SemanticOperation):
                if _is_anm_visibility_boundary(node.operation):
                    self._check_entity_anm_setup(state, lane, node)
                if node.operation not in ANM_SET_OPERATIONS:
                    self._flush_anm_group(state, lane, node)
                if self._apply_anm_operation(state, node, lane):
                    state.pc += 1
                    queue.append(state)
                    continue
                if node.operation.startswith("enemy.create"):
                    if not all_routines:
                        self._enqueue_spawn(state, node, lane, queue)
                    state.pc += 1
                    queue.append(state)
                    continue
                if node.operation == "flow.ret":
                    if not state.stack:
                        self._check_entity_anm_setup(state, lane, node)
                    returned = self._return_state(state)
                    if returned is not None:
                        queue.append(returned)
                    continue
                if node.operation == "flow.delete":
                    continue
                state.pc += 1
                queue.append(state)
                continue

            self._flush_anm_group(state, lane, node)
            state.pc += 1
            queue.append(state)

        return reached, True

    def _audit_call_without_expansion(
        self,
        state: _ExecutionState,
        node: SyntaxStatement,
        lane: str,
    ) -> None:
        if node.statement_kind != "async_call":
            return
        callee_name = str(node.attributes.get("function", ""))
        callee = self._resolve_routine(callee_name, state.routine_ref.unit)
        if callee is None or not self._routine_mutates_anm(callee.routine):
            return
        self.add(
            "warning",
            "anm.async_state_race",
            difficulty=lane,
            unit=state.routine_ref.unit,
            routine=state.routine_ref.routine.name,
            node=node,
            message=f"async routine {callee_name} mutates ANM state",
            path=state.path,
            details={"callee": callee_name, "audit_mode": True},
        )

    def _return_state(self, state: _ExecutionState) -> _ExecutionState | None:
        if not state.stack:
            return None
        frame = state.stack[-1]
        caller = self._routine_for_key(frame.routine_key)
        if caller is None:
            return None
        return _ExecutionState(
            routine_ref=caller,
            pc=frame.pc,
            initialized=set(frame.initialized),
            values=dict(frame.values),
            anm=state.anm,
            stack=state.stack[:-1],
            path=state.path,
            spawned=state.spawned,
            entity_root=state.entity_root,
            entity_role=state.entity_role,
        )

    def _label_target(
        self,
        ref: _RoutineRef,
        node: SyntaxStatement,
        cache: dict[str, dict[str, int]],
    ) -> int | None:
        if ref.key not in cache:
            cache[ref.key] = {
                str(candidate.attributes.get("name", "")): index
                for index, candidate in enumerate(ref.routine.body)
                if isinstance(candidate, SyntaxStatement)
                and candidate.statement_kind == "label"
            }
        return cache[ref.key].get(str(node.attributes.get("label", "")))

    def _enqueue_conditional(
        self,
        state: _ExecutionState,
        node: SyntaxStatement,
        lane: str,
        queue: deque[_ExecutionState],
        labels: dict[str, dict[str, int]],
    ) -> None:
        expression = str(node.attributes.get("condition", ""))
        value = _evaluate_condition(expression, state.values)
        if node.attributes.get("condition_type") == "unless" and value is not None:
            value = not value
        target = self._label_target(state.routine_ref, node, labels)
        if value is not False and target is not None:
            branch = state.clone()
            _apply_post_mutations(expression, branch.values, branch.initialized)
            branch.pc = target
            queue.append(branch)
        if value is not True:
            fallthrough = state.clone()
            _apply_post_mutations(expression, fallthrough.values, fallthrough.initialized)
            fallthrough.pc += 1
            queue.append(fallthrough)
        if target is None:
            self.add(
                "error",
                "control_flow.unresolved_target",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message="conditional branch target is unresolved",
                path=state.path,
                details={"label": node.attributes.get("label", "")},
            )

    def _apply_assignment(self, state: _ExecutionState, node: SyntaxStatement) -> None:
        target = str(node.attributes.get("target", ""))
        match = re.fullmatch(r"[%$]([A-Za-z_]\w*)", target.strip())
        if match is None:
            return
        name = match.group(1)
        state.initialized.add(name)
        state.values[name] = _bounded_constant(
            _evaluate_numeric(str(node.attributes.get("expr", "")), state.values)
        )

    def _call_values(
        self,
        callee: _RoutineRef,
        raw_args: Sequence[object],
        caller_values: dict[str, int | float | None],
    ) -> dict[str, int | float | None]:
        signature = self.package.signatures.get(
            callee.routine.name,
            callee.routine.params,
        )
        return {
            name: _bounded_constant(
                _evaluate_numeric(str(raw_args[index]), caller_values)
                if index < len(raw_args)
                else None
            )
            for index, name in enumerate(_parameter_names(signature))
        }

    def _enqueue_call(
        self,
        state: _ExecutionState,
        node: SyntaxStatement,
        lane: str,
        queue: deque[_ExecutionState],
    ) -> None:
        callee_name = str(node.attributes.get("function", ""))
        callee = self._resolve_routine(callee_name, state.routine_ref.unit)
        if callee is None:
            state.pc += 1
            queue.append(state)
            return
        raw_args = node.attributes.get("args", [])
        args = raw_args if isinstance(raw_args, list) else []
        values = self._call_values(callee, args, state.values)
        if node.statement_kind == "async_call":
            inherited = state.anm.clone()
            queue.append(
                self._initial_state(
                    callee,
                    anm=inherited,
                    values=values,
                    path=_extend_path(state.path, f"async:{callee.key}"),
                    spawned=state.spawned,
                    entity_root=state.entity_root,
                    entity_role=state.entity_role,
                )
            )
            if self._routine_mutates_anm(callee.routine):
                self.add(
                    "warning",
                    "anm.async_state_race",
                    difficulty=lane,
                    unit=state.routine_ref.unit,
                    routine=state.routine_ref.routine.name,
                    node=node,
                    message=(
                        f"async routine {callee_name} mutates ANM state; interleaving with the "
                        "caller cannot be ordered statically"
                    ),
                    path=state.path,
                    details={"callee": callee_name},
                )
                state.anm.selected_bank = None
                state.anm.bank_unknown = True
                state.anm.slot_bindings.clear()
                state.anm.slots_unknown = True
            state.pc += 1
            queue.append(state)
            return

        active_keys = {state.routine_ref.key, *(frame.routine_key for frame in state.stack)}
        if callee.key in active_keys:
            self.add(
                "warning",
                "execution.recursive_call_unproven",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message=f"recursive call to {callee_name} was summarized conservatively",
                path=state.path,
                details={"callee": callee_name},
            )
            if self._routine_mutates_anm(callee.routine):
                state.anm.bank_unknown = True
                state.anm.slots_unknown = True
            state.pc += 1
            queue.append(state)
            return
        frame = _ReturnFrame(
            routine_key=state.routine_ref.key,
            pc=state.pc + 1,
            initialized=frozenset(state.initialized),
            values=tuple(sorted(state.values.items())),
        )
        queue.append(
            self._initial_state(
                callee,
                anm=state.anm,
                values=values,
                stack=(*state.stack, frame),
                path=_extend_path(state.path, f"call:{callee.key}"),
                spawned=state.spawned,
                entity_root=state.entity_root,
                entity_role=state.entity_role,
            )
        )

    def _enqueue_spawn(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
        queue: deque[_ExecutionState],
    ) -> None:
        encoded = _operation_operand_text(node, "routine", 0)
        callee_name = _string_literal(encoded)
        if callee_name is None:
            self.add(
                "warning",
                "routine.dynamic_spawn_target_unproven",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message="dynamic enemy routine target cannot be executed statically",
                path=state.path,
                details={"target": encoded},
            )
            return
        callee = self._resolve_routine(callee_name, state.routine_ref.unit)
        if callee is None:
            self.add(
                "warning",
                "routine.spawn_target_unresolved",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message=f"spawned routine {callee_name} is not defined in the loaded package",
                path=state.path,
                details={"callee": callee_name},
            )
            return
        queue.append(
            self._initial_state(
                callee,
                path=_extend_path(state.path, f"spawn:{callee.key}"),
                spawned=True,
                entity_root=callee.key,
                entity_role=_routine_role(callee.unit.role, callee.routine.name),
            )
        )

    def _routine_mutates_anm(self, routine: SemanticRoutine) -> bool:
        return any(
            isinstance(node, SemanticOperation)
            and node.operation in {"anm.select", "anm.reset", *ANM_SET_OPERATIONS}
            for node in routine.body
        )

    def _apply_anm_operation(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
    ) -> bool:
        operation = node.operation
        if operation == "anm.select":
            value = _integer_literal(_operation_operand_text(node, "resource_bank", 0))
            if value is None:
                state.anm.selected_bank = None
                state.anm.bank_unknown = True
                self._dynamic_anm(state, node, lane, "resource_bank")
            else:
                state.anm.selected_bank = value
                state.anm.bank_unknown = False
                known_banks = {item.bank for item in self.package.pool.combinations}
                known_banks.update(item.bank for item in self.package.pool.routine_plays)
                if known_banks and value not in known_banks:
                    self.add(
                        "error",
                        "anm.bank_not_in_target_package",
                        difficulty=lane,
                        unit=state.routine_ref.unit,
                        routine=state.routine_ref.routine.name,
                        node=node,
                        message=f"ANM bank {value} is not used by the target package",
                        path=state.path,
                        details={"bank": value, "known_banks": sorted(known_banks)},
                    )
            return True
        if operation in ANM_SET_OPERATIONS:
            self._apply_anm_set(state, node, lane)
            return True
        if operation in ANM_PLAY_OPERATIONS:
            self._check_anm_play(state, node, lane)
            return True
        if operation == "enemy.death_anm":
            self._check_death_anm(state, node, lane)
            return False
        if operation == "anm.reset":
            self.add(
                "warning",
                "anm.reset_state_unproven",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message="the exact slot effects of anm.reset are undocumented; ANM state was widened",
                path=state.path,
            )
            state.anm.selected_bank = None
            state.anm.bank_unknown = True
            state.anm.slot_bindings.clear()
            state.anm.slots_unknown = True
            return True
        if operation in ANM_SLOT_CONSUMERS:
            self._check_anm_slot_consumer(state, node, lane)
            return True
        return False

    def _apply_anm_set(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
    ) -> None:
        bank = state.anm.selected_bank
        state.anm.configured = True
        slot = _integer_literal(_operation_operand_text(node, "slot", 0))
        script = _integer_literal(_operation_operand_text(node, "script", 1))
        if bank is None and not state.anm.bank_unknown:
            self.add(
                "error",
                "anm.bank_unselected",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message=f"{node.operation} executes without a selected or evidenced default ANM bank",
                path=state.path,
            )
        if bank is None or slot is None or script is None:
            state.anm.pending_dynamic = True
            for name, value in (
                ("resource_bank", bank),
                ("slot", slot),
                ("script", script),
            ):
                if value is None:
                    self._dynamic_anm(state, node, lane, name)
        if slot is not None:
            state.anm.slot_bindings[slot] = script
        if bank is not None and slot is not None and script is not None:
            if state.anm.pending_bank not in {None, bank}:
                self._flush_anm_group(state, lane, node)
            state.anm.pending_bank = bank
            state.anm.pending_actions.append(
                AnmActionCandidate(node.operation, slot, script)
            )

    def _dynamic_anm(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
        operand: str,
    ) -> None:
        self.add(
            "warning",
            "anm.dynamic_operand_unproven",
            difficulty=lane,
            unit=state.routine_ref.unit,
            routine=state.routine_ref.routine.name,
            node=node,
            message=f"dynamic ANM {operand} cannot be checked against target package evidence",
            path=state.path,
            details={"operation": node.operation, "operand": operand},
        )

    def _flush_anm_group(
        self,
        state: _ExecutionState,
        lane: str,
        node: SemanticNode | None,
    ) -> None:
        actions = tuple(state.anm.pending_actions)
        bank = state.anm.pending_bank
        dynamic = state.anm.pending_dynamic
        state.anm.pending_actions.clear()
        state.anm.pending_bank = None
        state.anm.pending_dynamic = False
        if not actions or dynamic or bank is None or not self.package.pool.combinations:
            return
        matching = [
            candidate
            for candidate in self.package.pool.combinations
            if candidate.bank == bank and candidate.actions == actions
        ]
        if any(_anm_role_compatible(state.entity_role, candidate.role) for candidate in matching):
            return
        swapped = any(
            candidate.bank == bank
            and len(candidate.actions) == len(actions)
            and all(
                expected.operation == actual.operation
                and expected.slot == actual.script
                and expected.script == actual.slot
                for expected, actual in zip(candidate.actions, actions)
            )
            for candidate in self.package.pool.combinations
        )
        details = {
            "bank": bank,
            "actions": [
                {"operation": item.operation, "slot": item.slot, "script": item.script}
                for item in actions
            ],
        }
        reference_corpus = self._is_reference_corpus_unit(state.routine_ref.unit)
        wrong_role = bool(matching)
        self.add(
            "warning" if reference_corpus else "error",
            (
                "anm.reference_corpus_extraction_gap"
                if reference_corpus
                else "anm.combination_wrong_unit_role" if wrong_role
                else "anm.slot_script_swapped" if swapped
                else "anm.combination_not_in_target_package"
            ),
            difficulty=lane,
            unit=state.routine_ref.unit,
            routine=state.routine_ref.routine.name,
            node=node,
            message=(
                "ANM slot and script appear swapped relative to target package evidence"
                if swapped
                else "ANM combination exists in the package but not for this unit role"
                if wrong_role
                else "the complete ANM set combination is not present in the target package"
            ),
            path=state.path,
            details={
                **details,
                "unit_role": state.entity_role,
                "candidate_roles": sorted({candidate.role for candidate in matching}),
            },
        )

    def _check_anm_play(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
    ) -> None:
        if node.operation == "anm.selected_play":
            bank = state.anm.selected_bank
            script = _integer_literal(_operation_operand_text(node, "script", 0))
            if bank is None and not state.anm.bank_unknown:
                self.add(
                    "error",
                    "anm.selected_play_without_bank",
                    difficulty=lane,
                    unit=state.routine_ref.unit,
                    routine=state.routine_ref.routine.name,
                    node=node,
                    message="anm.selected_play executes without a selected ANM bank",
                    path=state.path,
                )
        else:
            bank = _integer_literal(_operation_operand_text(node, "resource_bank", 0))
            script = _integer_literal(_operation_operand_text(node, "script", 1))
        if bank is None or script is None:
            self._dynamic_anm(state, node, lane, "resource_bank/script")
            return
        action = AnmActionCandidate(node.operation, None, script)
        matching = [
            candidate
            for candidate in self.package.pool.combinations
            if candidate.bank == bank and candidate.actions == (action,)
        ]
        observed = any(
            _anm_role_compatible(state.entity_role, candidate.role)
            for candidate in matching
        )
        if self.package.pool.combinations and not observed:
            reference_corpus = self._is_reference_corpus_unit(state.routine_ref.unit)
            wrong_role = bool(matching)
            self.add(
                "warning" if reference_corpus else "error",
                (
                    "anm.reference_corpus_extraction_gap"
                    if reference_corpus
                    else "anm.play_wrong_unit_role" if wrong_role
                    else "anm.play_not_in_target_package"
                ),
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message=(
                    f"{node.operation} bank {bank} script {script} is evidenced only for "
                    "a different unit role"
                    if wrong_role
                    else f"{node.operation} bank {bank} script {script} is absent from target package evidence"
                ),
                path=state.path,
                details={
                    "operation": node.operation,
                    "bank": bank,
                    "script": script,
                    "unit_role": state.entity_role,
                    "candidate_roles": sorted({candidate.role for candidate in matching}),
                },
            )

    def _is_reference_corpus_unit(self, unit: _ModuleUnit) -> bool:
        if unit.path is None or self.package.stage_id is None:
            return False
        if self.package.reference_root is not None:
            reference_paths = [self.package.reference_root]
            for entry in self.package.pool.resources.get("ecli", ()):
                relative = Path(str(entry).replace("\\", "/")).with_suffix(".decl")
                reference_paths.append(
                    relative
                    if relative.is_absolute()
                    else self.package.reference_root.parent / relative
                )
            try:
                resolved_unit = unit.path.resolve()
                if any(
                    candidate.is_file() and candidate.resolve() == resolved_unit
                    for candidate in reference_paths
                ):
                    return True
            except OSError:
                pass
        names = {"default.decl"}
        for root_name in (
            f"st{self.package.stage_id}.decl",
            f"stage{self.package.stage_id}.decl",
        ):
            if (ROOT / self.package.game / root_name).is_file():
                names.add(root_name)
        names.update(
            Path(entry).with_suffix(".decl").name
            for entry in self.package.pool.resources.get("ecli", ())
        )
        if unit.path.name not in names:
            return False
        canonical = ROOT / self.package.game / unit.path.name
        try:
            return canonical.is_file() and canonical.resolve() == unit.path.resolve()
        except OSError:
            return False

    def _check_death_anm(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
    ) -> None:
        bank = _integer_literal(_operation_operand_text(node, "resource_bank", 0))
        script = _integer_literal(_operation_operand_text(node, "script", 1))
        if bank is None or script is None:
            self._dynamic_anm(state, node, lane, "resource_bank/script")
            return
        scripts = {
            action.script
            for candidate in self.package.pool.combinations
            if candidate.bank == bank
            for action in candidate.actions
        }
        if self.package.pool.combinations and script not in scripts:
            self.add(
                "warning",
                "anm.death_resource_unproven",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message="death ANM script is not otherwise evidenced in the target package pool",
                path=state.path,
                details={"bank": bank, "script": script},
            )

    def _check_anm_slot_consumer(
        self,
        state: _ExecutionState,
        node: SemanticOperation,
        lane: str,
    ) -> None:
        slot = _integer_literal(_operation_operand_text(node, "slot", 1 if node.operation == "anm.on_et" else 0))
        if slot is None:
            self._dynamic_anm(state, node, lane, "slot")
            return
        if slot in state.anm.slot_bindings:
            return
        if state.anm.slots_unknown:
            self.add(
                "warning",
                "anm.slot_binding_unproven",
                difficulty=lane,
                unit=state.routine_ref.unit,
                routine=state.routine_ref.routine.name,
                node=node,
                message=f"ANM slot {slot} may be changed by an unknown or concurrent ANM effect",
                path=state.path,
                details={"slot": slot, "operation": node.operation},
            )
            return
        self.add(
            "error",
            "anm.slot_unbound",
            difficulty=lane,
            unit=state.routine_ref.unit,
            routine=state.routine_ref.routine.name,
            node=node,
            message=f"{node.operation} consumes ANM slot {slot} before any reachable set_main/set_sprite",
            path=state.path,
            details={"slot": slot, "operation": node.operation},
        )

    def _check_entity_anm_setup(
        self,
        state: _ExecutionState,
        lane: str,
        node: SemanticNode | None,
    ) -> None:
        if not state.spawned or state.anm.configured or state.anm.setup_checked:
            return
        state.anm.setup_checked = True
        root_ref = self._routine_for_key(state.entity_root) or state.routine_ref
        if self._is_reference_corpus_unit(root_ref.unit):
            return
        expected = self._source_routine_has_anm_setup(root_ref, lane)
        if expected is False:
            return
        self.add(
            "error" if expected is True else "warning",
            "anm.unit_without_setup",
            difficulty=lane,
            unit=root_ref.unit,
            routine=root_ref.routine.name,
            node=node,
            message=(
                "spawned unit reaches visible behavior or termination without any reachable "
                "set_main/set_sprite"
            ),
            path=state.path,
            details={
                "entity_root": state.entity_root,
                "unit_role": state.entity_role,
                "source_expected_setup": expected,
            },
        )

    def _source_routine_has_anm_setup(
        self,
        ref: _RoutineRef,
        lane: str,
    ) -> bool | None:
        headers = _generated_headers(ref.unit.text)
        source = headers.get("source", "")
        source_game = normalize_game_id(headers.get("source game", ""))
        if not source or source_game not in KNOWN_GAME_IDS:
            return None
        source_path = _resolve_generated_source(source, ref.unit.path)
        if source_path is None:
            return None
        cache_key = f"{source_game}:{source_path.resolve()}"
        if cache_key not in self._source_module_cache:
            try:
                self._source_module_cache[cache_key] = _semantic_module_from_path(
                    source_path,
                    source_game,
                )
            except (OSError, ValueError):
                self._source_module_cache[cache_key] = None
        module = self._source_module_cache[cache_key]
        if module is None:
            return None
        routine = next(
            (candidate for candidate in module.routines if candidate.name == ref.routine.name),
            None,
        )
        if routine is None:
            return None
        traces, complete = _routine_anm_trace_paths(
            routine,
            lane,
            _default_bank_for_role(
                source_game,
                _routine_role(_artifact_role(source_path), routine.name),
            ),
        )
        if not complete:
            return None
        setup_by_path = [
            any(operation in ANM_SET_OPERATIONS for operation, _bank, _slot, _script in trace)
            for trace in traces
        ]
        if setup_by_path and all(setup_by_path):
            return True
        if any(
            kind in {"call", "async_call"}
            for kind, _target in _routine_control_edges(routine, lane)
        ):
            return None
        if setup_by_path and not any(setup_by_path):
            return False
        return None

    def check_source_target_trace(self) -> None:
        for unit in self.package.units:
            self._check_unit_source_target_trace(unit)

    def _check_unit_source_target_trace(self, unit: _ModuleUnit) -> None:
        headers = _generated_headers(unit.text)
        source_game = normalize_game_id(headers.get("source game", ""))
        source_name = headers.get("source", "")
        if not source_name or source_game not in KNOWN_GAME_IDS or source_game == self.package.game:
            return
        source_path = _resolve_generated_source(source_name, unit.path)
        if source_path is None:
            self.add(
                "warning",
                "anm.source_trace_unavailable",
                unit=unit,
                message="generated ECL names a source file that is not available for ANM trace comparison",
                details={"source": source_name, "source_game": source_game},
            )
            return
        try:
            source_module = _semantic_module_from_path(source_path, source_game)
            plan = build_anm_lowering_plan(
                source_module,
                self.package.game,
                target_pool=self.package.pool,
            )
        except (OSError, ValueError) as exc:
            self.add(
                "warning",
                "anm.source_trace_unavailable",
                unit=unit,
                message=f"source ANM trace could not be reconstructed: {exc}",
                details={"source": str(source_path), "source_game": source_game},
            )
            return

        source_nodes = {
            str(node.node_id): node
            for routine in source_module.routines
            for node in routine.body
        }
        reachable_by_routine = {
            routine.name: {
                lane: _routine_reachable_indices(routine, lane)
                for lane in self.report.difficulties
            }
            for routine in source_module.routines
        }
        unresolved_routines: set[str] = set()
        for routine in source_module.routines:
            reachable = reachable_by_routine[routine.name]
            for index, node in enumerate(routine.body):
                if not isinstance(node, SemanticOperation):
                    continue
                if node.operation not in ANM_RESOURCE_OPERATIONS:
                    continue
                if not any(index in lane_indices for lane_indices in reachable.values()):
                    continue
                if str(node.node_id) not in plan.selections:
                    unresolved_routines.add(routine.name)
                    self.add(
                        "error",
                        "anm.source_action_unresolved",
                        unit=unit,
                        routine=routine.name,
                        line=node.provenance.span.start_line,
                        message=(
                            f"source resource action {node.operation} has no target-package "
                            "ANM selection"
                        ),
                        details={
                            "source_node_id": str(node.node_id),
                            "operation": node.operation,
                            "source": str(source_path),
                        },
                    )

        target_by_name = {routine.name: routine for routine in unit.module.routines}
        for source_routine in source_module.routines:
            if source_routine.name not in target_by_name:
                self.add(
                    "error",
                    "routine.source_target_missing",
                    unit=unit,
                    routine=source_routine.name,
                    message="source routine is absent from the generated target module",
                    details={"source": str(source_path)},
                )
        for lane in self.report.difficulties:
            for source_routine in source_module.routines:
                target_routine = target_by_name.get(source_routine.name)
                if target_routine is None:
                    continue
                source_edges = _routine_control_edges(source_routine, lane)
                target_edges = _routine_control_edges(target_routine, lane)
                if source_edges != target_edges:
                    self.add(
                        "error",
                        "control_flow.source_target_edge_mismatch",
                        difficulty=lane,
                        unit=unit,
                        routine=source_routine.name,
                        message=(
                            "reachable call, async, or spawn edges differ between source "
                            "and generated target"
                        ),
                        details={
                            "source": str(source_path),
                            "expected": _control_edge_details(source_edges),
                            "actual": _control_edge_details(target_edges),
                        },
                    )
                if source_routine.name in unresolved_routines:
                    continue
                initial_bank = _default_bank_for_role(
                    self.package.game,
                    _routine_role(unit.role, target_routine.name),
                )
                expected, expected_complete = _planned_routine_anm_trace_paths(
                    source_routine,
                    lane,
                    initial_bank,
                    plan,
                )
                actual, actual_complete = _routine_anm_trace_paths(
                    target_routine,
                    lane,
                    initial_bank,
                )
                if not expected_complete or not actual_complete:
                    self.add(
                        "warning",
                        "anm.source_target_trace_unproven",
                        difficulty=lane,
                        unit=unit,
                        routine=source_routine.name,
                        message=(
                            "ANM path traces exceed the finite path/state bound; exact "
                            "source-target comparison is unavailable"
                        ),
                        details={
                            "source": str(source_path),
                            "expected_complete": expected_complete,
                            "actual_complete": actual_complete,
                        },
                    )
                    continue
                if expected == actual:
                    continue
                first_node = next(
                    (
                        source_nodes[node_id]
                        for node_id, selection in plan.selections.items()
                        if selection.actions
                        and source_nodes.get(node_id) is not None
                        and source_nodes[node_id].provenance.routine == source_routine.name
                    ),
                    None,
                )
                self.add(
                    "error",
                    "anm.source_target_trace_mismatch",
                    difficulty=lane,
                    unit=unit,
                    routine=source_routine.name,
                    line=(first_node.provenance.span.start_line if first_node is not None else None),
                    message=(
                        "target ANM path traces differ from the lowering plan for this routine; "
                        "an action may be missing, reordered, or attached to the wrong path"
                    ),
                    details={
                        "source": str(source_path),
                        "source_game": source_game,
                        "target_game": self.package.game,
                        "expected": _trace_path_details(expected),
                        "actual": _trace_path_details(actual),
                    },
                )


def _guard_active(node: SemanticNode, lane: str) -> bool:
    return node.guard.is_unconditional or lane in node.guard.mask


def _routine_reachable_indices(routine: SemanticRoutine, lane: str) -> set[int]:
    labels = {
        str(node.attributes.get("name", "")): index
        for index, node in enumerate(routine.body)
        if isinstance(node, SyntaxStatement) and node.statement_kind == "label"
    }
    pending = [0]
    visited: set[int] = set()
    reachable: set[int] = set()
    while pending:
        index = pending.pop()
        if index in visited or not 0 <= index < len(routine.body):
            continue
        visited.add(index)
        node = routine.body[index]
        if not _guard_active(node, lane):
            pending.append(index + 1)
            continue
        reachable.add(index)
        if isinstance(node, SyntaxStatement):
            if node.statement_kind == "goto":
                target = labels.get(str(node.attributes.get("label", "")))
                if target is not None:
                    pending.append(target)
                continue
            if node.statement_kind == "conditional_goto":
                value = _evaluate_condition(
                    str(node.attributes.get("condition", "")),
                    {},
                )
                if node.attributes.get("condition_type") == "unless" and value is not None:
                    value = not value
                target = labels.get(str(node.attributes.get("label", "")))
                if value is not False and target is not None:
                    pending.append(target)
                if value is not True:
                    pending.append(index + 1)
                continue
            if node.statement_kind == "return":
                continue
        if isinstance(node, SemanticOperation) and node.operation in {
            "flow.delete",
            "flow.ret",
        }:
            continue
        pending.append(index + 1)
    return reachable


def _extend_path(path: Sequence[str], item: str) -> tuple[str, ...]:
    return tuple((*path[-15:], item))


def _operation_operand_text(node: SemanticOperation, name: str, fallback: int) -> str:
    return _operand_text(node, name, fallback)


def _integer_literal(value: object) -> int | None:
    number = _literal_number(value)
    return number if isinstance(number, int) and not isinstance(number, bool) else None


def _string_literal(value: object) -> str | None:
    text = str(value).strip()
    if len(text) >= 2 and text[0] == text[-1] == '"':
        return text[1:-1]
    return None


def _default_bank_for_role(game: str, role: str) -> int | None:
    if role in {"boss", "midboss"}:
        return target_bank_for_role(game, "boss")
    if role == "stage":
        return target_bank_for_role(game, "stage")
    return None


def _routine_role(module_role: str, routine_name: str) -> str:
    name = routine_name.lower()
    if "mboss" in name or "midboss" in name:
        return "midboss"
    if name.startswith("boss") or name.startswith("mainboss"):
        return "boss"
    return module_role


def _anm_role_compatible(unit_role: str, candidate_role: str) -> bool:
    if candidate_role in {"common", "global"}:
        return True
    return unit_role == candidate_role


def _is_anm_visibility_boundary(operation: str) -> bool:
    return (
        operation in {"flow.wait", "flow.delete", "bullet.fire", "bullet.fire.immediate"}
        or operation.startswith("movement.")
        or operation.startswith("bullet.macro")
        or operation.startswith("unit.hitbox")
        or operation.startswith("unit.hurtbox")
        or operation.startswith("unit.visibility")
    )


def _bounded_constant(value: int | float | None) -> int | float | None:
    if value is None:
        return None
    if isinstance(value, int) and -8 <= value <= 8:
        return value
    if isinstance(value, float) and -8.0 <= value <= 8.0:
        return value
    return None


def _normalize_expression(
    expression: str,
    values: dict[str, int | float | None],
) -> str | None:
    text = expression.strip()
    text = re.sub(r"\b_?[if]\(([-+]?\d+(?:\.\d+)?f?)\)", r"\1", text)
    text = re.sub(r"(?<=\d)f\b", "", text)
    text = text.replace("&&", " and ").replace("||", " or ")
    text = re.sub(r"!(?!=)", " not ", text)
    text = re.sub(r"([%$])([A-Za-z_]\w*)(?:\+\+|--)", r"\1\2", text)
    unknown = False

    def local(match: re.Match[str]) -> str:
        nonlocal unknown
        value = values.get(match.group(2))
        if value is None:
            unknown = True
            return "0"
        return repr(value)

    text = re.sub(r"([%$])([A-Za-z_]\w*)", local, text)
    if re.search(r"\[[^\]]+\]", text):
        unknown = True
    if unknown:
        return None
    return text.strip()


def _eval_ast(node: ast.AST) -> int | float | bool | None:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
        return node.value
    if isinstance(node, ast.UnaryOp):
        value = _eval_ast(node.operand)
        if value is None:
            return None
        if isinstance(node.op, ast.USub):
            return -value
        if isinstance(node.op, ast.UAdd):
            return +value
        if isinstance(node.op, ast.Not):
            return not bool(value)
        if isinstance(node.op, ast.Invert) and isinstance(value, int):
            return ~value
        return None
    if isinstance(node, ast.BinOp):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        if left is None or right is None:
            return None
        try:
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.BitAnd):
                return int(left) & int(right)
            if isinstance(node.op, ast.BitOr):
                return int(left) | int(right)
            if isinstance(node.op, ast.BitXor):
                return int(left) ^ int(right)
            if isinstance(node.op, ast.LShift):
                return int(left) << int(right)
            if isinstance(node.op, ast.RShift):
                return int(left) >> int(right)
        except (ArithmeticError, ValueError, TypeError):
            return None
    if isinstance(node, ast.BoolOp):
        values = [_eval_ast(item) for item in node.values]
        if any(value is None for value in values):
            return None
        if isinstance(node.op, ast.And):
            return all(bool(value) for value in values)
        if isinstance(node.op, ast.Or):
            return any(bool(value) for value in values)
    if isinstance(node, ast.Compare):
        left = _eval_ast(node.left)
        if left is None:
            return None
        for operator, comparator in zip(node.ops, node.comparators):
            right = _eval_ast(comparator)
            if right is None:
                return None
            if isinstance(operator, ast.Eq):
                valid = left == right
            elif isinstance(operator, ast.NotEq):
                valid = left != right
            elif isinstance(operator, ast.Lt):
                valid = left < right
            elif isinstance(operator, ast.LtE):
                valid = left <= right
            elif isinstance(operator, ast.Gt):
                valid = left > right
            elif isinstance(operator, ast.GtE):
                valid = left >= right
            else:
                return None
            if not valid:
                return False
            left = right
        return True
    return None


def _evaluate_numeric(
    expression: str,
    values: dict[str, int | float | None],
) -> int | float | None:
    normalized = _normalize_expression(expression, values)
    if normalized is None:
        return None
    try:
        result = _eval_ast(ast.parse(normalized, mode="eval"))
    except (SyntaxError, ValueError):
        return None
    if isinstance(result, bool):
        return int(result)
    return result if isinstance(result, (int, float)) else None


def _evaluate_condition(
    expression: str,
    values: dict[str, int | float | None],
) -> bool | None:
    result = _evaluate_numeric(expression, values)
    return None if result is None else bool(result)


def _apply_post_mutations(
    expression: str,
    values: dict[str, int | float | None],
    initialized: set[str],
) -> None:
    for match in re.finditer(r"[%$]([A-Za-z_]\w*)(\+\+|--)", expression):
        name, operation = match.groups()
        initialized.add(name)
        value = values.get(name)
        if value is None:
            values[name] = None
        else:
            values[name] = _bounded_constant(value + (1 if operation == "++" else -1))


def _resolve_generated_source(source: str, target_path: Path | None) -> Path | None:
    normalized = str(source).replace("\\", "/")
    raw = Path(normalized)
    candidates = [raw]
    if not raw.is_absolute():
        candidates.extend((ROOT / raw, ROOT.parent / raw))
        if target_path is not None:
            candidates.append(target_path.parent / raw)
    parts = [part for part in normalized.split("/") if part]
    for index, part in enumerate(parts):
        game = normalize_game_id(part)
        if game in KNOWN_GAME_IDS:
            candidates.append(ROOT.joinpath(*parts[index:]))
            break
    if ROOT.name in parts:
        root_index = parts.index(ROOT.name)
        candidates.append(ROOT.joinpath(*parts[root_index + 1 :]))
    seen: set[Path] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            resolved = candidate.absolute()
        if resolved in seen:
            continue
        seen.add(resolved)
        if candidate.is_file():
            return candidate
    return None


_AnmTraceAction = tuple[str, int | None, int | None, int | None]
_AnmTrace = tuple[_AnmTraceAction, ...]


def _selection_trace(actions: Sequence[Any]) -> list[_AnmTraceAction]:
    return [
        (str(action.operation), action.bank, action.slot, action.script)
        for action in actions
    ]


def _routine_trace_paths(
    routine: SemanticRoutine,
    lane: str,
    initial_bank: int | None,
    emit: Callable[
        [int, SemanticNode, int | None],
        tuple[int | None, tuple[_AnmTraceAction, ...]],
    ],
    *,
    state_limit: int = 20_000,
    action_limit: int = 128,
    path_limit: int = 512,
) -> tuple[tuple[_AnmTrace, ...], bool]:
    labels = {
        str(node.attributes.get("name", "")): index
        for index, node in enumerate(routine.body)
        if isinstance(node, SyntaxStatement) and node.statement_kind == "label"
    }
    pending: list[tuple[int, int | None, _AnmTrace]] = [(0, initial_bank, ())]
    visited: set[tuple[int, int | None, _AnmTrace]] = set()
    terminal: set[_AnmTrace] = set()
    complete = True
    while pending:
        if len(visited) >= state_limit or len(pending) + len(terminal) > path_limit:
            complete = False
            break
        index, bank, trace = pending.pop()
        state = (index, bank, trace)
        if state in visited:
            terminal.add(trace)
            continue
        visited.add(state)
        if not 0 <= index < len(routine.body):
            terminal.add(trace)
            continue
        node = routine.body[index]
        if not _guard_active(node, lane):
            pending.append((index + 1, bank, trace))
            continue
        bank, emitted = emit(index, node, bank)
        next_trace = (*trace, *emitted)
        if len(next_trace) > action_limit:
            terminal.add(next_trace[:action_limit])
            complete = False
            continue
        if isinstance(node, SyntaxStatement):
            if node.statement_kind == "goto":
                target = labels.get(str(node.attributes.get("label", "")))
                if target is not None:
                    pending.append((target, bank, next_trace))
                else:
                    terminal.add(next_trace)
                continue
            if node.statement_kind == "conditional_goto":
                value = _evaluate_condition(
                    str(node.attributes.get("condition", "")),
                    {},
                )
                if node.attributes.get("condition_type") == "unless" and value is not None:
                    value = not value
                target = labels.get(str(node.attributes.get("label", "")))
                if value is not False and target is not None:
                    pending.append((target, bank, next_trace))
                if value is not True:
                    pending.append((index + 1, bank, next_trace))
                if target is None and value is True:
                    terminal.add(next_trace)
                continue
            if node.statement_kind == "return":
                terminal.add(next_trace)
                continue
        if isinstance(node, SemanticOperation) and node.operation in {
            "flow.delete",
            "flow.ret",
        }:
            terminal.add(next_trace)
            continue
        pending.append((index + 1, bank, next_trace))

    if not terminal:
        terminal.update(state[2] for state in visited)
    return tuple(sorted(terminal, key=repr)), complete


def _planned_routine_anm_trace_paths(
    routine: SemanticRoutine,
    lane: str,
    initial_bank: int | None,
    plan: Any,
) -> tuple[tuple[_AnmTrace, ...], bool]:
    actions_by_index: dict[int, tuple[_AnmTraceAction, ...]] = {}
    for index, node in enumerate(routine.body):
        actions: list[_AnmTraceAction] = []
        node_id = str(node.node_id)
        materialization = plan.call_materializations.get(node_id)
        if materialization is not None:
            actions.extend(_selection_trace(materialization.selection.actions))
        selection = plan.selections.get(node_id)
        if selection is not None and selection.actions:
            actions.extend(_selection_trace(selection.actions))
        if actions:
            actions_by_index[index] = tuple(actions)

    def emit(
        index: int,
        _node: SemanticNode,
        bank: int | None,
    ) -> tuple[int | None, tuple[_AnmTraceAction, ...]]:
        actions = actions_by_index.get(index, ())
        for operation, selected, _slot, _script in actions:
            if operation == "anm.select":
                bank = selected
        return bank, actions

    return _routine_trace_paths(routine, lane, initial_bank, emit)


def _routine_anm_trace_paths(
    routine: SemanticRoutine,
    lane: str,
    initial_bank: int | None,
) -> tuple[tuple[_AnmTrace, ...], bool]:
    def emit(
        _index: int,
        node: SemanticNode,
        bank: int | None,
    ) -> tuple[int | None, tuple[_AnmTraceAction, ...]]:
        if not isinstance(node, SemanticOperation):
            return bank, ()
        if node.operation == "anm.select":
            bank = _integer_literal(_operation_operand_text(node, "resource_bank", 0))
            return bank, ((node.operation, bank, None, None),)
        if node.operation in ANM_SET_OPERATIONS:
            return bank, (
                (
                    node.operation,
                    bank,
                    _integer_literal(_operation_operand_text(node, "slot", 0)),
                    _integer_literal(_operation_operand_text(node, "script", 1)),
                ),
            )
        if node.operation in ANM_EXPLICIT_PLAY_OPERATIONS or node.operation == "enemy.death_anm":
            return bank, (
                (
                    node.operation,
                    _integer_literal(_operation_operand_text(node, "resource_bank", 0)),
                    None,
                    _integer_literal(_operation_operand_text(node, "script", 1)),
                ),
            )
        if node.operation == "anm.selected_play":
            return bank, (
                (
                    node.operation,
                    bank,
                    None,
                    _integer_literal(_operation_operand_text(node, "script", 0)),
                ),
            )
        return bank, ()

    return _routine_trace_paths(routine, lane, initial_bank, emit)


def _routine_control_edges(
    routine: SemanticRoutine,
    lane: str,
) -> Counter[tuple[str, str]]:
    reachable = _routine_reachable_indices(routine, lane)
    edges: Counter[tuple[str, str]] = Counter()
    for index, node in enumerate(routine.body):
        if index not in reachable:
            continue
        if isinstance(node, SyntaxStatement) and node.statement_kind in {
            "call",
            "async_call",
        }:
            edges[(node.statement_kind, str(node.attributes.get("function", "")))] += 1
        elif isinstance(node, SemanticOperation) and node.operation.startswith("enemy.create"):
            encoded = _operation_operand_text(node, "routine", 0)
            edges[("spawn", _string_literal(encoded) or encoded)] += 1
    return edges


def _control_edge_details(edges: Counter[tuple[str, str]]) -> list[dict[str, Any]]:
    return [
        {"kind": kind, "target": target, "count": count}
        for (kind, target), count in sorted(edges.items())
    ]


def _trace_details(
    trace: Sequence[_AnmTraceAction],
) -> list[dict[str, Any]]:
    return [
        {"operation": operation, "bank": bank, "slot": slot, "script": script}
        for operation, bank, slot, script in trace
    ]


def _trace_path_details(paths: Sequence[_AnmTrace]) -> list[list[dict[str, Any]]]:
    return [_trace_details(path) for path in paths]


__all__ = [
    "EclExecutionDiagnostic",
    "EclExecutionReport",
    "check_ecl_file",
    "check_ecl_text",
]
