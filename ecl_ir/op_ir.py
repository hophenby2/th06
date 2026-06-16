from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

from .reference import opcode_info, opcode_reference, opcode_signature
from .semantics import generation_for_game

DOMAIN_RANGES = (
    ("flow", range(0, 100)),
    ("enemy", range(256, 400)),
    ("movement", range(300, 500)),
    ("unit", range(400, 600)),
    ("bullet", range(500, 700)),
    ("laser", range(600, 800)),
)

OVERRIDE_DOMAIN_BY_NAME = {
    "etNew": "bullet", "etOn": "bullet", "etSprite": "bullet", "etOffset": "bullet", "etAngle": "bullet",
    "etSpeed": "bullet", "etCount": "bullet", "etAim": "bullet", "etSound": "bullet", "etEx": "bullet",
    "etExSet": "bullet", "etExSet2": "bullet", "etEx2": "bullet", "etClearAll": "bullet", "etCopy": "bullet",
    "etCancel": "bullet", "etClear": "bullet", "etSpeedR3": "bullet", "etSpeedR5": "bullet", "etSpeedR2": "bullet",
    "etCountR3": "bullet", "etCountR5": "bullet", "etCountR2": "bullet", "angleToPlayer": "bullet", "etSpeedD": "bullet",
    "etCountD": "bullet", "etOffsetRad": "bullet", "etDist": "bullet", "etOffsetAbs": "bullet",
    "laserNew": "laser", "laserTiming": "laser", "laserOn": "laser", "laserStOn": "laser", "laserOnA": "laser", "laserOnA2": "laser", "laserOffset": "laser",
    "laserTrajectory": "laser", "laserStLength": "laser", "laserStWidth": "laser", "laserStAngle": "laser",
    "laserStRotation": "laser", "laserStEnd": "laser", "laserCuOn": "laser",
    "lifeSet": "boss", "setBoss": "boss", "timerReset": "boss", "setInterrupt": "boss", "setTimeout": "boss",
    "spellEnd": "boss", "setChapter": "boss", "spell": "boss", "spell2": "boss", "spell3": "boss",
    "bombShield": "unit", "gameSpeed": "unit", "rankF2": "unit",
}

OP_ALIASES = {
    "lifeset": "boss.life_set",
    "setboss": "boss.set_boss",
    "timerreset": "boss.timer_reset",
    "setinterrupt": "boss.set_interrupt",
    "settimeout": "boss.set_timeout",
    "spellend": "boss.spell_end",
    "spell_ex": "boss.spell_ex",
    "spell_unused": "boss.spell_unused",
    "setchapter": "boss.set_chapter",
    "anm_select": "anm.select",
    "anm_set_sprite": "anm.set_sprite",
    "anm_set_main": "anm.set_main",
    "anm_play": "anm.play",
    "anm_selected_play": "anm.selected_play",
    "anm_play_abs": "anm.play_abs",
    "anm_play_high": "anm.play_high",
    "anm_play_rotate": "anm.play_rotate",
    "enm_create": "enemy.create",
    "enm_create_a": "enemy.create_abs",
    "enm_create_m": "enemy.create_mirror",
    "enm_create_am": "enemy.create_abs_mirror",
    "enm_create_f": "enemy.create_func",
    "enm_create_af": "enemy.create_abs_func",
    "enm_create_mf": "enemy.create_mirror_func",
    "enm_create_amf": "enemy.create_abs_mirror_func",
    "enm_create270": "enemy.create_legacy270",
    "enm_maple_enemy": "enemy.create_maple",
    "move_pos": "movement.position.set",
    "move_pos_time": "movement.position.tween",
    "move_pos_rel": "movement.position_rel.set",
    "move_pos_rel_time": "movement.position_rel.tween",
    "move_vel": "movement.velocity.set",
    "move_vel_time": "movement.velocity.tween",
    "move_vel_rel": "movement.velocity_rel.set",
    "move_vel_rel_time": "movement.velocity_rel.tween",
    "move_circle": "movement.circle.set",
    "move_circle_time": "movement.circle.tween",
    "move_circle_rel": "movement.circle_rel.set",
    "move_circle_rel_time": "movement.circle_rel.tween",
    "move_ellipse": "movement.ellipse.set",
    "move_ellipse_time": "movement.ellipse.tween",
    "move_ellipse_rel": "movement.ellipse_rel.set",
    "move_ellipse_rel_time": "movement.ellipse_rel.tween",
    "move_bezier": "movement.bezier",
    "move_bezier_rel": "movement.bezier_rel",
    "move_reset": "movement.reset",
    "et_new": "bullet.et_new",
    "et_on": "bullet.fire",
    "et_sprite": "bullet.sprite",
    "et_offset": "bullet.offset",
    "et_angle": "bullet.angle",
    "et_speed": "bullet.speed",
    "et_count": "bullet.count",
    "et_aim": "bullet.aim",
    "et_sound": "bullet.sound",
    "et_ex": "bullet.transform",
    "et_ex_set": "bullet.transform_set",
    "et_ex_set2": "bullet.transform_set2",
    "et_ex2": "bullet.transform2",
    "et_clear_all": "bullet.clear_all",
    "et_copy": "bullet.copy",
    "et_cancel": "bullet.cancel_radius",
    "et_clear": "bullet.clear_radius",
    "et_speed_d": "bullet.speed_by_difficulty",
    "et_count_d": "bullet.count_by_difficulty",
    "et_dist": "bullet.distance",
    "laser_new": "laser.new",
    "laser_timing": "laser.timing",
    "laser_on": "laser.on",
    "laser_st_on": "laser.straight_on",
    "laser_on_a": "laser.on_aimed",
    "laser_on_a2": "laser.on_aimed2",
    "laser_offset": "laser.offset",
    "laser_trajectory": "laser.trajectory",
    "laser_st_length": "laser.length",
    "laser_st_width": "laser.width",
    "laser_st_angle": "laser.angle",
    "laser_st_rotation": "laser.rotation",
    "laser_st_end": "laser.end",
    "laser_cu_on": "laser.curve_on",
    "set_hurtbox": "unit.set_hurtbox",
    "set_hitbox": "unit.set_hitbox",
    "hitbox_set": "unit.set_hitbox",
    "hurtbox_set": "unit.set_hurtbox",
    "flag_set": "unit.flag_set",
    "flag_clear": "unit.flag_clear",
    "drop_clear": "unit.drop_clear",
    "drop_extra": "unit.drop_extra",
    "drop_area": "unit.drop_area",
    "drop_items": "unit.drop_items",
    "drop_items_sp": "unit.drop_items_sp",
    "drop_main": "unit.drop_main",
    "set_invuln": "unit.set_invuln",
    "play_sound": "unit.play_sound",
    "dialog_read": "unit.dialog_read",
    "dialog_wait": "unit.dialog_wait",
    "boss_wait": "unit.boss_wait",
    "diff_i": "unit.diff_i",
    "diff_f": "unit.diff_f",
    "diff_wait": "unit.diff_wait",
    "no_hitbox_dur": "unit.no_hitbox_dur",
    "flag_mirror": "unit.flag_mirror",
    "hitbox_rotate": "unit.hitbox_rotate",
    "life_marker": "unit.life_marker",
    "laser_cancel": "unit.laser_cancel",
    "death_wait": "unit.death_wait",
    "stars": "unit.stars",
    "set_screen_shake": "unit.set_screen_shake",
    "func_set": "unit.func_set",
    "call_std": "unit.call_std",
    "stage_logo": "unit.stage_logo",
    "bomb_shield": "unit.bomb_shield",
    "game_speed": "unit.game_speed",
    "rank_f2": "unit.rank_f2",
    "z_index": "unit.z_index",
    "hit_sound": "unit.hit_sound",
    "fog": "unit.fog",
    "move_set_mirror": "movement.move_set_mirror",
    "life_set": "boss.life_set",
    "set_boss": "boss.set_boss",
    "timer_reset": "boss.timer_reset",
    "set_interrupt": "boss.set_interrupt",
    "set_timeout": "boss.set_timeout",
    "spell_end": "boss.spell_end",
    "set_chapter": "boss.set_chapter",
    "spell": "boss.spell",
    "spell2": "boss.spell2",
    "spell3": "boss.spell3",
    "func_set2": "unit.func_set2",
    "call_async": "flow.call_async",
    "et_protect_range": "unit.et_protect_range",
}

OP_KEY_PREFIX_BY_DOMAIN = {
    "flow": "flow",
    "enemy": "enemy",
    "movement": "movement",
    "unit": "unit",
    "bullet": "bullet",
    "laser": "laser",
    "boss": "boss",
}


@dataclass(frozen=True)
class OpSpec:
    key: str
    domain: str
    name: str
    by_game: dict[str, int]
    signatures: dict[str, str]


def snake_name(name: str) -> str:
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text or "unknown"


def domain_for(game: str, opcode: int, name: str) -> str:
    if name in OVERRIDE_DOMAIN_BY_NAME:
        return OVERRIDE_DOMAIN_BY_NAME[name]
    if name.startswith("move"):
        return "movement"
    if name.startswith("anm"):
        return "anm"
    if name.startswith("enm"):
        return "enemy"
    for domain, span in DOMAIN_RANGES:
        if opcode in span:
            return domain
    return "raw"


def op_key_for_name(game: str, opcode: int, name: str) -> str:
    domain = domain_for(game, opcode, name)
    snake = snake_name(name)
    aliased = OP_ALIASES.get(snake)
    if aliased:
        return aliased
    prefix = OP_KEY_PREFIX_BY_DOMAIN.get(domain, domain)
    if snake.startswith(prefix + "_"):
        snake = snake[len(prefix) + 1:]
    return f"{prefix}.{snake}"


def op_key_for_opcode(game: str, opcode: int) -> str:
    if game.lower() == "th12" and opcode == 422:
        return "boss.spell_ex"
    info = opcode_info(game, opcode)
    if info and info.name:
        return op_key_for_name(game, opcode, info.name)
    return f"raw.{generation_for_game(game)}.{opcode}"


@lru_cache(maxsize=1)
def op_specs() -> dict[str, OpSpec]:
    specs: dict[str, OpSpec] = {}
    for game, table in opcode_reference().items():
        for opcode, info in table.items():
            if not info.name:
                continue
            key = op_key_for_name(game, opcode, info.name)
            old = specs.get(key)
            by_game = dict(old.by_game) if old else {}
            signatures = dict(old.signatures) if old else {}
            by_game[game] = opcode
            signatures[game] = info.signature
            specs[key] = OpSpec(key=key, domain=domain_for(game, opcode, info.name), name=info.name, by_game=by_game, signatures=signatures)
    return specs


def target_opcode_for_op_key(op_key: str, target: str) -> int | None:
    spec = op_specs().get(op_key)
    if not spec:
        return None
    target = target.lower()
    if target in spec.by_game:
        return spec.by_game[target]
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        for fallback in (target, "th15", "th13"):
            if fallback in spec.by_game:
                return spec.by_game[fallback]
    if target in {"th10", "th11"}:
        for fallback in (target, "th11", "th10"):
            if fallback in spec.by_game:
                return spec.by_game[fallback]
    if target in {"th06", "th07", "th08"}:
        return spec.by_game.get("th08")
    return None


SOURCE_SPECIFIC_DROP_OP_KEYS = {
    "unit.unknown569", "raw.spec1", "raw.spec2", "laser.debug700", "movement.unknown444",
    "enemy.create_maple", "anm.reset", "bullet.distance",
    "raw.eff_create", "raw.eff_create_angle", "raw.card_eff", "raw.timer_threshold", "raw.ins_129",
    "raw.et_on_auto_delay", "flow.familiar_create", "flow.familiar_create_f", "flow.familiar_create_a",
    "flow.trail_familiar_set", "anm.play_attack", "movement.move_rand_time", "flow.ins_79",
    "anm.set_ex", "anm.set_boss_ex", "movement.move_circle_change", "movement.move_accel", "movement.move_curve",
    "raw.et_delay", "raw.et_on_auto", "raw.set_life_bar", "raw.ins_153", "raw.timer_set", "raw.set_lives",
    "raw.life_threshold", "flow.float_time", "flow.math_circle_pos", "flow.inc", "raw.ins_173", "raw.ins_184",
    "flow.math_angle", "flow.math_distance", "flow.et_protect_range", "raw.val_set", "raw.player_nullify", "anm.familiar",
    "bullet.transform", "bullet.transform2",
}

OLD_TARGET_PRESENTATION_HELPERS = {
    "anm.on_et", "anm.rotate", "unit.z_index", "unit.hit_sound", "unit.fog",
    "unit.func_set", "movement.move_set_mirror", "unit.call_std", "unit.stage_logo",
    "laser.timing", "laser.angle",
}


def legacy_stack_vm_policy(key: str) -> dict[str, object] | None:
    binary_ops = {
        "flow.iadd": (50, 43), "flow.isub": (52, 43), "flow.imul": (54, 43), "flow.idiv": (56, 43), "flow.imod": (58, 43),
        "flow.fadd": (51, 45), "flow.fsub": (53, 45), "flow.fmul": (55, 45), "flow.fdiv": (57, 45), "flow.fmod": (58, 45),
    }
    set_binary_ops = {
        "flow.iset_add": (50, 43), "flow.iset_sub": (52, 43), "flow.iset_mul": (54, 43), "flow.iset_div": (56, 43), "flow.iset_mod": (58, 43),
        "flow.fset_add": (51, 45), "flow.fset_sub": (53, 45), "flow.fset_mul": (55, 45), "flow.fset_div": (57, 45), "flow.fset_mod": (58, 45),
    }
    if key == "flow.iset":
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 1}, {"ins": 43, "args": ["$0"]}], "reason": "legacy integer set lowered through target stack VM"}
    if key == "flow.fset":
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 1}, {"ins": 45, "args": ["$0"]}], "reason": "legacy float set lowered through target stack VM"}
    if key in binary_ops:
        op, setter = binary_ops[key]
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 0}, {"push_arg": 1}, {"ins": op, "args": []}, {"ins": setter, "args": ["$0"]}], "reason": "legacy binary expression lowered through target stack VM"}
    if key in set_binary_ops:
        op, setter = set_binary_ops[key]
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 1}, {"push_arg": 2}, {"ins": op, "args": []}, {"ins": setter, "args": ["$0"]}], "reason": "legacy set-binary expression lowered through target stack VM"}
    unary_float_ops = {"flow.fset_sin": 79, "flow.fset_cos": 80}
    if key in unary_float_ops:
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 1}, {"ins": unary_float_ops[key], "args": []}, {"ins": 45, "args": ["$0"]}], "reason": "legacy unary float expression lowered through target stack VM"}
    if key == "flow.inc":
        return {"strategy": "stack_vm_sequence", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "sequence": [{"push_arg": 0}, {"push": "1"}, {"ins": 50, "args": []}, {"ins": 43, "args": ["$0"]}], "reason": "legacy integer increment lowered through target stack VM"}
    if key == "flow.dec":
        return {"strategy": "emit_raw_ins", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "opcode": 78, "args": ["$0"], "reason": "legacy decrement maps to target deci"}
    if key == "flow.norm_rad":
        return {"strategy": "emit_raw_ins", "source_generations": ["th06_th08"], "target_generations": ["th10_th11", "th12", "th13_plus"], "opcode": 82, "args": ["$0"], "reason": "legacy normalize-radian maps to target validRad"}
    compare_ops = {
        "flow.jmp_equ": 59, "flow.jmp_equ_f": 60,
        "flow.jmp_neq": 61, "flow.jmp_neq_f": 62,
        "flow.jmp_lss": 63, "flow.jmp_lss_f": 64,
        "flow.jmp_leq": 65, "flow.jmp_leq_f": 66,
        "flow.jmp_gre": 67, "flow.jmp_gre_f": 68,
        "flow.jmp_geq": 69, "flow.jmp_geq_f": 70,
    }
    if key in compare_ops:
        return {
            "strategy": "legacy_conditional_jump",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "compare_opcode": compare_ops[key],
            "target_op_key": "flow.jmp_neq",
            "reason": "legacy conditional jump embeds comparison; target uses compare stack then conditional jump",
        }
    if key == "flow.loop":
        return {
            "strategy": "legacy_loop_jump",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "decrement_opcode": 78,
            "target_op_key": "flow.jmp_neq",
            "reason": "legacy loop embeds decrement and conditional branch",
        }
    return None


def op_lowering_policy(key: str, args: list[str]) -> dict[str, object] | None:
    if legacy_policy := legacy_stack_vm_policy(key):
        return legacy_policy
    if key == "boss.spell_ex":
        return {
            "strategy": "emit_target_op",
            "reason": "extended spell descriptor is a shared boss phase header in TH10+",
            "target_generations": ["th13_plus"],
            "target_op_key": "boss.spell_ex",
            "arg_policy": {"take_first": 4},
        }
    if key == "enemy.byakuren_butterfly":
        return {
            "strategy": "catalog_sprite",
            "reason": "boss_butterfly_visual_helper_maps_to_target_familiar_sprite",
            "target_generations": ["th13_plus"],
            "catalog_role": "boss",
            "catalog_purpose": "familiar",
            "catalog_kind": "sprite",
            "slot_arg_index": 0,
            "metadata_arg_names": {"1": "switch"},
        }
    if key in {"movement.bomb_shield", "unit.bomb_shield"}:
        return {
            "strategy": "emit_target_op",
            "reason": "TH12 bomb shield movement-domain opcode maps to TH13+ unit bomb shield",
            "target_generations": ["th13_plus"],
            "target_op_key": "unit.bomb_shield",
            "arg_policy": {"defaults": ["1", "0"], "int_indices": [1]},
        }
    if key in {"movement.game_speed", "unit.game_speed"}:
        return {
            "strategy": "emit_target_op",
            "reason": "game speed is a unit/runtime property in TH13+",
            "target_generations": ["th13_plus"],
            "target_op_key": "unit.game_speed",
        }
    if key == "movement.move_dir":
        return {
            "strategy": "emit_target_op",
            "reason": "TH06-08 directional movement aliases target velocity.set",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "target_op_key": "movement.velocity.set",
        }
    if key == "movement.move_dir_time":
        return {
            "strategy": "emit_target_op",
            "reason": "TH06-08 timed directional movement aliases target velocity.tween",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "target_op_key": "movement.velocity.tween",
        }
    if key == "anm.set":
        return {
            "strategy": "emit_target_op_sequence",
            "reason": "TH06-08 combined ANM set aliases target select+set_main",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "sequence": [
                {"target_op_key": "anm.select", "args": ["0"]},
                {"target_op_key": "anm.set_main", "args": ["0", "$0"]},
            ],
        }
    if key == "anm.set_sprite":
        return {
            "strategy": "emit_target_op",
            "reason": "TH06-08 sprite ANM set aliases target anm.set_sprite",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "target_op_key": "anm.set_sprite",
        }
    if key in {"anm.set_slot", "anm.set_boss_slot"}:
        return {
            "strategy": "emit_target_op",
            "reason": "TH06-08 slotted ANM set aliases target anm.set_sprite",
            "source_generations": ["th06_th08"],
            "target_generations": ["th10_th11", "th12", "th13_plus"],
            "target_op_key": "anm.set_sprite",
        }
    if key in {"unit.unknown531", "unit.property.31"}:
        return {
            "strategy": "approximate",
            "reason": "TH12 special body-hitbox flag has no verified TH13+ equivalent",
            "target_generations": ["th13_plus"],
            "approximation": "metadata_only_no_runtime_effect",
        }
    if key == "flow.debug22":
        return {"strategy": "drop", "reason": "debug_only"}
    if key in SOURCE_SPECIFIC_DROP_OP_KEYS:
        return {"strategy": "drop", "reason": "source_specific_runtime_helper"}
    if key == "flow.fset_rand_sign":
        return {"strategy": "approximate", "reason": "random_sign_unavailable", "approximation": "positive_magnitude"}
    if key == "unit.death_wait":
        return {"strategy": "approximate", "reason": "target_without_death_wait", "target_generations": ["th13_plus"], "approximation": "no_op"}
    if key == "boss.set_interrupt" and args and str(args[0]) == "-1":
        return {"strategy": "drop", "reason": "disabled_interrupt"}
    if key == "flow.call_async" and args and str(args[-1]) == "-1":
        return {"strategy": "drop", "reason": "disabled_async_call"}
    if key in OLD_TARGET_PRESENTATION_HELPERS:
        return {"strategy": "drop", "reason": "unsupported_presentation_helper", "target_generations": ["th10_th11"]}
    if key == "enemy.create_legacy270":
        return {
            "strategy": "emit_target_op",
            "target_op_key": "enemy.create_func",
            "reason": "TH10/11 enmCreate270 is used as background/helper enemy create; argument 3 is a legacy runtime flag not present in target func-create",
            "source_generations": ["th10_th11"],
            "target_generations": ["th12", "th13_plus"],
            "arg_policy": {"indices": [0, 1, 2, 4, 5, 6]},
        }
    if key == "laser.on_aimed":
        return {
            "strategy": "legacy_laser_on_aimed",
            "reason": "TH10/11 laserOnA approximated as target straight laser with same angle/length/width/timing",
            "source_generations": ["th10_th11"],
            "target_generations": ["th12", "th13_plus"],
        }
    return None


def op_event(game: str, opcode: int, args: list[str], line: int | None = None, difficulty: str | None = None) -> dict[str, object]:
    info = opcode_info(game, opcode)
    key = op_key_for_opcode(game, opcode)
    domain = "boss" if key == "boss.spell_ex" else domain_for(game, opcode, info.name if info else "")
    event = {
        "op_key": key,
        "domain": domain,
        "source_game": game,
        "source_opcode": opcode,
        "source_name": info.name if info else "",
        "signature": info.signature if info else "",
        "args": list(args),
        "line": line,
        "difficulty": difficulty,
    }
    policy = op_lowering_policy(key, list(args))
    if policy:
        event["lowering_policy"] = policy
    return event
