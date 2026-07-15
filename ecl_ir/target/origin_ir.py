from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..dialects.semantics import generation_for_game


@dataclass(frozen=True)
class LoweredInstruction:
    opcode: int
    args: list[str]


def bullet_origin_instructions(target: str, emitter_id: str, origin: dict[str, Any] | None) -> list[LoweredInstruction]:
    if not origin:
        return []
    generation = generation_for_game(target)
    if generation == "th13_plus":
        return th13plus_bullet_origin_instructions(emitter_id, origin)
    if generation == "th12":
        return th12_bullet_origin_instructions(emitter_id, origin)
    return []


def th13plus_bullet_origin_instructions(emitter_id: str, origin: dict[str, Any]) -> list[LoweredInstruction]:
    mode = str(origin.get("mode", "enemy"))
    instructions: list[LoweredInstruction] = []
    if mode == "offset":
        instructions.append(LoweredInstruction(603, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))]))
    elif mode == "polar":
        instructions.append(LoweredInstruction(626, [emitter_id, str(origin.get("angle", "0.0f")), str(origin.get("radius", "0.0f"))]))
    elif mode == "absolute":
        instructions.append(LoweredInstruction(628, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))]))
    if mode == "distance" or "distance" in origin:
        instructions.append(LoweredInstruction(627, [emitter_id, str(origin.get("distance", "0.0f"))]))
    return instructions


def th12_bullet_origin_instructions(emitter_id: str, origin: dict[str, Any]) -> list[LoweredInstruction]:
    mode = str(origin.get("mode", "enemy"))
    instructions: list[LoweredInstruction] = []
    if mode == "offset":
        instructions.append(LoweredInstruction(503, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))]))
    elif mode == "polar":
        instructions.append(LoweredInstruction(523, [emitter_id, str(origin.get("angle", "0.0f")), str(origin.get("radius", "0.0f"))]))
    elif mode == "absolute":
        if "distance" in origin:
            instructions.append(LoweredInstruction(524, [emitter_id, str(origin.get("distance", "0.0f"))]))
        instructions.append(LoweredInstruction(525, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))]))
        return instructions
    if mode == "distance" or "distance" in origin:
        instructions.append(LoweredInstruction(524, [emitter_id, str(origin.get("distance", "0.0f"))]))
    return instructions
