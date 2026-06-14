from __future__ import annotations

import re
from .arg_adapter import adapt_args_for_op_key, adapt_values_for_generation
from copy import deepcopy

from .model import BulletEmitter, BulletTransform
from .op_ir import target_opcode_for_op_key
from .reference import is_opcode_supported, validate_opcode_args
from .semantics import boss_phase_prefix_ops, bullet_shape_semantic, encode_bullet_shape, encode_spread_style, generation_for_game, opcode_map_for, remap_bullet_transform_mode, remap_raw_arg_by_semantic, remap_shape_change_arg, th12_double_flower_pair, th13_append_transform_to_th12_509, th13_transform_set_to_th12_509, unsupported_bullet_transform_mode_reason

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
    }.get(str(raw), "custom")


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
            if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
                continue
            out.append(mapped)
    return "".join(out) or None


def wrap_ranked_lines(lines: list[str], difficulty: str | None, target: str = "") -> list[str]:
    marker = normalized_rank_marker(difficulty, target)
    if not marker:
        return lines
    if marker == "*":
        return lines if lines and lines[0] == "!*" else ["!*", *lines]
    return [f"!{marker}", *lines, "!*"]



def emit_checked_instruction(target: str, opcode: int, args: list[object]) -> str:
    rendered = [str(arg) for arg in args]
    error = validate_opcode_args(target, opcode, rendered)
    if error:
        return f"// skipped invalid instruction from reference table: {error}; ins_{opcode}({', '.join(rendered)})"
    return f"ins_{opcode}({', '.join(rendered)});"


def as_float_expr(value: object) -> str:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return f"{text}.0f"
    text = re.sub(r"(?<![\w.])([-+]?\d+)(?![\w.])\s*/", lambda m: f"{m.group(1)}.0f /", text)
    text = re.sub(r"/\s*\(?([-+]?\d+)\)?(?![\w.])", lambda m: f"/ _f({m.group(1)})", text)
    text = re.sub(r"(?<![\w.])([-+]?\d+\.\d+)(?![\w.])", lambda m: m.group(1) + ("" if m.group(1).endswith("f") else "f"), text)
    return text


def as_int_expr(value: object):
    if isinstance(value, dict):
        result = dict(value)
        difficulty = result.get("difficulty")
        if isinstance(difficulty, dict):
            result["difficulty"] = {rank: as_int_expr(item) for rank, item in difficulty.items()}
        if "placeholder" in result:
            result["placeholder"] = as_int_expr(result["placeholder"])
        return result
    text = str(value).strip()
    text = re.sub(r"\[(-?\d+)\.0f\]", r"[\1]", text)
    text = re.sub(r"%([A-Za-z][A-Za-z0-9_]*)", r"$\1", text)
    if re.fullmatch(r"[-+]?\d+\.0f?", text):
        return text.split(".")[0]
    return text


def normalize_target_args_for_op_key(op_key: str, target: str, args: list[str]) -> list[str]:
    normalized = [str(arg) for arg in args]
    if target == "th12" and op_key in {
        "movement.position.tween", "movement.position_rel.tween",
        "movement.velocity.tween", "movement.velocity_rel.tween",
        "movement.ellipse.tween", "movement.ellipse_rel.tween",
        "movement.bezier", "movement.bezier_rel",
    }:
        if len(normalized) > 1 and normalized[1] not in {"0", "1", "4", "9"}:
            normalized[1] = "0"
    return normalized



UNSAFE_TARGET_OPCODES: dict[str, set[int]] = {
    # thtk12/thecl.exe -c 8 has no usable format entry for these despite names in th08.eclm.
    "th08": {143, 162},
    # Listed in eclmap, but thtk12's version-12 format table cannot serialize it.
    "th12": {22},
}


def target_opcode_is_safe(target: str, opcode: int) -> bool:
    return int(opcode) not in UNSAFE_TARGET_OPCODES.get(target, set())


def compile_lossy_semantic_fallback(event: dict[str, object], target: str) -> str | None:
    op_key = str(event.get("op_key") or "")
    args = ", ".join(str(arg) for arg in event.get("args", []))
    if op_key == "flow.debug22":
        return f"// dropped debug-only semantic op for {target}: debug22({args})"
    if op_key in {
        "unit.unknown569", "raw.spec1", "raw.spec2", "laser.debug700", "movement.unknown444",
        "enemy.create_legacy270", "enemy.create_maple", "anm.reset", "bullet.distance",
        "raw.eff_create", "raw.eff_create_angle", "raw.card_eff", "raw.timer_threshold", "raw.ins_129",
        "raw.et_on_auto_delay", "flow.familiar_create", "flow.familiar_create_f", "flow.familiar_create_a",
        "flow.trail_familiar_set", "anm.play_attack", "movement.move_rand_time", "flow.ins_79",
        "anm.set_ex", "anm.set_boss_ex", "movement.move_circle_change", "movement.move_accel", "movement.move_curve",
        "raw.et_delay", "raw.et_on_auto", "raw.set_life_bar", "raw.ins_153", "raw.timer_set", "raw.set_lives",
        "raw.life_threshold", "flow.float_time", "flow.math_circle_pos", "flow.inc", "raw.ins_173", "raw.ins_184",
        "flow.math_angle", "flow.math_distance", "flow.et_protect_range", "raw.val_set", "raw.player_nullify", "anm.familiar",
        "bullet.transform", "bullet.transform2",
    }:
        return f"// dropped source-specific semantic op for {target}: {op_key}({args})"
    if target in STACK_VM_TARGETS and op_key == "flow.fset_rand_sign":
        return f"// approximated random-sign float assignment unavailable in target stack VM: {op_key}({args})"
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"} and op_key == "unit.death_wait":
        return "// approximated deathWait on target without deathWait opcode: no-op"
    if op_key == "boss.set_interrupt" and str(event.get("args", [""])[0]) == "-1":
        return f"// dropped disabled interrupt for {target}: setInterrupt(-1)"
    if op_key == "flow.call_async" and str(event.get("args", ["", ""])[-1]) == "-1":
        return f"// dropped disabled async call for {target}: callAsync(..., -1)"
    if target in {"th10", "th11"} and op_key in {
        "anm.on_et", "anm.rotate", "unit.z_index", "unit.hit_sound", "unit.fog",
        "unit.func_set", "movement.move_set_mirror", "unit.call_std", "unit.stage_logo",
        "laser.timing", "laser.angle",
    }:
        return f"// dropped unsupported presentation/runtime helper for {target}: {op_key}({args})"
    if target in {"th12", "th13", "th14", "th15", "th16", "th17", "th18"} and op_key == "laser.on_aimed":
        return "// approximated old aimed laser macro on target laser manager: no-op setup placeholder"
    return None


STACK_VM_TARGETS = {"th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"}


def stack_push(value: str) -> str:
    return f"{value};"


def compile_th08_vm_arithmetic(event: dict[str, object], target: str) -> str | None:
    if target not in STACK_VM_TARGETS or str(event.get("source_game") or "") not in {"th06", "th07", "th08"}:
        return None
    op_key = str(event.get("op_key") or "")
    args = [str(arg) for arg in event.get("args", [])]
    args = adapt_values_for_generation(args, generation_for_game(str(event.get("source_game") or "")), generation_for_game(target))
    binary_ops = {
        "flow.iadd": (50, 43), "flow.isub": (52, 43), "flow.imul": (54, 43), "flow.idiv": (56, 43), "flow.imod": (58, 43),
        "flow.fadd": (51, 45), "flow.fsub": (53, 45), "flow.fmul": (55, 45), "flow.fdiv": (57, 45), "flow.fmod": (58, 45),
    }
    set_binary_ops = {
        "flow.iset_add": (50, 43), "flow.iset_sub": (52, 43), "flow.iset_mul": (54, 43), "flow.iset_div": (56, 43), "flow.iset_mod": (58, 43),
        "flow.fset_add": (51, 45), "flow.fset_sub": (53, 45), "flow.fset_mul": (55, 45), "flow.fset_div": (57, 45), "flow.fset_mod": (58, 45),
    }
    unary_float_ops = {"flow.fset_sin": 79, "flow.fset_cos": 80}
    if op_key == "flow.iset" and len(args) == 2:
        return "\n".join([stack_push(args[1]), f"ins_43({args[0]});"])
    if op_key == "flow.fset" and len(args) == 2:
        return "\n".join([stack_push(args[1]), f"ins_45({args[0]});"])
    if op_key in binary_ops and len(args) == 2:
        op, setter = binary_ops[op_key]
        return "\n".join([stack_push(args[0]), stack_push(args[1]), f"ins_{op}();", f"ins_{setter}({args[0]});"])
    if op_key in set_binary_ops and len(args) == 3:
        op, setter = set_binary_ops[op_key]
        return "\n".join([stack_push(args[1]), stack_push(args[2]), f"ins_{op}();", f"ins_{setter}({args[0]});"])
    if op_key in unary_float_ops and len(args) == 2:
        return "\n".join([stack_push(args[1]), f"ins_{unary_float_ops[op_key]}();", f"ins_45({args[0]});"])
    if op_key == "flow.fset_rand_sign" and len(args) == 2:
        return "\n".join([f"// random sign approximated using positive magnitude", stack_push(args[1]), f"ins_45({args[0]});"])
    if op_key == "flow.math_circle_pos" and len(args) == 4:
        return "\n".join([
            f"// TH08 circlePos lowered through stack VM",
            stack_push(args[2]), f"ins_80();", stack_push(args[3]), f"ins_55();", f"ins_45({args[0]});",
            stack_push(args[2]), f"ins_79();", stack_push(args[3]), f"ins_55();", f"ins_45({args[1]});",
        ])
    if op_key == "flow.math_angle" and len(args) == 5:
        return f"ins_87({args[0]}, {args[1]}, {args[2]}, {args[3]}, {args[4]});"
    if op_key == "flow.math_distance" and len(args) == 5:
        if target not in {"th13", "th14", "th15", "th16", "th17", "th18"}:
            return None
        # TH13+ squareSumRoot(dst, x_delta, y_delta) maps distance between two points.
        return "\n".join([
            stack_push(args[3]), stack_push(args[1]), "ins_53();", "ins_45([-9931.0f]);",
            stack_push(args[4]), stack_push(args[2]), "ins_53();", "ins_45([-9930.0f]);",
            f"ins_86({args[0]}, [-9931.0f], [-9930.0f]);",
        ])
    if op_key == "flow.dec" and len(args) == 1:
        return f"ins_78({args[0]});"
    if op_key == "flow.inc" and len(args) == 1:
        return "\n".join([stack_push(args[0]), "1;", "ins_50();", f"ins_43({args[0]});"])
    if op_key == "flow.norm_rad" and len(args) == 1:
        return f"ins_82({args[0]});"
    return None


def compile_th08_movement_alias(event: dict[str, object], target: str) -> str | None:
    if target not in STACK_VM_TARGETS or str(event.get("source_game") or "") not in {"th06", "th07", "th08"}:
        return None
    op_key = str(event.get("op_key") or "")
    args = adapt_values_for_generation([str(arg) for arg in event.get("args", [])], generation_for_game(str(event.get("source_game") or "")), generation_for_game(target))
    if op_key == "movement.move_dir" and len(args) == 2:
        opcode = target_opcode_for_op_key("movement.velocity.set", target)
        if opcode is not None and is_opcode_supported(target, opcode):
            return f"ins_{opcode}({args[0]}, {args[1]});"
    if op_key == "movement.move_dir_time" and len(args) == 4:
        opcode = target_opcode_for_op_key("movement.velocity.tween", target)
        if opcode is not None and is_opcode_supported(target, opcode):
            return f"ins_{opcode}({args[0]}, {args[1]}, {args[2]}, {args[3]});"
    return None


def compile_th08_conditional_jump(event: dict[str, object], target: str) -> str | None:
    if target not in STACK_VM_TARGETS or str(event.get("source_game") or "") not in {"th06", "th07", "th08"}:
        return None
    op_key = str(event.get("op_key") or "")
    args = adapt_values_for_generation([str(arg) for arg in event.get("args", [])], generation_for_game(str(event.get("source_game") or "")), generation_for_game(target))
    compare_ops = {
        "flow.jmp_equ": 59, "flow.jmp_equ_f": 60,
        "flow.jmp_neq": 61, "flow.jmp_neq_f": 62,
        "flow.jmp_lss": 63, "flow.jmp_lss_f": 64,
        "flow.jmp_leq": 65, "flow.jmp_leq_f": 66,
        "flow.jmp_gre": 67, "flow.jmp_gre_f": 68,
        "flow.jmp_geq": 69, "flow.jmp_geq_f": 70,
    }
    if op_key in compare_ops and len(args) == 4:
        jump_opcode = target_opcode_for_op_key("flow.jmp_neq", target)
        if jump_opcode is None or not is_opcode_supported(target, jump_opcode):
            return None
        return "\n".join([stack_push(args[0]), stack_push(args[1]), f"ins_{compare_ops[op_key]}();", f"ins_{jump_opcode}({args[3]}, {args[2]});"])
    if op_key == "flow.loop" and len(args) == 3:
        jump_opcode = target_opcode_for_op_key("flow.jmp_neq", target)
        if jump_opcode is None or not is_opcode_supported(target, jump_opcode):
            return None
        return "\n".join([f"ins_78({args[2]});", f"ins_{jump_opcode}({args[1]}, {args[0]});"])
    return None


def compile_th08_anm_alias(event: dict[str, object], target: str) -> str | None:
    if target not in STACK_VM_TARGETS or str(event.get("source_game") or "") not in {"th06", "th07", "th08"}:
        return None
    op_key = str(event.get("op_key") or "")
    args = [str(arg) for arg in event.get("args", [])]
    select_opcode = target_opcode_for_op_key("anm.select", target)
    main_opcode = target_opcode_for_op_key("anm.set_main", target)
    sprite_opcode = target_opcode_for_op_key("anm.set_sprite", target)
    if op_key == "anm.set" and len(args) == 1 and select_opcode and main_opcode and is_opcode_supported(target, select_opcode) and is_opcode_supported(target, main_opcode):
        return "\n".join([f"ins_{select_opcode}(0);", f"ins_{main_opcode}(0, {args[0]});"])
    if op_key in {"anm.set_ex", "anm.set_boss_ex"} and len(args) == 1 and select_opcode and main_opcode and is_opcode_supported(target, select_opcode) and is_opcode_supported(target, main_opcode):
        base = args[0]
        if re.fullmatch(r"-?\d+", base):
            values = [str(int(base) + i) for i in range(6)]
            return "\n".join([f"ins_{select_opcode}(0);", *[f"ins_{main_opcode}({slot}, {script});" for slot, script in enumerate(values)]])
    if op_key == "anm.set_slot" and len(args) == 2 and sprite_opcode and is_opcode_supported(target, sprite_opcode):
        return f"ins_{sprite_opcode}({args[0]}, {args[1]});"
    return None


def th12_stage6_to_th15_anm_args(event: dict[str, object], target: str, args: list[str], context: dict[str, object] | None = None) -> list[str]:
    if target != "th15" or str(event.get("source_game") or "") != "th12":
        return args
    if not str(context.get("source_path", "") if context else "").replace("\\", "/").endswith("/th12/stage06.decl"):
        return args

    function = str(context.get("function", "") if context else "")
    boss_like = function.startswith("Boss") or function in {"HPWait", "MBossCard1LaserHit"}
    op_key = str(event.get("op_key") or "")
    if op_key == "anm.select" and len(args) == 1 and args[0] == "1":
        # TH12 stage06 enemy sprites use stgenm06 bank 1.  TH15 stage6 enemy
        # sprites are in st06enm.anm, selected as bank 2 in the original stage.
        return ["2"]
    if op_key == "anm.select" and len(args) == 1 and args[0] == "2" and boss_like:
        # TH12 stage/boss ANM bank 2 corresponds to the external boss ANM bank 3
        # used by TH15 st06bs.decl.
        return ["3"]
    if op_key == "anm.set_sprite" and boss_like and len(args) == 2 and args[0] in {str(slot) for slot in range(3, 13)} and args[1] in {"48", "49", "50", "51", "52", "53", "54", "55", "56", "57"}:
        # These TH12 stage6 boss scripts are Byakuren's flower/wing slots.
        # TH15 st06bs uses script 6 from bank 3 as a known-good extra boss slot.
        return [args[0], "6"]
    if op_key == "anm.set_sprite" and function in {"BossCard4Laser", "BossCard4Laser2"} and len(args) == 2 and args[0] == "0" and args[1] == "[-9982]":
        # TH12 stage06 uses boss-bank script 69 for the four wall laser
        # familiars.  That script is not valid in TH15 st06bs bank 3; script 6
        # is already used as the safe boss-side auxiliary script for this
        # conversion.
        return ["0", "6"]
    if op_key == "anm.set_sprite" and function == "BossCard6_atLine" and len(args) == 2 and args == ["0", "82"]:
        # TH12 script 82 is the flying-bowl line helper in Byakuren's last
        # card.  It is not present in TH15 st06bs bank 3; use the same safe
        # auxiliary boss script used for other imported boss-side helpers.
        return ["0", "6"]
    if op_key in {"anm.play", "anm.play_abs"} and len(args) >= 2 and args[0] == "1":
        # anmPlay/anmPlayAbs carry their target ANM bank as an argument; remap it
        # alongside anmSelect or repeated stage enemy effects can play from
        # TH15 enemy.anm instead of st06enm.anm.
        return ["2", *args[1:]]
    if op_key in {"anm.play", "anm.play_abs"} and len(args) >= 2 and args[0] == "2" and boss_like:
        return ["3", *args[1:]]
    return args


def drop_th12_stage6_stage_mboss_boss_anm(event: dict[str, object], target: str, context: dict[str, object] | None = None) -> str | None:
    if target != "th15" or str(event.get("source_game") or "") != "th12":
        return None
    if not str(context.get("source_path", "") if context else "").replace("\\", "/").endswith("/th12/stage06.decl"):
        return None
    if str(context.get("function", "") if context else "") != "MBoss":
        return None
    op_key = str(event.get("op_key") or "")
    args = [str(arg) for arg in event.get("args", [])]
    if op_key == "anm.select" and args == ["2"]:
        return "// dropped TH12 MBoss boss-bank ANM select in TH15 stage-side script"
    if op_key == "anm.set_sprite" and len(args) == 2 and args[1] in {"46", "47"}:
        return f"// dropped TH12 MBoss boss-bank sprite script {args[1]} in TH15 stage-side script"
    return None


def is_th12_stage6_boss_like_context(event: dict[str, object], target: str, context: dict[str, object] | None = None) -> bool:
    if target != "th15" or str(event.get("source_game") or "") != "th12" or not context:
        return False
    if not str(context.get("source_path", "")).replace("\\", "/").endswith("/th12/stage06.decl"):
        return False
    function = str(context.get("function", ""))
    return function.startswith("Boss") or function in {"HPWait", "MBossCard1LaserHit"}


def compile_special_semantic_event(event: dict[str, object], target: str, context: dict[str, object] | None = None) -> str | None:
    op_key = str(event.get("op_key") or "")
    args = [str(arg) for arg in event.get("args", [])]
    if op_key == "boss.spell_ex" and target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        if len(args) >= 4:
            return f"ins_537({', '.join(args[:4])});"
        return f"// unsupported boss.spell_ex arity for {target}: {', '.join(args)}"
    if (
        op_key == "anm.set_sprite"
        and is_th12_stage6_boss_like_context(event, target, context)
        and len(args) == 2
        and args[0] in {str(slot) for slot in range(3, 13)}
        and args[1] in {"48", "49", "50", "51", "52", "53", "54", "55", "56", "57"}
    ):
        return "\n".join([
            "// approximated TH12 Byakuren flower/wing sprite with a TH15 boss ANM script",
            "ins_302(3);",
            f"ins_303({args[0]}, 6);",
        ])
    if op_key == "enemy.byakuren_butterfly" and target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        if not args:
            return f"// unsupported byakuren butterfly helper arity for {target}: {', '.join(args)}"
        slot = args[0]
        switch = args[1] if len(args) > 1 else "0"
        return "\n".join([
            "// approximated TH12 Byakuren butterfly slot with a TH15 boss ANM script",
            "ins_302(3);",
            f"ins_303({slot}, 6);",
            f"// TH12 butterfly switch argument preserved for audit: {switch}",
        ])
    if (
        op_key in {"enemy.create_abs", "enemy.create", "enemy.create_abs_func", "enemy.create_func"}
        and target == "th15"
        and is_th12_stage6_boss_like_context(event, target, context)
        and args
        and args[0].strip('"') == "BossCard6_atLine"
    ):
        return "// dropped TH12 flying-bowl line object for TH15; bullet independent drift transforms preserve the motion"
    if (
        op_key == "unit.func_set"
        and target in {"th13", "th14", "th15", "th16", "th17", "th18"}
        and is_th12_stage6_boss_like_context(event, target, context)
        and str(context.get("function", "") if context else "") == "BossCard6_atLine"
        and args == ["6"]
    ):
        return "// dropped TH12 flying-bowl line helper effect for TH15: unit.func_set(6)"
    return None


def compile_ir_op_event(event: dict[str, object], target: str, comment: str | None = None, context: dict[str, object] | None = None) -> str | None:
    op_key = str(event.get("op_key") or "")
    if not op_key:
        return None
    if dropped := drop_th12_stage6_stage_mboss_boss_anm(event, target, context):
        return dropped
    source_game = str(event.get("source_game") or "")
    source_opcode = int(event.get("source_opcode") or -1)
    if target == "th12" and source_game in {"th13", "th14", "th15", "th16", "th17", "th18"} and source_opcode in {611, 612}:
        return compile_lossy_semantic_fallback(event, target)
    if op_key == "flow.call_async" and str(event.get("source_game") or "") in {"th06", "th07", "th08"} and str(event.get("args", ["", ""])[-1]) == "-1":
        return f"// dropped disabled async call for {target}: callAsync(..., -1)"
    if op_key == "flow.float_time" and target not in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return compile_lossy_semantic_fallback(event, target)
    if lowered := compile_th08_vm_arithmetic(event, target):
        return lowered
    if lowered := compile_th08_movement_alias(event, target):
        return lowered
    if lowered := compile_th08_conditional_jump(event, target):
        return lowered
    if lowered := compile_th08_anm_alias(event, target):
        return lowered
    if lowered := compile_special_semantic_event(event, target, context):
        return lowered
    opcode = target_opcode_for_op_key(op_key, target)
    semantic_map = opcode_map_for(source_game, target, source_opcode) if source_game and source_opcode >= 0 else None
    if opcode is None and semantic_map is not None:
        opcode = semantic_map.target_opcode
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return compile_lossy_semantic_fallback(event, target)
    args = [str(arg) for arg in event.get("args", [])]
    if semantic_map is not None and semantic_map.arg_order is not None:
        args = [args[index] for index in semantic_map.arg_order if index < len(args)]
    if source_game and source_opcode >= 0:
        args = remap_raw_arg_by_semantic(source_game, target, source_opcode, opcode, args)
    args = th12_stage6_to_th15_anm_args(event, target, args, context)
    adapted_args = adapt_args_for_op_key(op_key, source_game, source_opcode, target, opcode, args)
    if adapted_args is None:
        return None
    args = normalize_target_args_for_op_key(op_key, target, adapted_args)
    error = validate_opcode_args(target, opcode, args)
    if error:
        return compile_lossy_semantic_fallback(event, target)
    line = emit_checked_instruction(target, opcode, args)
    prefix = boss_phase_prefix_ops(op_key, target)
    if prefix:
        line = "\n".join(prefix + [line])
    if comment:
        return f"// {comment}: {op_key} -> ins_{opcode}\n{line}"
    return line


def compile_unsupported_ir_op(event: dict[str, object], target: str) -> str:
    op_key = event.get("op_key") or "unknown"
    opcode = event.get("source_opcode")
    args = ", ".join(str(arg) for arg in event.get("args", []))
    return f"// unsupported semantic op for {target}: {op_key}; source ins_{opcode}({args})"



def sound_args(e: BulletEmitter, emitter_id: str, default_mode: str = "-1") -> list[str] | None:
    sound = e.sound.get("id")
    if sound in (None, ""):
        return None
    mode = e.sound.get("mode", default_mode)
    if mode in (None, ""):
        mode = default_mode
    return [emitter_id, str(sound), str(mode)]

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

def emit_th12_bullet_setup_lines(
    emitter_id: str,
    aim_raw_value,
    style_value,
    color_value,
    ways_value,
    ways: str,
    layers_value,
    layers: str,
    angle_value,
    angle_step_value,
    speed_value,
    speed: str,
    speed_step_value,
    speed_step: str,
) -> list[str]:
    emitter_id = as_int_expr(emitter_id)
    aim_raw_value = as_int_expr(aim_raw_value)
    style_value = as_int_expr(style_value)
    color_value = as_int_expr(color_value)
    ways_value = as_int_expr(ways_value)
    layers_value = as_int_expr(layers_value)
    ways = as_int_expr(ways)
    layers = as_int_expr(layers)
    lines: list[str] = [f"ins_500({emitter_id});"]
    lines.extend(emit_instruction_with_ranked_args(507, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(502, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    count_args = th12_difficulty_count_args(emitter_id, ways_value, ways, layers_value, layers)
    if count_args:
        lines.append(f"ins_522({', '.join(count_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(506, [emitter_id, ways, layers], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(504, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    speed_args = th12_difficulty_speed_args(emitter_id, speed_value, speed, speed_step_value, speed_step)
    if speed_args:
        lines.append(f"ins_521({', '.join(speed_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(505, [emitter_id, speed, speed_step], ["0", "1.0f", "0.0f"]))
    return lines


def append_sound_lines(lines: list[str], target: str, e: BulletEmitter, emitter_id: str) -> None:
    opcode = {"th10": 408, "th11": 408, "th12": 508, "th13": 608, "th14": 608, "th15": 608, "th16": 608, "th17": 608, "th18": 608}.get(target)
    if opcode is None:
        return
    args = sound_args(e, emitter_id)
    if args:
        lines.append(emit_checked_instruction(target, opcode, args))


def th12_aux_emitter_id(emitter_id: str) -> str | None:
    stripped = str(emitter_id).strip()
    if not re.fullmatch(r"\d+", stripped):
        return None
    aux = int(stripped) + 2
    if aux > 7:
        return None
    return str(aux)


def spread_semantics(e: BulletEmitter) -> dict:
    return getattr(e, "semantics", {}).get("bullet", {}).get("spread", {})


def target_flower_pair_from_semantics(e: BulletEmitter) -> tuple[str, str] | None:
    return th12_double_flower_pair(spread_semantics(e))


def fire_at_definition(emitter: BulletEmitter) -> bool:
    return bool(getattr(emitter, "semantics", {}).get("bullet", {}).get("fire_at_definition"))


def append_definition_fire(text: str, emitter: BulletEmitter, target: str) -> str:
    if not fire_at_definition(emitter):
        return text
    emitter_id = v(emitter.id, "0")
    fire_opcode = {
        "th10": 401, "th11": 401, "th12": 501,
        "th13": 601, "th14": 601, "th15": 601, "th16": 601, "th17": 601, "th18": 601,
    }.get(target)
    if fire_opcode is None:
        return text
    lines = text.splitlines()
    if any(re.search(rf"\bins_{fire_opcode}\s*\(\s*{re.escape(str(emitter_id))}\s*\)", line) for line in lines):
        return text
    lines.append(f"// LuaSTG direct bullet call lowered to target fire")
    lines.append(f"ins_{fire_opcode}({emitter_id});")
    aux_id = th12_aux_emitter_id(str(emitter_id)) if target == "th12" and target_flower_pair_from_semantics(emitter) else None
    if aux_id:
        lines.append(f"ins_{fire_opcode}({aux_id});")
    return "\n".join(lines)


def definition_emitter_state(emitter: BulletEmitter) -> BulletEmitter:
    state = getattr(emitter, "semantics", {}).get("definition_state")
    if not isinstance(state, dict):
        return emitter
    definition = BulletEmitter(
        game=emitter.game,
        function=emitter.function,
        source_line=emitter.source_line,
        id=emitter.id,
        family=emitter.family,
    )
    definition.origin = deepcopy(state.get("origin", emitter.origin))
    definition.appearance = deepcopy(state.get("appearance", emitter.appearance))
    definition.aim = deepcopy(state.get("aim", emitter.aim))
    definition.count = deepcopy(state.get("count", emitter.count))
    definition.speed = deepcopy(state.get("speed", emitter.speed))
    definition.sound = deepcopy(state.get("sound", emitter.sound))
    definition.flags = deepcopy(state.get("flags", emitter.flags))
    definition.semantics = deepcopy(emitter.semantics)
    if isinstance(state.get("semantics"), dict):
        definition.semantics["bullet"] = deepcopy(state["semantics"].get("bullet", definition.semantics.get("bullet", {})))
    definition.transforms = [BulletTransform(**transform) for transform in state.get("transforms", []) if isinstance(transform, dict)]
    definition.fire_lines = emitter.fire_lines[:]
    definition.raw = emitter.raw[:]
    definition.unsupported = emitter.unsupported[:]
    return definition


def compile_bullet_emitter(emitter: BulletEmitter, target: str) -> str:
    definition = definition_emitter_state(emitter)
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        compiled = compile_th13plus(definition)
    elif target == "th12":
        compiled = compile_th12(definition)
    elif target in {"th10", "th11"}:
        compiled = compile_th10_slot(definition, target)
    elif target in {"th06", "th07", "th08"}:
        compiled = compile_th08_macro(definition, target)
    else:
        raise ValueError(f"unsupported target backend: {target}")
    return append_definition_fire(compiled, emitter, target)


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
    elif kind == "EffectEmitter":
        compiled = compile_effect_emitter(obj, target)
    elif kind == "FamiliarSpawner":
        compiled = compile_familiar_spawner(obj, target)
    elif kind == "AutoBulletTimer":
        compiled = compile_auto_bullet_timer(obj, target)
    elif kind == "BossTimer":
        compiled = compile_boss_timer(obj, target)
    elif kind == "MotionModifier":
        compiled = compile_motion_modifier(obj, target)
    elif kind == "Timeline":
        compiled = compile_timeline(obj, target)
    else:
        compiled = compile_raw_comment(obj, target)
    if target in {"th06", "th07", "th08", "th09", "th10", "th11"}:
        compiled = strip_line_comments(compiled)
    difficulty = object_difficulty(obj)
    return "\n".join(wrap_ranked_lines(compiled.splitlines(), difficulty, target))


def strip_line_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        lines.append(line)
    return "\n".join(lines)


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
    "th10_th11": {"anmSelect": 258, "anmSetSprite": 259, "anmSetMain": 262, "anmPlay": 263, "anmPlayAbs": 264},
    "th13plus": {"anmSelect": 302, "anmSetSprite": 303, "anmSetMain": 306, "anmPlay": 307, "anmPlayAbs": 308, "anmSwitch": 317, "anmReset": 318},
}

ENEMY_OPS = {
    "th12": {"enmCreate": 256, "enmCreateA": 257, "enmCreateM": 260, "enmCreateAM": 261, "enmCreateF": 265, "enmCreateAF": 266, "enmCreateMF": 267, "enmCreateAMF": 268},
    "th10_th11": {"enmCreate": 256, "enmCreateA": 257, "enmCreateM": 260, "enmCreateAM": 261, "enmCreateF": 265, "enmCreateAF": 266, "enmCreateMF": 267, "enmCreateAMF": 268},
    "th13plus": {"enmCreate": 300, "enmCreateA": 301, "enmCreateM": 304, "enmCreateAM": 305, "enmCreateF": 309, "enmCreateAF": 310, "enmCreateMF": 311, "enmCreateAMF": 312},
}

BOSS_OPS = {
    "th12": {"lifeSet": 411, "setBoss": 412, "timerReset": 413, "setInterrupt": 414, "setTimeout": 421, "spellEnd": 423, "setChapter": 424, "spell": 437, "spell2": 438, "spell3": 439},
    "th13plus": {"lifeSet": 511, "setBoss": 512, "timerReset": 513, "setInterrupt": 514, "setTimeout": 521, "spellEnd": 523, "setChapter": 524, "spell": 537, "spell2": 538, "spell3": 539},
}


def target_family(target: str) -> str:
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return "th13plus"
    if target in {"th10", "th11"}:
        return "th10_th11"
    if target in {"th06", "th07", "th08"}:
        return "th08_macro"
    return "th12"


def compile_named_op(obj, target: str, table_by_family: dict[str, dict[str, int]]) -> str:
    if getattr(obj, "kind", None) == "Animation" and obj.fields.get("op") == "anmPlayAttack":
        lowered = emit_target_op(target, "anm.play", ["0", "0"])
        if lowered:
            return f"// animation semantic lowering {obj.family} -> {target}: legacy boss attack animation approximated as ANM play\n{lowered}"
        return compile_structured_preserve(obj, target, "legacy boss attack animation has no verified target slot")
    event = {
        "op_key": obj.fields.get("op_key"),
        "source_game": getattr(obj, "game", ""),
        "source_opcode": getattr(obj.raw[0], "opcode", -1) if getattr(obj, "raw", None) else -1,
        "args": obj.fields.get("args", []),
    }
    context = {"function": getattr(obj, "function", ""), "source_path": getattr(obj, "source", "") or obj.fields.get("source", "")}
    lowered = compile_ir_op_event(event, target, f"{obj.kind} lowering {obj.family} -> {target}", context)
    if lowered:
        return lowered
    if event.get("op_key"):
        return compile_raw_comment(obj, target) + f"\n// unsupported semantic op_key for {target}: {event.get('op_key')}"
    family = target_family(target)
    semantic = obj.fields.get("op")
    opcode = table_by_family.get(family, {}).get(semantic)
    if opcode is None:
        return compile_raw_comment(obj, target) + f"\n// unsupported legacy semantic op for {target}: {semantic}"
    args = remap_named_args(obj, target, semantic, obj.fields.get("args", []))
    return f"// legacy {obj.kind} lowering without op_key {obj.family} -> {target}: {semantic}\n" + emit_checked_instruction(target, opcode, args)


def remap_named_args(obj, target: str, semantic: str, args: list[str]) -> list[str]:
    args = list(args)
    if target == "th12" and getattr(obj, "family", "") == "th13plus" and semantic == "anmSelect" and args == ["2"]:
        # TH15 st01 enemy sprites live in st01enm.anm at ANM index 2.
        # TH12 stage01 has no st01enm.anm; index 2 points at stage/boss ANM, so use enemy.anm.
        return ["1"]
    if target == "th12" and getattr(obj, "family", "") == "th13plus" and semantic == "anmSelect" and args == ["3"]:
        # TH13+ stage boss/midboss scripts commonly select stage boss ANM at index 3.
        # TH12 stage01's boss ANM is selected with index 2; leaving 3 can crash at runtime.
        return ["2"]
    if target == "th12" and getattr(obj, "family", "") == "th13plus" and semantic in {"anmSetMain", "anmSetSprite"}:
        # Keep script IDs for now; the important crash/visual fix is the ANM file index.
        # A later sprite table can map TH15 st01enm script IDs to closer TH12 enemy.anm scripts.
        return args
    return args


def compile_boss_pattern(obj, target: str) -> str:
    lines = [f"// BossPattern lowering {obj.family} -> {target}; semantic op_key backend"]
    for item in obj.fields.get("ops", []):
        event = {
            "op_key": item.get("op_key"),
            "source_game": getattr(obj, "game", ""),
            "source_opcode": item.get("opcode", -1),
            "args": item.get("args", []),
        }
        lowered = compile_ir_op_event(event, target)
        if lowered:
            lines.extend(lowered.splitlines())
        else:
            lines.append(compile_unsupported_ir_op(event, target))
    return "\n".join(lines)


def compile_timeline(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    if getattr(obj, "game", "") == "luastg" and fields.get("op") == "wait":
        frames = str(fields.get("frames", "1"))
        if target in {"th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
            return f"// LuaSTG wait lowering -> {target}\nins_83({frames});"
        return f"// LuaSTG wait lowering -> {target}; old target wait syntax requires manual placement\n// wait {frames} frames"
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


def object_ir_events(obj) -> list[dict[str, object]]:
    events = list((getattr(obj, "fields", {}) or {}).get("ir_ops") or [])
    if events:
        return events
    return [
        {"op_key": None, "source_game": getattr(obj, "game", ""), "source_opcode": ins.opcode, "args": ins.args}
        for ins in getattr(obj, "raw", [])
    ]


def compile_structured_preserve(obj, target: str, reason: str = "no native equivalent") -> str:
    fields = getattr(obj, "fields", {}) or {}
    lines = [f"// semantic object preserved for {target}: {obj.kind}.{fields.get('semantic', obj.family)} ({reason})"]
    for key in ("effect", "spawn", "trail", "focus_animation", "timer", "interrupt", "life_bar", "motion"):
        if key in fields:
            lines.append(f"//   {key}: {fields[key]}")
    for ins in getattr(obj, "raw", []):
        lines.append(f"//   source: {ins.raw.strip()}")
    return "\n".join(lines)


def emit_if_supported(target: str, op_key: str, args: list[str], source_game: str = "", source_opcode: int = -1) -> str | None:
    opcode = target_opcode_for_op_key(op_key, target)
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return None
    adapted = adapt_args_for_op_key(op_key, source_game, source_opcode, target, opcode, [str(arg) for arg in args])
    if adapted is None:
        return None
    adapted = normalize_target_args_for_op_key(op_key, target, adapted)
    error = validate_opcode_args(target, opcode, adapted)
    if error:
        return None
    return emit_checked_instruction(target, opcode, adapted)


def emit_target_op(target: str, op_key: str, args: list[str]) -> str | None:
    opcode = target_opcode_for_op_key(op_key, target)
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return None
    normalized = normalize_target_args_for_op_key(op_key, target, [str(arg) for arg in args])
    error = validate_opcode_args(target, opcode, normalized)
    if error:
        return None
    return emit_checked_instruction(target, opcode, normalized)


def target_sub_name(value: object) -> str:
    text = str(value).strip()
    if text.startswith('"') and text.endswith('"'):
        return text
    if re.fullmatch(r"-?\d+", text):
        return f'"Sub{text}"'
    return f'"{text}"'


def float_literal(value: object, default: str = "0.0f") -> str:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return f"{text}.0f"
    if re.fullmatch(r"[-+]?\d+\.\d+f?", text):
        return text if text.endswith("f") else f"{text}f"
    if re.fullmatch(r"\[-?\d+\]", text):
        return text[:-1] + ".0f]"
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]", text):
        return text
    return default


def compile_effect_emitter(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    lines = [f"// EffectEmitter lowering {obj.family} -> {target}: {semantic}"]
    if semantic in {"effect_burst", "effect_burst_angle"}:
        effect = fields.get("effect", {}) or {}
        script_expr = str(effect.get("script_expr", "0"))
        amount = str(effect.get("amount", "1"))
        angle = str(effect.get("angle") or "0.0f")
        play_rotate = emit_target_op(target, "anm.play_rotate", ["0", script_expr, angle])
        play_plain = emit_target_op(target, "anm.play", ["0", script_expr])
        if play_rotate and semantic == "effect_burst_angle":
            lines.append(f"// approximated old etama effect count={amount} using target ANM play_rotate")
            lines.append(play_rotate)
            return "\n".join(lines)
        if play_plain:
            lines.append(f"// approximated old etama effect count={amount} using target ANM play")
            lines.append(play_plain)
            return "\n".join(lines)
    if semantic == "card_effect":
        lowered = next((compile_ir_op_event(event, target) for event in object_ir_events(obj) if compile_ir_op_event(event, target)), None)
        if lowered:
            lines.extend(lowered.splitlines())
            return "\n".join(lines)
    if semantic in {"spell_effect_state", "spell_start_effect_state"}:
        high = emit_target_op(target, "anm.play_high", ["0", "0"])
        if high:
            lines.append("// approximated legacy spell visual state as target high-priority ANM boundary")
            lines.append(high)
            return "\n".join(lines)
        lines.append("// metadata-only spell visual state boundary; no target runtime opcode required")
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "visual effect has no verified cross-generation equivalent").splitlines())


def compile_familiar_spawner(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    spawn = fields.get("spawn", {}) or {}
    lines = [f"// FamiliarSpawner lowering {obj.family} -> {target}: {semantic}"]
    if spawn:
        sub = target_sub_name(spawn.get("sub", ""))
        x = str(spawn.get("x", "0.0f"))
        y = str(spawn.get("y", "0.0f"))
        life = str(spawn.get("life", "0"))
        item = str(spawn.get("item", "0"))
        score = str(spawn.get("score", "0"))
        rel = spawn.get("position_mode") != "absolute"
        op_key = "enemy.create_func" if rel else "enemy.create_abs_func"
        fallback = [sub, x, y, life, item, score]
        if not emit_target_op(target, op_key, fallback):
            op_key = "enemy.create" if rel else "enemy.create_abs"
            fallback = [sub, x, y, life, item, score]
        lowered = emit_target_op(target, op_key, fallback)
        if lowered:
            lines.append("// approximated TH08 familiar as target enemy/familiar-like child; focus invulnerability is preserved only as semantic metadata")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "focus_animation":
        focus = fields.get("focus_animation", {}) or {}
        lowered = emit_target_op(target, "anm.play", ["0", str(focus.get("script_expr", "0"))])
        if lowered:
            lines.append("// approximated familiar focus ANM as ordinary ANM play")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "trail_toggle":
        lines.append("// metadata-only familiar trail toggle; target games have no verified equivalent trail runtime")
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "familiar runtime behavior is TH08-specific").splitlines())


def compile_auto_bullet_timer(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    timer = fields.get("timer", {}) or {}
    lines = [f"// AutoBulletTimer lowering {obj.family} -> {target}: {semantic}"]
    if semantic == "defer_attribute_fire":
        lines.append("// target slot emitters are configured without implicit fire; no instruction needed")
        return "\n".join(lines)
    interval = str(timer.get("interval", "1"))
    fire = emit_target_op(target, "bullet.fire", ["0"])
    if fire:
        lines.append(f"// auto-fire interval={interval} preserved as high-level timer; emitted one fire tick at source position")
        lines.append(fire)
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "target has no verified auto-fire timer primitive").splitlines())


def compile_boss_timer(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    lines = [f"// BossTimer lowering {obj.family} -> {target}: {semantic}"]
    interrupt = fields.get("interrupt", {}) or {}
    if interrupt:
        if interrupt.get("trigger") == "life_leq":
            args = ["0", str(interrupt.get("life", "0")), "0", target_sub_name(interrupt.get("sub", "-1"))]
        else:
            args = ["0", "0", str(interrupt.get("time", "0")), target_sub_name(interrupt.get("sub", "-1"))]
        lowered = emit_target_op(target, "boss.set_interrupt", args)
        if lowered:
            lines.append("// lowered threshold interrupt through target boss interrupt object")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "timer_set":
        lowered = emit_target_op(target, "boss.timer_reset", [])
        if lowered:
            lines.append("// target timer reset approximates legacy upward timer set")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "life_bar_segment":
        bar = fields.get("life_bar", {}) or {}
        marker_hp = float_literal(bar.get("life_min", "0"))
        lowered = emit_target_op(target, "unit.life_marker", [str(bar.get("slot", "0")), marker_hp, str(bar.get("color", "0"))])
        if lowered:
            lines.append("// lowered lifebar color segment to target life marker approximation")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "visible_life_count":
        if target == "th12":
            lowered = emit_target_op(target, "unit.life_hide", [])
        elif target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
            lowered = emit_target_op(target, "bullet.life_hide", ["0"])
        else:
            lowered = None
        if lowered:
            lines.append("// visible life-count HUD state approximated by keeping target lifebar visible")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "bomb_immunity_state":
        enabled = str((fields.get("args") or ["1"])[0]) != "0"
        if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
            lowered = emit_target_op(target, "unit.bomb_shield", ["1" if enabled else "0", "0"])
            invuln = emit_target_op(target, "unit.bomb_invuln", ["0.0f" if enabled else "1.0f"])
            if lowered or invuln:
                lines.append("// lowered legacy bomb-immunity state to target bomb shield/invulnerability controls")
                if lowered:
                    lines.append(lowered)
                if invuln:
                    lines.append(invuln)
                return "\n".join(lines)
        elif target == "th12":
            lowered = emit_target_op(target, "movement.bomb_shield", ["1" if enabled else "0", "0.0f"])
            if lowered:
                lines.append("// lowered legacy bomb-immunity state to TH12 bombShield approximation")
                lines.append(lowered)
                return "\n".join(lines)
    if semantic == "boss_runtime_state":
        lowered = emit_target_op(target, "unit.set_invuln", ["0"])
        if lowered:
            lines.append("// preserved unknown boss runtime state as explicit no-duration invulnerability state boundary")
            lines.append(lowered)
            return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "boss HUD/timer semantics differ across generations").splitlines())


def compile_motion_modifier(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    motion = fields.get("motion", {}) or {}
    lines = [f"// MotionModifier lowering {obj.family} -> {target}: {semantic}"]
    if semantic in {"random_direction_tween", "random_direction_tween_variant"}:
        lowered = emit_target_op(target, "movement.velocity.tween", [str(motion.get("time", "0")), str(motion.get("mode", "0")), "0.0f", str(motion.get("speed", "0.0f"))])
        if lowered:
            lines.append("// approximated bounded random direction as target velocity tween with neutral angle; semantic direction retained in object metadata")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "circle_speed_change":
        lowered = emit_target_op(target, "movement.circle.tween", [str(motion.get("time", "0")), "0", str(motion.get("angular_velocity", "0.0f")), "0.0f", str(motion.get("radius_velocity", "0.0f"))])
        if lowered:
            lines.append("// approximated legacy circle speed change through target circle tween")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "angular_velocity":
        lowered = emit_target_op(target, "movement.circle.tween", ["999999", "0", str(motion.get("angular_velocity", "0.0f")), "0.0f", "0.0f"])
        if lowered:
            lines.append("// approximated legacy per-frame angular velocity as long-lived target circle tween")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "linear_acceleration":
        lowered = emit_target_op(target, "movement.velocity.tween", ["999999", "0", "0.0f", str(motion.get("acceleration", "0.0f"))])
        if lowered:
            lines.append("// approximated legacy per-frame acceleration as long-lived target velocity tween")
            lines.append(lowered)
            return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "motion modifier needs runtime state unavailable in target opcode").splitlines())


def compile_luastg_laser(obj, target: str) -> str | None:
    if getattr(obj, "game", "") != "luastg":
        return None
    params = (getattr(obj, "fields", {}) or {}).get("params", {}) or {}
    laser_id = str(getattr(obj, "id", "0"))
    style = str(params.get("style", laser_id)).strip()
    length = str(params.get("length", "512.0f")).strip()
    width = str(params.get("width", "16.0f")).strip()
    warn = str(params.get("warn_time", "0")).strip()
    fade_in = str(params.get("fade_in", "0")).strip()
    active = str(params.get("active_time", "60")).strip()
    fade_out = str(params.get("fade_out", "15")).strip()
    angle = as_float_expr(params.get("angle", "0.0f"))
    kind = str(params.get("kind", "line")).strip().strip('"\'')
    if target == "th12":
        fire_opcode = 611 if kind == "curve" else 602
        return "\n".join([
            f"// LuaSTG laser semantic lowering -> th12: {kind}",
            f"ins_600({laser_id}, 0.0f, {length}, 0.0f, {width});",
            f"ins_601({laser_id}, {warn}, {fade_in}, {active}, {fade_out}, 0);",
            f"ins_608({laser_id}, {angle});",
            f"ins_{fire_opcode}({laser_id});",
        ])
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return "\n".join([
            f"// LuaSTG laser semantic lowering -> {target}: preserved draft, opcode mapping incomplete",
            f"// style={style} id={laser_id} length={length} width={width} angle={angle} timing={warn},{fade_in},{active},{fade_out} kind={kind}",
        ])
    return compile_raw_comment(obj, target) + f"\n// LuaSTG laser lowering to {target} is not implemented"


def compile_laser(obj, target: str) -> str:
    luastg_lowered = compile_luastg_laser(obj, target)
    if luastg_lowered is not None:
        return luastg_lowered
    if target in {"th06", "th07", "th08", "th10", "th11"}:
        return compile_raw_comment(obj, target) + f"\n// laser lowering to {target} is not implemented yet"
    if target not in {"th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported laser target: {target}")
    lines = [f"// laser lowering {obj.family} -> {target}; semantic op_key backend"]
    events = obj.fields.get("ir_ops") or []
    if not events:
        events = [
            {
                "op_key": None,
                "source_game": getattr(obj, "game", ""),
                "source_opcode": ins.opcode,
                "args": ins.args,
            }
            for ins in getattr(obj, "raw", [])
        ]
    for event in events:
        lowered = compile_ir_op_event(event, target)
        if lowered:
            lines.extend(lowered.splitlines())
        else:
            lines.append(compile_unsupported_ir_op(event, target))
    return "\n".join(lines)


def parenthesize_expr(expr: object) -> str:
    expr = str(expr).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", expr):
        return expr
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]|[%$][A-Za-z_][A-Za-z0-9_]*", expr):
        return expr
    if expr.startswith("(") and expr.endswith(")"):
        return expr
    return f"({expr})"


def add_float_expr(left: object, right: object) -> str:
    left_text = str(left).strip()
    right_text = str(right).strip()
    if right_text.startswith("-") and re.fullmatch(r"-\d+(?:\.\d+)?f?", right_text):
        return f"{parenthesize_expr(left_text)} - {right_text[1:]}"
    return f"{parenthesize_expr(left_text)} + {parenthesize_expr(right_text)}"


def th12_unit_move_mode(mode: object) -> str:
    text = str(mode).strip()
    return text if text in {"0", "1", "4", "9"} else "0"


def normalize_th12_move_args(movement: str, args: list[str]) -> list[str]:
    normalized = [str(arg) for arg in args]
    if movement in {"movePosTime", "movePosRelTime", "moveVelTime", "moveVelRelTime", "moveEllipseTime", "moveEllipseRelTime", "moveBezier", "moveBezierRel"}:
        if len(normalized) > 1 and normalized[1] not in {"0", "1", "4", "9"}:
            normalized[1] = "0"
    return normalized


def compile_split_motion_semantic(obj, target: str) -> str | None:
    if target != "th12":
        return None
    motion = obj.fields.get("semantics", {}).get("motion", {})
    op = motion.get("op")
    rel = op in {"moveDirRel", "moveDirRelTime", "moveSpeedRel", "moveSpeedRelTime"}
    direct_opcode = 306 if rel else 304
    time_opcode = 307 if rel else 305
    if op in {"moveDir", "moveDirRel"}:
        speed = motion.get("speed")
        direction = motion.get("direction")
        if speed is None or direction is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: direction set needs current speed"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered speed\nins_{direct_opcode}({direction}, {speed});"
    if op in {"moveDirTime", "moveDirRelTime"}:
        speed = motion.get("speed")
        base_direction = motion.get("base_direction")
        delta = motion.get("direction_delta")
        if speed is None or base_direction is None or delta is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: direction interpolation needs current direction and speed"
        direction = add_float_expr(base_direction, delta)
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered speed\nins_{time_opcode}({motion.get('time', '0')}, {th12_unit_move_mode(motion.get('mode', '0'))}, {direction}, {speed});"
    if op in {"moveSpeed", "moveSpeedRel"}:
        direction = motion.get("direction")
        speed = motion.get("speed")
        if direction is None or speed is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: speed set needs current direction"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered direction\nins_{direct_opcode}({direction}, {speed});"
    if op in {"moveSpeedTime", "moveSpeedRelTime"}:
        direction = motion.get("direction")
        speed = motion.get("speed")
        if direction is None or speed is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: speed interpolation needs current direction"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered direction\nins_{time_opcode}({motion.get('time', '0')}, {th12_unit_move_mode(motion.get('mode', '0'))}, {direction}, {speed});"
    return None


def compile_movement(obj, target: str) -> str:
    if target not in {"th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported movement target: {target}")
    semantic = compile_split_motion_semantic(obj, target)
    if semantic is not None:
        return semantic
    event = {
        "op_key": obj.fields.get("op_key"),
        "source_game": getattr(obj, "game", ""),
        "source_opcode": getattr(obj.raw[0], "opcode", -1) if getattr(obj, "raw", None) else -1,
        "args": obj.fields.get("args", []),
    }
    lowered = compile_ir_op_event(event, target, f"movement lowering {obj.family} -> {target}")
    if lowered:
        return lowered
    return compile_raw_comment(obj, target) + f"\n// unsupported movement semantic op_key for {target}: {obj.fields.get('op_key') or obj.fields.get('op')}"


def compile_th13plus(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = remap_bullet_spread_style_for_target(e, target="th15")
    if aim_raw_value is None:
        aim_raw_value = mode_raw(e.aim.get("mode"), default="1")
    style_value = remap_bullet_shape_for_target(e, target="th15")
    color_value = e.appearance.get("color")
    if e.game == "th12" and (emitter_has_curve_laser(e) or e.semantics.get("curve_laser_fire")):
        style_value = "0"
        color_value = "2"
    ways_value = e.count.get("ways")
    layers_value = e.count.get("layers")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    speed_value = e.speed.get("first")
    speed_step_value = e.speed.get("step")
    lines = [emit_checked_instruction("th15", 600, [emitter_id])]
    lines.extend(emit_instruction_with_ranked_args(607, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(602, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    lines.extend(emit_instruction_with_ranked_args(606, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(604, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    lines.extend(emit_instruction_with_ranked_args(605, [emitter_id, speed_value, speed_step_value if speed_step_value is not None else e.speed.get("last_or_step")], ["0", "1.0f", e.speed.get("last_or_step", "0.0f")]))
    lines.extend(th13plus_origin_lines(str(emitter_id), e.origin))
    lines.extend(th13plus_laser_origin_lines(e, str(emitter_id)))
    if args := sound_args(e, emitter_id):
        lines.append(emit_checked_instruction("th15", 608, args))
    for field, value in (("speed.first", e.speed.get("first")), ("count.ways", e.count.get("ways"))):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment)
    curve_laser = e.game == "th12" and (emitter_has_curve_laser(e) or e.semantics.get("curve_laser_fire"))
    transforms = curve_laser_th13plus_transforms(e.transforms) if curve_laser else th12_th13plus_transform_timeline(e.transforms, e.game, "th15")
    for transform in transforms:
        lowered = lower_transform_for_th13plus(transform, e.game, "th15", str(emitter_id))
        if lowered:
            lines.extend(lowered)
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    return "\n".join(lines)


def th12_th13plus_transform_timeline(transforms, source_game: str, target: str):
    if source_game != "th12" or generation_for_game(target) != "th13_plus":
        return transforms
    normalized = []
    next_index_by_emitter: dict[str, int] = {}
    next_start_by_emitter_channel: dict[tuple[str, str], str] = {}
    for transform in transforms:
        args = [str(arg) for arg in transform.raw_args]
        if transform.raw_opcode != 509 or len(args) != 8:
            normalized.append(transform)
            continue
        emitter_id, slot, channel, mode, duration, start, r, s = args
        if unsupported_bullet_transform_mode_reason(source_game, target, mode):
            continue
        args = args[:]
        if re.fullmatch(r"-?\d+", args[1]):
            expected = next_index_by_emitter.get(emitter_id, 0)
            args[1] = str(expected)
            next_index_by_emitter[emitter_id] = expected + 1
        if mode == "8" and start == INT_SENTINEL:
            timeline_key = (emitter_id, channel)
            args[5] = next_start_by_emitter_channel.get(timeline_key, "0")
            next_start_by_emitter_channel[timeline_key] = add_int_expr(args[5], duration)
        cloned = deepcopy(transform)
        cloned.raw_args = args
        normalized.append(cloned)
    return normalized


def add_int_expr(left: object, right: object) -> str:
    left_s = str(left).strip()
    right_s = str(right).strip()
    if re.fullmatch(r"-?\d+", left_s) and re.fullmatch(r"-?\d+", right_s):
        return str(int(left_s) + int(right_s))
    if left_s == "0":
        return right_s
    return f"{left_s} + {right_s}"


def curve_laser_th13plus_transforms(transforms):
    normalized = []
    next_index = 0
    for transform in transforms:
        args = [str(arg) for arg in transform.raw_args]
        if transform.raw_opcode == 509 and len(args) == 8:
            mode = args[3]
            if mode == "512":
                continue
            args = args[:]
            args[1] = str(next_index)
            if mode == "8" and args[5] == "-999999":
                args[5] = "0"
            next_index += 1
            cloned = deepcopy(transform)
            cloned.raw_args = args
            normalized.append(cloned)
            continue
        normalized.append(transform)
    return normalized


def lower_transform_for_th13plus(transform, source_game: str, target: str, emitter_id: str) -> list[str] | None:
    args = [str(arg) for arg in transform.raw_args]
    if transform.raw_opcode in {609, 610, 611, 612} and args:
        return [f"ins_{transform.raw_opcode}({', '.join(args)});"]
    if source_game == "th12" and transform.raw_opcode == 509 and len(args) == 8:
        reason = unsupported_bullet_transform_mode_reason(source_game, target, args[3])
        if reason:
            return [f"// dropped unsupported bullet transform mode from ins_509: {reason}; original args: {', '.join(args)}"]
        opcode, converted = th12_509_to_th13plus_transform(args, target)
        return [f"ins_{opcode}({', '.join(converted)});"]
    if source_game == "th12" and transform.raw_opcode == 510 and not args:
        return ["ins_610();"]
    if source_game == "th12" and transform.raw_opcode == 511 and len(args) == 2:
        return [f"ins_611({', '.join(args)});"]
    if source_game == "th12" and transform.raw_opcode == 512 and len(args) == 1:
        return [f"ins_612({', '.join(args)});"]
    if source_game == "th12" and transform.raw_opcode == 521 and len(args) == 9:
        return emit_instruction_with_ranked_args(624, args, [emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"])
    if source_game == "th12" and transform.raw_opcode == 522 and len(args) == 9:
        return emit_instruction_with_ranked_args(625, args, [emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"])
    return None


def th12_509_to_th13plus_609(args: list[str], target: str) -> list[str]:
    converted = args[:]
    converted[3] = remap_bullet_transform_mode("th12", target, converted[3])
    converted[4] = remap_shape_change_arg("th12", target, args[3], converted[4])
    if generation_for_game(target) == "th13_plus":
        converted = ["-999999.0f" if value == "-999.0f" and index >= 6 else value for index, value in enumerate(converted)]
    return converted


def th12_509_to_th13plus_transform(args: list[str], target: str) -> tuple[int, list[str]]:
    converted = th12_509_to_th13plus_609(args, target)
    if converted[3] == "16":
        et_id, slot, channel, mode, a, b, r, s = converted
        subtype = th12_pause_then_velocity_subtype(args[3])
        if args[3] == "32":
            r = th12_random_angle_expression_bound(r)
        mode_flags = "0"
        return 610, [et_id, slot, channel, mode, a, b, subtype, mode_flags, r, s, "-999999.0f", "-999999.0f"]
    return 609, converted


def th12_random_angle_expression_bound(expr: str) -> str:
    normalized = str(expr).strip()
    match = re.fullmatch(r"\[-9998\.0f\]\s*/\s*_f\(([-+]?\d+(?:\.\d+)?)\)", normalized)
    if match:
        return f"3.1415927f / _f({match.group(1)})"
    match = re.fullmatch(r"\[-9998\.0f\]\s*/\s*([-+]?\d+(?:\.\d+)?f?)", normalized)
    if match:
        denom = match.group(1)
        return f"3.1415927f / {denom}"
    if normalized == "[-9998.0f]":
        return "3.1415927f"
    return expr


def th12_pause_then_velocity_subtype(mode: str) -> str:
    # TH12 has three separate modes for delayed velocity changes; TH13+ folds
    # them into mode 16 and selects behavior with c.
    return {
        "16": "0",  # original direction + r, speed = s
        "32": "6",  # random aimed direction within +/-r, speed = s
        "64": "4",  # direction = r, speed = s
    }.get(str(mode), "0")


def th13plus_origin_lines(emitter_id: str, origin: dict[str, object]) -> list[str]:
    mode = str(origin.get("mode", "enemy")) if origin else "enemy"
    if mode == "offset":
        return [emit_checked_instruction("th15", 603, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))])]
    if mode == "polar":
        return [emit_checked_instruction("th15", 626, [emitter_id, str(origin.get("angle", "0.0f")), str(origin.get("radius", "0.0f"))])]
    if mode == "distance":
        return [emit_checked_instruction("th15", 627, [emitter_id, str(origin.get("distance", "0.0f"))])]
    if mode == "absolute":
        return [emit_checked_instruction("th15", 628, [emitter_id, str(origin.get("x", "0.0f")), str(origin.get("y", "0.0f"))])]
    return []


def emitter_has_curve_laser(e: BulletEmitter) -> bool:
    return any(getattr(ins, "opcode", None) == 611 for ins in getattr(e, "raw", []))


def th13plus_laser_origin_lines(e: BulletEmitter, emitter_id: str) -> list[str]:
    return []


def remap_bullet_spread_style_for_target(e: BulletEmitter, target: str):
    spread = spread_semantics(e)
    if spread:
        return encode_spread_style(spread, target, e.aim.get("mode_raw"))
    return e.aim.get("mode_raw")


def remap_bullet_shape_for_target(e: BulletEmitter, target: str):
    value = e.appearance.get("style")
    if isinstance(value, dict):
        return {rank: encode_bullet_shape(bullet_shape_semantic(e.game, shape), target, shape) for rank, shape in value.items()}
    semantic_shape = getattr(e, "semantics", {}).get("bullet", {}).get("shape")
    if semantic_shape:
        return encode_bullet_shape(semantic_shape, target, value)
    return value


def compile_th12(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = remap_bullet_spread_style_for_target(e, target="th12")
    if aim_raw_value is None:
        aim_raw_value = mode_raw(e.aim.get("mode"), default="1")
    style_value = remap_bullet_shape_for_target(e, target="th12")
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
    if speed_step_value is None and e.speed.get("last_or_step") is not None:
        speed_step_value = e.speed.get("last_or_step")
    speed_step = v(speed_step_value, e.speed.get("last_or_step", "0.0f"))

    double_flower = target_flower_pair_from_semantics(e)
    aux_emitter_id = th12_aux_emitter_id(str(emitter_id)) if double_flower else None
    if double_flower and aux_emitter_id:
        lines = [f"// TH15 double flower spread lowered to two TH12 single-side flower slots: {emitter_id}+{aux_emitter_id}"]
        lines.extend(emit_th12_bullet_setup_lines(emitter_id, double_flower[0], style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step))
        lines.extend(emit_th12_bullet_setup_lines(aux_emitter_id, double_flower[1], style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step))
    else:
        lines = emit_th12_bullet_setup_lines(emitter_id, aim_raw_value, style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step)

    append_sound_lines(lines, "th12", e, str(emitter_id))
    if aux_emitter_id:
        append_sound_lines(lines, "th12", e, str(aux_emitter_id))

    for field, value in (("speed.first", speed_value), ("speed.step", speed_step_value), ("count.ways", ways_value), ("count.layers", layers_value)):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment.replace("lowered using", "preserved as TH12 difficulty table; default preview"))
    next_transform_index = 0
    for transform in e.transforms:
        if transform.raw_opcode == 509 and len(transform.raw_args) == 8:
            lines.append(f"ins_509({', '.join(transform.raw_args)});")
            if str(transform.raw_args[0]) == str(emitter_id) and re.fullmatch(r"-?\d+", str(transform.raw_args[1])):
                next_transform_index = max(next_transform_index, int(str(transform.raw_args[1])) + 1)
        elif transform.raw_opcode == 510 and len(transform.raw_args) == 0:
            lines.append("ins_510();")
        elif transform.raw_opcode == 511 and len(transform.raw_args) == 2:
            lines.append(f"ins_511({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 512 and len(transform.raw_args) == 1:
            lines.append(f"ins_512({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 624 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(521, transform.raw_args, [emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
            if aux_emitter_id:
                aux_args = [aux_emitter_id, *transform.raw_args[1:]]
                lines.extend(emit_instruction_with_ranked_args(521, aux_args, [aux_emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
        elif transform.raw_opcode == 625 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(522, transform.raw_args, [emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
            if aux_emitter_id:
                aux_args = [aux_emitter_id, *transform.raw_args[1:]]
                lines.extend(emit_instruction_with_ranked_args(522, aux_args, [aux_emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
        elif transform.raw_opcode == 609 and len(transform.raw_args) == 8:
            converted = th13_transform_set_to_th12_509(transform.raw_args, e.game)
            if not converted:
                lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
                continue
            lines.append(f"ins_509({', '.join(converted)});")
            if str(transform.raw_args[0]) == str(emitter_id) and re.fullmatch(r"-?\d+", str(transform.raw_args[1])):
                next_transform_index = max(next_transform_index, int(str(transform.raw_args[1])) + 1)
        elif transform.raw_opcode == 611 and len(transform.raw_args) == 7:
            converted = th13_append_transform_to_th12_509(transform.raw_args, next_transform_index, e.game)
            if converted:
                lines.append(f"ins_509({', '.join(converted)});")
                if aux_emitter_id and str(transform.raw_args[0]) == str(emitter_id):
                    aux_converted = [aux_emitter_id, *converted[1:]]
                    lines.append(f"ins_509({', '.join(aux_converted)});")
                next_transform_index += 1
            else:
                lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {610, 612}:
            lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {510, 511, 512}:
            lines.append(f"// unsupported th12 transform opcode/arity in generated context; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    return "\n".join(lines)




def old_macro_arg(value: object, default: str, numeric: str = "float") -> str:
    text = str(v(value, default)).strip()
    if isinstance(value, dict):
        text = str(v(value, default)).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", text):
        return text
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]", text):
        return text
    if numeric == "int":
        return default
    return default


def old_macro_int(value: object, default: str) -> str:
    return old_macro_arg(value, default, "int")


def old_macro_float(value: object, default: str) -> str:
    return old_macro_arg(value, default, "float")


def clamp_old_shape(shape: object, target: str) -> str:
    value = str(v(shape, "0"))
    if not re.fullmatch(r"-?\d+", value):
        return value
    number = int(value)
    max_shape = 9 if target in {"th06", "th07"} else 20
    return str(min(max(number, 0), max_shape))


def compile_th08_macro(e: BulletEmitter, target: str) -> str:
    mode = e.aim.get("mode") or aim_mode_name(str(v(e.aim.get("mode_raw"), "1")))
    opcode = {
        "aimed_fan": 96,
        "fan": 97,
        "aimed_ring": 98,
        "ring": 99,
        "offset_aimed_ring": 100,
        "offset_ring": 101,
        "random_angle": 102,
        "random_speed": 103,
        "random_angle_speed": 104,
    }.get(mode, 97)
    style = clamp_old_shape(old_macro_int(e.appearance.get("style"), "0"), target)
    color = old_macro_int(e.appearance.get("color"), "0")
    ways = old_macro_int(e.count.get("ways"), "1")
    layers = old_macro_int(e.count.get("layers"), "1")
    speed_max = old_macro_float(e.speed.get("first"), "1.0f")
    speed_min = old_macro_float(e.speed.get("step", e.speed.get("last_or_step")), speed_max)
    angle = old_macro_float(e.aim.get("base_angle"), "0.0f")
    angle_step = old_macro_float(e.aim.get("angle_step"), "0.0f")
    flags = old_macro_int(e.flags.get("raw"), "0")
    lines = [f"// bullet lowering {e.family} -> {target}: macro opcode ins_{opcode}; semantic verification required"]
    for transform in e.transforms:
        if transform.raw_opcode == 111 and len(transform.raw_args) == 7:
            lines.append(f"ins_111({', '.join(str(arg) for arg in transform.raw_args)});")
        elif transform.raw_opcode in {409, 509, 609, 610, 611, 612}:
            lines.append(f"// transform not representable in {target} macro backend: ins_{transform.raw_opcode}({', '.join(str(arg) for arg in transform.raw_args)});")
    # TH06-08 macro order is minspeed, maxspeed; TH10+ slot order stores first/max then last/min.
    lines.append(f"ins_{opcode}({style}, {color}, {ways}, {layers}, {speed_min}, {speed_max}, {angle}, {angle_step}, {flags});")
    return "\n".join(lines)


def compile_th10_slot(e: BulletEmitter, target: str) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style_value = e.appearance.get("style")
    color_value = e.appearance.get("color")
    ways_value = e.count.get("ways")
    layers_value = e.count.get("layers")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    speed_value = e.speed.get("first")
    speed_step_value = e.speed.get("step", e.speed.get("last_or_step", "0.0f"))
    start_opcode = 401 if e.fire_lines and e.raw and e.raw[0].opcode == 401 else 400
    lines = [f"// bullet lowering {e.family} -> {target}: slot backend; semantic verification required"]
    lines.append(f"ins_{start_opcode}({emitter_id});")
    lines.extend(emit_instruction_with_ranked_args(407, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(402, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    lines.extend(emit_instruction_with_ranked_args(406, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(404, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    lines.extend(emit_instruction_with_ranked_args(405, [emitter_id, speed_value, speed_step_value], ["0", "1.0f", "0.0f"]))
    append_sound_lines(lines, target, e, str(emitter_id))
    for transform in e.transforms:
        if transform.raw_opcode == 409 and len(transform.raw_args) == 8:
            lines.append(f"ins_409({', '.join(str(arg) for arg in transform.raw_args)});")
        elif transform.raw_opcode in {509, 609, 610, 611, 612}:
            converted = convert_transform_to_th10(transform.raw_opcode, [str(arg) for arg in transform.raw_args])
            if converted:
                lines.append(f"ins_409({', '.join(converted)});")
            else:
                lines.append(f"// transform not representable in {target} slot backend: ins_{transform.raw_opcode}({', '.join(str(arg) for arg in transform.raw_args)});")
    if not e.fire_lines:
        lines.append(f"// source emitter had no explicit fire line; add ins_401({emitter_id}) at call site if needed")
    elif start_opcode != 401:
        lines.append(f"ins_401({emitter_id});")
    return "\n".join(lines)


def convert_transform_to_th10(opcode: int, args: list[str]) -> list[str] | None:
    if opcode == 409 and len(args) == 8:
        return args
    if opcode == 509 and len(args) == 8:
        return args
    if opcode == 609 and len(args) == 8:
        return args
    if opcode in {610, 612} and len(args) >= 12:
        return [args[0], args[1], args[2], args[3], args[4], args[5], args[8], args[9]]
    if opcode == 611 and len(args) >= 7:
        return [args[0], "0", args[1], args[2], args[3], args[4], args[5], args[6]]
    return None


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
