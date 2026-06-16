from __future__ import annotations

from collections import defaultdict
import re
from typing import Iterable

from .lifter import lift_program as lift_bullets
from .model import (
    AnimationOp,
    AutoBulletTimer,
    EnemyVisualOp,
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
    ModeOp,
    Program,
    UnitFlagOp,
)
from .op_ir import op_event, op_key_for_opcode
from .program_lifter import lift_program_adapters
from .semantics import bullet_transform_mode_semantic, remap_bullet_transform_mode, remap_unit_flag_mask, unit_flag_semantics
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


def source_stage_kind(program: Program) -> str:
    source = program.source.replace("\\", "/").lower()
    name = source.rsplit("/", 1)[-1]
    if any(token in name for token in ("boss", "mbs", "bs")):
        return "boss"
    if "stage06" in source and "/th12/" in source:
        return "th12_stage06"
    return "stage"


def anm_role_for_context(program: Program, func: Function) -> str:
    stage_kind = source_stage_kind(program)
    if stage_kind == "boss":
        return "boss"
    return "stage"


def annotate_animation_policy(obj: AnimationOp, program: Program, func: Function, op_name: str, ins: Instruction) -> None:
    role = anm_role_for_context(program, func)
    obj.fields.setdefault("role", role)
    obj.fields.setdefault("target_policy", {})
    if program.game in {"th10", "th11"} and role == "stage" and op_name == "anmSetMain" and len(ins.args) == 2:
        script = a(ins, 1, "")
        obj.fields["target_policy"]["stage_enemy_wrapper_anm"] = {
            "semantic": "stage_enemy_wrapper_anm",
            "targets": ["th13", "th14", "th15", "th16", "th17", "th18"],
            "source_slot": a(ins, 0, "0"),
            "source_script": script,
            "native_combos": {
                "45": {"bank": "2", "main_slot": "0", "main_script": "0", "sprite_slot": "1", "sprite_script": ""},
                "46": {"bank": "2", "main_slot": "0", "main_script": "5", "sprite_slot": "1", "sprite_script": ""},
                "47": {"bank": "2", "main_slot": "0", "main_script": "35", "sprite_slot": "1", "sprite_script": "93"},
                "48": {"bank": "2", "main_slot": "0", "main_script": "40", "sprite_slot": "1", "sprite_script": "93"},
            },
        }
    if role == "boss" and op_name == "anmSetSprite" and len(ins.args) == 2 and a(ins, 0, "") in {str(slot) for slot in range(3, 13)}:
        obj.fields["target_policy"]["boss_aux_sprite"] = {
            "semantic": "boss_aux_sprite",
            "source_slot": a(ins, 0, "0"),
            "source_script": a(ins, 1, "0"),
            "catalog_role": "boss",
            "catalog_purpose": "familiar",
            "catalog_kind": "sprite",
        }
    if program.game == "th12" and source_stage_kind(program) == "th12_stage06" and func.name == "MBoss":
        if op_name == "anmSelect" and ins.args == ["2"]:
            obj.fields["target_policy"]["drop_for_target"] = {"targets": ["th15"], "reason": "th12_stage06_mboss_boss_bank_select"}
        if op_name == "anmSetSprite" and len(ins.args) == 2 and ins.args[1] in {"46", "47"}:
            obj.fields["target_policy"]["drop_for_target"] = {"targets": ["th15"], "reason": f"th12_stage06_mboss_boss_bank_sprite_{ins.args[1]}"}
    if op_name == "anmPlayAttack":
        obj.fields["target_policy"]["legacy_attack_animation"] = {"semantic": "legacy_attack_animation", "fallback_op_key": "anm.play", "args": ["0", "0"]}


def annotate_enemy_policy(obj: EnemyOp, program: Program, func: Function, ins: Instruction) -> None:
    sub = a(ins, 0, "").strip().strip('"')
    obj.fields.setdefault("target_policy", {})
    if program.game == "th10" and sub == "MapleEnemy":
        obj.fields["semantic"] = "visual_helper_enemy"
        obj.fields["target_policy"]["omit_runtime_entity"] = {
            "targets": ["th13", "th14", "th15", "th16", "th17", "th18"],
            "reason": "maple_enemy_visual_helper",
        }
    if program.game == "th12" and sub == "BossCard6_atLine":
        obj.fields.update({
            "semantic": "flying_bowl_line_visual",
            "target_behavior": "omit_visual_helper",
            "reason": "visual line helper; bullet motion is represented by transforms on the linked emitter",
        })
        obj.fields["target_policy"]["omit_runtime_entity"] = {"targets": ["th13", "th14", "th15", "th16", "th17", "th18"], "reason": "flying_bowl_line_visual"}


def lift_all_objects(program: Program) -> list[object]:
    objects: list[object] = []
    objects.extend(lift_program_adapters(program))
    objects.extend(lift_bullets(program))
    objects.extend(lift_timelines(program))
    for func in program.functions:
        objects.extend(lift_lasers(program, func))
        objects.extend(lift_movements(program, func))
        objects.extend(lift_unit_flags(program, func))
        objects.extend(lift_modes(program, func))
        objects.extend(lift_animation_enemy(program, func))
        objects.extend(lift_boss_patterns(program, func))
        objects.extend(lift_high_level_legacy_objects(program, func))
    return sorted(objects, key=lambda obj: (getattr(obj, "function", ""), getattr(obj, "source_line", 0), getattr(obj, "kind", "")))



def lift_unit_flags(program: Program, func: Function) -> list[UnitFlagOp]:
    opcodes = {
        "th10": {322: "unit.flag_set", 323: "unit.flag_clear"},
        "th11": {322: "unit.flag_set", 323: "unit.flag_clear"},
        "th12": {402: "unit.flag_set", 403: "unit.flag_clear"},
        "th13": {502: "unit.flag_set", 503: "unit.flag_clear"},
        "th14": {502: "unit.flag_set", 503: "unit.flag_clear"},
        "th15": {502: "unit.flag_set", 503: "unit.flag_clear"},
        "th16": {502: "unit.flag_set", 503: "unit.flag_clear"},
        "th17": {502: "unit.flag_set", 503: "unit.flag_clear"},
        "th18": {502: "unit.flag_set", 503: "unit.flag_clear"},
    }.get(program.game, {})
    objects: list[UnitFlagOp] = []
    for ins in func.body:
        if ins.opcode not in opcodes or not ins.args:
            continue
        op_key = opcodes[ins.opcode]
        raw_flag = a(ins, 0, "0")
        obj = make_obj(UnitFlagOp, program, func, ins, "unit_flag", raw_flag)
        targets = {target: remap_unit_flag_mask(program.game, target, raw_flag) for target in ("th10", "th11", "th12", "th13", "th15")}
        obj.fields.update({
            "semantic": "unit_flag",
            "op_key": op_key,
            "operation": "set" if op_key.endswith("flag_set") else "clear",
            "flag": unit_flag_semantics(program.game, op_key, raw_flag, func.name),
            "targets": targets,
            "args": ins.args,
            "difficulty": ins.difficulty,
        })
        objects.append(obj)
    return objects


def movement_mode_semantic(raw_mode: str) -> dict[str, str]:
    return {
        "0": {"name": "linear_or_default", "target": "0"},
        "1": {"name": "ease_or_smooth", "target": "1"},
        "4": {"name": "decelerate_or_curve", "target": "4"},
        "7": {"name": "legacy_exit_accel", "target": "0"},
        "9": {"name": "special_curve", "target": "9"},
    }.get(str(raw_mode), {"name": f"mode_{raw_mode}", "target": str(raw_mode)})


def lift_modes(program: Program, func: Function) -> list[ModeOp]:
    mode_arg_by_opcode = {
        **{op: 1 for op in (281, 283, 285, 287, 289, 291, 301, 303, 305, 306)},
        **{op: 1 for op in (301, 303, 305, 307, 309, 311, 321, 323, 325, 326)},
        **{op: 1 for op in (401, 403, 405, 407, 409, 411, 421, 423, 425, 426, 441, 443, 445, 447)},
    }
    bullet_transform_mode_arg_by_opcode = {409: 3, 509: 3, 609: 3}
    mirror_opcode = {"th12": 324, "th13": 424, "th14": 424, "th15": 424, "th16": 424, "th17": 424, "th18": 424}.get(program.game)
    objects: list[ModeOp] = []
    for ins in func.body:
        if ins.opcode == mirror_opcode and ins.args:
            obj = make_obj(ModeOp, program, func, ins, "mirror_mode", a(ins, 0, "0"))
            obj.fields.update({"semantic": "mirror_mode", "op_key": "movement.mirror_mode", "mode": {"raw": a(ins, 0, "0"), "name": "mirror_on" if a(ins, 0, "0") != "0" else "mirror_off"}, "args": ins.args, "difficulty": ins.difficulty})
            objects.append(obj)
            continue
        transform_index = bullet_transform_mode_arg_by_opcode.get(ins.opcode)
        if transform_index is not None and len(ins.args) > transform_index:
            raw_mode = a(ins, transform_index, "0")
            semantic = bullet_transform_mode_semantic(program.game, raw_mode)
            obj = make_obj(ModeOp, program, func, ins, "bullet_transform_mode", raw_mode)
            obj.fields.update({
                "semantic": "bullet_transform_mode",
                "op_key": op_key_for_opcode(program.game, ins.opcode),
                "mode": {
                    "raw": raw_mode,
                    "name": semantic,
                    "target_th12": remap_bullet_transform_mode(program.game, "th12", raw_mode),
                    "target_th15": remap_bullet_transform_mode(program.game, "th15", raw_mode),
                },
                "mode_arg_index": transform_index,
                "emitter_id": a(ins, 0, "0"),
                "transform_slot": a(ins, 1, "0"),
                "channel": a(ins, 2, "0"),
                "args": ins.args,
                "difficulty": ins.difficulty,
            })
            objects.append(obj)
            continue
        index = mode_arg_by_opcode.get(ins.opcode)
        if index is None or len(ins.args) <= index:
            continue
        raw_mode = a(ins, index, "0")
        obj = make_obj(ModeOp, program, func, ins, "movement_tween_mode", raw_mode)
        obj.fields.update({"semantic": "movement_tween_mode", "op_key": op_key_for_opcode(program.game, ins.opcode), "mode": {"raw": raw_mode, **movement_mode_semantic(raw_mode)}, "mode_arg_index": index, "args": ins.args, "difficulty": ins.difficulty})
        objects.append(obj)
    return objects


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
        fields["target_policy"] = {"visual_effect": {"strategy": "anm.play", "target_op_key": "anm.play", "args": ["0", fields["effect"]["script_expr"]]}}
    elif ins.opcode == 140:
        fields["effect"] = {"source": "etama.anm", "script_expr": f"({a(ins, 0, '0')} + 28)", "amount": a(ins, 1, "1"), "color": a(ins, 2, "0"), "angle": a(ins, 3, "0.0f"), "unknown": ins.args[4:]}
        fields["target_policy"] = {"visual_effect": {"strategy": "anm.play_rotate", "target_op_key": "anm.play_rotate", "args": ["0", fields["effect"]["script_expr"], fields["effect"].get("angle", "0.0f")]}}


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
        fields["target_policy"] = {"familiar_spawn": {"strategy": "enemy_child_approximation", "preserve_focus_invulnerability_as_metadata": True}}
    elif ins.opcode == 83:
        fields["trail"] = {"enabled": a(ins, 0, "0")}
        fields["target_policy"] = {"trail_toggle": {"strategy": "metadata_only"}}
    elif ins.opcode == 174:
        fields["focus_animation"] = {"source": "etama.anm", "script_expr": f"({a(ins, 0, '0')} + 48)"}
        fields["target_policy"] = {"focus_animation": {"strategy": "anm.play", "target_op_key": "anm.play", "args": ["0", fields["focus_animation"]["script_expr"]]}}


def apply_legacy_auto_bullet(obj: AutoBulletTimer, ins: Instruction) -> None:
    semantics = {105: "auto_fire_interval", 106: "auto_fire_interval_random_initial_delay", 107: "defer_attribute_fire"}
    obj.fields.update({"semantic": semantics.get(ins.opcode, f"auto_bullet_{ins.opcode}"), "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    if ins.opcode in {105, 106}:
        obj.fields["timer"] = {"interval": a(ins, 0, "1"), "initial_delay": "random_0_interval" if ins.opcode == 106 else "none", "fire_mode": "current_bullet_attributes"}
        obj.fields["lowering_plan"] = {"strategy": "emit_single_fire_tick", "target_op_key": "bullet.fire"}
    else:
        obj.fields["timer"] = {"defer_attribute_fire": True}
        obj.fields["lowering_plan"] = {"strategy": "metadata_only", "reason": "target slot emitters are configured explicitly"}



def target_sub_name(value: object) -> str:
    text = str(value).strip()
    if text == "-1":
        return '""'
    if re.fullmatch(r"\d+", text):
        return f'"Sub{text}"'
    return text


def float_literal(value: object) -> str:
    text = str(value).strip()
    if text.endswith("f"):
        return text
    if re.fullmatch(r"[-+]?\d+", text):
        return f"{text}.0f"
    if re.fullmatch(r"[-+]?\d+\.\d+", text):
        return f"{text}f"
    return text

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
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "boss.timer_reset", "args": [], "reason": "target timer reset approximates legacy upward timer set"}
    elif ins.opcode == 133:
        obj.fields["interrupt"] = {"trigger": "life_leq", "unknown": a(ins, 0, "0"), "life": a(ins, 1, "0"), "sub": a(ins, 2, "-1")}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "boss.set_interrupt", "args": ["0", a(ins, 1, "0"), "0", target_sub_name(a(ins, 2, "-1"))], "reason": "legacy life threshold interrupt"}
    elif ins.opcode == 134:
        obj.fields["interrupt"] = {"trigger": "timer_geq", "time": a(ins, 0, "0"), "sub": a(ins, 1, "-1")}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "boss.set_interrupt", "args": ["0", "0", a(ins, 0, "0"), target_sub_name(a(ins, 1, "-1"))], "reason": "legacy timer threshold interrupt"}
    elif ins.opcode == 148:
        obj.fields["lowering_plan"] = {"strategy": "target_by_generation", "plans": {"th12": {"target_op_key": "unit.life_hide", "args": []}, "th13_plus": {"target_op_key": "bullet.life_hide", "args": ["0"]}}, "reason": "visible life count approximated by target lifebar visibility controls"}
    elif ins.opcode == 158:
        obj.fields["life_bar"] = {"slot": a(ins, 0, "0"), "life_min": a(ins, 1, "0"), "life_max": a(ins, 2, "0"), "color": a(ins, 3, "0")}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "unit.life_marker", "args": [a(ins, 0, "0"), float_literal(a(ins, 1, "0")), a(ins, 3, "0")], "reason": "legacy lifebar color segment approximated as target life marker"}
    elif ins.opcode == 173:
        enabled = "1" if a(ins, 0, "1") != "0" else "0"
        obj.fields["lowering_plan"] = {"strategy": "target_by_generation", "plans": {"th12": {"target_op_key": "movement.bomb_shield", "args": [enabled, "0.0f"]}, "th13_plus": {"sequence": [{"target_op_key": "unit.bomb_shield", "args": [enabled, "0"]}, {"target_op_key": "unit.bomb_invuln", "args": ["0.0f" if enabled == "1" else "1.0f"]}]}}, "reason": "legacy bomb immunity state"}
    elif ins.opcode == 184:
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "unit.set_invuln", "args": ["0"], "reason": "unknown boss runtime state preserved as invulnerability boundary"}


def apply_legacy_motion_modifier(obj: MotionModifier, ins: Instruction) -> None:
    semantics = {
        67: "random_direction_tween",
        70: "angular_velocity",
        71: "linear_acceleration",
        74: "circle_speed_change",
        178: "random_direction_tween_variant",
    }
    semantic = semantics.get(ins.opcode, f"motion_modifier_{ins.opcode}")
    obj.fields.update({"semantic": semantic, "op_key": op_key_for_opcode(obj.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
    plans = {
        "random_direction_tween": {"strategy": "velocity_tween_neutral_angle", "target_op_key": "movement.velocity.tween"},
        "random_direction_tween_variant": {"strategy": "velocity_tween_neutral_angle", "target_op_key": "movement.velocity.tween"},
        "circle_speed_change": {"strategy": "circle_tween_approximation", "target_op_key": "movement.circle.tween"},
        "angular_velocity": {"strategy": "long_lived_circle_tween", "target_op_key": "movement.circle.tween"},
        "linear_acceleration": {"strategy": "long_lived_velocity_tween", "target_op_key": "movement.velocity.tween"},
    }
    if ins.opcode in {67, 178}:
        obj.fields["motion"] = {"time": a(ins, 0, "0"), "mode": a(ins, 1, "0"), "speed": a(ins, 2, "0.0f"), "direction": "random_player_bounded", "variant": ins.opcode == 178}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "movement.velocity.tween", "args": [a(ins, 0, "0"), a(ins, 1, "0"), "0.0f", a(ins, 2, "0.0f")], "reason": "bounded random direction approximated as neutral-angle velocity tween"}
    elif ins.opcode == 70:
        obj.fields["motion"] = {"angular_velocity": a(ins, 0, "0.0f")}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "movement.circle.tween", "args": ["999999", "0", a(ins, 0, "0.0f"), "0.0f", "0.0f"], "reason": "legacy per-frame angular velocity approximated as long-lived circle tween"}
    elif ins.opcode == 71:
        obj.fields["motion"] = {"acceleration": a(ins, 0, "0.0f")}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "movement.velocity.tween", "args": ["999999", "0", "0.0f", a(ins, 0, "0.0f")], "reason": "legacy per-frame acceleration approximated as long-lived velocity tween"}
    elif ins.opcode == 74:
        obj.fields["motion"] = {"time": a(ins, 0, "0"), "angular_velocity": a(ins, 1, "0.0f"), "radius_velocity": a(ins, 2, "0.0f"), "requires_circle_motion": True}
        obj.fields["lowering_plan"] = {"strategy": "emit_target_op", "target_op_key": "movement.circle.tween", "args": [a(ins, 0, "0"), "0", a(ins, 1, "0.0f"), "0.0f", a(ins, 2, "0.0f")], "reason": "legacy circle speed change approximated through target circle tween"}
    elif semantic in plans:
        obj.fields["lowering_plan"] = plans[semantic]


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
    elif program.game in {"th10", "th11"}:
        start_ops = {412, 413, 428, 429}
        laser_ops = {412, 413, 414, 415, 416, 417, 418, 419, 428, 429}
        family = "th10_th11"
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
    elif game == "th12":
        names = {
            601: "timing", 602: "on", 603: "straight_on", 604: "offset", 605: "trajectory",
            606: "length", 607: "width", 608: "angle", 609: "rotation", 610: "end", 611: "curve_on",
        }
    else:
        names = {
            412: "on_aimed", 413: "straight_on", 414: "unknown414", 415: "unknown415",
            416: "unknown416", 417: "unknown417", 418: "unknown418", 419: "unknown419",
            428: "on", 429: "straight_on2",
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
        movement_names = {
            280: "movePos", 281: "movePosTime", 282: "movePosRel", 283: "movePosRelTime",
            284: "moveVel", 285: "moveVelTime", 286: "moveVelRel", 287: "moveVelRelTime",
            288: "moveCircle", 289: "moveCircleTime", 290: "moveCircleRel", 291: "moveCircleRelTime",
            292: "moveRandom", 293: "moveRandomRel",
            300: "moveEllipse", 301: "moveEllipseTime", 302: "moveEllipseRel", 303: "moveEllipseRelTime",
            305: "moveBezier", 306: "moveBezierRel",
        }
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
        if len(ins.args) > 1 and op_name.endswith("Time"):
            obj.fields.setdefault("semantics", {})["mode"] = {"raw": ins.args[1], **movement_mode_semantic(ins.args[1])}
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



def stage_enemy_visual_from_script(script: int) -> dict[str, str] | None:
    mapping = {
        45: {"main_script": "0", "overlay_script": "", "drop_style": "2", "color": "blue"},
        46: {"main_script": "5", "overlay_script": "", "drop_style": "1", "color": "red"},
        47: {"main_script": "35", "overlay_script": "93", "drop_style": "3", "color": "green"},
        48: {"main_script": "40", "overlay_script": "93", "drop_style": "4", "color": "yellow"},
    }
    return mapping.get(script)


def lift_enemy_visuals(program: Program, func: Function) -> list[IRObject]:
    if program.game not in {"th10", "th11"}:
        return []
    objects: list[IRObject] = []
    body = func.body
    for index, ins in enumerate(body):
        if ins.opcode not in {259, 262} or len(ins.args) < 2:
            continue
        try:
            script = int(str(ins.args[1]).strip())
        except ValueError:
            continue
        semantic = stage_enemy_visual_from_script(script)
        if semantic is None:
            continue
        previous_select = next((body[pos] for pos in range(index - 1, -1, -1) if body[pos].opcode == 258), None)
        previous_drop = next((body[pos] for pos in range(index - 1, max(-1, index - 4), -1) if body[pos].opcode == 330), None)
        next_drop = next((body[pos] for pos in range(index + 1, min(len(body), index + 4)) if body[pos].opcode == 330), None)
        drop = next_drop or previous_drop
        if previous_select is None and drop is None:
            continue
        selected_bank = previous_select.args[0] if previous_select is not None and previous_select.args else "1"
        if str(selected_bank).strip() != "1":
            continue
        obj = make_obj(EnemyVisualOp, program, func, ins, "stage_enemy_visual", str(script))
        obj.raw = []
        if previous_select is not None and previous_select.line_no in {ins.line_no - 1, ins.line_no - 2}:
            obj.raw.append(previous_select)
            append_ir_op(obj, program.game, previous_select)
        if previous_drop is not None and previous_drop.line_no in {ins.line_no - 1, ins.line_no - 2}:
            obj.raw.append(previous_drop)
            append_ir_op(obj, program.game, previous_drop)
        obj.raw.append(ins)
        if obj.fields.get("ir_ops"):
            obj.fields["ir_ops"] = obj.fields["ir_ops"][-1:]
        append_ir_op(obj, program.game, ins)
        if next_drop is not None:
            obj.raw.append(next_drop)
            append_ir_op(obj, program.game, next_drop)
        obj.fields.update({
            "semantic": "stage_enemy_visual",
            "source_bank": selected_bank,
            "source_script": str(script),
            "source_set_op": "anm.set_sprite" if ins.opcode == 259 else "anm.set_main",
            "main_slot": "0",
            "main_script": semantic["main_script"],
            "overlay_slot": "1",
            "overlay_script": semantic["overlay_script"],
            "drop_style": str(drop.args[0]) if drop is not None and drop.args else semantic["drop_style"],
            "color": semantic["color"],
        })
        objects.append(obj)
    return objects

def lift_animation_enemy(program: Program, func: Function) -> list[IRObject]:
    objects: list[IRObject] = []
    objects.extend(lift_enemy_visuals(program, func))
    visual_covered_lines = {raw.line_no for obj in objects if getattr(obj, "kind", None) == "EnemyVisual" for raw in getattr(obj, "raw", [])}
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
        if ins.line_no in visual_covered_lines:
            continue
        if ins.opcode in animation:
            obj = make_obj(AnimationOp, program, func, ins, family)
            op_name = animation[ins.opcode]
            op_key = op_key_for_opcode(program.game, ins.opcode)
            obj.fields.update({"op": op_name, "op_key": op_key, "args": ins.args, "difficulty": ins.difficulty})
            if op_name in {"anmSetMain", "anmSetSprite"} and len(ins.args) >= 2:
                obj.fields["display"] = {
                    "kind": "main" if op_name == "anmSetMain" else "sprite",
                    "slot": ins.args[0],
                    "script": ins.args[1],
                }
            annotate_animation_policy(obj, program, func, op_name, ins)
            objects.append(obj)
        elif ins.opcode in enemy:
            obj = make_obj(EnemyOp, program, func, ins, family)
            obj.fields.update({"op": enemy[ins.opcode], "op_key": op_key_for_opcode(program.game, ins.opcode), "args": ins.args, "difficulty": ins.difficulty})
            obj.fields["create"] = enemy_create_semantics(program, func, ins, enemy[ins.opcode])
            annotate_enemy_policy(obj, program, func, ins)
            objects.append(obj)
    return objects


def enemy_create_semantics(program: Program, func: Function, ins: Instruction, op_name: str) -> dict[str, object]:
    sub = a(ins, 0, "")
    sub_name = sub.strip().strip('"')
    role = "boss" if enemy_create_is_boss(sub_name, func.name, program.source) else "stage_enemy"
    create = {
        "sub": sub,
        "x": a(ins, 1, "0.0f"),
        "y": a(ins, 2, "0.0f"),
        "life": a(ins, 3, "0"),
        "score": a(ins, 4, "0"),
        "item": a(ins, 5, "0"),
        "role": role,
        "position_mode": "absolute" if "A" in op_name else "relative",
        "mirror": "M" in op_name,
        "func": op_name.endswith("F"),
    }
    create["target_forms"] = enemy_create_target_forms(create)
    return create


def enemy_create_target_forms(create: dict[str, object]) -> dict[str, str]:
    if str(create.get("role") or "") != "stage_enemy":
        return {}
    suffix = "_func" if create.get("func") else ""
    absolute = create.get("position_mode") == "absolute"
    mirror = bool(create.get("mirror"))
    if absolute and mirror:
        old_form = f"enemy.create_abs_mirror{suffix}"
        th13_form = f"enemy.create_mirror{suffix}"
    elif absolute:
        old_form = f"enemy.create_abs{suffix}"
        th13_form = f"enemy.create{suffix}"
    elif mirror:
        old_form = f"enemy.create_mirror{suffix}"
        th13_form = old_form
    else:
        old_form = f"enemy.create{suffix}"
        th13_form = old_form
    return {"th10_th11": old_form, "th12": old_form, "th13_plus": th13_form}


def enemy_create_is_boss(sub_name: str, function: str, source: str) -> bool:
    lowered = sub_name.lower()
    if lowered in {"boss", "mboss"} or lowered.startswith(("boss", "mboss")):
        return True
    function_lower = function.lower()
    if function_lower.startswith(("boss", "mboss")) and lowered in {"", "main"}:
        return True
    source_name = source.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return any(token in source_name for token in ("boss", "mbs", "bs")) and lowered in {"boss", "mboss"}


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
                if op_key_for_opcode(program.game, ins.opcode) == "boss.spell_ex":
                    current.fields.setdefault("target_policy", {})["spell_ex_common_header"] = {
                        "strategy": "emit_target_op",
                        "target_generations": ["th13_plus"],
                        "target_op_key": "boss.spell_ex",
                        "arg_policy": {"take_first": 4},
                        "reason": "extended spell descriptor is a shared boss phase header in TH10+",
                    }
            elif boss_ops[ins.opcode] == "setInterrupt":
                current.fields["interrupt"] = {"args": ins.args}
    return objects


def summarize_by_kind(objects: Iterable[object]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for obj in objects:
        counts[getattr(obj, "kind", obj.__class__.__name__)] += 1
    return dict(sorted(counts.items()))
