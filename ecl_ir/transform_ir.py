from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .model import BulletTransform
from .origin_ir import LoweredInstruction
from .semantics import (
    bullet_shape_semantic,
    bullet_transform_generation_for_game,
    bullet_transform_mode_can_encode,
    bullet_transform_mode_semantic,
    encode_bullet_shape,
    encode_bullet_transform_mode,
    generation_for_game,
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


@dataclass(frozen=True)
class TransformLayout:
    opcode: int
    generation: str
    fields: tuple[str, ...]


TRANSFORM_LAYOUTS: dict[tuple[str, int], TransformLayout] = {
    ("th10_th11", 409): TransformLayout(409, "th10_th11", ("emitter_id", "slot", "channel", "mode", "a", "b", "r", "s")),
    ("th12", 509): TransformLayout(509, "th12", ("emitter_id", "slot", "channel", "mode", "a", "b", "r", "s")),
    ("th13_plus", 609): TransformLayout(609, "th13_plus", ("emitter_id", "slot", "channel", "mode", "a", "b", "r", "s")),
    ("th13_plus", 610): TransformLayout(610, "th13_plus", ("emitter_id", "slot", "channel", "mode", "a", "b", "c", "d", "r", "s", "m", "n")),
    ("th13_plus", 611): TransformLayout(611, "th13_plus", ("emitter_id", "channel", "mode", "a", "b", "r", "s")),
    ("th13_plus", 612): TransformLayout(612, "th13_plus", ("emitter_id", "channel", "mode", "a", "b", "c", "d", "r", "s", "m", "n")),
}


def transform_layout(game: str, opcode: int) -> TransformLayout | None:
    return TRANSFORM_LAYOUTS.get((generation_for_game(game), opcode))


def normalize_target_float_sentinel(value: str, target: str) -> str:
    if generation_for_game(target) == "th13_plus" and value == "-999.0f":
        return "-999999.0f"
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
    source_game: str
    source_opcode: int
    values: dict[str, str]
    mode_semantic: str
    shape_semantic: str | None = None
    source_args: tuple[str, ...] = ()

    @classmethod
    def from_opcode(cls, source_game: str, opcode: int, args: list[Any]) -> "BulletTransformIR | None":
        layout = transform_layout(source_game, opcode)
        rendered = [str(arg) for arg in args]
        if not layout or len(rendered) != len(layout.fields):
            return None
        values = dict(zip(layout.fields, rendered))
        mode = values.get("mode", "0")
        mode_semantic = bullet_transform_mode_semantic(source_game, mode)
        shape_semantic = bullet_shape_semantic(source_game, values.get("a", "0")) if mode_semantic == "shape_change" else None
        return cls(
            source_game=source_game,
            source_opcode=opcode,
            values=values,
            mode_semantic=mode_semantic,
            shape_semantic=shape_semantic,
            source_args=tuple(rendered),
        )

    def unsupported_reason(self, target: str) -> str | None:
        return unsupported_bullet_transform_mode_reason(self.source_game, target, self.values.get("mode", "0"))

    def with_slot(self, slot: str) -> "BulletTransformIR":
        values = dict(self.values)
        values["slot"] = slot
        return BulletTransformIR(
            source_game=self.source_game,
            source_opcode=self.source_opcode,
            values=values,
            mode_semantic=self.mode_semantic,
            shape_semantic=self.shape_semantic,
            source_args=self.source_args,
        )

    def with_emitter(self, emitter_id: str) -> "BulletTransformIR":
        values = dict(self.values)
        values["emitter_id"] = emitter_id
        return BulletTransformIR(
            source_game=self.source_game,
            source_opcode=self.source_opcode,
            values=values,
            mode_semantic=self.mode_semantic,
            shape_semantic=self.shape_semantic,
            source_args=self.source_args,
        )

    def encoded_a(self, target: str) -> str:
        value = self.values.get("a", "-999999")
        if self.mode_semantic != "shape_change":
            return value
        return encode_bullet_shape(self.shape_semantic or bullet_shape_semantic(self.source_game, value), target, value)

    def encoded_mode(self, target: str) -> str:
        return encode_bullet_transform_mode(self.mode_semantic, target, self.values.get("mode", "0"))

    def encoded_b(self, target: str) -> str:
        value = self.values.get("b", "-999999")
        if bullet_transform_generation_for_game(target) in {"th12", "th13_plus"}:
            return {
                "bounce_all": "15",
                "bounce_no_bottom": "13",
                "bounce_bottom": "2",
                "bounce_horizontal": "12",
                "wall_pass_horizontal": "12",
            }.get(self.mode_semantic, value)
        return value

    def encoded_r(self, target: str) -> str:
        value = self.values.get("r", "-999999.0f")
        if bullet_transform_generation_for_game(target) in {"th12", "th13_plus"} and self.mode_semantic in {"bounce_bottom", "bounce_horizontal", "wall_pass_horizontal"}:
            return "-999999.0f"
        return normalize_target_float_sentinel(value, target)

    def lower_parametric_to_legacy(self) -> LoweredInstruction | None:
        if self.mode_semantic == "bounce":
            mode = legacy_bounce_mode_for_mask(self.values.get("b", "-999999"))
            if mode is None:
                return None
            r = self.values.get("r", "-999999.0f") if mode in {"1024", "2048"} else "-999999.0f"
            return LoweredInstruction(
                409,
                [
                    self.values.get("emitter_id", "0"),
                    self.values.get("slot", "0"),
                    self.values.get("channel", "0"),
                    mode,
                    self.values.get("a", "-999999"),
                    "-999999",
                    r,
                    "-999999.0f",
                ],
            )
        if self.mode_semantic == "wall_pass" and normalized_int(self.values.get("b", "-999999")) == "12":
            return LoweredInstruction(
                409,
                [
                    self.values.get("emitter_id", "0"),
                    self.values.get("slot", "0"),
                    self.values.get("channel", "0"),
                    "1048576",
                    self.values.get("a", "-999999"),
                    "-999999",
                    "-999999.0f",
                    "-999999.0f",
                ],
            )
        return None

    def base_fields_for(self, target: str) -> list[str]:
        return [
            self.values.get("emitter_id", "0"),
            self.values.get("slot", "0"),
            self.values.get("channel", "0"),
            self.encoded_mode(target),
            self.encoded_a(target),
            self.encoded_b(target),
            self.encoded_r(target),
            normalize_target_float_sentinel(self.values.get("s", "-999999.0f"), target),
        ]

    def th13plus_pause_subtype(self) -> str:
        return {
            "pause_then_relative_velocity": "0",
            "pause_then_aimed_velocity": "6",
            "pause_then_velocity": "4",
        }.get(self.mode_semantic, "0")

    def lower_to(self, target: str) -> LoweredInstruction | None:
        if self.unsupported_reason(target):
            return None
        target_generation = generation_for_game(target)
        target_transform_generation = bullet_transform_generation_for_game(target)
        source_transform_generation = bullet_transform_generation_for_game(self.source_game)
        if target_generation == "th10_th11" and target_transform_generation == "th10_th11":
            parametric = self.lower_parametric_to_legacy()
            if parametric is not None:
                return parametric
        if not bullet_transform_mode_can_encode(self.mode_semantic, target):
            return None
        if target_generation == "th13_plus":
            fields = self.base_fields_for(target)
            if fields[3] == "16" and source_transform_generation != "th13_plus":
                emitter_id, slot, channel, mode, a, b, r, s = fields
                if self.mode_semantic == "pause_then_aimed_velocity":
                    r = th12_random_angle_expression_bound(r)
                return LoweredInstruction(
                    610,
                    [emitter_id, slot, channel, mode, a, b, self.th13plus_pause_subtype(), "0", r, s, "-999999.0f", "-999999.0f"],
                )
            return LoweredInstruction(609, fields)
        if target_generation == "th12":
            fields = self.base_fields_for(target)
            return LoweredInstruction(509, fields)
        if target_generation == "th10_th11":
            fields = self.base_fields_for(target)
            return LoweredInstruction(409, fields)
        return None


def bullet_transform_ir_from_opcode(source_game: str, opcode: int, args: list[Any], append_slot: int | str | None = None) -> BulletTransformIR | None:
    transform = BulletTransformIR.from_opcode(source_game, opcode, args)
    if not transform:
        return None
    if "slot" not in transform.values and append_slot is not None:
        transform = transform.with_slot(str(append_slot))
    return transform


def lower_transform_opcode_to_instruction(source_game: str, target: str, opcode: int, args: list[Any], append_slot: int | str | None = None) -> LoweredInstruction | None:
    transform = bullet_transform_ir_from_opcode(source_game, opcode, args, append_slot)
    if not transform:
        return None
    return transform.lower_to(target)


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
