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


ARG_LAYOUT_OVERRIDES: dict[tuple[str, str, int], ArgLayout] = {}


# 参数语义表：同一个 op_key 下，不同世代可以有不同 layout。
# lowering 时先 source args -> semantic fields，再 semantic fields -> target args。
ARG_LAYOUTS: dict[str, dict[str, ArgLayout]] = {
    "movement.circle.set": {
        # TH08 moveCircle(t, theta, angSpd, radSpd): t 是圆周运动持续时间，半径从 0 开始增长。
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        # TH12+/TH13+ moveCircle(theta, angSpd, radius, radInc)。
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle_rel.set": {
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
    },
    "movement.circle_rel.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {"compat_flag": "0"}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
    },

    "movement.ellipse.set": {
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_mode", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
    },
    "movement.ellipse_rel.set": {
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_mode", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
    },
    "movement.ellipse.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
    },
    "movement.ellipse_rel.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
    },
    "movement.move_dir": {
        GEN_OLD: ArgLayout(("angle", "speed"), {}),
        GEN_10: ArgLayout(("angle", "speed"), {}),
        GEN_12: ArgLayout(("angle", "speed"), {}),
        GEN_13: ArgLayout(("angle", "speed"), {}),
    },
    "movement.move_dir_time": {
        GEN_OLD: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_10: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angle", "speed"), {}),
    },
    "unit.set_hitbox": {
        GEN_OLD: ArgLayout(("width", "height"), {}),
        GEN_10: ArgLayout(("width", "height"), {}),
        GEN_12: ArgLayout(("width", "height"), {}),
        GEN_13: ArgLayout(("width", "height"), {}),
    },
    "unit.set_hurtbox": {
        GEN_OLD: ArgLayout(("width", "height"), {}),
        GEN_10: ArgLayout(("width", "height"), {}),
        GEN_12: ArgLayout(("width", "height"), {}),
        GEN_13: ArgLayout(("width", "height"), {}),
    },
    "flow.jmp": {
        GEN_OLD: ArgLayout(("time", "label"), {}),
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.jmp_eq": {
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.jmp_neq": {
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.nop": {
        GEN_OLD: ArgLayout((), {}),
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.delete": {
        GEN_OLD: ArgLayout((), {}),
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "bullet.fire": {
        GEN_OLD: ArgLayout((), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "bullet.offset": {
        GEN_OLD: ArgLayout(("x", "y"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
    },
    "bullet.sound": {
        GEN_OLD: ArgLayout(("fire_sound", "transform_sound"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
        GEN_12: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
        GEN_13: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
    },
    "bullet.transform": {
        GEN_OLD: ArgLayout(("slot", "mode", "channel", "a", "b", "r", "s"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "slot", "mode", "channel", "a", "b", "r", "s"), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id", "slot", "mode", "channel", "a", "b", "r", "s"), {"et_id": "0"}),
        # TH13+ opcode 609 has explicit slot; opcode 611 is append-style and has no slot.
        GEN_13: ArgLayout(("et_id", "slot", "channel", "mode", "a", "b", "r", "s"), {"et_id": "0", "slot": "0"}),
    },
    "bullet.cancel_radius": {
        GEN_OLD: ArgLayout((), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("radius",), {"radius": "0.0f"}),
        GEN_12: ArgLayout(("radius",), {"radius": "0.0f"}),
        GEN_13: ArgLayout(("radius",), {"radius": "0.0f"}),
    },


    "laser.on": {
        GEN_10: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "laser.on_aimed": {
        GEN_10: ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0", "slot": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "laser.straight_on": {
        GEN_10: ArgLayout(("et_id", "slot", "sprite", "color", "angle", "speed", "length", "width", "start", "duration", "stop", "unknown"), {"et_id": "0", "slot": "0", "sprite": "0", "color": "0", "angle": "0.0f", "speed": "0.0f", "length": "128.0f", "width": "16.0f", "start": "0", "duration": "60", "stop": "0", "unknown": "0"}),
        GEN_12: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_13: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
    },
    "laser.new": {
        GEN_12: ArgLayout(("et_id", "init_length", "final_length", "unknown", "width"), {"et_id": "0", "init_length": "0.0f", "final_length": "0.0f", "unknown": "0.0f", "width": "16.0f"}),
        GEN_13: ArgLayout(("et_id", "init_length", "final_length", "unknown", "width"), {"et_id": "0", "init_length": "0.0f", "final_length": "0.0f", "unknown": "0.0f", "width": "16.0f"}),
    },
    "laser.timing": {
        GEN_12: ArgLayout(("et_id", "start", "duration", "stop", "graze_delay", "graze_speed"), {"et_id": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
        GEN_13: ArgLayout(("et_id", "start", "duration", "stop", "graze_delay", "graze_speed"), {"et_id": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
    },
    "laser.width": {
        GEN_12: ArgLayout(("et_id", "width"), {"et_id": "0", "width": "16.0f"}),
        GEN_13: ArgLayout(("et_id", "width"), {"et_id": "0", "width": "16.0f"}),
    },
    "laser.length": {
        GEN_12: ArgLayout(("et_id", "length"), {"et_id": "0", "length": "128.0f"}),
        GEN_13: ArgLayout(("et_id", "length"), {"et_id": "0", "length": "128.0f"}),
    },
    "laser.offset": {
        GEN_12: ArgLayout(("laser_id", "x", "y"), {"laser_id": "0", "x": "0.0f", "y": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "x", "y"), {"laser_id": "0", "x": "0.0f", "y": "0.0f"}),
    },
    "laser.trajectory": {
        GEN_12: ArgLayout(("laser_id", "speed", "angle"), {"laser_id": "0", "speed": "0.0f", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "x_speed", "y_speed"), {"laser_id": "0", "x_speed": "0.0f", "y_speed": "0.0f"}),
    },
    "laser.angle": {
        GEN_12: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
    },
    "laser.rotation": {
        GEN_12: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
    },
    "laser.end": {
        GEN_12: ArgLayout(("laser_id",), {"laser_id": "0"}),
        GEN_13: ArgLayout(("laser_id",), {"laser_id": "0"}),
    },
    "laser.curve_on": {
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "anm.rotate": {
        GEN_OLD: ArgLayout(("angle",), {"slot": "0"}),
        GEN_12: ArgLayout(("slot", "angle"), {"slot": "0"}),
        GEN_13: ArgLayout(("slot", "angle"), {"slot": "0"}),
    },
    "anm.on_et": {
        GEN_10: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_12: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_13: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
    },
    "unit.z_index": {
        GEN_OLD: ArgLayout(("layers",), {}),
        GEN_12: ArgLayout(("layers",), {}),
        GEN_13: ArgLayout(("layers",), {}),
    },
    "bullet.distance": {
        GEN_12: ArgLayout(("et_id", "distance"), {"et_id": "0", "distance": "0.0f"}),
        GEN_13: ArgLayout(("et_id", "distance"), {"et_id": "0", "distance": "0.0f"}),
    },
    "unit.hit_sound": {
        GEN_12: ArgLayout(("sound",), {"sound": "0"}),
        GEN_13: ArgLayout(("sound",), {"sound": "0"}),
    },
    "unit.fog": {
        GEN_10: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
        GEN_12: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
        GEN_13: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
    },
    "unit.boss_wait": {
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.death_wait": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.stage_logo": {
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.unknown569": {
        GEN_13: ArgLayout(("value",), {"value": "0"}),
    },

    "unit.call_std": {
        GEN_10: ArgLayout(("mode",), {"mode": "0"}),
        GEN_12: ArgLayout((), {"mode": "0"}),
        GEN_13: ArgLayout(("mode",), {"mode": "0"}),
    },
    "flow.call_async": {
        GEN_OLD: ArgLayout(("slot", "sub"), {"slot": "0"}),
        GEN_10: ArgLayout(("sub",), {"slot": "0"}),
        GEN_12: ArgLayout(("sub",), {"slot": "0"}),
        GEN_13: ArgLayout(("sub",), {"slot": "0"}),
    },
    "flow.debug22": {
        GEN_12: ArgLayout((), {"mode": "0", "name": '""'}),
        GEN_13: ArgLayout(("mode", "name"), {"mode": "0", "name": '""'}),
    },
    "flow.float_time": {
        GEN_OLD: ArgLayout(("var", "duration", "curve", "mode", "initial", "final", "p1", "p2"), {"slot": "0"}),
        GEN_10: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
        GEN_12: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
        GEN_13: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
    },
    "unit.et_protect_range": {
        GEN_OLD: ArgLayout(("radius",), {}),
        GEN_10: ArgLayout(("radius",), {}),
        GEN_12: ArgLayout(("radius",), {}),
        GEN_13: ArgLayout(("radius",), {}),
    },
    "boss.set_interrupt": {
        GEN_OLD: ArgLayout(("sub",), {"phase": "0", "life": "0", "time": "0"}),
        GEN_10: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
        GEN_12: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
        GEN_13: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
    },
    "boss.spell": {
        GEN_OLD: ArgLayout(("phase", "spell_id", "score", "name", "user", "desc1", "desc2"), {"timeout": "0"}),
        GEN_10: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_12: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_13: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
    },
}

ARG_LAYOUT_OVERRIDES.update({
    ("movement.circle_rel.tween", GEN_10, 291): ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "compat_flag"), {"compat_flag": "0"}),
    ("laser.on", GEN_10, 412): ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0"}),
    ("laser.on", GEN_10, 431): ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0"}),
    ("bullet.transform", GEN_13, 611): ArgLayout(("et_id", "channel", "mode", "a", "b", "r", "s"), {"slot": "0"}),
})

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
        return adapt_special_args(op_key, source_gen, target_gen, values)
    source_layout = ARG_LAYOUT_OVERRIDES.get((op_key, source_gen, source_opcode), layouts.get(source_gen))
    target_layout = ARG_LAYOUT_OVERRIDES.get((op_key, target_gen, target_opcode), layouts.get(target_gen))
    if not source_layout or not target_layout:
        return None

    fields = fields_from_args(source_layout, values)
    if fields is None:
        return None
    for key, default in source_layout.defaults.items():
        fields.setdefault(key, default)
    target_defaults = target_layout.defaults | (target_layout.target_only_defaults or {})
    target_fields = target_layout.fields
    if op_key == "bullet.transform" and target_gen == GEN_13 and target_opcode == 611:
        target_fields = ("et_id", "channel", "mode", "a", "b", "r", "s")
    if op_key == "laser.trajectory" and source_gen == GEN_12 and target_gen == GEN_13:
        speed = fields.get("speed", target_defaults.get("speed", "0.0f"))
        angle = fields.get("angle", target_defaults.get("angle", "0.0f"))
        fields["x_speed"] = f"({speed}) * cos({angle})"
        fields["y_speed"] = f"({speed}) * sin({angle})"
    result = [adapt_field_value(field, fields.get(field, target_defaults.get(field, "")), source_gen, target_gen) for field in target_fields]
    return result


def adapt_special_args(op_key: str, source_gen: str, target_gen: str, values: list[str]) -> list[str] | None:
    if op_key == "flow.call" and values:
        result = list(values)
        result[0] = adapt_sub_value(result[0], source_gen, target_gen)
        return result
    return values


def adapt_field_value(field: str, value: str, source_gen: str, target_gen: str) -> str:
    if field in {"sub", "function"}:
        return adapt_sub_value(value, source_gen, target_gen)
    if field == "layers" and source_gen == GEN_12 and target_gen == GEN_13:
        match = re.fullmatch(r"(-?\d+)\.0f", str(value).strip())
        if match:
            return match.group(1)
    return value


def adapt_sub_value(value: str, source_gen: str, target_gen: str) -> str:
    text = str(value).strip()
    if source_gen == GEN_OLD and target_gen in {GEN_10, GEN_12, GEN_13} and re.fullmatch(r"\d+", text):
        return f'"Sub{text}"'
    if target_gen == GEN_OLD:
        match = re.fullmatch(r"Sub(\d+)", text)
        if match:
            return match.group(1)
    return text


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
        -10000: 10032,
        -9997: 10079,
        -9996: 10080,
        -9999: 10033,
        -9998: 10082,
        -9987: 10035,
        **{-9981 + index: 10016 + index for index in range(4)},
        **{-9977 + index: 10020 + index for index in range(4)},
        **{-9973 + index: 10024 + index for index in range(8)},
        **{-9935 + index: 10094 + index for index in range(4)},
        **{-9985 + index: 10000 + index for index in range(4)},
        -9928: 10057, -9927: 10058, -9926: 10059, -9925: 10060,
        -9982: 10082,
    }

    def repl(match: re.Match[str]) -> str:
        number = int(match.group(1))
        mapped = mapping.get(number)
        return f"[{mapped}.0f]" if mapped is not None else match.group(0)

    return re.sub(r"\[(-\d+)\.0f\]", repl, value)
