from __future__ import annotations

from collections.abc import Iterable

from .model import BulletEmitter, BulletTransform, Function, Instruction, Program

TH13PLUS_GAMES = {"th13", "th14", "th15", "th16", "th17", "th18"}
TH12_GAMES = {"th12"}
TH08_GAMES = {"th08"}
TH10_GAMES = {"th10", "th11"}


def arg(args: list[str], index: int, default: str = "") -> str:
    return args[index] if index < len(args) else default


def with_difficulty(value: str, literals: dict[str, str]) -> object:
    if value in {"[-1]", "[-1.0f]"} and literals:
        return {"placeholder": value, "difficulty": literals}
    return value


def apply_th13plus(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 607:
        emitter.aim["mode_raw"] = arg(args, 1, "0")
        emitter.aim.setdefault("mode", aim_mode_name(arg(args, 1, "0")))
    elif op == 602:
        emitter.appearance["style"] = arg(args, 1)
        emitter.appearance["color"] = arg(args, 2)
    elif op == 603:
        emitter.origin["x"] = arg(args, 1, "0") if not hasattr(emitter, "origin") else emitter.origin.get("x", arg(args, 1, "0"))
        emitter.origin["y"] = arg(args, 2, "0") if not hasattr(emitter, "origin") else arg(args, 2, "0")
    elif op == 604:
        emitter.aim["base_angle"] = arg(args, 1, "0")
        emitter.aim["angle_step"] = arg(args, 2, "0")
    elif op == 605:
        emitter.speed["first"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.speed["step"] = arg(args, 2, "0")
    elif op == 606:
        emitter.count["ways"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.count["layers"] = arg(args, 2, "1")
    elif op == 608:
        emitter.sound["id"] = arg(args, 1)
        emitter.sound["mode"] = arg(args, 2)
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
    elif op in {617, 618, 619, 624}:
        emitter.speed.setdefault("difficulty_raw", []).append({"opcode": op, "args": args[:], "difficulty": ins.difficulty})
    elif op in {620, 621, 622, 625}:
        emitter.count.setdefault("difficulty_raw", []).append({"opcode": op, "args": args[:], "difficulty": ins.difficulty})
    elif op == 601:
        emitter.fire_lines.append(ins.line_no)


def apply_th12(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 507:
        emitter.aim["mode_raw"] = arg(args, 1, "0")
        emitter.aim.setdefault("mode", aim_mode_name(arg(args, 1, "0")))
    elif op == 502:
        emitter.appearance["style"] = arg(args, 1)
        emitter.appearance["color"] = arg(args, 2)
    elif op == 503:
        emitter.origin = {"x": arg(args, 1, "0"), "y": arg(args, 2, "0")}
    elif op == 504:
        emitter.aim["base_angle"] = arg(args, 1, "0")
        emitter.aim["angle_step"] = arg(args, 2, "0")
    elif op == 505:
        emitter.speed["first"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.speed["step"] = arg(args, 2, "0")
    elif op == 506:
        emitter.count["ways"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.count["layers"] = arg(args, 2, "1")
    elif op == 508:
        emitter.sound["id"] = arg(args, 1)
        emitter.sound["mode"] = arg(args, 2)
    elif op in {509, 510, 511, 512}:
        emitter.transforms.append(BulletTransform(index=arg(args, 1, "0"), action_type="etEx", raw_opcode=op, raw_args=args[:], difficulty=ins.difficulty))
    elif op == 501:
        emitter.fire_lines.append(ins.line_no)


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
            active[emitter_id] = emitter
            emitters.append(emitter)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if emitter and ins.opcode in {601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 617, 618, 619, 620, 621, 622, 624, 625}:
            emitter.raw.append(ins)
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
            active[emitter_id] = emitter
            emitters.append(emitter)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if emitter and ins.opcode in {501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 517, 518, 519, 520, 521, 522, 523, 524, 525}:
            emitter.raw.append(ins)
            apply_th12(emitter, ins)
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
            if ins.opcode == 401:
                emitter.fire_lines.append(ins.line_no)
            continue
        emitter_id = arg(ins.args, 0, "0")
        emitter = active.get(emitter_id)
        if not emitter:
            continue
        if ins.opcode in {402, 404, 405, 406, 407, 408, 409, 410, 411}:
            emitter.raw.append(ins)
            apply_th10(emitter, ins)
    return emitters


def apply_th10(emitter: BulletEmitter, ins: Instruction) -> None:
    args = ins.args
    op = ins.opcode
    if op == 402:
        emitter.appearance["style"] = arg(args, 1)
        emitter.appearance["color"] = arg(args, 2)
    elif op == 404:
        emitter.aim["base_angle"] = arg(args, 1, "0")
        emitter.aim["angle_step"] = arg(args, 2, "0")
    elif op == 405:
        emitter.speed["first"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.speed["step"] = arg(args, 2, "0")
    elif op == 406:
        emitter.count["ways"] = with_difficulty(arg(args, 1, "1"), ins.difficulty_literals)
        emitter.count["layers"] = arg(args, 2, "1")
    elif op == 407:
        emitter.aim["mode_raw"] = arg(args, 1, "0")
        emitter.aim["mode"] = aim_mode_name(arg(args, 1, "0"))
    elif op == 408:
        emitter.sound["id"] = arg(args, 1)
    elif op == 409:
        emitter.transforms.append(BulletTransform(index=arg(args, 1, "0"), channel=arg(args, 2, "0"), action_type="th10Transform", raw_opcode=409, raw_args=args[:], difficulty=ins.difficulty))
    elif op in {410, 411}:
        emitter.flags.setdefault("raw_ops", []).append({"opcode": op, "args": args[:], "line": ins.line_no})
