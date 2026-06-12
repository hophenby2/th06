from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .lifter import lift_program as lift_bullets
from .model import AnimationOp, BossPattern, EnemyOp, Function, Instruction, IRObject, LaserEmitter, MovementOp, Program
from .timeline_lifter import lift_timelines

TH13PLUS = {"th13", "th14", "th15", "th16", "th17", "th18"}


def a(ins: Instruction, index: int, default: str = "") -> str:
    return ins.args[index] if index < len(ins.args) else default


def make_obj(cls, program: Program, func: Function, ins: Instruction, family: str, object_id: str = "0") -> IRObject:
    obj = cls(program.game, func.name, ins.line_no, object_id, family)
    obj.raw.append(ins)
    return obj


def lift_all_objects(program: Program) -> list[object]:
    objects: list[object] = []
    objects.extend(lift_bullets(program))
    objects.extend(lift_timelines(program))
    for func in program.functions:
        objects.extend(lift_lasers(program, func))
        objects.extend(lift_movements(program, func))
        objects.extend(lift_animation_enemy(program, func))
        objects.extend(lift_boss_patterns(program, func))
    return sorted(objects, key=lambda obj: (getattr(obj, "function", ""), getattr(obj, "source_line", 0), getattr(obj, "kind", "")))


def lift_lasers(program: Program, func: Function) -> list[LaserEmitter]:
    objects: list[LaserEmitter] = []
    active: dict[str, LaserEmitter] = {}
    if program.game in TH13PLUS:
        start_ops = {700}
        laser_ops = set(range(701, 715))
        family = "th13plus"
    elif program.game == "th12":
        start_ops = {600}
        laser_ops = set(range(601, 616))
        family = "th12"
    else:
        return objects
    for ins in func.body:
        if ins.opcode in start_ops:
            laser_id = a(ins, 0, "0")
            obj = make_obj(LaserEmitter, program, func, ins, family, laser_id)
            active[laser_id] = obj
            objects.append(obj)
            continue
        laser_id = a(ins, 0, "0")
        obj = active.get(laser_id)
        if obj and ins.opcode in laser_ops:
            obj.raw.append(ins)
            apply_laser(obj, ins, program.game)
    return objects


def apply_laser(obj: LaserEmitter, ins: Instruction, game: str) -> None:
    op = ins.opcode
    if game in TH13PLUS:
        names = {
            701: "timing", 702: "on", 703: "straight_on", 704: "offset", 705: "trajectory",
            706: "length", 707: "width", 708: "angle", 709: "rotation", 710: "end", 711: "curve_on", 712: "cancel_rect",
        }
    else:
        names = {
            601: "timing", 602: "on", 603: "straight_on", 604: "offset", 605: "trajectory",
            606: "length", 607: "width", 608: "angle", 609: "rotation", 610: "end", 611: "curve_on",
        }
    key = names.get(op, f"ins_{op}")
    obj.fields.setdefault(key, []).append({"args": ins.args, "line": ins.line_no})


def lift_movements(program: Program, func: Function) -> list[MovementOp]:
    objects: list[MovementOp] = []
    if program.game in TH13PLUS:
        movement_names = {
            400: "movePos", 401: "movePosTime", 402: "movePosRel", 403: "movePosRelTime",
            404: "moveVel", 405: "moveVelTime", 406: "moveVelRel", 407: "moveVelRelTime",
            408: "moveCircle", 409: "moveCircleTime", 410: "moveCircleRel", 411: "moveCircleRelTime",
            420: "moveEllipse", 421: "moveEllipseTime", 422: "moveEllipseRel", 423: "moveEllipseRelTime",
            424: "moveSetMirror", 425: "moveBezier", 426: "moveBezierRel", 427: "moveReset",
            432: "moveEnm", 433: "moveEnmRel", 434: "moveCurve", 435: "moveCurveRel",
            440: "moveDir", 441: "moveDirTime", 442: "moveDirRel", 443: "moveDirRelTime",
            444: "moveSpeed", 445: "moveSpeedTime", 446: "moveSpeedRel", 447: "moveSpeedRelTime",
        }
        family = "th13plus"
    elif program.game == "th12":
        movement_names = {
            300: "movePos", 301: "movePosTime", 302: "movePosRel", 303: "movePosRelTime",
            304: "moveVel", 305: "moveVelTime", 306: "moveVelRel", 307: "moveVelRelTime",
            320: "moveEllipse", 321: "moveEllipseTime", 322: "moveEllipseRel", 323: "moveEllipseRelTime",
            325: "moveBezier", 326: "moveBezierRel", 327: "moveReset",
        }
        family = "th12"
    elif program.game in {"th10", "th11"}:
        movement_names = {300: "moveEllipse", 320: "movePos", 321: "movePosTime", 322: "moveVel", 323: "moveVelTime", 327: "moveReset"}
        family = "th10"
    else:
        return objects
    current_direction: str | None = None
    current_speed: str | None = None
    for ins in func.body:
        if ins.opcode not in movement_names:
            continue
        obj = make_obj(MovementOp, program, func, ins, family)
        op_name = movement_names[ins.opcode]
        obj.fields["op"] = op_name
        obj.fields["args"] = ins.args
        obj.fields["difficulty"] = ins.difficulty
        obj.fields.setdefault("semantics", {})["motion"] = {"op": op_name}
        if program.game in TH13PLUS:
            if ins.opcode in {404, 406} and len(ins.args) >= 2:
                current_direction, current_speed = ins.args[0], ins.args[1]
                obj.fields["semantics"]["motion"].update({"direction": current_direction, "speed": current_speed})
            elif ins.opcode in {405, 407} and len(ins.args) >= 4:
                current_direction, current_speed = ins.args[2], ins.args[3]
                obj.fields["semantics"]["motion"].update({"time": ins.args[0], "mode": ins.args[1], "direction": current_direction, "speed": current_speed})
            elif ins.opcode in {440, 442} and len(ins.args) >= 1:
                current_direction = ins.args[0]
                obj.fields["semantics"]["motion"].update({"direction": current_direction, "speed": current_speed})
            elif ins.opcode in {441, 443} and len(ins.args) >= 3:
                obj.fields["semantics"]["motion"].update({"time": ins.args[0], "mode": ins.args[1], "direction_delta": ins.args[2], "base_direction": current_direction, "speed": current_speed})
                if current_direction is not None:
                    current_direction = f"{current_direction} + {ins.args[2]}"
            elif ins.opcode in {444, 446} and len(ins.args) >= 1:
                current_speed = ins.args[0]
                obj.fields["semantics"]["motion"].update({"direction": current_direction, "speed": current_speed})
            elif ins.opcode in {445, 447} and len(ins.args) >= 3:
                current_speed = ins.args[2]
                obj.fields["semantics"]["motion"].update({"time": ins.args[0], "mode": ins.args[1], "direction": current_direction, "speed": current_speed})
        objects.append(obj)
    return objects


def lift_animation_enemy(program: Program, func: Function) -> list[IRObject]:
    objects: list[IRObject] = []
    if program.game in TH13PLUS:
        animation = {302: "anmSelect", 303: "anmSetSprite", 306: "anmSetMain", 307: "anmPlay", 308: "anmPlayAbs", 317: "anmSwitch", 318: "anmReset"}
        enemy = {300: "enmCreate", 301: "enmCreateA", 304: "enmCreateM", 305: "enmCreateAM", 309: "enmCreateF", 310: "enmCreateAF", 311: "enmCreateMF", 312: "enmCreateAMF"}
        family = "th13plus"
    elif program.game in {"th10", "th11", "th12"}:
        animation = {258: "anmSelect", 259: "anmSetSprite", 262: "anmSetMain", 263: "anmPlay", 264: "anmPlayAbs"}
        enemy = {256: "enmCreate", 257: "enmCreateA", 260: "enmCreateM", 261: "enmCreateAM", 265: "enmCreateF", 266: "enmCreateAF", 267: "enmCreateMF", 268: "enmCreateAMF"}
        family = "th10_th12"
    else:
        return objects
    for ins in func.body:
        if ins.opcode in animation:
            obj = make_obj(AnimationOp, program, func, ins, family)
            obj.fields = {"op": animation[ins.opcode], "args": ins.args, "difficulty": ins.difficulty}
            objects.append(obj)
        elif ins.opcode in enemy:
            obj = make_obj(EnemyOp, program, func, ins, family)
            obj.fields = {"op": enemy[ins.opcode], "args": ins.args, "difficulty": ins.difficulty}
            objects.append(obj)
    return objects


def lift_boss_patterns(program: Program, func: Function) -> list[BossPattern]:
    objects: list[BossPattern] = []
    if program.game in TH13PLUS:
        boss_ops = {511: "lifeSet", 512: "setBoss", 513: "timerReset", 514: "setInterrupt", 521: "setTimeout", 523: "spellEnd", 524: "setChapter", 537: "spell", 538: "spell2", 539: "spell3"}
        family = "th13plus"
    elif program.game == "th12":
        boss_ops = {411: "lifeSet", 412: "setBoss", 413: "timerReset", 414: "setInterrupt", 421: "setTimeout", 423: "spellEnd", 424: "setChapter", 526: "spell", 527: "callStd", 528: "lifeHide"}
        family = "th12"
    else:
        return objects
    current: BossPattern | None = None
    for ins in func.body:
        if ins.opcode in boss_ops:
            if current is None or ins.opcode in {514, 537, 538, 539, 414, 526}:
                current = make_obj(BossPattern, program, func, ins, family)
                objects.append(current)
            else:
                current.raw.append(ins)
            current.fields.setdefault("ops", []).append({"op": boss_ops[ins.opcode], "opcode": ins.opcode, "args": ins.args, "line": ins.line_no})
            if boss_ops[ins.opcode].startswith("spell"):
                current.fields["spell"] = {"opcode": ins.opcode, "args": ins.args}
            elif boss_ops[ins.opcode] == "setInterrupt":
                current.fields["interrupt"] = {"args": ins.args}
    return objects


def summarize_by_kind(objects: Iterable[object]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for obj in objects:
        counts[getattr(obj, "kind", obj.__class__.__name__)] += 1
    return dict(sorted(counts.items()))
