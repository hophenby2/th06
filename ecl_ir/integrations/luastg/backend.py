from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from ...source.model import Function, Program, Statement
from ...source.parser import parse_decl

BOSS_FUNC_RE = re.compile(r"^(Boss|Boss\d+|BossCard\d*|Boss.*_at.*|BossEyes\d*|HPWait)$")


def lua_ident(name: str) -> str:
    return re.sub(r"\W", "_", name)


def clean_num(value: object, default: str = "0") -> str:
    text = str(value).strip()
    text = text.replace("f", "")
    text = re.sub(r"_f\(([^)]+)\)", r"(\1)", text)
    text = re.sub(r"_\(([^)]+)\)", r"(\1)", text)
    text = text.replace("[-9998.0]", "0")
    text = text.replace("[-9998.0f]", "0")
    text = re.sub(r"\[(-?\d+)(?:\.0f?)?\]", r"ecl_var[\1]", text)
    text = text.replace("%", "v_").replace("$", "i_")
    if text == "":
        return default
    return text


def lua_string(value: object) -> str:
    text = str(value).strip()
    if text.startswith('"') and text.endswith('"'):
        return text
    return '"' + text.replace('"', '\\"') + '"'


@dataclass
class LaserState:
    laser_id: str
    style: str = "1"
    start_offset: str = "0"
    length: str = "512"
    tail_offset: str = "0"
    width: str = "16"
    warn_time: str = "0"
    in_time: str = "0"
    active_time: str = "60"
    out_time: str = "15"
    angle: str = "0"
    x: str = "self.x"
    y: str = "self.y"


@dataclass
class EmitterState:
    et_id: str
    style: str = "1"
    color: str = "0"
    aim_mode: str = "3"
    ways: str = "1"
    layers: str = "1"
    angle: str = "0"
    angle_step: str = "0"
    speed: str = "1.0"
    speed_step: str = "0.0"
    offset_x: str = "0"
    offset_y: str = "0"
    distance: str = "0"
    transforms: list[str] = field(default_factory=list)


def shot_mode_for_aim(raw: str) -> str:
    raw = str(raw).strip()
    return {
        "0": "0",  # aimed fan
        "1": "1",  # fan
        "2": "3",  # aimed ring-ish
        "3": "3",  # ring
        "4": "0",  # offset aimed fan approximation
        "5": "1",  # offset fan approximation
        "6": "8",  # random angle
        "7": "7",  # random speed
        "8": "8",  # random angle/speed
    }.get(raw, "1")


def bullet_class_name(prefix: str, style: str, color: str) -> str:
    style_key = re.sub(r"\W+", "_", str(style)).strip("_") or "0"
    color_key = re.sub(r"\W+", "_", str(color)).strip("_") or "0"
    return f"{prefix}_Bullet_{style_key}_{color_key}"


class LuaSTGEmitter:
    def __init__(self, prefix: str, runtime: str = "liu_10_mc"):
        self.prefix = prefix
        self.runtime = runtime
        self.states: dict[str, EmitterState] = {}
        self.lasers: dict[str, LaserState] = {}
        self.classes: set[tuple[str, str, str]] = set()

    def rank_pick(self, values: list[str]) -> str:
        return "ecl_pick_rank(" + ", ".join(clean_num(v) for v in values) + ")"

    def angle(self, value: str) -> str:
        return f"ecl_rad({clean_num(value)})"

    def state(self, et_id: object) -> EmitterState:
        key = clean_num(et_id, "0")
        if key not in self.states:
            self.states[key] = EmitterState(et_id=key)
        return self.states[key]

    def laser_state(self, laser_id: object) -> LaserState:
        key = clean_num(laser_id, "0")
        if key not in self.lasers:
            self.lasers[key] = LaserState(laser_id=key)
        return self.lasers[key]

    def handle_laser_instruction(self, opcode: int, args: list[str]) -> list[str] | None:
        if opcode == 600 and len(args) >= 5:
            laser = self.laser_state(args[0])
            laser.start_offset = clean_num(args[1])
            laser.length = clean_num(args[2])
            laser.tail_offset = clean_num(args[3])
            laser.width = clean_num(args[4])
            return [f"-- laserShape id={laser.laser_id} length={laser.length} width={laser.width}"]
        if opcode == 601 and len(args) >= 6:
            laser = self.laser_state(args[0])
            laser.warn_time = clean_num(args[1])
            laser.in_time = clean_num(args[2])
            laser.active_time = clean_num(args[3])
            laser.out_time = clean_num(args[4])
            return [f"-- laserTiming id={laser.laser_id} warn={laser.warn_time} active={laser.active_time}"]
        if opcode in {602, 603, 611} and args:
            laser = self.laser_state(args[0])
            style = clean_num(args[1]) if opcode == 603 and len(args) >= 2 else laser.laser_id
            laser.style = style
            kind = "curve" if opcode == 611 else "line"
            return [f"ecl_laser({laser.style}, self.x, self.y, {laser.angle}, {laser.length}, {laser.width}, {laser.warn_time}, {laser.in_time}, {laser.active_time}, {laser.out_time}, {lua_string(kind)})"]
        if opcode == 604 and len(args) >= 3:
            laser = self.laser_state(args[0])
            laser.x = clean_num(args[1])
            laser.y = clean_num(args[2])
            return [f"-- laserOrigin id={laser.laser_id} x={laser.x} y={laser.y}"]
        if opcode == 608 and len(args) >= 2:
            laser = self.laser_state(args[0])
            laser.angle = self.angle(args[1])
            return [f"-- laserAngle id={laser.laser_id} angle={laser.angle}"]
        return None

    def handle_instruction(self, opcode: int, args: list[str]) -> list[str] | None:
        if opcode == 500:
            self.state(args[0] if args else "0")
            return [f"-- etNew({clean_num(args[0] if args else '0')})"]
        if opcode == 502 and len(args) >= 3:
            st = self.state(args[0]); st.style = clean_num(args[1]); st.color = clean_num(args[2])
            return [f"-- etSprite et={st.et_id} style={st.style} color={st.color}"]
        if opcode == 503 and len(args) >= 3:
            st = self.state(args[0]); st.offset_x = clean_num(args[1]); st.offset_y = clean_num(args[2])
            return [f"-- etOffset et={st.et_id} x={st.offset_x} y={st.offset_y}"]
        if opcode == 504 and len(args) >= 3:
            st = self.state(args[0]); st.angle = self.angle(args[1]); st.angle_step = self.angle(args[2])
            return [f"-- etAngle et={st.et_id} angle={st.angle} step={st.angle_step}"]
        if opcode == 505 and len(args) >= 3:
            st = self.state(args[0]); st.speed = clean_num(args[1]); st.speed_step = clean_num(args[2])
            return [f"-- etSpeed et={st.et_id} speed={st.speed} step={st.speed_step}"]
        if opcode == 506 and len(args) >= 3:
            st = self.state(args[0]); st.ways = clean_num(args[1]); st.layers = clean_num(args[2])
            return [f"-- etCount et={st.et_id} ways={st.ways} layers={st.layers}"]
        if opcode == 521 and len(args) >= 9:
            st = self.state(args[0]); st.speed = self.rank_pick(args[1:5]); st.speed_step = self.rank_pick(args[5:9])
            return [f"-- etSpeedD et={st.et_id} speed={st.speed} step={st.speed_step}"]
        if opcode == 522 and len(args) >= 9:
            st = self.state(args[0]); st.ways = self.rank_pick(args[1:5]); st.layers = self.rank_pick(args[5:9])
            return [f"-- etCountD et={st.et_id} ways={st.ways} layers={st.layers}"]
        if opcode == 507 and len(args) >= 2:
            st = self.state(args[0]); st.aim_mode = clean_num(args[1])
            return [f"-- etAim et={st.et_id} mode={st.aim_mode}"]
        if opcode == 509:
            st = self.state(args[0] if args else "0"); st.transforms.append("{" + ", ".join(clean_num(a) for a in args[1:]) + "}")
            return [f"-- etEx et={st.et_id} params preserved"]
        if opcode == 524 and len(args) >= 2:
            st = self.state(args[0]); st.distance = clean_num(args[1])
            return [f"-- etDist et={st.et_id} distance={st.distance}"]
        if opcode == 525 and len(args) >= 3:
            st = self.state(args[0]); st.offset_x = f"({clean_num(args[1])}) - self.x"; st.offset_y = f"({clean_num(args[2])}) - self.y"
            return [f"-- etOffsetAbs et={st.et_id} x={clean_num(args[1])} y={clean_num(args[2])}"]
        if opcode == 501:
            et = args[0] if args else "0"
            st = self.state(et)
            mode = shot_mode_for_aim(st.aim_mode)
            param = "{" + ", ".join(st.transforms[-1:]) + "}" if st.transforms else "nil"
            if self.runtime == "liu_10_mc":
                cls = bullet_class_name(self.prefix, st.style, st.color)
                self.classes.add((cls, st.style, st.color))
                return [
                    f"liu_10_mc.bullet.ShotBulletMode({mode}, {st.et_id}, _editor_class[{lua_string(cls)}], self.x, self.y, {st.offset_x}, {st.offset_y}, {st.distance}, 0, 0, math.max(1, math.floor({st.ways})), math.max(1, math.floor({st.layers})), {st.speed}, {st.speed_step}, {st.angle}, {st.angle_step}, {param})"
                ]
            return [
                f"ecl_shot({mode}, {st.et_id}, {st.style}, {st.color}, self.x, self.y, {st.offset_x}, {st.offset_y}, {st.distance}, 0, 0, math.max(1, math.floor({st.ways})), math.max(1, math.floor({st.layers})), {st.speed}, {st.speed_step}, {st.angle}, {st.angle_step}, {param})"
            ]
        return None


def lua_expr(expr: str) -> str:
    text = clean_num(expr)
    text = re.sub(r"\bv_([A-Za-z])\b", r"v_\1", text)
    text = re.sub(r"\bi_([A-Za-z])\b", r"i_\1", text)
    text = text.replace("||", " or ").replace("&&", " and ")
    text = re.sub(r"!(?!=)", "not ", text)
    return text


def ecl_var_names(name: str) -> tuple[str, str]:
    base = re.sub(r"\W+", "_", str(name).strip()).strip("_") or "A"
    return f"v_{base}", f"i_{base}"


def lower_instruction(opcode: int, args: list[str], emit: LuaSTGEmitter) -> list[str]:
    bullet = emit.handle_instruction(opcode, args)
    if bullet is not None:
        return bullet
    if opcode == 1:
        return ["do return end"]
    if opcode == 83:
        return [f"task._Wait({clean_num(args[0] if args else '1')})"]
    if opcode == 81 and len(args) >= 4:
        return [
            f"{lua_expr(args[0])} = math.cos({clean_num(args[2])}) * ({clean_num(args[3])})",
            f"{lua_expr(args[1])} = math.sin({clean_num(args[2])}) * ({clean_num(args[3])})",
        ]
    if opcode in {300, 400} and len(args) >= 2:
        return [f"self.x, self.y = {clean_num(args[0])}, {clean_num(args[1])}", "ecl_sync_self(self)"]
    if opcode in {301, 401} and len(args) >= 4:
        return [f"task.MoveTo({clean_num(args[2])}, {clean_num(args[3])}, {clean_num(args[0])}, {clean_num(args[1])})", "ecl_sync_self(self)"]
    if opcode in {304, 404} and len(args) >= 2:
        return [f"SetV2(self, {clean_num(args[1])}, ecl_rad({clean_num(args[0])}), true, false)"]
    if opcode in {305, 405} and len(args) >= 4:
        return [f"task.New(self, function() SetV2(self, {clean_num(args[3])}, ecl_rad({clean_num(args[2])}), true, false); task._Wait({clean_num(args[0])}) end)"]
    if opcode == 312 and len(args) >= 3:
        if emit.runtime == "liu_10_mc":
            return [f"task.New(self, _editor_tasks[{lua_string('liu_10_mc_moveRand')}]({clean_num(args[0])}, {clean_num(args[1])}, {clean_num(args[2])}))"]
        return [f"ecl_move_rand(self, {clean_num(args[0])}, {clean_num(args[1])}, {clean_num(args[2])})"]
    if opcode == 414 and len(args) >= 4:
        return [f"-- setInterrupt phase={clean_num(args[0])} life={clean_num(args[1])} time={clean_num(args[2])} sub={args[3]}"]
    if opcode == 411 and args:
        return [f"self.hp, self.maxhp = {clean_num(args[0])}, {clean_num(args[0])}"]
    if opcode == 413:
        return ["-- timerReset"]
    if opcode in {423, 424, 425, 427, 437, 438, 439, 421, 422}:
        return [f"-- boss/meta ins_{opcode}({', '.join(args)})"]
    if opcode in {600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611}:
        laser = emit.handle_laser_instruction(opcode, args)
        if laser is not None:
            return laser
        return [f"-- laser ins_{opcode}({', '.join(args)}) TODO: map to THlib laser object"]
    if opcode in {258, 259, 262, 263, 269, 272, 273, 274, 277, 416, 440, 445, 529}:
        return [f"-- visual/helper ins_{opcode}({', '.join(args)})"]
    return [f"-- unsupported ins_{opcode}({', '.join(args)})"]




def _is_label(stmt: Statement, label: str) -> bool:
    return stmt.kind == "label" and stmt.attrs.get("name") == label


def _goto_label(stmt: Statement) -> str | None:
    if stmt.kind in {"goto", "conditional_goto"}:
        return str(stmt.attrs.get("label", ""))
    return None


def _loop_counter(condition: str) -> str | None:
    match = re.fullmatch(r"\s*\$([A-Za-z0-9_]+)--\s*", condition)
    if not match:
        return None
    return ecl_var_names(match.group(1))[1]


def _indent(lines: list[str], prefix: str = "    ") -> list[str]:
    return [prefix + line for line in lines]


def lower_statement_block(statements: list[Statement], emit: LuaSTGEmitter) -> list[str]:
    lines: list[str] = []
    index = 0
    while index < len(statements):
        stmt = statements[index]
        if stmt.kind == "goto":
            end_label = str(stmt.attrs.get("label", ""))
            if index + 1 < len(statements) and statements[index + 1].kind == "label":
                body_label = str(statements[index + 1].attrs.get("name", ""))
                end_index = None
                for probe in range(index + 2, len(statements) - 1):
                    if _is_label(statements[probe], end_label):
                        tail = statements[probe + 1]
                        if _goto_label(tail) == body_label:
                            end_index = probe
                            break
                if end_index is not None:
                    tail = statements[end_index + 1]
                    body = lower_statement_block(statements[index + 2:end_index], emit)
                    if tail.kind == "conditional_goto":
                        cond_type = str(tail.attrs.get("condition_type", ""))
                        cond = str(tail.attrs.get("condition", ""))
                        counter = _loop_counter(cond)
                        if cond_type == "if" and counter:
                            lines.append(f"for _ecl_loop = 1, math.max(0, math.floor({counter})) do")
                            lines.extend(_indent(body))
                            lines.append("end")
                            index = end_index + 2
                            continue
                        if cond_type == "if" and clean_num(cond) == "1":
                            lines.append("while true do")
                            lines.extend(_indent(body))
                            if not any("task._Wait" in line or "task.Wait" in line for line in body):
                                lines.append("    task._Wait(1)")
                            lines.append("end")
                            index = end_index + 2
                            continue
                    lines.append(f"-- loop pattern preserved: goto {end_label}; label {body_label}")
        for out in lower_statement(stmt, emit):
            lines.append(out)
        index += 1
    return lines
def lower_statement(stmt: Statement, emit: LuaSTGEmitter, include_labels: bool = False) -> list[str]:
    if stmt.kind == "instruction":
        return lower_instruction(int(stmt.attrs.get("opcode", -1)), [str(a) for a in stmt.attrs.get("args", [])], emit)
    if stmt.kind == "call":
        fn = lua_ident(str(stmt.attrs.get("function", "")))
        args = ", ".join(lua_expr(str(a)) for a in stmt.attrs.get("args", []))
        return [f"ecl_{fn}(self{', ' if args else ''}{args})"]
    if stmt.kind == "async_call":
        fn = lua_ident(str(stmt.attrs.get("function", "")))
        args = ", ".join(lua_expr(str(a)) for a in stmt.attrs.get("args", []))
        return [f"task.New(self, function() ecl_{fn}(self{', ' if args else ''}{args}) end)"]
    if stmt.kind == "assign":
        return [f"{lua_expr(str(stmt.attrs.get('target', '')))} = {lua_expr(str(stmt.attrs.get('expr', '0')))}"]
    if stmt.kind == "var":
        names: list[str] = []
        values: list[str] = []
        for var in stmt.attrs.get("vars", []):
            float_name, int_name = ecl_var_names(str(var))
            names.extend([float_name, int_name])
            values.extend(["0", "0"])
        return ["local " + ", ".join(names) + " = " + ", ".join(values)] if names else []
    if stmt.kind == "return":
        return ["do return end"]
    if stmt.kind == "time":
        return [str(stmt.text)] if include_labels else ["-- " + str(stmt.text)]
    if stmt.kind == "label":
        return ["-- label " + str(stmt.attrs.get("name", stmt.text))]
    if stmt.kind in {"goto", "conditional_goto"}:
        return ["-- control-flow not structurally lowered: " + stmt.text]
    return ["-- raw " + stmt.text] if stmt.text else []



def thlib_runtime_helpers() -> list[str]:
    return [
        "local function ecl_new_bullet(style, color, x, y, speed, angle, delay, param)",
        "    param = param or {}",
        "    local obj = New(_straight, style, color, x, y, speed, angle, false, 0, true, true, delay or 0, false)",
        "    obj.ecl_param = param",
        "    return obj",
        "end",
        "local function ecl_shot(mode, num, style, color, x, y, dx, dy, dis, o, r, way, layer, spd1, spd2, ang1, ang2, param)",
        "    local result = {}",
        "    local sx, sy = x + dx + r * cos(o), y + dy + r * sin(o)",
        "    way, layer = math.max(1, math.floor(way or 1)), math.max(1, math.floor(layer or 1))",
        "    for i = 1, layer do",
        "        local speed = spd1 + ((spd2 or spd1) - spd1) * ((layer == 1) and 0 or ((i - 1) / (layer - 1)))",
        "        for j = 1, way do",
        "            local angle",
        "            if mode == 0 then",
        "                angle = Angle(sx, sy, player.x, player.y) + ang1 + (j - (way + 1) / 2) * ang2",
        "            elseif mode == 1 then",
        "                angle = ang1 + (j - (way + 1) / 2) * ang2",
        "            elseif mode == 2 then",
        "                angle = Angle(sx, sy, player.x, player.y) + ang1 + (j - 1) * 360 / way - (i - 1) * ang2",
        "            elseif mode == 3 then",
        "                angle = ang1 + (j - 1) * 360 / way - (i - 1) * ang2",
        "            else",
        "                angle = ang1 + (j - 1) * 360 / way - (i - 1) * ang2",
        "            end",
        "            local bullet_obj = ecl_new_bullet(style, color, sx + dis * cos(angle), sy + dis * sin(angle), speed, angle, 0, param)",
        "            bullet_obj.layer = bullet_obj.layer - 0.000001 * i + 0.0000001 * j + 0.0005 * (num or 0)",
        "            table.insert(result, bullet_obj)",
        "        end",
        "    end",
        "    return result",
        "end",
        "local function ecl_laser(style, x, y, angle, length, width, warn_time, in_time, active_time, out_time, kind)",
        "    local obj = New(laser, style or 1, x or 0, y or 0, angle or 0, 0, length or 512, 0, width or 16, 0, 0)",
        "    obj.ecl_timing = {warn = warn_time or 0, fade_in = in_time or 0, active = active_time or 60, fade_out = out_time or 15, kind = kind or 'line'}",
        "    task.New(obj, function()",
        "        if warn_time and warn_time > 0 then task._Wait(warn_time) end",
        "        obj.colli = true",
        "        obj.alpha = 1",
        "        obj.w = width or obj.w0 or 16",
        "        task._Wait(active_time or 60)",
        "        Del(obj)",
        "    end)",
        "    return obj",
        "end",
        "local function ecl_move_rand(self, time, mode, radius)",
        "    local cx, cy = self.x or 0, self.y or 0",
        "    local angle = ran:Float(0, 360)",
        "    local dist = radius or 0",
        "    task.New(self, function() task.MoveTo(cx + dist * cos(angle), cy + dist * sin(angle), time or 1, mode or 4); ecl_sync_self(self) end)",
        "end",
    ]

def selected_boss_functions(program: Program, names: Iterable[str] | None = None) -> list[Function]:
    wanted = set(names or [])
    funcs = []
    for func in program.functions:
        if wanted and func.name not in wanted:
            continue
        if wanted or BOSS_FUNC_RE.match(func.name):
            funcs.append(func)
    return funcs


def emit_luastg(program: Program, module_name: str = "ecl_stage06_boss", names: Iterable[str] | None = None, runtime: str = "liu_10_mc") -> str:
    emit = LuaSTGEmitter(module_name, runtime)
    funcs = selected_boss_functions(program, names)
    lines: list[str] = []
    lines.append("-- Auto-generated LuaSTG approximation from ECL IR")
    lines.append(f"-- source: {program.source}")
    lines.append("-- This is a semantic draft: timings/bullets are approximate and intended for manual refinement.")
    lines.append("local M = {}")
    lines.append("local ecl_var = setmetatable({}, { __index = function() return 0 end })")
    lines.append("local function ecl_rad(value) return (value or 0) * 180 / math.pi end")
    lines.append("local function ecl_sync_self(self)")
    lines.append("    if self then ecl_var[-9997], ecl_var[-9996] = self.x or 0, self.y or 0 end")
    lines.append("end")
    if runtime == "thlib":
        lines.extend(thlib_runtime_helpers())
    if runtime != "thlib":
        lines.append("local function ecl_laser(...) return nil end")
    lines.append("local function ecl_pick_rank(easy, normal, hard, lunatic)")
    lines.append("    local rank = _G.difficulty or (lstg and lstg.var and (lstg.var.difficulty or lstg.var.rank)) or 2")
    lines.append("    if type(rank) == 'string' then")
    lines.append("        local key = string.lower(rank)")
    lines.append("        rank = ({easy = 1, e = 1, normal = 2, n = 2, hard = 3, h = 3, lunatic = 4, l = 4})[key] or 2")
    lines.append("    end")
    lines.append("    local values = {easy, normal, hard, lunatic}")
    lines.append("    return values[math.max(1, math.min(4, math.floor(rank or 2)))] or normal or easy or 0")
    lines.append("end")
    if funcs:
        lines.append("local " + ", ".join(f"ecl_{lua_ident(func.name)}" for func in funcs))
    lines.append("")
    for func in funcs:
        params = [p.strip().split()[-1] for p in func.params.split(',') if p.strip()]
        lua_params = ["self"] + [ecl_var_names(p)[0] for p in params]
        lines.append(f"function ecl_{lua_ident(func.name)}({', '.join(lua_params)})")
        lines.append("    ecl_sync_self(self)")
        for param in params:
            float_name, int_name = ecl_var_names(param)
            lines.append(f"    local {int_name} = {float_name} or 0")
        if not func.statements:
            lines.append("    -- empty")
        for out in lower_statement_block(func.statements, emit):
            lines.append("    " + out)
        lines.append("end")
        lines.append(f"M.{lua_ident(func.name)} = ecl_{lua_ident(func.name)}")
        lines.append("")
    if emit.classes:
        lines.append("-- Bullet classes synthesized from ECL etSprite state")
    for cls, style, color in sorted(emit.classes):
        lines.append(f"_editor_class[{lua_string(cls)}] = _editor_class[{lua_string(cls)}] or Class(bullet)")
        lines.append("do")
        lines.append(f"    local bullet_class = _editor_class[{lua_string(cls)}]")
        lines.append("    function bullet_class:init(x, y, ...)")
        lines.append("        bullet.init(self, liu_10_mc.bullet.bullet_class, COLOR_RED, true, true)")
        lines.append("        self.x, self.y = x, y")
        lines.append(f"        liu_10_mc.bullet.BulletClassInit(self, {style}, {color})")
        lines.append("        liu_10_mc.bullet.SetBulletPreimg(self, 1, true)")
        lines.append("    end")
        lines.append("end")
        lines.append("")
    lines.append("function M.attach_to_boss_card(card)")
    lines.append("    task.New(card, function()")
    lines.append("        ecl_Boss(card)")
    lines.append("    end)")
    lines.append("end")
    lines.append("")
    lines.append("return M")
    return "\n".join(lines)


def emit_luastg_file(input_path: str, output_path: str, module_name: str = "ecl_stage06_boss", names: Iterable[str] | None = None, runtime: str = "liu_10_mc") -> None:
    program = parse_decl(input_path)
    Path(output_path).write_text(emit_luastg(program, module_name, names, runtime))
