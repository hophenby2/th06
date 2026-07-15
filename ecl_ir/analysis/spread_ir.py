from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

from ..dialects.semantics import th12_double_flower_pair


RANK_PLACEHOLDER_RE = re.compile(r"\[-(\d+)\]")


@dataclass(frozen=True)
class DoubleFlowerLowering:
    primary_style: str
    aux_style: str
    aux_emitter_id: str


def th12_aux_emitter_id(emitter_id: str) -> str | None:
    stripped = str(emitter_id).strip()
    if not re.fullmatch(r"\d+", stripped):
        return None
    aux = int(stripped) + 2
    if aux > 7:
        return None
    return str(aux)


def double_flower_lowering_for_th12(emitter_id: str, spread: dict[str, Any]) -> DoubleFlowerLowering | None:
    pair = th12_double_flower_pair(spread)
    aux_id = th12_aux_emitter_id(emitter_id)
    if not pair or not aux_id:
        return None
    return DoubleFlowerLowering(pair[0], pair[1], aux_id)


def parse_float_literal(expr: object) -> float | None:
    text = str(expr).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", text):
        return float(text.rstrip("f"))
    return None


def format_float_literal(value: float) -> str:
    text = f"{value:.8f}".rstrip("0").rstrip(".")
    if text == "-0":
        text = "0"
    if "." not in text:
        text += ".0"
    return f"{text}f"


def add_float_expr(expr: object, delta: object) -> str:
    text = str(expr).strip()
    delta_text = str(delta).strip()
    base_value = parse_float_literal(text)
    delta_value = parse_float_literal(delta_text)
    if base_value is not None and delta_value is not None:
        return format_float_literal(base_value + delta_value)
    if delta_text.startswith("-"):
        return f"{text} - {delta_text[1:]}"
    return f"{text} + {delta_text}"


def negated_float_expr(expr: object) -> str:
    text = str(expr).strip()
    match = re.fullmatch(r"([-+]?)(\d+(?:\.\d+)?f?)", text)
    if match:
        sign, number = match.groups()
        if sign == "-":
            return number
        return f"-{number}"
    return f"0.0f - ({text})"


def double_flower_center_delta(ways: object | None) -> str | None:
    if ways is None:
        return None
    text = str(ways).strip()
    if text in {"", "0"}:
        return None
    ways_value = parse_float_literal(text)
    if ways_value is None or ways_value == 0:
        return None
    return format_float_literal(math.pi / (2.0 * ways_value))


def halve_positive_int_literal(value: object) -> str:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        number = int(text)
        if number > 1:
            return str(max(1, number // 2))
    return text


def halve_rank_group(group: dict[str, str]) -> dict[str, str]:
    return {key: halve_positive_int_literal(value) for key, value in group.items()}


def halve_rank_placeholder_group(arg: object, difficulty_literals: object) -> object:
    text = str(arg).strip()
    match = RANK_PLACEHOLDER_RE.fullmatch(text)
    if not match:
        return difficulty_literals
    group_index = int(match.group(1)) - 1
    if isinstance(difficulty_literals, list):
        groups = list(difficulty_literals)
        if 0 <= group_index < len(groups) and isinstance(groups[group_index], dict):
            groups[group_index] = halve_rank_group(groups[group_index])
        return groups
    if isinstance(difficulty_literals, dict) and group_index == 0:
        return halve_rank_group(difficulty_literals)
    return difficulty_literals


def halve_double_flower_layer_args(args: list[str], difficulty_literals: object) -> tuple[list[str], object]:
    if len(args) < 3:
        return args, difficulty_literals
    adjusted = args[:]
    adjusted[2] = halve_positive_int_literal(adjusted[2])
    return adjusted, halve_rank_placeholder_group(args[2], difficulty_literals)


def double_flower_aux_config_args(args: list[str], aux_id: str) -> list[str]:
    if not args:
        return args
    return [aux_id, *args[1:]]
