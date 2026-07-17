from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from ..dialects.game_profile import (
    CAP_TRANSFORM_HITBOX_RADIUS,
    CAP_TRANSFORM_HIGHLIGHT_REMOVE,
    CAP_TRANSFORM_HOMING_VELOCITY_BLEND,
    CAP_TRANSFORM_JUMP_LOOP_COUNT,
    CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE,
    CAP_TRANSFORM_RANDOM_SPEED_SUBTYPE,
    CAP_TRANSFORM_SPAWN_BULLET_EXPANDED,
    CAP_TRANSFORM_SPAWN_BULLET_PACKED_V13,
    CAP_TRANSFORM_SPAWN_LASER,
    profile_for_game,
)
from ..legacy.model import BulletTransform
from ..target.origin_ir import LoweredInstruction
from ..canonical.semantic_ir import (
    OperandState,
    OperandValue,
    SemanticOperand,
    SemanticOperation,
    ValueType,
    contextualize_transform_operands,
    transform_engine_value_token,
    transform_keep_current_token,
)
from ..dialects.semantics import (
    bullet_shape_can_encode,
    bullet_shape_is_lossy,
    bullet_shape_semantic,
    bullet_transform_generation_for_game,
    bullet_transform_mode_can_encode,
    bullet_transform_mode_semantic,
    encode_bullet_shape,
    encode_bullet_transform_mode,
    encode_spread_style,
    generation_for_game,
    spread_can_encode,
    spread_is_lossy,
    spread_semantic,
    unsupported_bullet_transform_mode_reason,
)

INT_SENTINEL = "-999999"


def add_int_expr(left: object, right: object) -> str:
    left_s = str(left).strip()
    right_s = str(right).strip()
    if re.fullmatch(r"-?\d+", left_s) and re.fullmatch(r"-?\d+", right_s):
        return str(int(left_s) + int(right_s))
    if left_s == "0":
        return right_s
    return f"{left_s} + {right_s}"


class TransformTimelineState:
    def __init__(self, slot_maps: dict[str, dict[str, str]] | None = None) -> None:
        self.next_start_by_emitter_channel: dict[tuple[str, str], str] = {}
        self.slot_maps = slot_maps or {}

    def reset_emitter(self, emitter_id: str) -> None:
        for key in [key for key in self.next_start_by_emitter_channel if key[0] == emitter_id]:
            self.next_start_by_emitter_channel.pop(key, None)

    def map_slot(self, emitter_id: str, source_slot: str) -> str:
        return self.slot_maps.get(emitter_id, {}).get(source_slot, source_slot)

    def annotate_th12_to_th13plus_args(self, args: list[Any], source_game: str, target: str) -> tuple[list[str] | None, dict[str, Any]]:
        rendered = [str(arg) for arg in args]
        if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus" or len(rendered) != 8:
            return rendered, {}
        emitter_id, source_slot, channel, mode, duration, start, _r, _s = rendered
        reason = unsupported_bullet_transform_mode_reason(source_game, target, mode)
        if reason:
            return None, {"drop": True, "drop_reason": reason}
        target_slot = self.map_slot(emitter_id, source_slot)
        rendered[1] = target_slot
        semantics: dict[str, Any] = {"source_slot": source_slot, "target_slot": target_slot}
        if mode == "8" and start == INT_SENTINEL:
            timeline_key = (emitter_id, channel)
            effective_start = self.next_start_by_emitter_channel.get(timeline_key, "0")
            rendered[5] = effective_start
            self.next_start_by_emitter_channel[timeline_key] = add_int_expr(effective_start, duration)
            semantics["effective_start"] = effective_start
        return rendered, semantics


def build_th12_to_th13plus_slot_maps_from_args(transform_args: list[list[Any]], source_game: str, target: str) -> dict[str, dict[str, str]]:
    if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus":
        return {}
    slots_by_emitter: dict[str, set[int]] = {}
    for args in transform_args:
        rendered = [str(arg) for arg in args]
        if len(rendered) != 8:
            continue
        emitter_id, source_slot, _channel, mode, *_rest = rendered
        if unsupported_bullet_transform_mode_reason(source_game, target, mode):
            continue
        if not re.fullmatch(r"-?\d+", source_slot):
            continue
        slots_by_emitter.setdefault(emitter_id, set()).add(int(source_slot))
    return {
        emitter_id: {str(source_slot): str(index) for index, source_slot in enumerate(sorted(slots))}
        for emitter_id, slots in slots_by_emitter.items()
    }


def annotate_th12_to_th13plus_transforms(transforms: list[BulletTransform], source_game: str, target: str) -> list[BulletTransform]:
    if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus":
        return transforms
    slot_maps = build_th12_to_th13plus_slot_maps_from_args(
        [transform.raw_args for transform in transforms if transform.raw_opcode == 509],
        source_game,
        target,
    )
    state = TransformTimelineState(slot_maps)
    annotated: list[BulletTransform] = []
    for transform in transforms:
        if transform.raw_opcode != 509 or len(transform.raw_args) != 8:
            annotated.append(transform)
            continue
        rendered, semantics = state.annotate_th12_to_th13plus_args(transform.raw_args, source_game, target)
        clone = deepcopy(transform)
        clone.semantics = {**getattr(transform, "semantics", {}), **semantics}
        if rendered is not None:
            clone.raw_args = rendered
        annotated.append(clone)
    return annotated


def target_transform_args(transform: BulletTransform) -> list[str] | None:
    semantics = getattr(transform, "semantics", {}) or {}
    if semantics.get("drop"):
        return None
    return [str(arg) for arg in transform.raw_args]


def normalize_target_float_sentinel(value: str, target: str) -> str:
    return value


def normalized_int(value: object) -> str:
    return str(value).strip()


def legacy_bounce_mode_for_mask(mask: object) -> str | None:
    return {
        "15": "1024",
        "13": "2048",
        "2": "2097152",
        "12": "134217728",
    }.get(normalized_int(mask))


@dataclass(frozen=True)
class BulletTransformIR:
    """Canonical value for one transform-program write.

    Source opcodes select a dialect form only while decoding.  Target opcode
    selection uses ``write_kind`` and ``parameter_set`` plus the target profile.
    """

    source_game: str
    source_opcode: int
    write_kind: str
    parameter_set: str
    values: dict[str, OperandValue]
    mode_semantic: str
    shape_semantic: str | None = None
    source_args: tuple[str, ...] = ()

    @classmethod
    def from_opcode(cls, source_game: str, opcode: int, args: list[Any]) -> "BulletTransformIR | None":
        profile = profile_for_game(source_game)
        form = profile.transform_dialect.form_for_opcode(opcode)
        rendered = [str(arg) for arg in args]
        if not form or form.write_kind == "legacy_config" or len(rendered) != len(form.operand_names):
            return None
        operands = cls._contextualized_values(
            source_game,
            form.write_kind,
            form.operand_names,
            rendered,
        )
        return cls._from_values(
            source_game,
            opcode,
            form.write_kind,
            form.parameter_set,
            operands,
            tuple(rendered),
        )

    @classmethod
    def from_semantic_operation(cls, operation: SemanticOperation) -> "BulletTransformIR | None":
        if operation.operation not in {"bullet.transform.replace", "bullet.transform.append"}:
            return None
        write_kind = operation.operation.rsplit(".", 1)[-1]
        values = {operand.name: operand.value for operand in operation.operands}
        parameter_set = (
            "extended"
            if any(name in values for name in ("c", "d", "m", "n"))
            else "base"
        )
        source_form = operation.annotations.get("source_form")
        if isinstance(source_form, dict):
            annotated_form = str(source_form.get("transform_parameter_set") or "")
            if annotated_form in {"base", "extended"}:
                parameter_set = annotated_form
        return cls._from_values(
            operation.provenance.game,
            operation.provenance.opcode if operation.provenance.opcode is not None else -1,
            write_kind,
            parameter_set,
            values,
            tuple(operation.encoded_args()),
        )

    @classmethod
    def _from_values(
        cls,
        source_game: str,
        source_opcode: int,
        write_kind: str,
        parameter_set: str,
        values: dict[str, OperandValue],
        source_args: tuple[str, ...],
    ) -> "BulletTransformIR":
        mode = cls._raw_value(values.get("mode"), "0")
        mode_semantic = cls._mode_semantic(source_game, mode, values)
        a = cls._raw_value(values.get("a"), "0")
        shape_semantic = bullet_shape_semantic(source_game, a) if mode_semantic == "shape_change" else None
        return cls(
            source_game=source_game,
            source_opcode=source_opcode,
            write_kind=write_kind,
            parameter_set=parameter_set,
            values=dict(values),
            mode_semantic=mode_semantic,
            shape_semantic=shape_semantic,
            source_args=source_args,
        )

    @staticmethod
    def _contextualized_values(
        source_game: str,
        write_kind: str,
        names: tuple[str, ...],
        rendered: list[str],
    ) -> dict[str, OperandValue]:
        operands = [
            SemanticOperand(
                name,
                OperandValue.value(
                    raw,
                    ValueType.FLOAT32 if name in {"r", "s", "m", "n"} else ValueType.INT32,
                ),
            )
            for name, raw in zip(names, rendered)
        ]
        contextualized = contextualize_transform_operands(
            f"bullet.transform.{write_kind}",
            operands,
            profile_for_game(source_game).sentinels,
            bullet_transform_mode_semantic(
                source_game,
                next((raw for name, raw in zip(names, rendered) if name == "mode"), "0"),
            ),
            source_game,
        )
        return {operand.name: operand.value for operand in contextualized}

    @staticmethod
    def _raw_value(value: OperandValue | None, default: str) -> str:
        if value is None:
            return default
        return value.source_text or (value.expression.text if value.expression else default)

    @classmethod
    def _mode_semantic(
        cls,
        source_game: str,
        raw_mode: str,
        values: dict[str, OperandValue],
    ) -> str:
        semantic = bullet_transform_mode_semantic(source_game, raw_mode)
        if bullet_transform_generation_for_game(source_game) == "th13_plus" and raw_mode == "8192":
            return (
                "spawn_bullet_packed_v13"
                if source_game == "th13"
                else "spawn_bullet_expanded"
            )
        if bullet_transform_generation_for_game(source_game) == "th13_plus" and raw_mode == "16384":
            return f"contextual_spawn_attributes:{source_game}"
        if bullet_transform_generation_for_game(source_game) == "th13_plus" and raw_mode == "16":
            subtype = cls._raw_value(values.get("c"), "0")
            return {
                "0": "pause_then_relative_velocity",
                "1": "pause_then_player_related_unknown",
                "2": "pause_then_aimed_velocity",
                "3": "pause_then_marked_direction_velocity",
                "4": "pause_then_velocity",
                "5": "pause_then_random_relative_velocity",
                "6": "pause_then_random_aimed_velocity",
                "7": (
                    "pause_then_preserve_direction_velocity"
                    if profile_for_game(source_game).supports(
                        CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE
                    )
                    else "pause_then_random_speed"
                ),
            }.get(subtype, f"pause_then_subtype:{subtype}")
        return semantic

    def raw(self, name: str, default: str) -> str:
        return self._raw_value(self.values.get(name), default)

    def unsupported_reason(self, target: str, resolved_index: int | str | None = None) -> str | None:
        source_profile = profile_for_game(self.source_game)
        target_profile = profile_for_game(target)
        raw_mode = self.raw("mode", "0")
        if source_profile.transform_dialect.mode_encoding == "opaque":
            return "the source transform dialect is opaque"
        if generation_for_game(self.source_game) == "th06_th08" and target != self.source_game:
            return "TH07/08 transform bitmasks do not have a verified cross-game semantic mapping"
        if (
            bullet_transform_generation_for_game(self.source_game) == "th13_plus"
            and raw_mode == "16"
            and self.parameter_set != "extended"
        ):
            return "modern pause-and-redirect transforms require the extended parameter set"
        if reason := unsupported_bullet_transform_mode_reason(self.source_game, target, raw_mode):
            return reason
        if self.mode_semantic.startswith("contextual_spawn_attributes:") and target != self.source_game:
            return (
                "transform mode 16384 changes meaning with its preceding spawn operation; "
                "cross-game lowering requires a bundled transform sequence"
            )
        if (
            self.mode_semantic == "pause_then_preserve_direction_velocity"
            and not target_profile.supports(CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE)
        ):
            return "pause subtype 7 changes from fixed speed to random speed in TH15"
        required_capability = self.required_capability()
        if required_capability and not target_profile.supports(required_capability):
            return (
                f"transform mode {self.mode_semantic} requires target capability "
                f"{required_capability}"
            )
        for name, value in self.values.items():
            if value.state is not OperandState.ENGINE_SENTINEL or value.engine_value is None:
                continue
            if transform_engine_value_token(target, value.engine_value.kind) is None:
                return (
                    f"engine value {value.engine_value.kind.value} in transform operand {name} "
                    "has no verified target encoding"
                )
        if self.mode_semantic == "shape_change":
            shape_semantic = self.shape_semantic or bullet_shape_semantic(
                self.source_game,
                self.raw("a", "0"),
            )
            if not bullet_shape_can_encode(shape_semantic, target):
                return f"bullet shape {shape_semantic} has no verified target catalog entry"
        target_form = target_profile.transform_dialect.form_for_write(
            self.target_write_kind(target, resolved_index),
            self.target_parameter_set(target),
        )
        if target_form is None:
            if self.parameter_set == "extended":
                return "extended transform parameters cannot be represented by the target dialect"
            if self.write_kind == "append" and resolved_index is None:
                return "the target requires an explicit transform index but the append cursor is unresolved"
            return "the target transform dialect has no compatible write form"
        if self.mode_semantic.startswith("raw:"):
            if target != self.source_game:
                return f"unrecognized source transform mode {raw_mode} cannot be re-encoded safely"
            return None
        target_semantic = self.target_mode_semantic(target)
        if target_semantic.startswith("pause_then_") and generation_for_game(target) == "th13_plus":
            return None
        if not bullet_transform_mode_can_encode(target_semantic, target):
            return f"transform mode {self.mode_semantic} has no target encoding"
        return None

    def lossy_reason(self, target: str) -> str | None:
        target_generation = bullet_transform_generation_for_game(target)
        if (
            self.mode_semantic == "shape_change"
            and self.shape_semantic is not None
            and bullet_shape_is_lossy(self.shape_semantic, target)
        ):
            return "target bullet catalog merges this shape-change visual with its base shape"
        if (
            (self.mode_semantic == "bounce" and self.raw("b", "") == "2" and target_generation == "th10_th11")
            or (self.mode_semantic == "bounce_bottom" and target_generation in {"th12", "th13_plus"})
        ):
            return (
                "bottom-only legacy bounce and parametric bounce-mask count semantics "
                "are not documented as equivalent"
            )
        return None

    def required_capability(self) -> str | None:
        fixed = {
            "spawn_bullet_packed_v13": CAP_TRANSFORM_SPAWN_BULLET_PACKED_V13,
            "spawn_bullet_expanded": CAP_TRANSFORM_SPAWN_BULLET_EXPANDED,
            "spawn_laser": CAP_TRANSFORM_SPAWN_LASER,
            "hitbox_radius": CAP_TRANSFORM_HITBOX_RADIUS,
            "homing_velocity_blend": CAP_TRANSFORM_HOMING_VELOCITY_BLEND,
            "pause_then_random_speed": CAP_TRANSFORM_RANDOM_SPEED_SUBTYPE,
        }.get(self.mode_semantic)
        if fixed is not None:
            return fixed
        if self.mode_semantic == "jump":
            value = self.values.get("b")
            if value is not None and value.state is not OperandState.UNUSED:
                return CAP_TRANSFORM_JUMP_LOOP_COUNT
        if self.mode_semantic == "highlight" and self.raw("a", "") == "2":
            return CAP_TRANSFORM_HIGHLIGHT_REMOVE
        return None

    def with_index(self, index: str) -> "BulletTransformIR":
        values = dict(self.values)
        values["index"] = OperandValue.value(index, ValueType.INT32)
        return BulletTransformIR(
            source_game=self.source_game,
            source_opcode=self.source_opcode,
            write_kind=self.write_kind,
            parameter_set=self.parameter_set,
            values=values,
            mode_semantic=self.mode_semantic,
            shape_semantic=self.shape_semantic,
            source_args=self.source_args,
        )

    def with_slot(self, slot: str) -> "BulletTransformIR":
        return self.with_index(slot)

    def with_emitter(self, emitter_id: str) -> "BulletTransformIR":
        values = dict(self.values)
        values["manager"] = OperandValue.value(emitter_id, ValueType.INT32)
        return BulletTransformIR(
            source_game=self.source_game,
            source_opcode=self.source_opcode,
            write_kind=self.write_kind,
            parameter_set=self.parameter_set,
            values=values,
            mode_semantic=self.mode_semantic,
            shape_semantic=self.shape_semantic,
            source_args=self.source_args,
        )

    def target_write_kind(self, target: str, resolved_index: int | str | None) -> str:
        dialect = profile_for_game(target).transform_dialect
        if self.write_kind == "append" and dialect.form_for_write("append", self.target_parameter_set(target)) is None:
            return "replace" if resolved_index is not None else "append"
        return self.write_kind

    def target_parameter_set(self, target: str) -> str:
        pause_modes = {
            "pause_then_relative_velocity",
            "pause_then_aimed_velocity",
            "pause_then_velocity",
        }
        if (
            generation_for_game(target) == "th13_plus"
            and bullet_transform_generation_for_game(self.source_game) != "th13_plus"
            and self.mode_semantic in pause_modes
        ):
            return "extended"
        if self.parameter_set == "extended" and self.can_project_extended_to_base(target):
            return "base"
        return self.parameter_set

    def can_project_extended_to_base(self, target: str) -> bool:
        if profile_for_game(target).transform_dialect.form_for_write("replace", "extended") is not None:
            return False
        if self.mode_semantic not in {
            "pause_then_relative_velocity",
            "pause_then_aimed_velocity",
            "pause_then_velocity",
        }:
            return False
        if self.raw("d", "") != "0":
            return False
        return all(
            value is not None and value.state is OperandState.UNUSED
            for value in (self.values.get("m"), self.values.get("n"))
        )

    def target_mode_semantic(self, target: str) -> str:
        semantic = {
            "spawn_bullet_packed_v13": "spawn_bullet_advanced",
            "spawn_bullet_expanded": "spawn_bullet_advanced",
        }.get(self.mode_semantic, self.mode_semantic)
        if semantic.startswith("contextual_spawn_attributes:"):
            semantic = "spawn_laser_attributes"
        if bullet_transform_generation_for_game(target) != "th10_th11":
            return semantic
        if semantic == "bounce":
            return {
                "15": "bounce_all",
                "13": "bounce_no_bottom",
                "2": "bounce_bottom",
                "12": "bounce_horizontal",
            }.get(normalized_int(self.raw("b", "-999999")), semantic)
        if semantic == "wall_pass" and normalized_int(self.raw("b", "-999999")) == "12":
            return "wall_pass_horizontal"
        return semantic

    def encoded_state(self, name: str, target: str, default: str) -> str:
        value = self.values.get(name)
        if value is None:
            return default
        sentinels = profile_for_game(target).sentinels
        is_float = name in {"r", "s", "m", "n"}
        if value.state is OperandState.ENGINE_SENTINEL and value.engine_value is not None:
            token = transform_engine_value_token(target, value.engine_value.kind)
            return token if token is not None else self.raw(name, default)
        if value.state is OperandState.UNUSED:
            token = sentinels.unused_float if is_float else sentinels.unused_int
            return token if token is not None else self.raw(name, default)
        if value.state is OperandState.KEEP_CURRENT and is_float:
            token = (
                transform_keep_current_token(
                    target,
                    self.target_mode_semantic(target),
                    name,
                )
                or sentinels.keep_current_float
                or sentinels.unused_float
            )
            return token if token is not None else self.raw(name, default)
        raw = self.raw(name, default)
        return normalize_target_float_sentinel(raw, target) if is_float else raw

    def encoded_a(self, target: str) -> str:
        value = self.encoded_state("a", target, profile_for_game(target).sentinels.unused_int or "-999999")
        if self.mode_semantic != "shape_change":
            return value
        return encode_bullet_shape(self.shape_semantic or bullet_shape_semantic(self.source_game, value), target, value)

    def encoded_mode(self, target: str) -> str:
        semantic = self.target_mode_semantic(target)
        if semantic.startswith("pause_then_") and generation_for_game(target) == "th13_plus":
            return "16"
        return encode_bullet_transform_mode(semantic, target, self.raw("mode", "0"))

    def encoded_b(self, target: str) -> str:
        sentinels = profile_for_game(target).sentinels
        value = self.encoded_state("b", target, sentinels.unused_int or "-999999")
        if bullet_transform_generation_for_game(target) in {"th12", "th13_plus"}:
            return {
                "bounce_all": "15",
                "bounce_no_bottom": "13",
                "bounce_bottom": "2",
                "bounce_horizontal": "12",
                "wall_pass_horizontal": "12",
            }.get(self.mode_semantic, value)
        if self.mode_semantic in {"bounce", "wall_pass"}:
            return sentinels.unused_int or value
        return value

    def encoded_r(self, target: str) -> str:
        sentinels = profile_for_game(target).sentinels
        value = self.encoded_state("r", target, sentinels.unused_float or "-999999.0f")
        if bullet_transform_generation_for_game(target) in {"th12", "th13_plus"} and self.mode_semantic in {"bounce_bottom", "bounce_horizontal", "wall_pass_horizontal"}:
            return sentinels.unused_float or value
        if bullet_transform_generation_for_game(target) == "th10_th11" and self.target_mode_semantic(target) in {"bounce_bottom", "bounce_horizontal", "wall_pass_horizontal"}:
            return sentinels.unused_float or value
        return value

    def th13plus_pause_subtype(self) -> str:
        return {
            "pause_then_relative_velocity": "0",
            "pause_then_aimed_velocity": "2",
            "pause_then_velocity": "4",
        }.get(self.mode_semantic, self.raw("c", "0"))

    def encoded_field(self, name: str, target: str, resolved_index: int | str | None) -> str:
        sentinels = profile_for_game(target).sentinels
        if name == "manager":
            return self.raw("manager", "0")
        if name == "index":
            return str(resolved_index) if resolved_index is not None else self.raw("index", "0")
        if name == "channel":
            return self.raw("channel", "0")
        if name == "mode":
            return self.encoded_mode(target)
        if name == "a":
            return self.encoded_a(target)
        if name == "b":
            return self.encoded_b(target)
        if name == "r":
            return self.encoded_r(target)
        if name == "c" and self.encoded_mode(target) == "16":
            return self.th13plus_pause_subtype()
        if (
            name == "d"
            and self.parameter_set == "base"
            and self.target_parameter_set(target) == "extended"
            and self.encoded_mode(target) == "16"
        ):
            return "0"
        default = sentinels.unused_float if name in {"r", "s", "m", "n"} else sentinels.unused_int
        return self.encoded_state(name, target, default or ("-999999.0f" if name in {"r", "s", "m", "n"} else "-999999"))

    def lower_to(
        self,
        target: str,
        resolved_index: int | str | None = None,
    ) -> LoweredInstruction | None:
        if self.unsupported_reason(target, resolved_index):
            return None
        target_profile = profile_for_game(target)
        write_kind = self.target_write_kind(target, resolved_index)
        parameter_set = self.target_parameter_set(target)
        form = target_profile.transform_dialect.form_for_write(write_kind, parameter_set)
        if form is None:
            return None
        args = [self.encoded_field(name, target, resolved_index) for name in form.operand_names]
        return LoweredInstruction(form.opcode, args)


@dataclass(frozen=True)
class BulletSpawnTransformBundleIR:
    """A spawned-bullet operation represented by two transform records.

    TH11/12 mode 524288 consumes the following mode-1048576 record as the
    second half of its payload. TH13 retains that packed layout under modes
    8192/16384. TH14+ expands the same fields across two extended records.
    """

    source_game: str
    write_kind: str
    manager: str
    first_index: str | None
    second_index: str | None
    channel: str
    spread_style: str
    bullet_shape: str
    bullet_color: str
    resume_transform_index: str
    remove_source_bullet: str
    way_count: str
    layer_count: str
    direction: str
    direction_delta: str
    speed: str
    speed_delta: str
    cancel_effect_id: str

    @classmethod
    def from_operations(
        cls,
        first_node: SemanticOperation,
        second_node: SemanticOperation,
    ) -> "BulletSpawnTransformBundleIR | None":
        if (
            first_node.operation not in {"bullet.transform.replace", "bullet.transform.append"}
            or second_node.operation != first_node.operation
            or first_node.provenance.game != second_node.provenance.game
            or first_node.guard != second_node.guard
            or first_node.selected_values
            or second_node.selected_values
        ):
            return None
        first = BulletTransformIR.from_semantic_operation(first_node)
        second = BulletTransformIR.from_semantic_operation(second_node)
        if first is None or second is None:
            return None
        if (
            first.write_kind != second.write_kind
            or first.raw("manager", "0") != second.raw("manager", "0")
            or first.raw("channel", "0") != second.raw("channel", "0")
        ):
            return None

        first_index = first.raw("index", "") or None
        second_index = second.raw("index", "") or None
        if first.write_kind == "replace":
            parsed_first = _parse_integer_literal(first_index)
            parsed_second = _parse_integer_literal(second_index)
            if parsed_first is None or parsed_second != parsed_first + 1:
                return None

        packed_pair = (
            first.mode_semantic == "spawn_bullet_legacy"
            and second.mode_semantic == "spawn_bullet_layers_legacy"
            and first.parameter_set == second.parameter_set == "base"
        ) or (
            first.mode_semantic == "spawn_bullet_packed_v13"
            and second.mode_semantic == "contextual_spawn_attributes:th13"
            and first.parameter_set == second.parameter_set == "base"
        )
        if packed_pair:
            packed = _parse_integer_literal(first.raw("a", ""))
            if packed is None or not -(1 << 31) <= packed <= 0xFFFFFFFF:
                return None
            payload = packed & 0xFFFFFFFF
            shape_byte = (payload >> 8) & 0xFF
            jump_and_delete = (payload >> 24) & 0xFF
            return cls(
                source_game=first.source_game,
                write_kind=first.write_kind,
                manager=first.raw("manager", "0"),
                first_index=first_index,
                second_index=second_index,
                channel=first.raw("channel", "0"),
                spread_style=str(payload & 0xFF),
                bullet_shape=str(shape_byte - 0x100 if shape_byte & 0x80 else shape_byte),
                bullet_color=str((payload >> 16) & 0xFF),
                resume_transform_index=str(jump_and_delete & 0x7F),
                remove_source_bullet="1" if jump_and_delete & 0x80 else "0",
                way_count=first.raw("b", "0"),
                layer_count=second.raw("a", "0"),
                direction=second.raw("r", "0.0f"),
                direction_delta=second.raw("s", "0.0f"),
                speed=first.raw("r", "0.0f"),
                speed_delta=first.raw("s", "0.0f"),
                cancel_effect_id=second.raw("b", "0"),
            )

        expanded_pair = (
            first.mode_semantic == "spawn_bullet_expanded"
            and second.mode_semantic == f"contextual_spawn_attributes:{first.source_game}"
            and first.parameter_set == second.parameter_set == "extended"
            and all(
                _is_zero_float_literal(second.raw(name, ""))
                for name in ("r", "s", "m", "n")
            )
        )
        if not expanded_pair:
            return None
        return cls(
            source_game=first.source_game,
            write_kind=first.write_kind,
            manager=first.raw("manager", "0"),
            first_index=first_index,
            second_index=second_index,
            channel=first.raw("channel", "0"),
            spread_style=first.raw("a", "0"),
            bullet_shape=second.raw("a", "0"),
            bullet_color=second.raw("b", "0"),
            resume_transform_index=first.raw("b", "0"),
            remove_source_bullet=second.raw("c", "0"),
            way_count=first.raw("c", "0"),
            layer_count=first.raw("d", "0"),
            direction=first.raw("r", "0.0f"),
            direction_delta=first.raw("s", "0.0f"),
            speed=first.raw("m", "0.0f"),
            speed_delta=first.raw("n", "0.0f"),
            cancel_effect_id=second.raw("d", "0"),
        )

    def unsupported_reason(
        self,
        target: str,
        first_index: int | str | None = None,
        second_index: int | str | None = None,
    ) -> str | None:
        target_profile = profile_for_game(target)
        spread = spread_semantic(self.source_game, self.spread_style)
        if not spread_can_encode(spread, target):
            return "spawn bundle spread style has no exact target encoding"
        if spread_is_lossy(spread, target):
            return "spawn bundle spread style requires a multi-emitter target expansion"
        shape = bullet_shape_semantic(self.source_game, self.bullet_shape)
        if not bullet_shape_can_encode(shape, target):
            return f"spawn bundle bullet shape {shape} has no verified target catalog entry"
        if bullet_shape_is_lossy(shape, target):
            return "target bullet catalog merges the spawn bundle's bullet shape"
        color = _parse_integer_literal(self.bullet_color)
        if color is None or not 0 <= color <= 0xFF:
            return "spawn bundle bullet color must be one literal palette index"
        if target == "th10":
            return (
                "TH10's spawn payload cannot encode the TH11+ bullet color and "
                "resume-transform fields"
            )
        if self.write_kind == "append" and not target_profile.transform_dialect.uses_append_cursor:
            parsed_first = _parse_integer_literal(first_index)
            parsed_second = _parse_integer_literal(second_index)
            if parsed_first is None or parsed_second != parsed_first + 1:
                return "the target requires one resolved contiguous pair of transform indices"
        if target == "th13" or bullet_transform_generation_for_game(target) == "th12":
            return self._packed_payload_error(target)
        if target_profile.supports(CAP_TRANSFORM_SPAWN_BULLET_EXPANDED):
            return None
        return "the target has no verified spawned-bullet transform bundle encoding"

    def lower_to(
        self,
        target: str,
        first_index: int | str | None = None,
        second_index: int | str | None = None,
    ) -> list[LoweredInstruction] | None:
        if self.unsupported_reason(target, first_index, second_index):
            return None
        target_profile = profile_for_game(target)
        write_kind = self.write_kind
        if write_kind == "append" and not target_profile.transform_dialect.uses_append_cursor:
            write_kind = "replace"

        if target == "th13" or bullet_transform_generation_for_game(target) == "th12":
            form = target_profile.transform_dialect.form_for_write(write_kind, "base")
            packed = self._packed_payload(target)
            if form is None or packed is None:
                return None
            modes = ("8192", "16384") if target == "th13" else ("524288", "1048576")
            indices = self._target_indices(first_index, second_index)
            records = (
                {
                    "manager": self.manager,
                    "index": indices[0],
                    "channel": self.channel,
                    "mode": modes[0],
                    "a": packed,
                    "b": self.way_count,
                    "r": self._encode_float(self.speed, target, "m", keep_current=True),
                    "s": self._encode_float(self.speed_delta, target, "n"),
                },
                {
                    "manager": self.manager,
                    "index": indices[1],
                    "channel": self.channel,
                    "mode": modes[1],
                    "a": self.layer_count,
                    "b": self.cancel_effect_id,
                    "r": self._encode_float(self.direction, target, "r", keep_current=True),
                    "s": self._encode_float(self.direction_delta, target, "s"),
                },
            )
            return [
                LoweredInstruction(form.opcode, [record[name] for name in form.operand_names])
                for record in records
            ]

        form = target_profile.transform_dialect.form_for_write(write_kind, "extended")
        if form is None:
            return None
        indices = self._target_indices(first_index, second_index)
        records = (
            {
                "manager": self.manager,
                "index": indices[0],
                "channel": self.channel,
                "mode": "8192",
                "a": self._encoded_spread(target),
                "b": self.resume_transform_index,
                "c": self.way_count,
                "d": self.layer_count,
                "r": self._encode_float(self.direction, target, "r", keep_current=True),
                "s": self._encode_float(self.direction_delta, target, "s"),
                "m": self._encode_float(self.speed, target, "m", keep_current=True),
                "n": self._encode_float(self.speed_delta, target, "n"),
            },
            {
                "manager": self.manager,
                "index": indices[1],
                "channel": self.channel,
                "mode": "16384",
                "a": self._encoded_shape(target),
                "b": self.bullet_color,
                "c": self.remove_source_bullet,
                "d": self.cancel_effect_id,
                "r": "0.0f",
                "s": "0.0f",
                "m": "0.0f",
                "n": "0.0f",
            },
        )
        return [
            LoweredInstruction(form.opcode, [record[name] for name in form.operand_names])
            for record in records
        ]

    def _target_indices(
        self,
        first_index: int | str | None,
        second_index: int | str | None,
    ) -> tuple[str, str]:
        return (
            str(first_index) if first_index is not None else str(self.first_index or "0"),
            str(second_index) if second_index is not None else str(self.second_index or "0"),
        )

    def _encoded_spread(self, target: str) -> str:
        return encode_spread_style(
            spread_semantic(self.source_game, self.spread_style),
            target,
            self.spread_style,
        )

    def _encoded_shape(self, target: str) -> str:
        return encode_bullet_shape(
            bullet_shape_semantic(self.source_game, self.bullet_shape),
            target,
            self.bullet_shape,
        )

    def _packed_payload_error(self, target: str) -> str | None:
        fields = {
            "spread_style": (self._encoded_spread(target), 0, 0xFF),
            "bullet_shape": (self._encoded_shape(target), -0x80, 0xFF),
            "bullet_color": (self.bullet_color, 0, 0xFF),
            "resume_transform_index": (self.resume_transform_index, 0, 0x7F),
            "remove_source_bullet": (self.remove_source_bullet, 0, 1),
        }
        for name, (value, minimum, maximum) in fields.items():
            parsed = _parse_integer_literal(value)
            if parsed is None or not minimum <= parsed <= maximum:
                return f"spawn bundle field {name} cannot be packed into the target payload"
        return None

    def _packed_payload(self, target: str) -> str | None:
        if self._packed_payload_error(target):
            return None
        spread = int(self._encoded_spread(target), 0)
        shape = int(self._encoded_shape(target), 0)
        color = int(self.bullet_color, 0)
        jump = int(self.resume_transform_index, 0)
        remove = int(self.remove_source_bullet, 0)
        packed = (
            (spread & 0xFF)
            | ((shape & 0xFF) << 8)
            | ((color & 0xFF) << 16)
            | (((jump & 0x7F) | (remove << 7)) << 24)
        )
        return str(packed - (1 << 32) if packed & (1 << 31) else packed)

    def _encode_float(
        self,
        raw: str,
        target: str,
        operand_name: str,
        *,
        keep_current: bool = False,
    ) -> str:
        source_codec = profile_for_game(self.source_game).sentinels
        target_codec = profile_for_game(target).sentinels
        source_keep = transform_keep_current_token(
            self.source_game,
            "spawn_bullet_advanced",
            operand_name,
        )
        if keep_current and (
            source_codec.is_keep_current_float(raw)
            or (source_keep is not None and raw == source_keep)
        ):
            return (
                transform_keep_current_token(target, "spawn_bullet_advanced", operand_name)
                or target_codec.keep_current_float
                or target_codec.unused_float
                or raw
            )
        if source_codec.is_unused_float(raw):
            return target_codec.unused_float or raw
        return raw


def _parse_integer_literal(value: object) -> int | None:
    text = str(value or "").strip()
    if not re.fullmatch(r"[-+]?(?:0[xX][0-9a-fA-F]+|\d+)", text):
        return None
    try:
        return int(text, 0)
    except ValueError:
        return None


def _is_zero_float_literal(value: object) -> bool:
    text = str(value or "").strip().lower()
    if not re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?f?", text):
        return False
    try:
        return float(text.rstrip("f")) == 0.0
    except ValueError:
        return False


def bullet_transform_ir_from_opcode(source_game: str, opcode: int, args: list[Any], append_slot: int | str | None = None) -> BulletTransformIR | None:
    transform = BulletTransformIR.from_opcode(source_game, opcode, args)
    if not transform:
        return None
    if "index" not in transform.values and append_slot is not None:
        transform = transform.with_index(str(append_slot))
    return transform


def lower_transform_opcode_to_instruction(source_game: str, target: str, opcode: int, args: list[Any], append_slot: int | str | None = None) -> LoweredInstruction | None:
    transform = bullet_transform_ir_from_opcode(source_game, opcode, args, append_slot)
    if not transform:
        return None
    return transform.lower_to(target, append_slot)


def th12_random_angle_expression_bound(expr: str) -> str:
    normalized = str(expr).strip()
    match = re.fullmatch(r"\[-9998\.0f\]\s*/\s*_f\(([-+]?\d+(?:\.\d+)?)\)", normalized)
    if match:
        return f"3.1415927f / _f({match.group(1)})"
    match = re.fullmatch(r"\[-9998\.0f\]\s*/\s*([-+]?\d+(?:\.\d+)?f?)", normalized)
    if match:
        denom = match.group(1)
        return f"3.1415927f / {denom}"
    if normalized == "[-9998.0f]":
        return "3.1415927f"
    return expr


def bullet_transform_instructions(transform: BulletTransform, source_game: str, target: str) -> list[LoweredInstruction] | None:
    args = target_transform_args(transform)
    if args is None:
        return None
    if transform.raw_opcode in {609, 610, 611, 612} and args:
        return [LoweredInstruction(transform.raw_opcode, args)]
    if generation_for_game(source_game) == "th10_th11" and generation_for_game(target) == "th13_plus":
        if transform.raw_opcode == 409 and len(args) == 8:
            ir = BulletTransformIR.from_opcode(source_game, transform.raw_opcode, args)
            if not ir or ir.unsupported_reason(target):
                return None
            lowered = ir.lower_to(target)
            return [lowered] if lowered else None
    if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        if transform.raw_opcode == 509 and len(args) == 8:
            ir = BulletTransformIR.from_opcode(source_game, transform.raw_opcode, args)
            if not ir or ir.unsupported_reason(target):
                return None
            lowered = ir.lower_to(target)
            return [lowered] if lowered else None
        if transform.raw_opcode == 510 and not args:
            return [LoweredInstruction(610, [])]
        if transform.raw_opcode == 511 and len(args) == 2:
            return [LoweredInstruction(611, args)]
        if transform.raw_opcode == 512 and len(args) == 1:
            return [LoweredInstruction(612, args)]
        if transform.raw_opcode == 521 and len(args) == 9:
            return [LoweredInstruction(624, args)]
        if transform.raw_opcode == 522 and len(args) == 9:
            return [LoweredInstruction(625, args)]
    return None
