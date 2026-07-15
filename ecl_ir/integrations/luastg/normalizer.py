from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .lifter import LuaSTGIRObject, lift_luastg_file
from ...legacy.model import BulletEmitter, IRObject, LaserEmitter, MovementOp, TimelineOp


def lua_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1"}


def strip_wrapper(expr: str, prefix: str) -> str:
    text = str(expr).strip()
    pattern = re.compile(rf"^{re.escape(prefix)}\((.*)\)$")
    match = pattern.match(text)
    return match.group(1).strip() if match else text


def lua_deg_to_ecl_rad_expr(expr: str) -> str:
    text = str(expr).strip()
    if text.startswith("ecl_rad(") and text.endswith(")"):
        return strip_wrapper(text, "ecl_rad")
    return f"(({text}) * 0.017453292519943295)"


def ecl_helper_angle_to_ecl_expr(expr: str) -> str:
    text = str(expr).strip()
    if text.startswith("ecl_rad(") and text.endswith(")"):
        return strip_wrapper(text, "ecl_rad")
    return text


def unwrap_math_floor(expr: str) -> str:
    text = str(expr).strip()
    match = re.fullmatch(r"math\.max\(1,\s*math\.floor\((.*)\)\)", text)
    return match.group(1).strip() if match else text


def ecl_pick_to_ranked(expr: str) -> dict[str, object] | str:
    text = str(expr).strip()
    match = re.fullmatch(r"ecl_pick_rank\((.*)\)", text)
    if not match:
        return text
    parts = split_args(match.group(1))
    keys = ["E", "N", "H", "L"]
    difficulty = {key: parts[index] for index, key in enumerate(keys) if index < len(parts)}
    placeholder = difficulty.get("N") or difficulty.get("E") or next(iter(difficulty.values()), "")
    return {"difficulty": difficulty, "placeholder": placeholder}


def lua_expr_to_ecl_expr(expr: object) -> str:
    text = str(expr).strip()
    text = text.replace("self.x", "[-9997.0f]").replace("self.y", "[-9996.0f]")
    text = re.sub(r"\becl_var\[(-?\d+)\]", lambda m: f"[{m.group(1)}.0f]", text)
    text = re.sub(r"\bv_([A-Za-z][A-Za-z0-9_]*)\b", lambda m: f"%{m.group(1)}", text)
    text = re.sub(r"\bi_([A-Za-z][A-Za-z0-9_]*)\b", lambda m: f"${m.group(1)}", text)
    text = re.sub(r"/\s*\(\$([A-Za-z][A-Za-z0-9_]*)\)", lambda m: f"/ _f(${m.group(1)})", text)
    text = re.sub(r"/\s*\$([A-Za-z][A-Za-z0-9_]*)", lambda m: f"/ _f(${m.group(1)})", text)
    text = text.replace("nil", "0")
    return text


def lua_rank_expr_to_ecl(expr: object) -> dict[str, object] | str:
    ranked = ecl_pick_to_ranked(unwrap_math_floor(lua_expr_to_ecl_expr(expr)))
    if isinstance(ranked, dict):
        difficulty = ranked.get("difficulty", {})
        if isinstance(difficulty, dict):
            ranked["difficulty"] = {rank: lua_expr_to_ecl_expr(value) for rank, value in difficulty.items()}
            ranked["placeholder"] = lua_expr_to_ecl_expr(ranked.get("placeholder", ""))
    return ranked


def split_args(text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    quote = ""
    escape = False
    for char in str(text):
        if in_string:
            current.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                in_string = False
            continue
        if char in {'"', "'"}:
            in_string = True
            quote = char
            current.append(char)
        elif char in "({[":
            depth += 1
            current.append(char)
        elif char in ")}]":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def aim_for_ecl_shot(mode: str) -> dict[str, Any]:
    raw = str(mode).strip()
    return {
        "0": {"mode": "aimed_fan", "mode_raw": "0"},
        "1": {"mode": "absolute_fan", "mode_raw": "1"},
        "2": {"mode": "aimed_ring", "mode_raw": "2"},
        "3": {"mode": "absolute_ring", "mode_raw": "3"},
    }.get(raw, {"mode": "absolute", "mode_raw": raw})


def normalize_bullet_emitter(obj: LuaSTGIRObject) -> BulletEmitter:
    params = obj.params
    emitter = BulletEmitter("luastg", obj.function, obj.line, lua_expr_to_ecl_expr(params.get("emitter", "0")), obj.name)
    if obj.name == "ecl_shot":
        emitter.appearance.update({"style": lua_expr_to_ecl_expr(params.get("style", "0")), "color": lua_expr_to_ecl_expr(params.get("color", "0"))})
        emitter.origin.update({
            "x": lua_expr_to_ecl_expr(params.get("x", "self.x")),
            "y": lua_expr_to_ecl_expr(params.get("y", "self.y")),
            "offset_x": lua_expr_to_ecl_expr(params.get("dx", "0")),
            "offset_y": lua_expr_to_ecl_expr(params.get("dy", "0")),
            "distance": lua_expr_to_ecl_expr(params.get("distance", "0")),
        })
        emitter.aim.update(aim_for_ecl_shot(str(params.get("mode", "1"))))
        emitter.aim.update({
            "base_angle": lua_expr_to_ecl_expr(ecl_helper_angle_to_ecl_expr(str(params.get("angle", "0.0")))),
            "angle_step": lua_expr_to_ecl_expr(ecl_helper_angle_to_ecl_expr(str(params.get("angle_step", "0.0")))),
            "unit_source": "degree",
        })
        emitter.count.update({
            "ways": lua_rank_expr_to_ecl(params.get("ways", "1")),
            "layers": lua_rank_expr_to_ecl(params.get("layers", "1")),
        })
        emitter.speed.update({
            "first": lua_rank_expr_to_ecl(params.get("speed", "1.0f")),
            "step": lua_rank_expr_to_ecl(params.get("speed_step", "0.0f")),
        })
        emitter.semantics.setdefault("luastg", {})["source"] = "ecl_shot"
        emitter.semantics.setdefault("bullet", {})["fire_at_definition"] = True
    elif obj.name == "_create_bullet_group":
        emitter.id = str(obj.line)
        emitter.appearance.update({"style": lua_expr_to_ecl_expr(params.get("style", "0")), "color": lua_expr_to_ecl_expr(params.get("color", "0"))})
        emitter.origin.update({"x": lua_expr_to_ecl_expr(params.get("x", "self.x")), "y": lua_expr_to_ecl_expr(params.get("y", "self.y"))})
        emitter.aim.update({
            "mode": "aimed_fan" if lua_bool(params.get("aim", "false")) else "absolute_fan",
            "mode_raw": "0" if lua_bool(params.get("aim", "false")) else "1",
            "base_angle": lua_expr_to_ecl_expr(lua_deg_to_ecl_rad_expr(str(params.get("angle", "0.0")))),
            "angle_step": lua_expr_to_ecl_expr(lua_deg_to_ecl_rad_expr(str(params.get("angle_spread", "0.0")))),
            "unit_source": "degree",
        })
        emitter.count.update({"ways": lua_expr_to_ecl_expr(params.get("count", "1")), "layers": "1", "interval": lua_expr_to_ecl_expr(params.get("interval", "0"))})
        emitter.speed.update({"first": lua_expr_to_ecl_expr(params.get("speed1", "1.0")), "last_or_step": lua_expr_to_ecl_expr(params.get("speed2", "1.0"))})
        emitter.semantics.setdefault("luastg", {})["source"] = "_create_bullet_group"
        emitter.semantics.setdefault("bullet", {})["fire_at_definition"] = True
    return emitter


def normalize_movement(obj: LuaSTGIRObject) -> MovementOp:
    params = obj.params
    movement = MovementOp("luastg", obj.function, obj.line, str(obj.line), obj.name)
    if obj.name == "task.MoveTo":
        movement.fields.update({
            "op": "movePosTime",
            "op_key": "movement.position.tween",
            "args": [lua_expr_to_ecl_expr(params.get("time", "0")), lua_expr_to_ecl_expr(params.get("mode", "4")), lua_expr_to_ecl_expr(params.get("x", "0.0f")), lua_expr_to_ecl_expr(params.get("y", "0.0f"))],
            "semantics": {"motion": {"op": "movePosTime", "time": params.get("time"), "mode": params.get("mode"), "x": params.get("x"), "y": params.get("y")}},
        })
    elif obj.name == "SetV2":
        movement.fields.update({
            "op": "moveVel",
            "op_key": "movement.velocity.set",
            "args": [lua_expr_to_ecl_expr(lua_deg_to_ecl_rad_expr(str(params.get("angle", "0.0")))), lua_expr_to_ecl_expr(params.get("speed", "0.0f"))],
            "semantics": {"motion": {"op": "moveVel", "direction": params.get("angle"), "speed": params.get("speed"), "unit_source": "degree"}},
        })
    return movement


def normalize_wait(obj: LuaSTGIRObject) -> TimelineOp:
    timeline = TimelineOp("luastg", obj.function, obj.line, str(obj.line), "wait")
    timeline.fields.update({"op": "wait", "frames": lua_expr_to_ecl_expr(obj.params.get("frames", "1"))})
    return timeline


def normalize_boss_pattern(obj: LuaSTGIRObject) -> IRObject:
    pattern = IRObject("BossPattern", "luastg", obj.function, obj.line, str(obj.line), obj.name)
    pattern.fields.update(obj.params)
    return pattern


def normalize_laser(obj: LuaSTGIRObject) -> LaserEmitter:
    params = obj.params
    laser_id = lua_expr_to_ecl_expr(params.get("style", obj.line))
    laser = LaserEmitter("luastg", obj.function, obj.line, laser_id, obj.name)
    normalized_params = dict(params)
    if "angle" in normalized_params:
        normalized_params["angle"] = lua_expr_to_ecl_expr(ecl_helper_angle_to_ecl_expr(str(normalized_params["angle"])))
    laser.fields.update({"semantic": normalized_params.get("kind", "line"), "params": normalized_params})
    laser.fields.setdefault("ir_ops", [])
    return laser


def normalize_luastg_object(obj: LuaSTGIRObject):
    if obj.kind == "BulletEmitter":
        return normalize_bullet_emitter(obj)
    if obj.kind == "Movement":
        return normalize_movement(obj)
    if obj.kind == "Wait":
        return normalize_wait(obj)
    if obj.kind == "BossPattern":
        return normalize_boss_pattern(obj)
    if obj.kind == "LaserEmitter":
        return normalize_laser(obj)
    return IRObject(obj.kind, "luastg", obj.function, obj.line, str(obj.line), obj.name, fields=obj.params, unsupported=[obj.raw])


def normalize_luastg_file(path: str | Path) -> list[Any]:
    return [normalize_luastg_object(obj) for obj in lift_luastg_file(path)]


def emit_normalized_json(path: str | Path) -> str:
    objects = normalize_luastg_file(path)
    return json.dumps({"source": str(path), "objects": [obj.to_dict() for obj in objects]}, ensure_ascii=False, indent=2)
