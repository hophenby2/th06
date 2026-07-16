from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
from ..canonical.op_ir import op_key_for_opcode
from ..canonical.semantic_ir import (
    RawInstructionOp,
    SemanticModule,
    SemanticOperation,
    SyntaxStatement,
)
from ..dialects.anm_catalog import SOURCE_SET_PURPOSES, source_bank_role, target_bank_for_role
from ..dialects.semantics import generation_for_game
from ..source.parser import parse_decl


ROOT = Path(__file__).resolve().parents[2]
_STAGE_NAME_RE = re.compile(r"^(?:stage|st)(\d{2})(.*)\.decl$", re.IGNORECASE)
_SET_OPERATIONS = {"anm.set_main", "anm.set_sprite"}
_EXPLICIT_BANK_PLAY_OPERATIONS = {
    "anm.play",
    "anm.play_abs",
    "anm.play_high",
    "anm.play_pos",
    "anm.play_rotate",
}
_PLAY_OPERATIONS = {*_EXPLICIT_BANK_PLAY_OPERATIONS, "anm.selected_play"}
_SUPPORTED_OPERATIONS = {"anm.select", *_SET_OPERATIONS, *_PLAY_OPERATIONS}


@dataclass(frozen=True, slots=True)
class AnmActionCandidate:
    operation: str
    slot: int | None
    script: int


@dataclass(frozen=True, slots=True)
class AnmCombinationCandidate:
    bank: int
    role: str
    actions: tuple[AnmActionCandidate, ...]
    occurrences: int
    evidence: tuple[str, ...]
    purpose_scores: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True, slots=True)
class AnmRoutinePlayCandidate:
    operation: str
    bank: int
    script: int
    routine: str
    ordinal: int
    evidence: str


@dataclass(frozen=True, slots=True)
class AnmCandidatePool:
    game: str
    stage_id: str | None
    resources: dict[str, tuple[str, ...]]
    combinations: tuple[AnmCombinationCandidate, ...]
    routine_plays: tuple[AnmRoutinePlayCandidate, ...] = ()

    def for_role(self, role: str | None) -> tuple[AnmCombinationCandidate, ...]:
        if role is None:
            return self.combinations
        return tuple(candidate for candidate in self.combinations if candidate.role == role)


@dataclass(frozen=True, slots=True)
class AnmTargetAction:
    operation: str
    bank: int | None = None
    slot: int | None = None
    script: int | None = None


@dataclass(frozen=True, slots=True)
class AnmCandidateSelection:
    source_node_id: str
    actions: tuple[AnmTargetAction, ...]
    match_kind: str
    target_stage_id: str | None
    evidence: tuple[str, ...]
    source_bank: int | None = None
    source_scripts: tuple[int, ...] = ()
    folded_into: str | None = None
    lossy: bool = False
    dynamic_source: bool = False

    def details(self) -> dict[str, object]:
        return {
            "match_kind": self.match_kind,
            "target_stage_id": self.target_stage_id,
            "evidence": list(self.evidence),
            "source_bank": self.source_bank,
            "source_scripts": list(self.source_scripts),
            "target_actions": [
                {
                    "operation": action.operation,
                    "bank": action.bank,
                    "slot": action.slot,
                    "script": action.script,
                }
                for action in self.actions
            ],
            "folded_into": self.folded_into,
            "dynamic_source": self.dynamic_source,
        }


@dataclass(frozen=True, slots=True)
class AnmLoweringPlan:
    target_game: str
    target_stage_id: str | None
    selections: dict[str, AnmCandidateSelection]
    call_materializations: dict[str, AnmCallSiteMaterialization]
    target_anim: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AnmCallSiteMaterialization:
    call_node_id: str
    callee: str
    selection: AnmCandidateSelection


@dataclass(frozen=True, slots=True)
class _SourceAnmGroup:
    select: SemanticOperation | None
    actions: tuple[SemanticOperation, ...]
    source_bank: int | None
    role: str | None
    routine: str
    bank_ambiguous: bool = False
    operation_ordinal: int | None = None


def _source_name(source: str) -> str:
    return str(source).replace("\\", "/").rsplit("/", 1)[-1]


def stage_id_from_source(source: str) -> str | None:
    match = _STAGE_NAME_RE.match(_source_name(source))
    return match.group(1) if match else None


def _artifact_role(path: Path) -> str:
    name = path.name.lower()
    match = _STAGE_NAME_RE.match(name)
    suffix = match.group(2) if match else ""
    if "mboss" in suffix or re.fullmatch(r"mbs\d*", suffix):
        return "midboss"
    if "boss" in suffix or re.fullmatch(r"bs\d*", suffix):
        return "boss"
    if name == "default.decl":
        return "global"
    return "stage"


def _root_stage_path(game: str, stage_id: str) -> Path | None:
    directory = ROOT / game
    for name in (f"st{stage_id}.decl", f"stage{stage_id}.decl"):
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def _pool_paths(game: str, stage_id: str | None) -> tuple[Path, ...]:
    directory = ROOT / game
    if not directory.is_dir():
        return ()
    if stage_id is None:
        return ()

    root = _root_stage_path(game, stage_id)
    if root is None:
        return ()
    return _pool_paths_from_root(root)


def _pool_paths_from_root(root: Path) -> tuple[Path, ...]:
    if not root.is_file():
        return ()
    program = parse_decl(root)
    paths = [root]
    for entry in program.resources.get("ecli", []):
        if entry.lower() == "default.ecl":
            continue
        relative = Path(str(entry).replace("\\", "/")).with_suffix(".decl")
        sibling = relative if relative.is_absolute() else root.parent / relative
        if sibling.is_file() and sibling not in paths:
            paths.append(sibling)
    return tuple(paths)


def _literal_int(value: object) -> int | None:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return int(text)
    return None


def _routine_role(routine: str) -> str | None:
    normalized = routine.lower()
    if normalized.startswith("mboss") or "midboss" in normalized:
        return "midboss"
    if normalized.startswith("boss"):
        return "boss"
    return None


def _role_for_bank(
    game: str,
    bank: int | None,
    artifact_role: str,
    routine: str = "",
) -> str:
    if bank is not None:
        common_banks = {0, 1} if generation_for_game(game) == "th13_plus" else {0}
        if bank in common_banks:
            return "common"
        role = source_bank_role(game, bank)
        if role == "stage":
            return role
        if role == "boss":
            return _routine_role(routine) or (
                artifact_role if artifact_role in {"boss", "midboss"} else role
            )
    return _routine_role(routine) or artifact_role


def _routine_purpose_scores(routine: str) -> dict[str, int]:
    """Extract weak semantic labels from target-corpus routine evidence.

    Names are evidence only: they rank combinations already proven to exist in
    the target package and never authorize a script outside that package.
    """

    normalized = routine.lower()
    scores: dict[str, int] = {}
    explicit = {
        "blue": "stage_blue",
        "red": "stage_red",
        "green": "stage_green",
        "yellow": "stage_yellow",
    }
    for token, purpose in explicit.items():
        if token in normalized:
            scores[purpose] = 40

    legacy = re.match(r"^([brgy])girl", normalized)
    if legacy:
        purpose = {
            "b": "stage_blue",
            "r": "stage_red",
            "g": "stage_green",
            "y": "stage_yellow",
        }[legacy.group(1)]
        scores[purpose] = max(scores.get(purpose, 0), 35)

    generic = re.search(r"(?:^|_)girl([abcd])(\d+)([a-z]*)$", normalized)
    if generic:
        purpose = {
            "a": "stage_blue",
            "b": "stage_red",
            "c": "stage_green",
            "d": "stage_yellow",
        }[generic.group(1)]
        # Prefer the base preset over suffix variants such as GirlA01b.
        score = 25 if not generic.group(3) else 15
        scores[purpose] = max(scores.get(purpose, 0), score)
    return scores


def _candidate_key(
    bank: int,
    role: str,
    actions: tuple[AnmActionCandidate, ...],
) -> tuple[int, str, tuple[AnmActionCandidate, ...]]:
    return bank, role, actions


@lru_cache(maxsize=64)
def candidate_pool_for_stage(
    game: str,
    stage_id: str | None,
    reference_package: str | Path | None = None,
) -> AnmCandidatePool:
    if stage_id is None and reference_package is not None:
        stage_id = stage_id_from_source(str(reference_package))
    if stage_id is None:
        return AnmCandidatePool(game, None, {}, ())
    counts: Counter[tuple[int, str, tuple[AnmActionCandidate, ...]]] = Counter()
    evidence: dict[tuple[int, str, tuple[AnmActionCandidate, ...]], set[str]] = defaultdict(set)
    purpose_scores: dict[
        tuple[int, str, tuple[AnmActionCandidate, ...]],
        dict[str, int],
    ] = defaultdict(dict)
    routine_plays: list[AnmRoutinePlayCandidate] = []
    resources: dict[str, tuple[str, ...]] = {}

    paths = (
        _pool_paths_from_root(Path(reference_package))
        if reference_package is not None
        else _pool_paths(game, stage_id)
    )
    for path in paths:
        program = parse_decl(path)
        if not resources and _artifact_role(path) == "stage":
            resources = {
                name: tuple(entries)
                for name, entries in program.resources.items()
            }
        artifact_role = _artifact_role(path)
        for function in program.functions:
            play_ordinals: Counter[str] = Counter()
            current_bank = target_bank_for_role(game, artifact_role)
            current_bank_guard = "*"
            pending_bank: int | None = None
            pending_guard: str | None = None
            pending_actions: list[AnmActionCandidate] = []

            def flush() -> None:
                nonlocal pending_bank, pending_guard, pending_actions
                if pending_bank is None or not pending_actions:
                    pending_bank = None
                    pending_guard = None
                    pending_actions = []
                    return
                actions = tuple(pending_actions)
                role = _role_for_bank(game, pending_bank, artifact_role, function.name)
                key = _candidate_key(pending_bank, role, actions)
                counts[key] += 1
                evidence[key].add(f"{path.name}:{function.name}")
                for purpose, score in _routine_purpose_scores(function.name).items():
                    purpose_scores[key][purpose] = max(
                        purpose_scores[key].get(purpose, 0),
                        score,
                    )
                pending_bank = None
                pending_guard = None
                pending_actions = []

            for statement in function.statements:
                if statement.kind != "instruction":
                    flush()
                    if statement.kind in {
                        "async_call",
                        "call",
                        "conditional_goto",
                        "goto",
                        "label",
                        "return",
                    }:
                        current_bank = None
                        current_bank_guard = ""
                    continue
                opcode = int(statement.attrs.get("opcode", -1))
                args = [str(arg) for arg in statement.attrs.get("args", [])]
                guard = str(statement.difficulty or "*")
                operation = op_key_for_opcode(game, opcode)
                if operation == "anm.select":
                    flush()
                    current_bank = _literal_int(args[0]) if args else None
                    current_bank_guard = guard
                    continue
                if current_bank_guard not in {"", "*", guard}:
                    current_bank = None
                    current_bank_guard = ""
                if operation in _SET_OPERATIONS and len(args) >= 2:
                    bank = current_bank
                    slot = _literal_int(args[0])
                    script = _literal_int(args[1])
                    if bank is not None and script is not None:
                        if pending_actions and pending_guard != guard:
                            flush()
                        if pending_bank is None:
                            pending_bank = bank
                        if pending_bank != bank:
                            flush()
                            pending_bank = bank
                        pending_guard = guard
                        pending_actions.append(AnmActionCandidate(operation, slot, script))
                        continue
                flush()
                if operation in _EXPLICIT_BANK_PLAY_OPERATIONS and len(args) >= 2:
                    ordinal = play_ordinals[operation]
                    play_ordinals[operation] += 1
                    bank = _literal_int(args[0])
                    script = _literal_int(args[1])
                    if bank is not None and script is not None:
                        action = AnmActionCandidate(operation, None, script)
                        role = _role_for_bank(game, bank, artifact_role, function.name)
                        key = _candidate_key(bank, role, (action,))
                        counts[key] += 1
                        evidence[key].add(f"{path.name}:{function.name}")
                        routine_plays.append(
                            AnmRoutinePlayCandidate(
                                operation,
                                bank,
                                script,
                                function.name,
                                ordinal,
                                f"{path.name}:{function.name}",
                            )
                        )
                elif operation == "anm.selected_play" and args:
                    ordinal = play_ordinals[operation]
                    play_ordinals[operation] += 1
                    script = _literal_int(args[0])
                    if current_bank is not None and script is not None:
                        action = AnmActionCandidate(operation, None, script)
                        role = _role_for_bank(game, current_bank, artifact_role, function.name)
                        key = _candidate_key(current_bank, role, (action,))
                        counts[key] += 1
                        evidence[key].add(f"{path.name}:{function.name}")
                        routine_plays.append(
                            AnmRoutinePlayCandidate(
                                operation,
                                current_bank,
                                script,
                                function.name,
                                ordinal,
                                f"{path.name}:{function.name}",
                            )
                        )
            flush()

    combinations = tuple(
        AnmCombinationCandidate(
            bank=bank,
            role=role,
            actions=actions,
            occurrences=count,
            evidence=tuple(sorted(evidence[(bank, role, actions)])),
            purpose_scores=tuple(sorted(purpose_scores[(bank, role, actions)].items())),
        )
        for (bank, role, actions), count in sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0][1],
                item[0][0],
                tuple((action.operation, action.slot or -1, action.script) for action in item[0][2]),
            ),
        )
    )
    return AnmCandidatePool(game, stage_id, resources, combinations, tuple(routine_plays))


def candidate_pool_for_module(game: str, source: str) -> AnmCandidatePool:
    stage_id = stage_id_from_source(source)
    if stage_id is None:
        return AnmCandidatePool(game, None, {}, ())
    return candidate_pool_for_stage(game, stage_id)


def _operand_text(node: SemanticOperation, name: str, index: int) -> str | None:
    for operand in node.operands:
        if operand.name == name:
            return operand.value.source_text
    if index < len(node.operands):
        return node.operands[index].value.source_text
    return None


def _node_bank(node: SemanticOperation) -> int | None:
    return _literal_int(_operand_text(node, "resource_bank", 0))


def _node_slot(node: SemanticOperation) -> int | None:
    return _literal_int(_operand_text(node, "slot", 0))


def _node_script(node: SemanticOperation) -> int | None:
    index = 0 if node.operation == "anm.selected_play" else 1
    return _literal_int(_operand_text(node, "script", index))


def _module_role(source: str) -> str:
    name = _source_name(source).lower()
    match = _STAGE_NAME_RE.match(name)
    suffix = match.group(2) if match else ""
    if "mboss" in suffix or re.fullmatch(r"mbs\d*", suffix):
        return "midboss"
    if "boss" in suffix or re.fullmatch(r"bs\d*", suffix):
        return "boss"
    return "stage"


def _source_groups(module: SemanticModule) -> tuple[_SourceAnmGroup, ...]:
    groups: list[_SourceAnmGroup] = []
    default_role = _module_role(module.source)
    for routine in module.routines:
        play_ordinals: Counter[str] = Counter()
        current_bank: int | None = None
        current_bank_guard = None
        bank_ambiguous = False
        pending_select: SemanticOperation | None = None
        pending_guard = None
        pending_actions: list[SemanticOperation] = []

        def flush() -> None:
            nonlocal pending_select, pending_guard, pending_actions
            if pending_select is None and not pending_actions:
                return
            bank = _node_bank(pending_select) if pending_select is not None else current_bank
            role = _role_for_bank(
                module.source_game,
                bank,
                default_role,
                routine.name,
            )
            groups.append(
                _SourceAnmGroup(
                    pending_select,
                    tuple(pending_actions),
                    bank,
                    role,
                    routine.name,
                    bank_ambiguous,
                )
            )
            pending_select = None
            pending_guard = None
            pending_actions = []

        for node in routine.body:
            if not isinstance(node, SemanticOperation):
                flush()
                if isinstance(node, SyntaxStatement) and node.statement_kind in {
                    "async_call",
                    "call",
                    "conditional_goto",
                    "goto",
                    "label",
                    "return",
                }:
                    current_bank = None
                    current_bank_guard = None
                    bank_ambiguous = True
                continue
            if node.operation == "anm.select":
                flush()
                current_bank = _node_bank(node)
                current_bank_guard = node.guard
                bank_ambiguous = current_bank is None
                pending_select = node
                pending_guard = node.guard
                continue
            if node.operation in _SET_OPERATIONS:
                if pending_select is not None and node.guard != pending_select.guard:
                    flush()
                if (
                    current_bank_guard is not None
                    and not current_bank_guard.is_unconditional
                    and node.guard != current_bank_guard
                ):
                    current_bank = None
                    bank_ambiguous = True
                if pending_actions and pending_guard != node.guard:
                    flush()
                pending_guard = node.guard
                pending_actions.append(node)
                continue
            flush()
            if node.operation in _PLAY_OPERATIONS:
                ordinal = play_ordinals[node.operation]
                play_ordinals[node.operation] += 1
                bank = _node_bank(node) if node.operation != "anm.selected_play" else current_bank
                role = _role_for_bank(
                    module.source_game,
                    bank,
                    default_role,
                    routine.name,
                )
                groups.append(
                    _SourceAnmGroup(
                        None,
                        (node,),
                        bank,
                        role,
                        routine.name,
                        bank is None
                        or (bank_ambiguous and node.operation == "anm.selected_play"),
                        ordinal,
                    )
                )
        flush()
    return tuple(groups)


def _candidate_purpose_score(candidate: AnmCombinationCandidate, purpose: str) -> int:
    return dict(candidate.purpose_scores).get(purpose, 0)


def _action_matches(
    candidate: AnmActionCandidate,
    source: SemanticOperation,
    script: int,
) -> bool:
    if candidate.operation != source.operation or candidate.script != script:
        return False
    if source.operation not in _SET_OPERATIONS:
        return True
    source_slot = _node_slot(source)
    return source_slot is None or candidate.slot == source_slot


def _source_purpose(
    module: SemanticModule,
    group: _SourceAnmGroup,
    source_pool: AnmCandidatePool,
    scripts: tuple[int | None, ...] | None = None,
) -> str | None:
    role = group.role or ""
    resolved_scripts = scripts or tuple(_node_script(node) for node in group.actions)
    for node, script in zip(group.actions, resolved_scripts):
        if node.operation not in _SET_OPERATIONS:
            continue
        if script is None:
            continue
        kind = "main" if node.operation == "anm.set_main" else "sprite"
        purpose = SOURCE_SET_PURPOSES.get(
            (
                module.source_game,
                role,
                kind,
                group.source_bank if group.source_bank is not None else -1,
                script,
            )
        )
        if purpose:
            return purpose

    routine_scores = _routine_purpose_scores(group.routine)
    if routine_scores:
        return max(routine_scores, key=lambda purpose: routine_scores[purpose])

    corpus_scores: dict[str, int] = {}
    for candidate in source_pool.for_role(group.role):
        if group.source_bank is not None and candidate.bank != group.source_bank:
            continue
        if not all(
            script is not None
            and any(_action_matches(action, node, script) for action in candidate.actions)
            for node, script in zip(group.actions, resolved_scripts)
        ):
            continue
        for purpose, score in candidate.purpose_scores:
            corpus_scores[purpose] = max(corpus_scores.get(purpose, 0), score)
    if corpus_scores:
        return max(corpus_scores, key=lambda purpose: corpus_scores[purpose])
    return None


def _shape_score(
    candidate: AnmCombinationCandidate,
    source_actions: tuple[SemanticOperation, ...],
) -> int:
    source_kinds = Counter(node.operation for node in source_actions)
    target_kinds = Counter(action.operation for action in candidate.actions)
    shared = sum(min(count, target_kinds[kind]) for kind, count in source_kinds.items())
    return shared * 20 - abs(len(candidate.actions) - len(source_actions)) * 2


def _choose_combination(
    pool: AnmCandidatePool,
    group: _SourceAnmGroup,
    purpose: str | None,
    scripts: tuple[int | None, ...] | None = None,
) -> tuple[AnmCombinationCandidate | None, str]:
    candidates = list(pool.for_role(group.role))
    if not candidates:
        return None, "unresolved"

    if len(group.actions) == 1 and group.operation_ordinal is not None:
        source_operation = group.actions[0].operation
        routine_match = next(
            (
                use
                for use in pool.routine_plays
                if use.routine == group.routine
                and use.operation == source_operation
                and use.ordinal == group.operation_ordinal
            ),
            None,
        )
        if routine_match is not None:
            target_action = AnmActionCandidate(
                routine_match.operation,
                None,
                routine_match.script,
            )
            matched = next(
                (
                    candidate
                    for candidate in candidates
                    if candidate.bank == routine_match.bank
                    and candidate.actions == (target_action,)
                ),
                None,
            )
            if matched is not None:
                return matched, "routine_sequence"

    if purpose:
        purpose_matches = [
            candidate
            for candidate in candidates
            if _candidate_purpose_score(candidate, purpose) > 0
        ]
        if purpose_matches:
            return max(
                purpose_matches,
                key=lambda item: (
                    _candidate_purpose_score(item, purpose),
                    _shape_score(item, group.actions),
                    item.occurrences,
                    -len(item.actions),
                ),
            ), "semantic_purpose"

    source_operations = {node.operation for node in group.actions}
    compatible = [
        candidate
        for candidate in candidates
        if source_operations & {action.operation for action in candidate.actions}
    ]
    if source_operations and not compatible:
        return None, "unresolved"
    if compatible:
        candidates = compatible

    resolved_scripts = scripts or tuple(_node_script(node) for node in group.actions)
    source_scripts = tuple(script for script in resolved_scripts if script is not None)
    if source_scripts:
        exact = [
            candidate
            for candidate in candidates
            if all(
                script is None
                or any(_action_matches(action, node, script) for action in candidate.actions)
                for node, script in zip(group.actions, resolved_scripts)
            )
        ]
        if exact:
            return max(
                exact,
                key=lambda item: (_shape_score(item, group.actions), item.occurrences),
            ), "exact_script"

    ranked = sorted(
        candidates,
        key=lambda item: (
            -_shape_score(item, group.actions),
            -item.occurrences,
            item.bank,
            tuple((action.operation, action.slot or -1, action.script) for action in item.actions),
        ),
    )
    if not ranked:
        return None, "unresolved"
    return ranked[0], "target_corpus_candidate"


def _select_bank(pool: AnmCandidatePool, role: str | None) -> AnmCombinationCandidate | None:
    candidates = list(pool.for_role(role))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item.occurrences)


def _candidate_target_actions(
    candidate: AnmCombinationCandidate,
    *,
    include_select: bool,
) -> tuple[AnmTargetAction, ...]:
    actions: list[AnmTargetAction] = []
    if include_select:
        actions.append(AnmTargetAction("anm.select", bank=candidate.bank))
    actions.extend(
        AnmTargetAction(
            action.operation,
            bank=candidate.bank,
            slot=action.slot,
            script=action.script,
        )
        for action in candidate.actions
    )
    return tuple(actions)


def _candidate_needs_selected_bank(candidate: AnmCombinationCandidate) -> bool:
    return any(
        action.operation in _SET_OPERATIONS or action.operation == "anm.selected_play"
        for action in candidate.actions
    )


def _formal_parameter_names(params: str) -> tuple[str, ...]:
    names: list[str] = []
    for part in params.split(","):
        tokens = re.findall(r"[A-Za-z_]\w*", part)
        if tokens:
            names.append(tokens[-1])
    return tuple(names)


def _formal_script_index(node: SemanticOperation, formals: tuple[str, ...]) -> int | None:
    text = _operand_text(node, "script", 1)
    if text is None:
        return None
    match = re.fullmatch(r"[$%]?([A-Za-z_]\w*)", text.strip())
    if match is None or match.group(1) not in formals:
        return None
    return formals.index(match.group(1))


def _is_entry_anm_group(module: SemanticModule, group: _SourceAnmGroup) -> bool:
    if group.select is None or group.source_bank is None or not group.actions:
        return False
    nodes = (group.select, *group.actions)
    if any(not node.guard.is_unconditional or node.selected_values for node in nodes):
        return False
    if any(
        node.operation in _SET_OPERATIONS and _node_slot(node) is None
        for node in group.actions
    ):
        return False
    routine = next((item for item in module.routines if item.name == group.routine), None)
    if routine is None:
        return False
    positions = [
        index
        for index, item in enumerate(routine.body)
        if str(item.node_id) in {str(node.node_id) for node in nodes}
    ]
    if len(positions) != len(nodes) or positions != list(range(positions[0], positions[0] + len(nodes))):
        return False
    return all(
        isinstance(item, SyntaxStatement) and item.statement_kind in {"comment", "var"}
        for item in routine.body[: positions[0]]
    )


def _direct_calls_to(
    module: SemanticModule,
    callee: str,
) -> tuple[tuple[str, SyntaxStatement], ...] | None:
    calls: list[tuple[str, SyntaxStatement]] = []
    if any(re.search(rf"\b{re.escape(callee)}\b", node.text) for node in module.top_level):
        return None
    for routine in module.routines:
        for node in routine.body:
            if isinstance(node, SemanticOperation):
                if any(
                    operand.value.source_text.strip().strip('"\'') == callee
                    for operand in node.operands
                ):
                    return None
                continue
            if isinstance(node, RawInstructionOp):
                if any(str(arg).strip().strip('"\'') == callee for arg in node.args):
                    return None
                continue
            if not isinstance(node, SyntaxStatement):
                continue
            if node.statement_kind not in {"call", "async_call"}:
                if re.search(rf"\b{re.escape(callee)}\b", node.text):
                    return None
                continue
            if str(node.attributes.get("function", "")) != callee:
                continue
            if node.statement_kind != "call" or routine.name == callee:
                return None
            calls.append((routine.name, node))
    return tuple(calls) if calls else None


def _build_call_bound_materializations(
    module: SemanticModule,
    target_pool: AnmCandidatePool,
    source_pool: AnmCandidatePool,
    groups: tuple[_SourceAnmGroup, ...],
) -> tuple[
    dict[str, AnmCandidateSelection],
    dict[str, AnmCallSiteMaterialization],
    frozenset[str],
]:
    folded_selections: dict[str, AnmCandidateSelection] = {}
    materializations: dict[str, AnmCallSiteMaterialization] = {}
    consumed: set[str] = set()
    seen_routines: set[str] = set()

    source_stage_id = stage_id_from_source(module.source)
    package_paths = _pool_paths(module.source_game, source_stage_id)
    module_path = Path(module.source)
    if not module_path.is_absolute():
        module_path = ROOT / module_path
    external_ecli = tuple(
        entry
        for entry in module.resources.get("ecli", [])
        if entry.lower() != "default.ecl"
    )
    if (
        source_stage_id is None
        or len(package_paths) != 1
        or package_paths[0].resolve() != module_path.resolve()
        or external_ecli
    ):
        return folded_selections, materializations, frozenset()

    for group in groups:
        if (
            group.bank_ambiguous
            or group.routine in seen_routines
            or not _is_entry_anm_group(module, group)
        ):
            continue
        formals = _formal_parameter_names(
            next(routine.params for routine in module.routines if routine.name == group.routine)
        )
        if not formals:
            continue

        bindings: list[tuple[str, int]] = []
        has_formal = False
        valid = True
        for node in group.actions:
            literal = _node_script(node)
            if literal is not None:
                bindings.append(("literal", literal))
                continue
            formal_index = _formal_script_index(node, formals)
            if formal_index is None:
                valid = False
                break
            bindings.append(("formal", formal_index))
            has_formal = True
        calls = _direct_calls_to(module, group.routine)
        if not valid or not has_formal or calls is None:
            continue

        pending: list[tuple[SyntaxStatement, AnmCandidateSelection]] = []
        for _caller, call in calls:
            raw_args = call.attributes.get("args", [])
            if not isinstance(raw_args, list):
                valid = False
                break
            resolved: list[int | None] = []
            for kind, value in bindings:
                if kind == "literal":
                    resolved.append(value)
                elif value < len(raw_args):
                    resolved.append(_literal_int(raw_args[value]))
                else:
                    resolved.append(None)
            scripts = tuple(resolved)
            if any(script is None for script in scripts):
                valid = False
                break
            purpose = _source_purpose(module, group, source_pool, scripts)
            if purpose is None:
                valid = False
                break
            candidate, match_kind = _choose_combination(
                target_pool,
                group,
                purpose,
                scripts,
            )
            if candidate is None or match_kind != "semantic_purpose":
                valid = False
                break
            selection = AnmCandidateSelection(
                source_node_id=str(call.node_id),
                actions=_candidate_target_actions(
                    candidate,
                    include_select=_candidate_needs_selected_bank(candidate),
                ),
                match_kind="call_bound_semantic_purpose",
                target_stage_id=target_pool.stage_id,
                evidence=candidate.evidence,
                source_bank=group.source_bank,
                source_scripts=tuple(int(script) for script in scripts if script is not None),
            )
            pending.append((call, selection))
        if not valid or not pending:
            continue

        seen_routines.add(group.routine)
        call_ids = tuple(str(call.node_id) for call, _selection in pending)
        evidence = tuple(sorted({item for _call, selection in pending for item in selection.evidence}))
        for call, selection in pending:
            materializations[str(call.node_id)] = AnmCallSiteMaterialization(
                call_node_id=str(call.node_id),
                callee=group.routine,
                selection=selection,
            )
        for node in (group.select, *group.actions):
            node_id = str(node.node_id)
            folded_selections[node_id] = AnmCandidateSelection(
                source_node_id=node_id,
                actions=(),
                match_kind="call_bound_folded",
                target_stage_id=target_pool.stage_id,
                evidence=evidence,
                source_bank=group.source_bank,
                folded_into=f"call-sites:{','.join(call_ids)}",
            )
            consumed.add(node_id)

    return folded_selections, materializations, frozenset(consumed)


def build_anm_lowering_plan(
    module: SemanticModule,
    target_game: str,
    *,
    target_pool: AnmCandidatePool | None = None,
) -> AnmLoweringPlan:
    if module.source_game == target_game:
        return AnmLoweringPlan(target_game, stage_id_from_source(module.source), {}, {}, ())

    target_pool = target_pool or candidate_pool_for_module(target_game, module.source)
    source_pool = candidate_pool_for_module(module.source_game, module.source)
    groups = _source_groups(module)
    selections, call_materializations, consumed = _build_call_bound_materializations(
        module,
        target_pool,
        source_pool,
        groups,
    )
    for group in groups:
        group_node_ids = {
            str(node.node_id)
            for node in ((group.select,) if group.select is not None else ()) + group.actions
        }
        if group_node_ids & consumed or group.bank_ambiguous:
            continue
        purpose = _source_purpose(module, group, source_pool)
        if group.select is not None and not group.actions:
            candidate = _select_bank(target_pool, group.role)
            match_kind = "role_bank" if candidate is not None else "unresolved"
        else:
            candidate, match_kind = _choose_combination(target_pool, group, purpose)
        if candidate is None and group.select is not None:
            candidate = _select_bank(target_pool, group.role)
            match_kind = "role_bank" if candidate is not None else "unresolved"
        if candidate is None:
            continue

        source_scripts = tuple(
            script
            for node in group.actions
            if (script := _node_script(node)) is not None
        )
        dynamic = any(
            _node_script(node) is None
            or (node.operation in _SET_OPERATIONS and _node_slot(node) is None)
            for node in group.actions
        )
        lossy = dynamic or match_kind in {"exact_script", "target_corpus_candidate"}
        common = {
            "match_kind": match_kind,
            "target_stage_id": target_pool.stage_id,
            "evidence": candidate.evidence,
            "source_bank": group.source_bank,
            "source_scripts": source_scripts,
        }
        if group.select is not None:
            selections[str(group.select.node_id)] = AnmCandidateSelection(
                source_node_id=str(group.select.node_id),
                actions=(AnmTargetAction("anm.select", bank=candidate.bank),),
                lossy=lossy,
                dynamic_source=dynamic,
                **common,
            )
        if group.actions:
            primary = group.actions[0]
            target_actions = _candidate_target_actions(
                candidate,
                include_select=(
                    group.select is None and _candidate_needs_selected_bank(candidate)
                ),
            )
            selections[str(primary.node_id)] = AnmCandidateSelection(
                source_node_id=str(primary.node_id),
                actions=target_actions,
                lossy=lossy,
                dynamic_source=dynamic,
                **common,
            )
            for folded in group.actions[1:]:
                selections[str(folded.node_id)] = AnmCandidateSelection(
                    source_node_id=str(folded.node_id),
                    actions=(),
                    folded_into=str(primary.node_id),
                    lossy=lossy,
                    dynamic_source=dynamic,
                    **common,
                )

    return AnmLoweringPlan(
        target_game=target_game,
        target_stage_id=target_pool.stage_id,
        selections=selections,
        call_materializations=call_materializations,
        target_anim=target_pool.resources.get("anim", ()),
    )


def supported_candidate_operations() -> frozenset[str]:
    return frozenset(_SUPPORTED_OPERATIONS)


def candidate_summary(pool: AnmCandidatePool) -> dict[str, object]:
    return {
        "game": pool.game,
        "stage_id": pool.stage_id,
        "resources": {name: list(entries) for name, entries in pool.resources.items()},
        "routine_plays": [
            {
                "operation": candidate.operation,
                "bank": candidate.bank,
                "script": candidate.script,
                "routine": candidate.routine,
                "ordinal": candidate.ordinal,
                "evidence": candidate.evidence,
            }
            for candidate in pool.routine_plays
        ],
        "combinations": [
            {
                "bank": candidate.bank,
                "role": candidate.role,
                "occurrences": candidate.occurrences,
                "purpose_scores": dict(candidate.purpose_scores),
                "actions": [
                    {
                        "operation": action.operation,
                        "slot": action.slot,
                        "script": action.script,
                    }
                    for action in candidate.actions
                ],
                "evidence": list(candidate.evidence),
            }
            for candidate in pool.combinations
        ],
    }
