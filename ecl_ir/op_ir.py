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
}

OP_ALIASES = {
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


def op_event(game: str, opcode: int, args: list[str], line: int | None = None, difficulty: str | None = None) -> dict[str, object]:
    info = opcode_info(game, opcode)
    key = op_key_for_opcode(game, opcode)
    return {
        "op_key": key,
        "domain": domain_for(game, opcode, info.name if info else ""),
        "source_game": game,
        "source_opcode": opcode,
        "source_name": info.name if info else "",
        "signature": info.signature if info else "",
        "args": list(args),
        "line": line,
        "difficulty": difficulty,
    }
