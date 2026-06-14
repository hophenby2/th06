from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from .model import BulletTransform
from .origin_ir import LoweredInstruction
from .semantics import generation_for_game, remap_bullet_transform_mode, remap_shape_change_arg, unsupported_bullet_transform_mode_reason

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


def th12_509_to_th13plus_609(args: list[str], target: str) -> list[str]:
    converted = args[:]
    converted[3] = remap_bullet_transform_mode("th12", target, converted[3])
    converted[4] = remap_shape_change_arg("th12", target, args[3], converted[4])
    if generation_for_game(target) == "th13_plus":
        converted = ["-999999.0f" if value == "-999.0f" and index >= 6 else value for index, value in enumerate(converted)]
    return converted


def th12_509_to_th13plus_transform(args: list[str], target: str) -> LoweredInstruction:
    converted = th12_509_to_th13plus_609(args, target)
    if converted[3] == "16":
        et_id, slot, channel, mode, a, b, r, s = converted
        subtype = th12_pause_then_velocity_subtype(args[3])
        if args[3] == "32":
            r = th12_random_angle_expression_bound(r)
        mode_flags = "0"
        return LoweredInstruction(610, [et_id, slot, channel, mode, a, b, subtype, mode_flags, r, s, "-999999.0f", "-999999.0f"])
    return LoweredInstruction(609, converted)


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


def th12_pause_then_velocity_subtype(mode: str) -> str:
    return {
        "16": "0",
        "32": "6",
        "64": "4",
    }.get(str(mode), "0")


def bullet_transform_instructions(transform: BulletTransform, source_game: str, target: str) -> list[LoweredInstruction] | None:
    args = target_transform_args(transform)
    if args is None:
        return None
    if transform.raw_opcode in {609, 610, 611, 612} and args:
        return [LoweredInstruction(transform.raw_opcode, args)]
    if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        if transform.raw_opcode == 509 and len(args) == 8:
            reason = unsupported_bullet_transform_mode_reason(source_game, target, args[3])
            if reason:
                return None
            return [th12_509_to_th13plus_transform(args, target)]
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
