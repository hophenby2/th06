from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .lifter import lift_program as lift_bullets
from .model import (
    AnimationOp,
    AutoBulletTimer,
    BossPattern,
    BossTimer,
    EffectEmitter,
    EnemyOp,
    FamiliarSpawner,
    Function,
    Instruction,
    IRObject,
    LaserEmitter,
    MotionModifier,
    MovementOp,
    Program,
)
from .op_ir import op_event, op_key_for_opcode
from .program_lifter import lift_program_adapters
from .timeline_lifter import lift_timelines

TH13PLUS = {"th13", "th14", "th15", "th16", "th17", "th18"}


def a(ins: Instruction, index: int, default: str = "") -> str:
    return ins.args[index] if index < len(ins.args) else default


def make_obj(cls, program: Program, func: Function, ins: Instruction, family: str, object_id: str = "0") -> IRObject:
    obj = cls(program.game, func.name, ins.line_no, object_id, family)
    obj.source = program.source
    obj.raw.append(ins)
    obj.fields.setdefault("ir_ops", []).append(op_event(program.game, ins.opcode, ins.args, ins.line_no, ins.difficulty))
    return obj


def append_ir_op(obj: IRObject, game: str, ins: Instruction) -> None:
    obj.fields.setdefault("ir_ops", []).append(op_event(game, ins.opcode, ins.args, ins.line_no, ins.difficulty))


def lift_all_objects(program: Program) -> list[object]:
    objects: list[object] = []
    objects.extend(lift_program_adapters(program))
    objects.extend(lift_bullets(program))
    objects.extend(lift_timelines(program))
    for func in program.functions:
        objects.extend(lift_lasers(program, func))
        objects.extend(lift_movements(program, func))
        objects.extend(lift_animation_enemy(program, func))
        objects.extend(lift_boss_patterns(program, func))
        objects.extend(lift_high_level_legacy_objects(program, func))
    return sorted(objects, key=lambda obj: (getattr(obj, "function", ""), getattr(obj, "source_line", 0), getattr(obj, "kind", "")))


def lift_high_level_legacy_objects(program: Program, func: Function) -> list[IRObject]:
    if program.game not in {"th06", "th07", "th08"}:
        return []
    objects: list[IRObject] = []
    for ins in func.body:
        op = ins.opcode
        if op in {128, 129, 139, 140, 153}:
            obj = make_obj(EffectEmitter, program, func, ins, "th08_effect", a(ins, 0, "0"))
            apply_legacy_effect(obj, ins)
            objects.append(obj)
        elif op in {83, 90, 91, 92, 174}:
            obj = make_obj(FamiliarSpawner, program, func, ins, "th08_familiar", a(ins, 0, "0"))
            apply_legacy_familiar(obj, ins)
            objects.append(obj)
        elif op in {105, 106, 107}:
            obj = make_obj(AutoBulletTimer, program, func, ins, "th08_auto_bullet", "0")
            apply_legacy_auto_bullet(obj, ins)
            objects.append(obj)
        elif op in {132, 133, 134, 148, 158, 173, 184}:
            obj = make_obj(BossTimer, program, func, ins, "th08_boss_timer", a(ins, 0, "0"))
            apply_legacy_boss_timer(obj, ins)
            objects.append(obj)
        elif op in {67, 70, 71, 74, 178}:
            obj = make_obj(MotionModifier, program, func, ins, "th08_motion_modifier", "0")
            apply_legacy_motion_modifier(obj, ins)
            objects.append(obj)
    return objects


def apply_legacy_effect(obj: EffectEmitter, ins: Instruction) -> None:
    effect_names = {
        128: "card_effect",
        129: "spell_effect_state",
        139: "effect_burst",
        140: "effect_burst_angle",
        153: "spell_start_effect_state",
    }
    fields = obj.fields
    fields.update({"semantic": effect_names.get(ins.opcode, f"effect_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode == 139:
        fields["effect"] = {"source": "etama.anm", "script_expr": f"({a(ins, 0, '0')} + 28)", "amount": a(ins, 1, "1"), "color": a(ins, 2, "0"), "angle": None}
    elif ins.opcode == 140:
        fields["effect"] = {"source": "etama.anm", "script_expr": f"({a(ins, 0, '0')} + 28)", "amount": a(ins, 1, "1"), "color": a(ins, 2, "0"), "angle": a(ins, 3, "0.0f"), "unknown": ins.args[4:]}


def apply_legacy_familiar(obj: FamiliarSpawner, ins: Instruction) -> None:
    familiar_names = {
        83: "trail_toggle",
        90: "create_absolute",
        91: "create_relative",
        92: "create_following",
        174: "focus_animation",
    }
    fields = obj.fields
    fields.update({"semantic": familiar_names.get(ins.opcode, f"familiar_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode in {90, 91, 92}:
        fields["spawn"] = {
            "sub": a(ins, 0, ""),
            "x": a(ins, 1, "0.0f"),
            "y": a(ins, 2, "0.0f"),
            "life": a(ins, 3, "0"),
            "item": a(ins, 4, "0"),
            "score": a(ins, 5, "0"),
            "position_mode": "absolute" if ins.opcode == 90 else "relative",
            "follow_owner": ins.opcode == 92,
            "focus_invulnerable": True,
            "clear_bullets_on_death": True,
        }
    elif ins.opcode == 83:
        fields["trail"] = {"enabled": a(ins, 0, "0")}
    elif ins.opcode == 174:
        fields["focus_animation"] = {"source": "etama.anm", "script_expr": f"({a(ins, 0, '0')} + 48)"}


def apply_legacy_auto_bullet(obj: AutoBulletTimer, ins: Instruction) -> None:
    semantics = {105: "auto_fire_interval", 106: "auto_fire_interval_random_initial_delay", 107: "defer_attribute_fire"}
    obj.fields.update({"semantic": semantics.get(ins.opcode, f"auto_bullet_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode in {105, 106}:
        obj.fields["timer"] = {"interval": a(ins, 0, "1"), "initial_delay": "random_0_interval" if ins.opcode == 106 else "none", "fire_mode": "current_bullet_attributes"}
    else:
        obj.fields["timer"] = {"defer_attribute_fire": True}


def apply_legacy_boss_timer(obj: BossTimer, ins: Instruction) -> None:
    semantics = {
        132: "timer_set",
        133: "life_threshold_interrupt",
        134: "timer_threshold_interrupt",
        148: "visible_life_count",
        158: "life_bar_segment",
        173: "bomb_immunity_state",
        184: "boss_runtime_state",
    }
    obj.fields.update({"semantic": semantics.get(ins.opcode, f"boss_timer_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode == 132:
        obj.fields["timer"] = {"start": a(ins, 0, "0"), "direction": "up", "attack_timer_expr": "threshold - timer"}
    elif ins.opcode == 133:
        obj.fields["interrupt"] = {"trigger": "life_leq", "unknown": a(ins, 0, "0"), "life": a(ins, 1, "0"), "sub": a(ins, 2, "-1")}
    elif ins.opcode == 134:
        obj.fields["interrupt"] = {"trigger": "timer_geq", "time": a(ins, 0, "0"), "sub": a(ins, 1, "-1")}
    elif ins.opcode == 158:
        obj.fields["life_bar"] = {"slot": a(ins, 0, "0"), "life_min": a(ins, 1, "0"), "life_max": a(ins, 2, "0"), "color": a(ins, 3, "0")}


def apply_legacy_motion_modifier(obj: MotionModifier, ins: Instruction) -> None:
    semantics = {
        67: "random_direction_tween",
        70: "angular_velocity",
        71: "linear_acceleration",
        74: "circle_speed_change",
        178: "random_direction_tween_variant",
    }
    obj.fields.update({"semantic": semantics.get(ins.opcode, f"motion_modifier_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode in {67, 178}:
        obj.fields["motion"] = {"time": a(ins, 0, "0"), "mode": a(ins, 1, "0"), "speed": a(ins, 2, "0.0f"), "direction": "random_player_bounded", "variant": ins.opcode == 178}
    elif ins.opcode == 70:
        obj.fields["motion"] = {"angular_velocity": a(ins, 0, "0.0f")}
    elif ins.opcode == 71:
        obj.fields["motion"] = {"acceleration": a(ins, 0, "0.0f")}
    elif ins.opcode == 74:
        obj.fields["motion"] = {"time": a(ins, 0, "0"), "angular_velocity": a(ins, 1, "0.0f"), "radius_velocity": a(ins, 2, "0.0f"), "requires_circle_motion": True}


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
            append_ir_op(obj, program.game, ins)
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
            425: "moveBezier", 426: "moveBezierRel", 427: "moveReset",
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
        obj.fields["op_key"] = op_key_for_opcode(program.game, ins.opcode)
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
    elif program.game == "th12":
        animation = {258: "anmSelect", 259: "anmSetSprite", 262: "anmSetMain", 263: "anmPlay", 264: "anmPlayAbs"}
        enemy = {256: "enmCreate", 257: "enmCreateA", 260: "enmCreateM", 261: "enmCreateAM", 265: "enmCreateF", 266: "enmCreateAF", 267: "enmCreateMF", 268: "enmCreateAMF"}
        family = "th12"
    elif program.game in {"th10", "th11"}:
        animation = {258: "anmSelect", 259: "anmSetSprite", 262: "anmSetMain", 263: "anmPlay", 264: "anmPlayAbs"}
        enemy = {256: "enmCreate", 257: "enmCreateA", 260: "enmCreateM", 261: "enmCreateAM", 265: "enmCreateF", 266: "enmCreateAF", 267: "enmCreateMF", 268: "enmCreateAMF"}
        family = "th10_th11"
    elif program.game in {"th06", "th07", "th08"}:
        animation = {62: "anmPlayAttack"}
        enemy = {}
        family = "th08_legacy"
    else:
        return objects
    for ins in func.body:
        if ins.opcode in animation:
            obj = make_obj(AnimationOp, program, func, ins, family)
            obj.fields.update({"op": animation[ins.opcode], "op_key": op_key_for_opcode(program.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
            objects.append(obj)
        elif ins.opcode in enemy:
            obj = make_obj(EnemyOp, program, func, ins, family)
            obj.fields.update({"op": enemy[ins.opcode], "op_key": op_key_for_opcode(program.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
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
                append_ir_op(current, program.game, ins)
            current.fields.setdefault("ops", []).append({"op": boss_ops[ins.opcode], "op_key": op_key_for_opcode(program.game, ins.opcode), "opcode": ins.opcode, "args": ins.args, "line": ins.line_no})
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
