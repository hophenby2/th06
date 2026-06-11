from __future__ import annotations

from .model import BulletEmitter

INT_SENTINEL = "-999999"
FLOAT_SENTINEL = "-999999.0f"


TARGET_DIFFICULTY = "N"
DIFFICULTY_FALLBACK_ORDER = ("N", "H", "E", "LO", "L")


def choose_difficulty(difficulty: dict[str, str], default: str = "") -> tuple[str, str]:
    normalized = normalize_difficulty(difficulty)
    for key in DIFFICULTY_FALLBACK_ORDER:
        if key in normalized:
            return normalized[key], key
    return default, "placeholder"


def v(value, default):
    if isinstance(value, dict):
        difficulty = value.get("difficulty", {})
        chosen, _ = choose_difficulty(difficulty, value.get("placeholder", default))
        return chosen
    return value if value not in (None, "") else default


def difficulty_comment(field: str, value) -> str | None:
    if not isinstance(value, dict) or "difficulty" not in value:
        return None
    parts = ", ".join(f"{key}={val}" for key, val in value["difficulty"].items())
    _, rank = choose_difficulty(value["difficulty"], value.get("placeholder", ""))
    return f"// difficulty {field}: {parts}; lowered using {rank}={v(value, '')}"




def normalize_difficulty(difficulty: dict[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in difficulty.items():
        if key == "*":
            continue
        for rank in key:
            if rank in {"E", "N", "H", "L"}:
                normalized[rank] = value
            elif rank == "O":
                normalized.setdefault("L", value)
    return normalized


def first_difficulty_group(literals: object) -> dict[str, str]:
    if isinstance(literals, dict):
        return literals
    if isinstance(literals, list):
        for item in literals:
            if isinstance(item, dict) and item:
                return item
    return {}


def difficulty_rank_order(difficulty: dict[str, str]) -> list[str]:
    normalized = normalize_difficulty(difficulty)
    return [rank for rank in ("E", "N", "H", "L") if rank in normalized]


def normalized_rank_marker(marker: str | None, target: str = "") -> str | None:
    if not marker:
        return None
    marker = str(marker).strip()
    if not marker:
        return None
    if marker == "*":
        return "*"
    out: list[str] = []
    for ch in marker:
        mapped = "L" if ch == "O" else ch
        if mapped in "ENHL":
            if mapped not in out:
                out.append(mapped)
        elif mapped in "01234567X":
            out.append(mapped)
    return "".join(out) or None


def wrap_ranked_lines(lines: list[str], difficulty: str | None, target: str = "") -> list[str]:
    marker = normalized_rank_marker(difficulty, target)
    if not marker:
        return lines
    if marker == "*":
        return ["!*", *lines]
    return [f"!{marker}", *lines, "!*"]


def emit_ranked_instruction(opcode: int, args: list[str], difficulty: dict[str, str], replace_index: int) -> list[str]:
    lines: list[str] = []
    normalized = normalize_difficulty(difficulty)
    for rank in difficulty_rank_order(difficulty):
        ranked_args = list(args)
        ranked_args[replace_index] = normalized[rank]
        lines.append(f"!{rank}")
        lines.append(f"ins_{opcode}({', '.join(ranked_args)});")
    if lines:
        lines.append("!*")
    return lines


def maybe_difficulty_table(value) -> dict[str, str] | None:
    if isinstance(value, dict) and isinstance(value.get("difficulty"), dict):
        return value["difficulty"]
    return None


def resolved_arg(value, default: str) -> str:
    return v(value, default)


def emit_instruction_with_ranked_args(opcode: int, args: list[object], defaults: list[str]) -> list[str]:
    if not any(maybe_difficulty_table(value) for value in args):
        return [f"ins_{opcode}({', '.join(str(resolved_arg(value, defaults[idx])) for idx, value in enumerate(args))});"]
    lines: list[str] = []
    for rank in ("E", "N", "H", "L"):
        ranked_args: list[str] = []
        has_rank = False
        for idx, value in enumerate(args):
            difficulty = maybe_difficulty_table(value)
            if difficulty:
                normalized = normalize_difficulty(difficulty)
                ranked_args.append(str(normalized.get(rank, resolved_arg(value, defaults[idx]))))
                has_rank = has_rank or rank in normalized
            else:
                ranked_args.append(str(resolved_arg(value, defaults[idx])))
        if has_rank:
            lines.append(f"!{rank}")
            lines.append(f"ins_{opcode}({', '.join(ranked_args)});")
    if lines:
        lines.append("!*")
    return lines


def rank_values(value, fallback: str) -> list[str] | None:
    difficulty = maybe_difficulty_table(value)
    if not difficulty:
        return None
    normalized = normalize_difficulty(difficulty)
    return [normalized.get(rank, fallback) for rank in ("E", "N", "H", "L")]


def th12_difficulty_speed_args(emitter_id: str, speed_value, fallback_speed: str, speed_step_value, fallback_step: str) -> list[str] | None:
    first = rank_values(speed_value, fallback_speed)
    step = rank_values(speed_step_value, fallback_step)
    if not first and not step:
        return None
    first = first or [fallback_speed for _ in range(4)]
    step = step or [fallback_step for _ in range(4)]
    return [emitter_id, *first, *step]


def th12_difficulty_count_args(emitter_id: str, ways_value, fallback_ways: str, layers_value, fallback_layers: str) -> list[str] | None:
    ways = rank_values(ways_value, fallback_ways)
    layer_values = rank_values(layers_value, fallback_layers)
    if not ways and not layer_values:
        return None
    ways = ways or [fallback_ways for _ in range(4)]
    layer_values = layer_values or [fallback_layers for _ in range(4)]
    return [emitter_id, *ways, *layer_values]

def compile_bullet_emitter(emitter: BulletEmitter, target: str) -> str:
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return compile_th13plus(emitter)
    if target == "th12":
        return compile_th12(emitter)
    raise ValueError(f"unsupported target backend: {target}")


def compile_object(obj, target: str) -> str:
    kind = getattr(obj, "kind", None)
    if kind == "BulletEmitter":
        compiled = compile_bullet_emitter(obj, target)
    elif kind == "LaserEmitter":
        compiled = compile_laser(obj, target)
    elif kind == "Movement":
        compiled = compile_movement(obj, target)
    elif kind == "Animation":
        compiled = compile_named_op(obj, target, ANIMATION_OPS)
    elif kind == "Enemy":
        compiled = compile_named_op(obj, target, ENEMY_OPS)
    elif kind == "BossPattern":
        compiled = compile_boss_pattern(obj, target)
    elif kind == "Timeline":
        compiled = compile_timeline(obj, target)
    else:
        compiled = compile_raw_comment(obj, target)
    difficulty = object_difficulty(obj)
    return "\n".join(wrap_ranked_lines(compiled.splitlines(), difficulty, target))


def object_difficulty(obj) -> str | None:
    raw = getattr(obj, "raw", []) or []
    difficulties = [getattr(ins, "difficulty", None) for ins in raw if getattr(ins, "difficulty", None)]
    if difficulties and all(item == difficulties[0] for item in difficulties):
        return difficulties[0]
    fields = getattr(obj, "fields", {}) or {}
    difficulty = fields.get("difficulty")
    return str(difficulty) if difficulty else None


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
    args = remap_named_args(obj, target, semantic, obj.fields.get("args", []))
    return f"// {obj.kind} lowering {obj.family} -> {target}: {semantic}; semantic verification required\nins_{opcode}({', '.join(args)});"


def remap_named_args(obj, target: str, semantic: str, args: list[str]) -> list[str]:
    args = list(args)
    if target == "th12" and getattr(obj, "family", "") == "th13plus" and semantic == "anmSelect" and args == ["2"]:
        # TH15 st01 enemy sprites live in st01enm.anm at ANM index 2.
        # TH12 stage01 has no st01enm.anm; index 2 points at stage/boss ANM, so use enemy.anm.
        return ["1"]
    if target == "th12" and getattr(obj, "family", "") == "th13plus" and semantic in {"anmSetMain", "anmSetSprite"}:
        # Keep script IDs for now; the important crash/visual fix is the ANM file index.
        # A later sprite table can map TH15 st01enm script IDs to closer TH12 enemy.anm scripts.
        return args
    return args


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
    aim_raw_value = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style_value = e.appearance.get("style")
    color_value = e.appearance.get("color")
    ways_value = e.count.get("ways")
    layers_value = e.count.get("layers")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    speed_value = e.speed.get("first")
    speed_step_value = e.speed.get("step")
    lines = [f"ins_600({emitter_id});"]
    lines.extend(emit_instruction_with_ranked_args(607, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(602, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    lines.extend(emit_instruction_with_ranked_args(606, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(604, [emitter_id, angle_value, angle_step_value], ["0", "0.0f", "0.0f"]))
    lines.extend(emit_instruction_with_ranked_args(605, [emitter_id, speed_value, speed_step_value], ["0", "1.0f", e.speed.get("last_or_step", "0.0f")]))
    for field, value in (("speed.first", e.speed.get("first")), ("count.ways", e.count.get("ways"))):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment)
    for transform in e.transforms:
        if transform.raw_opcode in {609, 610, 611, 612} and transform.raw_args:
            lines.append(f"ins_{transform.raw_opcode}({', '.join(transform.raw_args)});")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    return "\n".join(lines)


def compile_th12(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style_value = e.appearance.get("style")
    color_value = e.appearance.get("color")
    ways_value = e.count.get("ways")
    speed_value = e.speed.get("first")
    ways = v(ways_value, "1")
    layers_value = e.count.get("layers")
    layers = v(layers_value, "1")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    angle = v(angle_value, "0.0f")
    angle_step = v(angle_step_value, "0.0f")
    speed = v(speed_value, "1.0f")
    speed_step_value = e.speed.get("step")
    speed_step = v(speed_step_value, e.speed.get("last_or_step", "0.0f"))
    lines = [f"ins_500({emitter_id});"]
    lines.extend(emit_instruction_with_ranked_args(507, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(502, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    count_args = th12_difficulty_count_args(emitter_id, ways_value, ways, layers_value, layers)
    if count_args:
        lines.append(f"ins_522({', '.join(count_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(506, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(504, [emitter_id, angle_value, angle_step_value], ["0", "0.0f", "0.0f"]))
    speed_args = th12_difficulty_speed_args(emitter_id, speed_value, speed, speed_step_value, speed_step)
    if speed_args:
        lines.append(f"ins_521({', '.join(speed_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(505, [emitter_id, speed_value, speed_step_value], ["0", "1.0f", "0.0f"]))
    for field, value in (("speed.first", speed_value), ("speed.step", speed_step_value), ("count.ways", ways_value), ("count.layers", layers_value)):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment.replace("lowered using", "preserved as TH12 difficulty table; default preview"))
    for transform in e.transforms:
        if transform.raw_opcode == 509 and len(transform.raw_args) == 8:
            lines.append(f"ins_509({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 510 and len(transform.raw_args) == 0:
            lines.append("ins_510();")
        elif transform.raw_opcode == 511 and len(transform.raw_args) == 2:
            lines.append(f"ins_511({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 512 and len(transform.raw_args) == 1:
            lines.append(f"ins_512({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 624 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(521, transform.raw_args, [emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
        elif transform.raw_opcode == 625 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(522, transform.raw_args, [emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
        elif transform.raw_opcode in {609, 610, 611, 612}:
            lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {510, 511, 512}:
            lines.append(f"// unsupported th12 transform opcode/arity in generated context; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
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
