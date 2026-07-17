from __future__ import annotations

from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field, replace
import re
from typing import Any, Iterable

from .control_flow import ControlFlowEdge, analyze_routine_control_flow
from ..dialects.game_profile import GameProfile, profile_for_game
from ..canonical.semantic_ir import (
    DIFFICULTY_LANES,
    DifficultyGuard,
    NodeId,
    OperandValue,
    SemanticModule,
    SemanticOperand,
    SemanticOperation,
    SemanticRoutine,
    contextualize_transform_operands,
)


TRANSFORM_PAYLOAD_NAMES = frozenset({"a", "b", "c", "d", "r", "s", "m", "n"})


def literal_int(value: object) -> int | None:
    text = str(value).strip()
    if not re.fullmatch(r"[-+]?(?:0[xX][0-9a-fA-F]+|\d+)", text):
        return None
    try:
        return int(text, 0)
    except ValueError:
        return None


def active_difficulty_lanes(guard: DifficultyGuard) -> tuple[str, ...]:
    if guard.is_unconditional:
        return DIFFICULTY_LANES
    return tuple(lane for lane in guard.mask if lane in DIFFICULTY_LANES)


def operand_map(operation: SemanticOperation) -> dict[str, OperandValue]:
    return {operand.name: operand.value for operand in operation.operands}


def raw_operand(value: OperandValue | None, default: str = "") -> str:
    if value is None:
        return default
    return value.source_text or (value.expression.text if value.expression else default)


def operation_payload(operation: SemanticOperation, implicit_manager: bool) -> list[OperandValue]:
    values = [operand.value for operand in operation.operands]
    return values if implicit_manager else values[1:]


@dataclass(frozen=True)
class TransformWrite:
    source_node_id: NodeId
    index: int | None
    index_expression: str
    channel: str
    mode: str
    operands: tuple[SemanticOperand, ...]
    source_opcode: int
    parameter_set: str
    string_operand: OperandValue | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_node_id": str(self.source_node_id),
            "index": self.index,
            "index_expression": self.index_expression,
            "channel": self.channel,
            "mode": self.mode,
            "operands": [operand.to_dict() for operand in self.operands],
            "source_opcode": self.source_opcode,
            "parameter_set": self.parameter_set,
            "string_operand": self.string_operand.to_dict() if self.string_operand else None,
        }


@dataclass
class TransformProgram:
    slots: dict[int, TransformWrite] = field(default_factory=dict)
    append_cursor: int = 0
    dynamic_writes: list[TransformWrite] = field(default_factory=list)
    unresolved_patches: list[dict[str, Any]] = field(default_factory=list)

    def replace(self, node: TransformWrite) -> None:
        if node.index is None:
            self.dynamic_writes.append(node)
            return
        self.slots[node.index] = node

    def append(self, node: TransformWrite) -> TransformWrite:
        appended = replace(
            node,
            index=self.append_cursor,
            index_expression=str(self.append_cursor),
        )
        self.slots[self.append_cursor] = appended
        self.append_cursor += 1
        return appended

    def decrement_cursor(self) -> None:
        self.append_cursor = max(0, self.append_cursor - 1)

    def patch_string(self, index_expression: str, value: OperandValue, source_node_id: NodeId) -> None:
        index = literal_int(index_expression)
        if index is None or index not in self.slots:
            self.unresolved_patches.append(
                {
                    "source_node_id": str(source_node_id),
                    "index_expression": index_expression,
                    "value": value.to_dict(),
                }
            )
            return
        self.slots[index] = replace(self.slots[index], string_operand=value)

    def copy_from(self, source: TransformProgram, preserve_cursor: bool) -> None:
        cursor = self.append_cursor
        self.slots = deepcopy(source.slots)
        self.dynamic_writes = deepcopy(source.dynamic_writes)
        self.unresolved_patches = deepcopy(source.unresolved_patches)
        self.append_cursor = cursor if preserve_cursor else source.append_cursor

    def contiguous_prefix(self) -> tuple[int, ...]:
        result: list[int] = []
        index = 0
        while index in self.slots:
            result.append(index)
            index += 1
        return tuple(result)

    def to_dict(self) -> dict[str, Any]:
        prefix = self.contiguous_prefix()
        return {
            "slots": {str(index): node.to_dict() for index, node in sorted(self.slots.items())},
            "append_cursor": self.append_cursor,
            "dynamic_writes": [node.to_dict() for node in self.dynamic_writes],
            "unresolved_patches": deepcopy(self.unresolved_patches),
            "normal_execution_prefix": list(prefix),
            "has_hole_before_last_slot": bool(self.slots) and len(prefix) != max(self.slots) + 1,
        }


@dataclass
class BulletVisual:
    bullet_type: OperandValue | None = None
    color: OperandValue | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "bullet_type": self.bullet_type.to_dict() if self.bullet_type else None,
            "color": self.color.to_dict() if self.color else None,
        }


@dataclass
class ShotFormation:
    mode: str = ""
    ways: OperandValue | None = None
    layers: OperandValue | None = None
    speed_a: OperandValue | None = None
    speed_b: OperandValue | None = None
    angle_a: OperandValue | None = None
    angle_b: OperandValue | None = None
    flags: OperandValue | None = None
    deferred_rank_mutations: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "ways": self.ways.to_dict() if self.ways else None,
            "layers": self.layers.to_dict() if self.layers else None,
            "speed_a": self.speed_a.to_dict() if self.speed_a else None,
            "speed_b": self.speed_b.to_dict() if self.speed_b else None,
            "angle_a": self.angle_a.to_dict() if self.angle_a else None,
            "angle_b": self.angle_b.to_dict() if self.angle_b else None,
            "flags": self.flags.to_dict() if self.flags else None,
            "deferred_rank_mutations": deepcopy(self.deferred_rank_mutations),
        }


@dataclass
class BulletOrigin:
    mode: str = "enemy"
    operands: dict[str, OperandValue] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "operands": {name: value.to_dict() for name, value in self.operands.items()},
        }


@dataclass
class BulletSounds:
    fire: OperandValue | None = None
    transform: OperandValue | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fire": self.fire.to_dict() if self.fire else None,
            "transform": self.transform.to_dict() if self.transform else None,
        }


@dataclass
class AutoFireSchedule:
    interval: OperandValue
    random_initial_delay: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "interval": self.interval.to_dict(),
            "random_initial_delay": self.random_initial_delay,
        }


@dataclass
class BulletEmitterDefinition:
    visual: BulletVisual = field(default_factory=BulletVisual)
    formation: ShotFormation = field(default_factory=ShotFormation)
    origin: BulletOrigin = field(default_factory=BulletOrigin)
    sounds: BulletSounds = field(default_factory=BulletSounds)
    transforms: TransformProgram = field(default_factory=TransformProgram)
    auto_fire: AutoFireSchedule | None = None
    fire_deferred: bool = False

    def snapshot(self) -> BulletEmitterDefinition:
        return deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "visual": self.visual.to_dict(),
            "formation": self.formation.to_dict(),
            "origin": self.origin.to_dict(),
            "sounds": self.sounds.to_dict(),
            "transforms": self.transforms.to_dict(),
            "auto_fire": self.auto_fire.to_dict() if self.auto_fire else None,
            "fire_deferred": self.fire_deferred,
        }


@dataclass
class BulletManagerState:
    manager: str
    definition: BulletEmitterDefinition = field(default_factory=BulletEmitterDefinition)
    revision: int = 0

    def mutate(self) -> None:
        self.revision += 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "manager": self.manager,
            "revision": self.revision,
            "definition": self.definition.to_dict(),
        }


@dataclass(frozen=True)
class EmitterMutation:
    source_node_id: NodeId
    manager: str
    operation: str
    guard: DifficultyGuard
    applied: bool = True

    @property
    def kind(self) -> str:
        return "emitter_mutation"

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source_node_id": str(self.source_node_id),
            "manager": self.manager,
            "operation": self.operation,
            "guard": self.guard.to_dict(),
            "applied": self.applied,
        }


@dataclass(frozen=True)
class EmitterFire:
    source_node_id: NodeId
    manager: str
    trigger: str
    guard: DifficultyGuard
    snapshots: tuple[tuple[str, BulletEmitterDefinition], ...]

    @property
    def kind(self) -> str:
        return "emitter_fire"

    def snapshot_for(self, lane: str) -> BulletEmitterDefinition | None:
        return next((snapshot for candidate, snapshot in self.snapshots if candidate == lane), None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source_node_id": str(self.source_node_id),
            "manager": self.manager,
            "trigger": self.trigger,
            "guard": self.guard.to_dict(),
            "snapshots": {lane: snapshot.to_dict() for lane, snapshot in self.snapshots},
        }


@dataclass(frozen=True)
class BulletSystemAction:
    source_node_id: NodeId
    operation: str
    guard: DifficultyGuard
    operands: tuple[SemanticOperand, ...]

    @property
    def kind(self) -> str:
        return "bullet_system_action"

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source_node_id": str(self.source_node_id),
            "operation": self.operation,
            "guard": self.guard.to_dict(),
            "operands": [operand.to_dict() for operand in self.operands],
        }


BulletAction = EmitterMutation | EmitterFire | BulletSystemAction


@dataclass
class BulletRoutineAnalysis:
    routine: str
    actions: list[BulletAction]
    final_states: dict[str, dict[str, BulletManagerState]]
    resolved_transform_indices: dict[str, dict[str, int | None]] = field(default_factory=dict)
    cyclic_node_ids: frozenset[str] = frozenset()
    diagnostics: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "routine": self.routine,
            "actions": [action.to_dict() for action in self.actions],
            "final_states": {
                lane: {manager: state.to_dict() for manager, state in states.items()}
                for lane, states in self.final_states.items()
            },
            "resolved_transform_indices": deepcopy(self.resolved_transform_indices),
            "cyclic_node_ids": sorted(self.cyclic_node_ids),
            "diagnostics": deepcopy(self.diagnostics),
        }


@dataclass
class BulletModuleAnalysis:
    source_game: str
    routines: list[BulletRoutineAnalysis]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "th062.bullet-analysis",
            "schema_version": 1,
            "source_game": self.source_game,
            "routines": [routine.to_dict() for routine in self.routines],
        }


def transform_node_from_operation(
    operation: SemanticOperation,
    profile: GameProfile,
    append_index: int | None = None,
) -> TransformWrite:
    values = operand_map(operation)
    index_expression = raw_operand(values.get("index"), "")
    index = literal_int(index_expression) if index_expression else append_index
    channel = raw_operand(values.get("channel"), "0")
    mode = raw_operand(values.get("mode"), "0")
    decoded_operands = contextualize_transform_operands(
        operation.operation,
        list(operation.operands),
        profile.sentinels,
        str(operation.annotations.get("transform_mode") or ""),
        operation.provenance.game,
    )
    payload = tuple(
        operand
        for operand in decoded_operands
        if operand.name in TRANSFORM_PAYLOAD_NAMES
    )
    opcode = operation.provenance.opcode if operation.provenance.opcode is not None else -1
    parameter_set = "extended" if any(operand.name in {"c", "d", "m", "n"} for operand in payload) else "base"
    return TransformWrite(
        source_node_id=operation.node_id,
        index=index,
        index_expression=index_expression or (str(append_index) if append_index is not None else ""),
        channel=channel,
        mode=mode,
        operands=payload,
        source_opcode=opcode,
        parameter_set=parameter_set,
    )


class BulletStateInterpreter:
    def __init__(self, game: str) -> None:
        self.profile = profile_for_game(game)
        self.states: dict[str, dict[str, BulletManagerState]] = {
            lane: {} for lane in DIFFICULTY_LANES
        }
        self.actions: list[BulletAction] = []
        self.resolved_transform_indices: dict[str, dict[str, int | None]] = {}
        self.diagnostics: list[dict[str, Any]] = []

    def state(self, lane: str, manager: str) -> BulletManagerState:
        return self.states[lane].setdefault(manager, BulletManagerState(manager))

    def manager_for(self, operation: SemanticOperation) -> str:
        if self.profile.bullet_dialect.implicit_manager:
            return "0"
        values = operand_map(operation)
        manager = values.get("manager")
        if manager is not None:
            return raw_operand(manager, "0")
        return raw_operand(operation.operands[0].value, "0") if operation.operands else "0"

    def record_mutation(self, operation: SemanticOperation, manager: str, applied: bool = True) -> None:
        self.actions.append(
            EmitterMutation(operation.node_id, manager, operation.operation, operation.guard, applied)
        )

    def record_fire(self, operation: SemanticOperation, manager: str, trigger: str) -> None:
        lanes = active_difficulty_lanes(operation.guard)
        snapshots = tuple(
            (lane, self.state(lane, manager).definition.snapshot()) for lane in lanes
        )
        self.actions.append(
            EmitterFire(operation.node_id, manager, trigger, operation.guard, snapshots)
        )

    def apply(self, operation: SemanticOperation) -> None:
        if operation.domain != "bullet":
            return
        name = operation.operation
        lanes = active_difficulty_lanes(operation.guard)

        if name in {"bullet.clear_all", "bullet.cancel_radius", "bullet.clear_radius"}:
            self.actions.append(
                BulletSystemAction(operation.node_id, name, operation.guard, tuple(operation.operands))
            )
            return

        if name == "bullet.manager.copy":
            self.apply_copy(operation, lanes)
            return

        manager = self.manager_for(operation)

        if name == "bullet.fire":
            self.record_fire(operation, manager, "explicit")
            return
        if name == "bullet.fire.immediate":
            self.record_fire(operation, manager, "immediate")
            return
        if name == "bullet.fire.enable":
            for lane in lanes:
                self.state(lane, manager).definition.fire_deferred = False
                self.state(lane, manager).mutate()
            self.record_mutation(operation, manager)
            self.record_fire(operation, manager, "enable")
            return
        if name == "bullet.manager.reset":
            for lane in lanes:
                self.states[lane][manager] = BulletManagerState(manager)
            self.record_mutation(operation, manager)
            return
        if name == "bullet.transform.replace":
            for lane in lanes:
                state = self.state(lane, manager)
                node = transform_node_from_operation(operation, self.profile)
                state.definition.transforms.replace(node)
                self.resolved_transform_indices.setdefault(str(operation.node_id), {})[lane] = node.index
                state.mutate()
            self.record_mutation(operation, manager)
            return
        if name == "bullet.transform.append":
            for lane in lanes:
                state = self.state(lane, manager)
                node = transform_node_from_operation(
                    operation,
                    self.profile,
                    state.definition.transforms.append_cursor,
                )
                appended = state.definition.transforms.append(node)
                self.resolved_transform_indices.setdefault(str(operation.node_id), {})[lane] = appended.index
                state.mutate()
            self.record_mutation(operation, manager)
            return
        if name == "bullet.transform.append_cursor.decrement":
            for lane in lanes:
                state = self.state(lane, manager)
                state.definition.transforms.decrement_cursor()
                state.mutate()
            self.record_mutation(operation, manager)
            return
        if name == "bullet.transform.string_operand.patch":
            values = operation_payload(operation, self.profile.bullet_dialect.implicit_manager)
            index_expression = raw_operand(values[0], "") if values else ""
            value = values[1] if len(values) > 1 else OperandValue.value("")
            for lane in lanes:
                state = self.state(lane, manager)
                state.definition.transforms.patch_string(index_expression, value, operation.node_id)
                state.mutate()
            self.record_mutation(operation, manager)
            return
        if name == "bullet.transform.legacy_config":
            self.record_mutation(operation, manager, applied=False)
            self.diagnostics.append(
                {
                    "source_node_id": str(operation.node_id),
                    "code": "bullet.transform.legacy_config.opaque",
                    "message": "TH06 transform configuration is preserved without inventing slot semantics",
                }
            )
            return

        applied = self.apply_definition_mutation(operation, manager, lanes)
        self.record_mutation(operation, manager, applied)
        if name == "bullet.macro.configure":
            fire_lanes = tuple(
                lane for lane in lanes if not self.state(lane, manager).definition.fire_deferred
            )
            if fire_lanes:
                snapshots = tuple(
                    (lane, self.state(lane, manager).definition.snapshot()) for lane in fire_lanes
                )
                self.actions.append(
                    EmitterFire(operation.node_id, manager, "macro_default", operation.guard, snapshots)
                )

    def apply_copy(self, operation: SemanticOperation, lanes: tuple[str, ...]) -> None:
        values = [operand.value for operand in operation.operands]
        destination = raw_operand(values[0], "0") if values else "0"
        source = raw_operand(values[1], "0") if len(values) > 1 else "0"
        preserve_cursor = self.profile.transform_dialect.uses_append_cursor
        for lane in lanes:
            destination_state = self.state(lane, destination)
            destination_cursor = destination_state.definition.transforms.append_cursor
            copied = self.state(lane, source).definition.snapshot()
            if preserve_cursor:
                copied.transforms.append_cursor = destination_cursor
            destination_state.definition = copied
            destination_state.mutate()
        self.actions.append(
            EmitterMutation(operation.node_id, destination, operation.operation, operation.guard, True)
        )

    def apply_definition_mutation(
        self,
        operation: SemanticOperation,
        manager: str,
        lanes: tuple[str, ...],
    ) -> bool:
        name = operation.operation
        payload = operation_payload(operation, self.profile.bullet_dialect.implicit_manager)
        macro_mode = str(operation.annotations.get("macro_mode") or "")
        applied = True
        for lane in lanes:
            state = self.state(lane, manager)
            definition = state.definition
            if name == "bullet.macro.configure" and len(payload) >= 9:
                definition.visual.bullet_type = payload[0]
                definition.visual.color = payload[1]
                definition.formation.ways = payload[2]
                definition.formation.layers = payload[3]
                definition.formation.speed_a = payload[4]
                definition.formation.speed_b = payload[5]
                definition.formation.angle_a = payload[6]
                definition.formation.angle_b = payload[7]
                definition.formation.flags = payload[8]
                definition.formation.mode = macro_mode
            elif name == "bullet.visual.set" and len(payload) >= 2:
                definition.visual.bullet_type, definition.visual.color = payload[:2]
            elif name == "bullet.origin.offset.set":
                names = [operand.name for operand in operation.operands]
                definition.origin = BulletOrigin(
                    "relative",
                    {
                        operand.name: operand.value
                        for operand in operation.operands
                        if operand.name != "manager"
                    },
                )
                if all(item.startswith("operand_") for item in names):
                    definition.origin.operands = {
                        f"component_{index}": value for index, value in enumerate(payload)
                    }
            elif name == "bullet.origin.polar_offset.set":
                definition.origin = BulletOrigin(
                    "polar_relative",
                    {f"component_{index}": value for index, value in enumerate(payload)},
                )
            elif name == "bullet.origin.distance.set":
                definition.origin.operands["distance"] = payload[0] if payload else OperandValue.value("0")
            elif name == "bullet.origin.absolute.set":
                definition.origin = BulletOrigin(
                    "absolute",
                    {f"component_{index}": value for index, value in enumerate(payload)},
                )
            elif name == "bullet.formation.angles.set" and len(payload) >= 2:
                definition.formation.angle_a, definition.formation.angle_b = payload[:2]
            elif name == "bullet.formation.speeds.set" and len(payload) >= 2:
                definition.formation.speed_a, definition.formation.speed_b = payload[:2]
            elif name == "bullet.formation.counts.set" and len(payload) >= 2:
                definition.formation.ways, definition.formation.layers = payload[:2]
            elif name == "bullet.formation.set" and payload:
                definition.formation.mode = raw_operand(payload[0])
            elif name == "bullet.sounds.set" and payload:
                definition.sounds.fire = payload[0]
                definition.sounds.transform = payload[1] if len(payload) > 1 else None
            elif name == "bullet.fire.defer":
                definition.fire_deferred = True
            elif name in {"bullet.auto_fire.schedule", "bullet.auto_fire.schedule_random_delay"} and payload:
                definition.auto_fire = AutoFireSchedule(
                    payload[0], name.endswith("random_delay")
                )
            elif name in {
                "bullet.formation.speeds.by_difficulty",
                "bullet.formation.counts.by_difficulty",
            } and len(payload) >= 8:
                lane_index = {"E": 0, "N": 1, "H": 2, "L": 3}.get(lane)
                if lane_index is not None:
                    if name.endswith("speeds.by_difficulty"):
                        definition.formation.speed_a = payload[lane_index]
                        definition.formation.speed_b = payload[lane_index + 4]
                    else:
                        definition.formation.ways = payload[lane_index]
                        definition.formation.layers = payload[lane_index + 4]
            elif name in {
                "bullet.formation.speeds.by_rank",
                "bullet.formation.counts.by_rank",
            }:
                definition.formation.deferred_rank_mutations.append(
                    {
                        "source_node_id": str(operation.node_id),
                        "operation": name,
                        "operands": [value.to_dict() for value in payload],
                    }
                )
            else:
                applied = False
                continue
            state.mutate()
        return applied


def analyze_bullet_routine(routine: SemanticRoutine, game: str) -> BulletRoutineAnalysis:
    interpreter = BulletStateInterpreter(game)
    control_flow = analyze_routine_control_flow(routine)
    for node in routine.body:
        if isinstance(node, SemanticOperation):
            interpreter.apply(node)
            node_id = str(node.node_id)
    cyclic_appends = {
        str(node.node_id)
        for node in routine.body
        if isinstance(node, SemanticOperation)
        and node.operation == "bullet.transform.append"
        and str(node.node_id) in control_flow.cyclic_node_ids
    }
    cyclic_indices = (
        _resolve_cyclic_append_indices(routine, interpreter, control_flow.edges)
        if cyclic_appends
        else {}
    )
    for node in routine.body:
        if not isinstance(node, SemanticOperation):
            continue
        node_id = str(node.node_id)
        if node_id not in cyclic_appends:
            continue
        lanes = active_difficulty_lanes(node.guard)
        resolved = cyclic_indices.get(node_id, {lane: None for lane in lanes})
        interpreter.resolved_transform_indices[node_id] = resolved
        if any(index is None for index in resolved.values()):
            interpreter.diagnostics.append(
                {
                    "source_node_id": node_id,
                    "code": "bullet.transform.append.cyclic_control_flow",
                    "message": (
                        "append cursor is loop-carried and cannot be materialized as one static index"
                    ),
                }
            )
    return BulletRoutineAnalysis(
        routine=routine.name,
        actions=interpreter.actions,
        final_states=interpreter.states,
        resolved_transform_indices=interpreter.resolved_transform_indices,
        cyclic_node_ids=control_flow.cyclic_node_ids,
        diagnostics=interpreter.diagnostics,
    )


def _resolve_cyclic_append_indices(
    routine: SemanticRoutine,
    interpreter: BulletStateInterpreter,
    edges: tuple[ControlFlowEdge, ...],
) -> dict[str, dict[str, int | None]]:
    """Resolve looped append cursors when CFG reset barriers make them stable."""

    if not routine.body:
        return {}
    successors: list[list[int]] = [[] for _ in routine.body]
    for edge in edges:
        successors[edge.source_index].append(edge.target_index)

    resolved: dict[str, dict[str, int | None]] = {}
    for lane in DIFFICULTY_LANES:
        incoming: list[dict[str, int | None] | None] = [None] * len(routine.body)
        incoming[0] = {}
        pending = deque([0])
        queued = {0}
        while pending:
            index = pending.popleft()
            queued.discard(index)
            state = dict(incoming[index] or {})
            node = routine.body[index]
            if isinstance(node, SemanticOperation) and lane in active_difficulty_lanes(node.guard):
                manager = interpreter.manager_for(node)
                if node.operation == "bullet.manager.reset":
                    state[manager] = 0
                elif node.operation == "bullet.transform.append":
                    cursor = state.get(manager, 0)
                    state[manager] = cursor + 1 if cursor is not None else None
                elif node.operation == "bullet.transform.append_cursor.decrement":
                    cursor = state.get(manager, 0)
                    state[manager] = max(0, cursor - 1) if cursor is not None else None
                elif (
                    node.operation == "bullet.manager.copy"
                    and not interpreter.profile.transform_dialect.uses_append_cursor
                ):
                    values = [operand.value for operand in node.operands]
                    destination = raw_operand(values[0], "0") if values else "0"
                    source = raw_operand(values[1], "0") if len(values) > 1 else "0"
                    state[destination] = state.get(source, 0)

            for target in successors[index]:
                merged = _merge_cursor_states(incoming[target], state)
                if merged == incoming[target]:
                    continue
                incoming[target] = merged
                if target not in queued:
                    pending.append(target)
                    queued.add(target)

        for index, node in enumerate(routine.body):
            if not isinstance(node, SemanticOperation) or node.operation != "bullet.transform.append":
                continue
            if lane not in active_difficulty_lanes(node.guard):
                continue
            node_id = str(node.node_id)
            state = incoming[index]
            manager = interpreter.manager_for(node)
            resolved.setdefault(node_id, {})[lane] = (
                state.get(manager, 0) if state is not None else None
            )
    return resolved


def _merge_cursor_states(
    current: dict[str, int | None] | None,
    incoming: dict[str, int | None],
) -> dict[str, int | None]:
    if current is None:
        return dict(incoming)
    merged: dict[str, int | None] = {}
    for manager in current.keys() | incoming.keys():
        left = current.get(manager, 0)
        right = incoming.get(manager, 0)
        merged[manager] = left if left == right else None
    return merged


def analyze_bullet_module(module: SemanticModule) -> BulletModuleAnalysis:
    routines = [
        analysis
        for routine in module.routines
        if (analysis := analyze_bullet_routine(routine, module.source_game)).actions
    ]
    return BulletModuleAnalysis(module.source_game, routines)


def bullet_analysis_summary(analysis: BulletModuleAnalysis) -> dict[str, int]:
    actions = [action for routine in analysis.routines for action in routine.actions]
    return {
        "routines": len(analysis.routines),
        "actions": len(actions),
        "mutations": sum(isinstance(action, EmitterMutation) for action in actions),
        "fires": sum(isinstance(action, EmitterFire) for action in actions),
        "system_actions": sum(isinstance(action, BulletSystemAction) for action in actions),
        "diagnostics": sum(len(routine.diagnostics) for routine in analysis.routines),
    }


def iter_fire_actions(analysis: BulletRoutineAnalysis) -> Iterable[EmitterFire]:
    return (action for action in analysis.actions if isinstance(action, EmitterFire))
