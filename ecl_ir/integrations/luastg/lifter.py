from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class LuaSTGIRObject:
    kind: str
    source: str
    line: int
    function: str = ""
    name: str = ""
    params: dict[str, str] = field(default_factory=dict)
    raw: str = ""
    confidence: str = "pattern"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


FUNC_RE = re.compile(r"^\s*(?:local\s+)?function\s+([A-Za-z_][\w\.]*)\s*\(([^)]*)\)")
ASSIGN_FUNC_RE = re.compile(r"^\s*function\s+([A-Za-z_][\w\.]*)\s*:\s*([A-Za-z_]\w*)\s*\(([^)]*)\)")
CALL_RE = re.compile(r"([A-Za-z_][\w\.]*|_create_bullet_group|ecl_shot|ecl_laser|task\._Wait|task\.Wait|task\.MoveTo|New|SetV2)\s*\((.*)\)")
TASK_NEW_RE = re.compile(r"task\.New\s*\((.*)\)")
BOSS_CARD_RE = re.compile(r"boss\.card\.New\s*\((.*)\)")
HELPER_FUNCTIONS = {"ecl_new_bullet", "ecl_shot", "ecl_laser", "ecl_move_rand", "ecl_pick_rank", "ecl_rad", "ecl_sync_self"}


def split_args(text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    quote = ""
    escape = False
    for char in text:
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


def clean_lua_line(line: str) -> str:
    text = line.strip()
    if "--" in text:
        text = text.split("--", 1)[0].rstrip()
    return text


def detect_function(line: str) -> str | None:
    if match := FUNC_RE.match(line):
        return match.group(1)
    if match := ASSIGN_FUNC_RE.match(line):
        return f"{match.group(1)}:{match.group(2)}"
    return None


def lift_ecl_shot(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = [
        "mode", "emitter", "style", "color", "x", "y", "dx", "dy", "distance",
        "origin_angle", "origin_radius", "ways", "layers", "speed", "speed_step",
        "angle", "angle_step", "extra",
    ]
    return LuaSTGIRObject(
        kind="BulletEmitter",
        source=path,
        line=line_no,
        function=function,
        name="ecl_shot",
        params={key: args[index] for index, key in enumerate(keys) if index < len(args)},
        raw=raw,
        confidence="direct_ecl_helper",
    )


def lift_ecl_laser(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = ["style", "x", "y", "angle", "length", "width", "warn_time", "fade_in", "active_time", "fade_out", "kind"]
    return LuaSTGIRObject(
        kind="LaserEmitter",
        source=path,
        line=line_no,
        function=function,
        name="ecl_laser",
        params={key: args[index] for index, key in enumerate(keys) if index < len(args)},
        raw=raw,
        confidence="direct_ecl_helper",
    )


def lift_create_bullet_group(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = [
        "style", "color", "x", "y", "count", "interval", "speed1", "speed2",
        "angle", "angle_spread", "aim", "omega", "stay", "destroyable", "delay", "reflect",
        "owner",
    ]
    return LuaSTGIRObject(
        kind="BulletEmitter",
        source=path,
        line=line_no,
        function=function,
        name="_create_bullet_group",
        params={key: args[index] for index, key in enumerate(keys) if index < len(args)},
        raw=raw,
        confidence="thlib_editor_pattern",
    )


def lift_new_object(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject | None:
    if not args:
        return None
    class_name = args[0]
    values = args[1:]
    if class_name == "_straight":
        keys = ["style", "color", "x", "y", "speed", "angle", "aim", "omega", "stay", "destroyable", "delay", "reflect"]
        return LuaSTGIRObject(
            kind="Bullet",
            source=path,
            line=line_no,
            function=function,
            name="New(_straight)",
            params={key: values[index] for index, key in enumerate(keys) if index < len(values)},
            raw=raw,
            confidence="thlib_straight_bullet",
        )
    if class_name in {"laser", "laser_bent"}:
        keys = ["style", "x", "y", "angle", "head_length", "body_length", "tail_length", "width", "node", "head"]
        return LuaSTGIRObject(
            kind="LaserEmitter",
            source=path,
            line=line_no,
            function=function,
            name=f"New({class_name})",
            params={key: values[index] for index, key in enumerate(keys) if index < len(values)},
            raw=raw,
            confidence="thlib_laser",
        )
    return None


def lift_wait(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    return LuaSTGIRObject("Wait", path, line_no, function, "task_wait", {"frames": args[0] if args else "1"}, raw, "task_api")


def lift_move(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = ["x", "y", "time", "mode"]
    return LuaSTGIRObject("Movement", path, line_no, function, "task.MoveTo", {key: args[index] for index, key in enumerate(keys) if index < len(args)}, raw, "task_api")


def lift_setv2(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = ["object", "speed", "angle", "set_rot", "angle_is_degree"]
    return LuaSTGIRObject("Movement", path, line_no, function, "SetV2", {key: args[index] for index, key in enumerate(keys) if index < len(args)}, raw, "motion_api")


def lift_boss_card(path: str, line_no: int, function: str, raw: str, args: list[str]) -> LuaSTGIRObject:
    keys = ["name", "t1", "t2", "time", "hp", "drop", "is_spell"]
    return LuaSTGIRObject("BossPattern", path, line_no, function, "boss.card.New", {key: args[index] for index, key in enumerate(keys) if index < len(args)}, raw, "thlib_boss_card")


def lift_luastg_file(path: str | Path) -> list[LuaSTGIRObject]:
    path = str(path)
    objects: list[LuaSTGIRObject] = []
    current_function = ""
    for line_no, line in enumerate(Path(path).read_text(errors="replace").splitlines(), 1):
        raw = line.rstrip()
        text = clean_lua_line(raw)
        if not text:
            continue
        if function_name := detect_function(text):
            current_function = function_name
            continue
        if current_function in HELPER_FUNCTIONS:
            continue
        for match in CALL_RE.finditer(text):
            callee = match.group(1)
            args = split_args(match.group(2))
            obj: LuaSTGIRObject | None = None
            if callee == "ecl_shot":
                obj = lift_ecl_shot(path, line_no, current_function, raw, args)
            elif callee == "ecl_laser":
                obj = lift_ecl_laser(path, line_no, current_function, raw, args)
            elif callee == "_create_bullet_group":
                obj = lift_create_bullet_group(path, line_no, current_function, raw, args)
            elif callee == "New":
                obj = lift_new_object(path, line_no, current_function, raw, args)
            elif callee in {"task._Wait", "task.Wait"}:
                obj = lift_wait(path, line_no, current_function, raw, args)
            elif callee == "task.MoveTo":
                obj = lift_move(path, line_no, current_function, raw, args)
            elif callee == "SetV2":
                obj = lift_setv2(path, line_no, current_function, raw, args)
            if obj:
                objects.append(obj)
        if match := BOSS_CARD_RE.search(text):
            objects.append(lift_boss_card(path, line_no, current_function, raw, split_args(match.group(1))))
    return objects


def emit_luastg_ir_json(path: str | Path) -> str:
    objects = lift_luastg_file(path)
    return json.dumps({"source": str(path), "objects": [obj.to_dict() for obj in objects]}, ensure_ascii=False, indent=2)
