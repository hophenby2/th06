from __future__ import annotations

from copy import deepcopy
from collections.abc import Iterable

from .model import BulletEmitter, BulletTransform, Function, Instruction, Program
from .op_ir import op_event
from .semantics import bullet_shape_semantic, spread_semantic
from .transform_ir import annotate_th12_to_th13plus_transforms

TH13PLUS_GAMES = {"th13", "th14", "th15", "th16", "th17", "th18"}
TH12_GAMES = {"th12"}
TH08_GAMES = {"th06", "th07", "th08"}
TH10_GAMES = {"th10", "th11"}


def arg(args: list[str], index: int, default: str = "") -> str:
    return args[index] if index < len(args) else default


def append_emitter_op(emitter: BulletEmitter, ins: Instruction) -> None:
    emitter.semantics.setdefault("ir_ops", []).append(op_event(emitter.game, ins.opcode, ins.args, ins.line_no, ins.difficulty))


def difficulty_literal_group(value: str, literals: object) -> dict[str, str]:
    if isinstance(literals, dict):
        return literals
    if not isinstance(literals, list) or not literals:
        return {}
    index = 1 if value in {"[-2]", "[-2.0f]"} else 0
    if index < len(literals) and isinstance(literals[index], dict):
        return literals[index]
    if isinstance(literals[-1], dict):
        return literals[-1]
    return {}


def with_difficulty(value: str, literals: object) -> object:
    if value in {"[-1]", "[-1.0f]", "[-2]", "[-2.0f]"}:
        group = difficulty_literal_group(value, literals)
        if group:
            return {"placeholder": value, "difficulty": group}
    return value


def apply_difficulty_args(args: list[str], literals: object) -> list[object]:
    return [with_difficulty(arg, literals) for arg in args]


def difficulty_table_value(args: list[str], start: int, default: str) -> object:
    values = {
        "E": arg(args, start, default),
        "N": arg(args, start + 1, default),
        "H": arg(args, start + 2, default),
        "L": arg(args, start + 3, default),
    }
    return {"placeholder": values["N"], "difficulty": values}


def with_rank(value: str, difficulty: str | None) -> object:
    if difficulty and difficulty != "*":
        return {"placeholder": value, "difficulty": {difficulty: value}}
    return value


def merge_ranked_value(current: object, value: object, difficulty: str | None) -> object:
    if not difficulty or difficulty == "*":
        if isinstance(value, dict) and isinstance(value.get("difficulty"), dict) and current not in (None, ""):
            merged = dict(value)
            if isinstance(current, dict) and isinstance(current.get("difficulty"), dict):
                difficulty_values = dict(current["difficulty"])
                difficulty_values.update(value["difficulty"])
                merged["difficulty"] = difficulty_values
                merged["placeholder"] = current.get("placeholder", value.get("placeholder"))
            else:
                merged["placeholder"] = current
            return merged
        return value
    if isinstance(current, dict) and isinstance(current.get("difficulty"), dict):
        merged = dict(current["difficulty"])
        merged[difficulty] = value
        return {"placeholder": current.get("placeholder", value), "difficulty": merged}
    merged = {}
    if current not in (None, ""):
        # Keep the previous non-ranked value as fallback preview only.
        if isinstance(current, dict):
            merged.update(current.get("difficulty", {}))
            placeholder = current.get("placeholder", value)
        else:
            placeholder = current
    else:
        placeholder = value
    merged[difficulty] = value
    return {"placeholder": placeholder, "difficulty": merged}


def set_ranked_field(container: dict, key: str, value: object, difficulty: str | None) -> None:
    container[key] = merge_ranked_value(container.get(key), value, difficulty)


def resolved_plain(value: object) -> str:
    if isinstance(value, dict):
        return str(value.get("placeholder", ""))
    return str(value)


def update_spread_semantics(emitter: BulletEmitter, style: object, family: str) -> None:
    game = emitter.game if family in {"th13plus", "th12"} else family
    emitter.semantics.setdefault("bullet", {}).setdefault("spread", {}).update(spread_semantic(game, style))


def update_shape_semantics(emitter: BulletEmitter, shape: object) -> None:
    emitter.semantics.setdefault("bullet", {})["shape"] = bullet_shape_semantic(emitter.game, shape)


def set_origin_base(emitter: BulletEmitter, base: dict[str, object]) -> None:
    origin = emitter.origin or {}
    distance = origin.get("distance")
    if distance is not None and base.get("mode") not in {"distance", "polar"}:
        base = dict(base)
        base["distance"] = distance
    emitter.origin = base


def set_origin_distance(emitter: BulletEmitter, distance: object) -> None:
    origin = dict(emitter.origin or {})
    if origin and origin.get("mode") != "distance":
        origin["distance"] = distance
    else:
        origin = {"mode": "distance", "distance": distance}
    emitter.origin = origin


def apply_th13plus(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 607:
        style = with_difficulty(arg(args, 1, "0"), ins.difficulty_literals)
        set_ranked_field(emitter.aim, "mode_raw", style, ins.difficulty)
        emitter.aim.setdefault("mode", aim_mode_name(arg(args, 1, "0")))
        update_spread_semantics(emitter, style, "th13plus")
    elif op == 602:
        shape = with_difficulty(arg(args, 1), ins.difficulty_literals)
        set_ranked_field(emitter.appearance, "style", shape, ins.difficulty)
        set_ranked_field(emitter.appearance, "color", with_difficulty(arg(args, 2), ins.difficulty_literals), ins.difficulty)
        update_shape_semantics(emitter, shape)
    elif op == 603:
        set_origin_base(emitter, {"mode": "offset", "x": arg(args, 1, "0"), "y": arg(args, 2, "0")})
    elif op == 604:
        set_ranked_field(emitter.aim, "base_angle", with_difficulty(arg(args, 1, "0"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.aim, "angle_step", with_difficulty(arg(args, 2, "0"), ins.difficulty_literals), ins.difficulty)
    elif op == 605:
        set_ranked_field(emitter.speed, "first", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.speed, "step", with_difficulty(arg(args, 2, "0"), ins.difficulty_literals), ins.difficulty)
    elif op == 606:
        set_ranked_field(emitter.count, "ways", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.count, "layers", with_difficulty(arg(args, 2, "1"), ins.difficulty_literals), ins.difficulty)
    elif op == 608:
        emitter.sound["id"] = arg(args, 1)
        emitter.sound["mode"] = arg(args, 2)
    elif op == 626:
        set_origin_base(emitter, {"mode": "polar", "angle": arg(args, 1, "0.0f"), "radius": arg(args, 2, "0.0f")})
    elif op == 627:
        set_origin_distance(emitter, arg(args, 1, "0.0f"))
    elif op == 628:
        set_origin_base(emitter, {"mode": "absolute", "x": arg(args, 1, "0.0f"), "y": arg(args, 2, "0.0f")})
    elif op in {609, 610, 611, 612}:
        emitter.transforms.append(
            BulletTransform(
                index=arg(args, 1, "0"),
                channel="0",
                action_type="etEx",
                raw_opcode=op,
                raw_args=args[:],
                difficulty=ins.difficulty,
            )
        )
    elif op in {617, 618, 619}:
        emitter.speed.setdefault("difficulty_raw", []).append({"opcode": op, "args": args[:], "difficulty": ins.difficulty})
    elif op in {620, 621, 622}:
        emitter.count.setdefault("difficulty_raw", []).append({"opcode": op, "args": args[:], "difficulty": ins.difficulty})
    elif op == 624:
        set_ranked_field(emitter.speed, "first", difficulty_table_value(args, 1, "1.0f"), ins.difficulty)
        set_ranked_field(emitter.speed, "step", difficulty_table_value(args, 5, "0.0f"), ins.difficulty)
    elif op == 625:
        set_ranked_field(emitter.count, "ways", difficulty_table_value(args, 1, "1"), ins.difficulty)
        set_ranked_field(emitter.count, "layers", difficulty_table_value(args, 5, "1"), ins.difficulty)
    elif op == 601:
        emitter.fire_lines.append(ins.line_no)


def apply_th12(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 507:
        style = with_difficulty(arg(args, 1, "0"), ins.difficulty_literals)
        set_ranked_field(emitter.aim, "mode_raw", style, ins.difficulty)
        emitter.aim.setdefault("mode", aim_mode_name(arg(args, 1, "0")))
        update_spread_semantics(emitter, style, "th12")
    elif op == 502:
        shape = with_difficulty(arg(args, 1), ins.difficulty_literals)
        set_ranked_field(emitter.appearance, "style", shape, ins.difficulty)
        set_ranked_field(emitter.appearance, "color", with_difficulty(arg(args, 2), ins.difficulty_literals), ins.difficulty)
        update_shape_semantics(emitter, shape)
    elif op == 503:
        set_origin_base(emitter, {"mode": "offset", "x": arg(args, 1, "0"), "y": arg(args, 2, "0")})
    elif op == 504:
        set_ranked_field(emitter.aim, "base_angle", with_difficulty(arg(args, 1, "0"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.aim, "angle_step", with_difficulty(arg(args, 2, "0"), ins.difficulty_literals), ins.difficulty)
    elif op == 505:
        set_ranked_field(emitter.speed, "first", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.speed, "step", with_difficulty(arg(args, 2, "0"), ins.difficulty_literals), ins.difficulty)
    elif op == 506:
        set_ranked_field(emitter.count, "ways", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.count, "layers", with_difficulty(arg(args, 2, "1"), ins.difficulty_literals), ins.difficulty)
    elif op == 508:
        emitter.sound["id"] = arg(args, 1)
        emitter.sound["mode"] = arg(args, 2)
    elif op == 523:
        set_origin_base(emitter, {"mode": "polar", "angle": arg(args, 1, "0.0f"), "radius": arg(args, 2, "0.0f")})
    elif op == 524:
        set_origin_distance(emitter, arg(args, 1, "0.0f"))
    elif op == 525:
        set_origin_base(emitter, {"mode": "absolute", "x": arg(args, 1, "0.0f"), "y": arg(args, 2, "0.0f")})
    elif op in {509, 510, 511, 512, 521, 522}:
        emitter.transforms.append(BulletTransform(index=arg(args, 1, "0"), action_type="etEx", raw_opcode=op, raw_args=args[:], difficulty=ins.difficulty))
    elif op == 501:
        emitter.fire_lines.append(ins.line_no)


def annotate_definition_prefix(emitter: BulletEmitter, apply_instruction) -> None:
    prefix = BulletEmitter(
        game=emitter.game,
        function=emitter.function,
        source_line=emitter.source_line,
        id=emitter.id,
        family=emitter.family,
    )
    prefix.origin = {"mode": "enemy", "x": "0", "y": "0"}
    previous_line: int | None = None
    for ins in emitter.raw:
        if previous_line is not None and ins.line_no != previous_line + 1:
            break
        prefix.raw.append(ins)
        append_emitter_op(prefix, ins)
        apply_instruction(prefix, ins)
        previous_line = ins.line_no
        if ins.opcode in {401, 501, 601}:
            break
    emitter.semantics["definition_state"] = {
        "origin": deepcopy(prefix.origin),
        "appearance": deepcopy(prefix.appearance),
        "aim": deepcopy(prefix.aim),
        "count": deepcopy(prefix.count),
        "speed": deepcopy(prefix.speed),
        "sound": deepcopy(prefix.sound),
        "flags": deepcopy(prefix.flags),
        "semantics": deepcopy(prefix.semantics),
        "transforms": [deepcopy(transform.__dict__) for transform in prefix.transforms],
        "raw_lines": [ins.line_no for ins in prefix.raw],
    }
    emitter.semantics["definition_state"]["transforms"] = [
        deepcopy(transform.__dict__)
        for transform in annotate_th12_to_th13plus_transforms(prefix.transforms, emitter.game, "th15")
    ]


def aim_mode_name(raw: str) -> str:
    return {
        "0": "aimed_fan",
        "1": "fan",
        "2": "aimed_ring",
        "3": "ring",
        "4": "offset_aimed_ring",
        "5": "offset_ring",
        "6": "random_angle",
        "7": "random_speed",
        "8": "random_angle_speed",
    }.get(raw, "custom")


def macro_mode_for_th08(opcode: int) -> str:
    return {
        96: "aimed_fan",
        97: "fan",
        98: "aimed_ring",
        99: "ring",
        100: "offset_aimed_ring",
        101: "offset_ring",
        102: "random_angle",
        103: "random_speed",
        104: "random_angle_speed",
    }.get(opcode, "custom")


def lift_th13plus_function(game: str, func: Function) -> list[BulletEmitter]:
    emitters: list[BulletEmitter] = []
    active: dict[str, BulletEmitter] = {}
    for ins in func.body:
        if ins.opcode == 600:
            emitter_id = arg(ins.args, 0, "0")
            emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id=emitter_id, family="th13plus")
            emitter.origin = {"mode": "enemy", "x": "0", "y": "0"}
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            active[emitter_id] = emitter
            emitters.append(emitter)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if emitter and ins.opcode in {601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 617, 618, 619, 620, 621, 622, 624, 625, 626, 627, 628}:
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            apply_th13plus(emitter, ins)
    return emitters


def lift_th12_function(game: str, func: Function) -> list[BulletEmitter]:
    emitters: list[BulletEmitter] = []
    active: dict[str, BulletEmitter] = {}
    for ins in func.body:
        if ins.opcode == 500:
            emitter_id = arg(ins.args, 0, "0")
            emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id=emitter_id, family="th12")
            emitter.origin = {"mode": "enemy", "x": "0", "y": "0"}
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            active[emitter_id] = emitter
            emitters.append(emitter)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if emitter and ins.opcode in {501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 517, 518, 519, 520, 521, 522, 523, 524, 525}:
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            apply_th12(emitter, ins)
    for emitter in emitters:
        annotate_definition_prefix(emitter, apply_th12)
        emitter.transforms = annotate_th12_to_th13plus_transforms(emitter.transforms, game, "th15")
    return emitters


def lift_th08_function(game: str, func: Function) -> list[BulletEmitter]:
    emitters: list[BulletEmitter] = []
    pending_transforms: list[BulletTransform] = []
    for ins in func.body:
        if ins.opcode == 111:
            pending_transforms.append(BulletTransform(index=arg(ins.args, 0, "0"), channel=arg(ins.args, 2, "0"), action_type="th08Transform", raw_opcode=111, raw_args=ins.args[:], difficulty=ins.difficulty))
        elif 96 <= ins.opcode <= 104:
            emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id="0", family="th08_macro")
            emitter.appearance = {"style": arg(ins.args, 0), "color": arg(ins.args, 1)}
            emitter.aim = {"mode": macro_mode_for_th08(ins.opcode), "base_angle": arg(ins.args, 6, "0"), "angle_step": arg(ins.args, 7, "0")}
            emitter.count = {"ways": arg(ins.args, 2, "1"), "layers": arg(ins.args, 3, "1")}
            emitter.speed = {"first": arg(ins.args, 4, "1"), "last_or_step": arg(ins.args, 5, "0")}
            emitter.flags = {"raw": arg(ins.args, 8, "0")}
            emitter.transforms = pending_transforms
            emitter.fire_lines = [ins.line_no]
            emitter.raw = [*[], ins]
            append_emitter_op(emitter, ins)
            emitters.append(emitter)
            pending_transforms = []
    return emitters


def lift_program(program: Program) -> list[BulletEmitter]:
    emitters: list[BulletEmitter] = []
    for func in program.functions:
        if program.game in TH13PLUS_GAMES:
            emitters.extend(lift_th13plus_function(program.game, func))
        elif program.game in TH12_GAMES:
            emitters.extend(lift_th12_function(program.game, func))
        elif program.game in TH08_GAMES:
            emitters.extend(lift_th08_function(program.game, func))
        elif program.game in TH10_GAMES:
            emitters.extend(lift_th10_function(program.game, func))
    return emitters


def lift_th10_function(game: str, func: Function) -> list[BulletEmitter]:
    emitters: list[BulletEmitter] = []
    active: dict[str, BulletEmitter] = {}
    for ins in func.body:
        if ins.opcode in {400, 401}:
            emitter_id = arg(ins.args, 0, "0")
            emitter = active.get(emitter_id)
            if emitter is None or emitter.fire_lines:
                emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id=emitter_id, family="th10_slot")
                emitter.origin = {"mode": "enemy", "x": "0", "y": "0"}
                active[emitter_id] = emitter
                emitters.append(emitter)
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            if ins.opcode == 401:
                emitter.fire_lines.append(ins.line_no)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if not emitter:
            if ins.opcode == 403:
                emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id=emitter_id, family="th10_slot")
                emitter.origin = {"mode": "enemy", "x": "0", "y": "0"}
                active[emitter_id] = emitter
                emitters.append(emitter)
            else:
                continue
        elif emitter.fire_lines and ins.opcode in {402, 403, 404, 405, 406, 407, 408, 409, 410, 411}:
            previous = emitter
            emitter = BulletEmitter(game=game, function=func.name, source_line=ins.line_no, id=emitter_id, family="th10_slot")
            emitter.origin = deepcopy(previous.origin)
            emitter.appearance = deepcopy(previous.appearance)
            emitter.aim = deepcopy(previous.aim)
            emitter.count = deepcopy(previous.count)
            emitter.speed = deepcopy(previous.speed)
            emitter.sound = deepcopy(previous.sound)
            emitter.flags = deepcopy(previous.flags)
            emitter.semantics = deepcopy(previous.semantics)
            emitter.transforms = deepcopy(previous.transforms)
            active[emitter_id] = emitter
            emitters.append(emitter)
        if ins.opcode in {402, 403, 404, 405, 406, 407, 408, 409, 410, 411}:
            emitter.raw.append(ins)
            append_emitter_op(emitter, ins)
            apply_th10(emitter, ins)
    return emitters


def apply_th10(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 402:
        shape = with_difficulty(arg(args, 1), ins.difficulty_literals)
        set_ranked_field(emitter.appearance, "style", shape, ins.difficulty)
        set_ranked_field(emitter.appearance, "color", arg(args, 2), ins.difficulty)
        update_shape_semantics(emitter, shape)
    elif op == 403:
        set_origin_base(emitter, {"mode": "offset", "x": arg(args, 1, "0.0f"), "y": arg(args, 2, "0.0f")})
    elif op == 404:
        set_ranked_field(emitter.aim, "base_angle", arg(args, 1, "0"), ins.difficulty)
        set_ranked_field(emitter.aim, "angle_step", arg(args, 2, "0"), ins.difficulty)
    elif op == 405:
        set_ranked_field(emitter.speed, "first", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.speed, "step", arg(args, 2, "0"), ins.difficulty)
    elif op == 406:
        set_ranked_field(emitter.count, "ways", with_difficulty(arg(args, 1, "1"), ins.difficulty_literals), ins.difficulty)
        set_ranked_field(emitter.count, "layers", arg(args, 2, "1"), ins.difficulty)
    elif op == 407:
        style = with_difficulty(arg(args, 1, "0"), ins.difficulty_literals)
        set_ranked_field(emitter.aim, "mode_raw", style, ins.difficulty)
        emitter.aim["mode"] = aim_mode_name(arg(args, 1, "0"))
        update_spread_semantics(emitter, style, "th10")
    elif op == 408:
        emitter.sound["id"] = arg(args, 1)
    elif op == 409:
        emitter.transforms.append(BulletTransform(index=arg(args, 1, "0"), channel=arg(args, 2, "0"), action_type="th10Transform", raw_opcode=409, raw_args=args[:], difficulty=ins.difficulty))
    elif op in {410, 411}:
        emitter.flags.setdefault("raw_ops", []).append({"opcode": op, "args": args[:], "line": ins.line_no})
