from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from .model import BulletTransform
from .semantics import generation_for_game, unsupported_bullet_transform_mode_reason

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
    def __init__(self) -> None:
        self.next_index_by_emitter: dict[str, int] = {}
        self.next_start_by_emitter_channel: dict[tuple[str, str], str] = {}
        self.index_by_emitter_source_slot: dict[tuple[str, str], str] = {}

    def reset_emitter(self, emitter_id: str) -> None:
        self.next_index_by_emitter[emitter_id] = 0
        for key in [key for key in self.next_start_by_emitter_channel if key[0] == emitter_id]:
            self.next_start_by_emitter_channel.pop(key, None)
        for key in [key for key in self.index_by_emitter_source_slot if key[0] == emitter_id]:
            self.index_by_emitter_source_slot.pop(key, None)

    def annotate_th12_to_th13plus_args(self, args: list[Any], source_game: str, target: str) -> tuple[list[str] | None, dict[str, Any]]:
        rendered = [str(arg) for arg in args]
        if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus" or len(rendered) != 8:
            return rendered, {}
        emitter_id, source_slot, channel, mode, duration, start, _r, _s = rendered
        reason = unsupported_bullet_transform_mode_reason(source_game, target, mode)
        if reason:
            return None, {"drop": True, "drop_reason": reason}
        source_key = (emitter_id, source_slot)
        effective_index = self.index_by_emitter_source_slot.get(source_key)
        if effective_index is None:
            effective_index = str(self.next_index_by_emitter.get(emitter_id, 0))
            self.index_by_emitter_source_slot[source_key] = effective_index
            self.next_index_by_emitter[emitter_id] = int(effective_index) + 1
        rendered[1] = effective_index
        semantics: dict[str, Any] = {"compact_index": effective_index, "source_slot": source_slot}
        if mode == "8" and start == INT_SENTINEL:
            timeline_key = (emitter_id, channel)
            effective_start = self.next_start_by_emitter_channel.get(timeline_key, "0")
            rendered[5] = effective_start
            self.next_start_by_emitter_channel[timeline_key] = add_int_expr(effective_start, duration)
            semantics["effective_start"] = effective_start
        return rendered, semantics


def annotate_th12_to_th13plus_transforms(transforms: list[BulletTransform], source_game: str, target: str) -> list[BulletTransform]:
    if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus":
        return transforms
    state = TransformTimelineState()
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
