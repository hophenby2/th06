from __future__ import annotations

import re
from dataclasses import dataclass

from .semantics import generation_for_game

GEN_OLD = "th06_th08"
GEN_10 = "th10_th11"
GEN_12 = "th12"
GEN_13 = "th13_plus"


@dataclass(frozen=True)
class ArgLayout:
    fields: tuple[str, ...]
    defaults: dict[str, str]
    target_only_defaults: dict[str, str] | None = None


# 参数语义表：同一个 op_key 下，不同世代可以有不同 layout。
# lowering 时先 source args -> semantic fields，再 semantic fields -> target args。
ARG_LAYOUTS: dict[str, dict[str, ArgLayout]] = {
    "movement.circle.set": {
        # TH08 moveCircle(t, theta, angSpd, radSpd): t 是圆周运动持续时间，半径从 0 开始增长。
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        # TH12+/TH13+ moveCircle(theta, angSpd, radius, radInc)。
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle_rel.set": {
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle.tween": {
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
    },
    "movement.circle_rel.tween": {
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
    },
    "flow.jmp": {
        GEN_OLD: ArgLayout(("time", "label"), {}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label",), {"time": "0"}),
    },
    "flow.jmp_eq": {
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label",), {"time": "0"}),
    },
    "flow.jmp_neq": {
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label",), {"time": "0"}),
    },
}

# 旧作条件跳转把比较也塞在同一个 op 里；TH12+ 的 jmpEq/jmpNeq 只吃 VM 条件标志。
# 没有同步比较栈时不能安全一条指令转换。
UNSAFE_LAYOUT_OPS: dict[str, set[tuple[str, str]]] = {
    "flow.jmp_eq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_neq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_lss": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_leq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_gre": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_geq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
}


def adapt_args_for_op_key(op_key: str, source_game: str, source_opcode: int, target: str, target_opcode: int, args: list[str]) -> list[str] | None:
    source_gen = generation_for_game(source_game)
    target_gen = generation_for_game(target)
    values = adapt_values_for_generation([str(arg) for arg in args], source_gen, target_gen)

    if (source_gen, target_gen) in UNSAFE_LAYOUT_OPS.get(op_key, set()):
        return None

    layouts = ARG_LAYOUTS.get(op_key)
    if not layouts:
        return values
    source_layout = layouts.get(source_gen)
    target_layout = layouts.get(target_gen)
    if not source_layout or not target_layout:
        return None

    fields = fields_from_args(source_layout, values)
    if fields is None:
        return None
    fields.update(source_layout.defaults)
    target_defaults = target_layout.defaults | (target_layout.target_only_defaults or {})
    return [fields.get(field, target_defaults.get(field, "")) for field in target_layout.fields]


def fields_from_args(layout: ArgLayout, args: list[str]) -> dict[str, str] | None:
    if len(args) != len(layout.fields):
        return None
    return dict(zip(layout.fields, args))


def adapt_value_for_generation(value: str, source_gen: str, target_gen: str) -> str:
    text = str(value).strip()
    if source_gen == GEN_OLD and target_gen in {GEN_12, GEN_13}:
        return adapt_th08_var_to_new(text)
    if source_gen in {GEN_12, GEN_13} and target_gen == GEN_OLD:
        return adapt_new_var_to_th08(text)
    return text


def adapt_values_for_generation(args: list[str], source_gen: str, target_gen: str) -> list[str]:
    return [adapt_value_for_generation(arg, source_gen, target_gen) for arg in args]


def adapt_th08_var_to_new(value: str) -> str:
    mapping = {
        **{10016 + index: -9981 + index for index in range(4)},
        **{10020 + index: -9977 + index for index in range(4)},
        **{10024 + index: -9973 + index for index in range(8)},
        **{10094 + index: -9935 + index for index in range(4)},
        10057: -9928, 10058: -9927, 10059: -9926, 10060: -9925,
        10065: -9928, 10066: -9927, 10067: -9926, 10068: -9925,
        10082: -9982,
    }

    def repl(match: re.Match[str]) -> str:
        number = int(match.group(1))
        mapped = mapping.get(number)
        return f"[{mapped}.0f]" if mapped is not None else match.group(0)

    return re.sub(r"\[(100\d+)\.0f\]", repl, value)


def adapt_new_var_to_th08(value: str) -> str:
    mapping = {
        **{-9981 + index: 10016 + index for index in range(4)},
        **{-9977 + index: 10020 + index for index in range(4)},
        **{-9973 + index: 10024 + index for index in range(8)},
        **{-9935 + index: 10094 + index for index in range(4)},
        -9928: 10057, -9927: 10058, -9926: 10059, -9925: 10060,
        -9982: 10082,
    }

    def repl(match: re.Match[str]) -> str:
        number = int(match.group(1))
        mapped = mapping.get(number)
        return f"[{mapped}.0f]" if mapped is not None else match.group(0)

    return re.sub(r"\[(-\d+)\.0f\]", repl, value)
