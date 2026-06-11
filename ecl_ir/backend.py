from __future__ import annotations

from .model import BulletEmitter

INT_SENTINEL = "-999999"
FLOAT_SENTINEL = "-999999.0f"


def v(value, default):
    if isinstance(value, dict):
        difficulty = value.get("difficulty", {})
        for key in ("LO", "L", "H", "N", "E"):
            if key in difficulty:
                return difficulty[key]
        return value.get("placeholder", default)
    return value if value not in (None, "") else default


def difficulty_comment(field: str, value) -> str | None:
    if not isinstance(value, dict) or "difficulty" not in value:
        return None
    parts = ", ".join(f"{key}={val}" for key, val in value["difficulty"].items())
    return f"// difficulty {field}: {parts}; lowered using {v(value, '')}"


def compile_bullet_emitter(emitter: BulletEmitter, target: str) -> str:
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return compile_th13plus(emitter)
    if target == "th12":
        return compile_th12(emitter)
    raise ValueError(f"unsupported target backend: {target}")


def compile_object(obj, target: str) -> str:
    kind = getattr(obj, "kind", None)
    if kind == "BulletEmitter":
        return compile_bullet_emitter(obj, target)
    if kind == "LaserEmitter":
        return compile_laser(obj, target)
    if kind == "Movement":
        return compile_movement(obj, target)
    if kind == "Animation":
        return compile_named_op(obj, target, ANIMATION_OPS)
    if kind == "Enemy":
        return compile_named_op(obj, target, ENEMY_OPS)
    if kind == "BossPattern":
        return compile_boss_pattern(obj, target)
    if kind == "Timeline":
        return compile_timeline(obj, target)
    return compile_raw_comment(obj, target)


ANIMATION_OPS = {
    "th12": {"anmSelect": 258, "anmSetSprite": 259, "anmSetMain": 262, "anmPlay": 263, "anmPlayAbs": 264},
    "th13plus": {"anmSelect": 302, "anmSetSprite": 303, "anmSetMain": 306, "anmPlay": 307, "anmPlayAbs": 308, "anmSwitch": 317, "anmReset": 318},
}

ENEMY_OPS = {
    "th12": {"enmCreate": 256, "enmCreateA": 257, "enmCreateM": 260, "enmCreateAM": 261, "enmCreateF": 265, "enmCreateAF": 266, "enmCreateMF": 267, "enmCreateAMF": 268},
    "th13plus": {"enmCreate": 300, "enmCreateA": 301, "enmCreateM": 304, "enmCreateAM": 305, "enmCreateF": 309, "enmCreateAF": 310, "enmCreateMF": 311, "enmCreateAMF": 312},
}

BOSS_OPS = {
    "th12": {"lifeSet": 411, "setBoss": 412, "timerReset": 413, "setInterrupt": 414, "setTimeout": 421, "spellEnd": 423, "setChapter": 424, "spell": 437, "spell2": 438, "spell3": 439},
    "th13plus": {"lifeSet": 511, "setBoss": 512, "timerReset": 513, "setInterrupt": 514, "setTimeout": 521, "spellEnd": 523, "setChapter": 524, "spell": 537, "spell2": 538, "spell3": 539},
}


def target_family(target: str) -> str:
    return "th12" if target == "th12" else "th13plus"


def compile_named_op(obj, target: str, table_by_family: dict[str, dict[str, int]]) -> str:
    family = target_family(target)
    semantic = obj.fields.get("op")
    opcode = table_by_family.get(family, {}).get(semantic)
    if opcode is None:
        return compile_raw_comment(obj, target) + f"\n// unsupported semantic op for {target}: {semantic}"
    args = obj.fields.get("args", [])
    return f"// {obj.kind} lowering {obj.family} -> {target}: {semantic}; semantic verification required\nins_{opcode}({', '.join(args)});"


def compile_boss_pattern(obj, target: str) -> str:
    family = target_family(target)
    table = BOSS_OPS[family]
    lines = [f"// BossPattern lowering {obj.family} -> {target}; semantic verification required"]
    for item in obj.fields.get("ops", []):
        semantic = item.get("op")
        opcode = table.get(semantic)
        if opcode is None:
            lines.append(f"// unsupported boss op {semantic}: ins_{item.get('opcode')}({', '.join(item.get('args', []))});")
        else:
            lines.append(f"ins_{opcode}({', '.join(item.get('args', []))});")
    return "\n".join(lines)


def compile_timeline(obj, target: str) -> str:
    lines = [f"// Timeline lowering {obj.family} -> {target}; structure-preserving draft"]
    lines.append("// control-flow, async scheduling, and expression semantics require target-game verification")
    for event in obj.fields.get("statements", []):
        kind = event.get("kind")
        text = event.get("text") or ""
        if kind == "instruction":
            lines.append(f"// body instruction preserved in object-specific lowerings too: {text}")
        elif kind in {"label", "time", "goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
            lines.append(text + (";" if kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"} and not str(text).endswith(";") else ""))
        elif text:
            lines.append(f"// raw: {text}")
    loops = obj.fields.get("loops", [])
    if loops:
        lines.append("// detected loops:")
        for loop in loops:
            lines.append(f"// - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return "\n".join(lines)


def compile_raw_comment(obj, target: str) -> str:
    lines = [f"// no safe lowering implemented for {obj.kind} family={obj.family} to {target}"]
    for ins in getattr(obj, "raw", []):
        lines.append(f"// {ins.raw.strip()}")
    return "\n".join(lines)


def compile_laser(obj, target: str) -> str:
    if target not in {"th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported laser target: {target}")
    to_th13 = target != "th12"
    offset = 100 if to_th13 and obj.family == "th12" else -100 if target == "th12" and obj.family == "th13plus" else 0
    lines = [f"// laser lowering {obj.family} -> {target}; semantic verification required"]
    for ins in obj.raw:
        opcode = ins.opcode + offset
        if target == "th12" and opcode < 600:
            lines.append(f"// unsupported laser opcode for th12: {ins.raw.strip()}")
        else:
            lines.append(f"ins_{opcode}({', '.join(ins.args)});")
    return "\n".join(lines)


def compile_movement(obj, target: str) -> str:
    if target not in {"th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported movement target: {target}")
    movement = obj.fields.get("op")
    args = obj.fields.get("args", [])
    th13 = {
        "movePos": 400, "movePosTime": 401, "movePosRel": 402, "movePosRelTime": 403,
        "moveVel": 404, "moveVelTime": 405, "moveVelRel": 406, "moveVelRelTime": 407,
        "moveEllipse": 420, "moveEllipseTime": 421, "moveBezier": 425, "moveBezierRel": 426, "moveReset": 427,
    }
    th12 = {
        "movePos": 300, "movePosTime": 301, "movePosRel": 302, "movePosRelTime": 303,
        "moveVel": 304, "moveVelTime": 305, "moveVelRel": 306, "moveVelRelTime": 307,
        "moveEllipse": 320, "moveEllipseTime": 321, "moveBezier": 325, "moveBezierRel": 326, "moveReset": 327,
    }
    table = th12 if target == "th12" else th13
    opcode = table.get(movement)
    if opcode is None:
        return compile_raw_comment(obj, target) + f"\n// unsupported movement semantic: {movement}"
    return f"// movement lowering {obj.family} -> {target}: {movement}\nins_{opcode}({', '.join(args)});"


def compile_th13plus(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style = v(e.appearance.get("style"), "0")
    color = v(e.appearance.get("color"), "0")
    ways = v(e.count.get("ways"), "1")
    layers = v(e.count.get("layers"), "1")
    angle = v(e.aim.get("base_angle"), "0.0f")
    angle_step = v(e.aim.get("angle_step"), "0.0f")
    speed = v(e.speed.get("first"), "1.0f")
    speed_step = v(e.speed.get("step"), e.speed.get("last_or_step", "0.0f"))
    lines = [
        f"ins_600({emitter_id});",
        f"ins_607({emitter_id}, {aim_raw});",
        f"ins_602({emitter_id}, {style}, {color});",
        f"ins_606({emitter_id}, {ways}, {layers});",
        f"ins_604({emitter_id}, {angle}, {angle_step});",
        f"ins_605({emitter_id}, {speed}, {speed_step});",
    ]
    for field, value in (("speed.first", e.speed.get("first")), ("count.ways", e.count.get("ways"))):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment)
    for transform in e.transforms:
        if transform.raw_opcode in {609, 610, 611, 612} and transform.raw_args:
            lines.append(f"ins_{transform.raw_opcode}({', '.join(transform.raw_args)});")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    lines.append(f"ins_601({emitter_id});")
    return "\n".join(lines)


def compile_th12(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style = v(e.appearance.get("style"), "0")
    color = v(e.appearance.get("color"), "0")
    ways = v(e.count.get("ways"), "1")
    layers = v(e.count.get("layers"), "1")
    angle = v(e.aim.get("base_angle"), "0.0f")
    angle_step = v(e.aim.get("angle_step"), "0.0f")
    speed = v(e.speed.get("first"), "1.0f")
    speed_step = v(e.speed.get("step"), e.speed.get("last_or_step", "0.0f"))
    lines = [
        f"ins_500({emitter_id});",
        f"ins_507({emitter_id}, {aim_raw});",
        f"ins_502({emitter_id}, {style}, {color});",
        f"ins_506({emitter_id}, {ways}, {layers});",
        f"ins_504({emitter_id}, {angle}, {angle_step});",
        f"ins_505({emitter_id}, {speed}, {speed_step});",
    ]
    for field, value in (("speed.first", e.speed.get("first")), ("count.ways", e.count.get("ways"))):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment)
    for transform in e.transforms:
        if transform.raw_opcode == 509 and len(transform.raw_args) == 8:
            lines.append(f"ins_509({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 510 and len(transform.raw_args) == 0:
            lines.append("ins_510();")
        elif transform.raw_opcode == 511 and len(transform.raw_args) == 2:
            lines.append(f"ins_511({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 512 and len(transform.raw_args) == 1:
            lines.append(f"ins_512({', '.join(transform.raw_args)});")
        elif transform.raw_opcode in {609, 610, 611, 612}:
            lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {510, 511, 512}:
            lines.append(f"// unsupported th12 transform opcode/arity in generated context; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    lines.append(f"ins_501({emitter_id});")
    return "\n".join(lines)


def mode_raw(mode: str | None, default: str = "1") -> str:
    return {
        "aimed_fan": "0",
        "fan": "1",
        "aimed_ring": "2",
        "ring": "3",
        "offset_aimed_ring": "4",
        "offset_ring": "5",
        "random_angle": "6",
        "random_speed": "7",
        "random_angle_speed": "8",
    }.get(mode or "", default)


def convert_th13_transform_to_th12(opcode: int, args: list[str]) -> tuple[int, list[str]] | None:
    mapping = {609: 509, 610: 510, 611: 511, 612: 512}
    if opcode not in mapping:
        return None
    return mapping[opcode], args
