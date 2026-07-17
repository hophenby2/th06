from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal

from ..canonical.semantic_ir import VariableUseKind
from ..canonical.variable_ir import rewrite_argument_variables
from ..dialects.game_ids import normalize_game_id
from ..dialects.semantics import generation_for_game

GEN_OLD = "th06_th08"
GEN_10 = "th10_th11"
GEN_12 = "th12"
GEN_13 = "th13_plus"


@dataclass(frozen=True)
class ArgLayout:
    fields: tuple[str, ...]
    defaults: dict[str, str]
    target_only_defaults: dict[str, str] | None = None
    omitted_field_defaults: dict[str, str] | None = None


ARG_LAYOUT_OVERRIDES: dict[tuple[str, str, int], ArgLayout] = {}
ARG_LAYOUT_GAME_OVERRIDES: dict[tuple[str, str, int], ArgLayout] = {}


# 参数语义表：同一个 op_key 下，不同世代可以有不同 layout。
# lowering 时先 source args -> semantic fields，再 semantic fields -> target args。
ARG_LAYOUTS: dict[str, dict[str, ArgLayout]] = {
    "enemy.create": {
        GEN_10: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
        GEN_12: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
        GEN_13: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
    },
    "enemy.create_func": {
        GEN_10: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
        GEN_12: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
        GEN_13: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
    },
    "enemy.create_maple": {
        GEN_12: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
        GEN_13: ArgLayout(("routine", "x", "y", "health", "score_reward", "item_drop"), {}),
    },
    "movement.circle.set": {
        # TH08 moveCircle(t, theta, angSpd, radSpd): t 是圆周运动持续时间，半径从 0 开始增长。
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        # TH12+/TH13+ moveCircle(theta, angSpd, radius, radInc)。
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle_rel.set": {
        GEN_OLD: ArgLayout(("duration", "theta", "angular_speed", "radius_delta"), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta"), {"duration": "999999"}),
    },
    "movement.circle.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {}),
    },
    "movement.circle_rel.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta"), {"compat_flag": "0"}),
        GEN_12: ArgLayout(
            ("duration", "mode", "angular_speed", "radius", "radius_delta"),
            {},
            omitted_field_defaults={"compat_flag": "0"},
        ),
        GEN_13: ArgLayout(
            ("duration", "mode", "angular_speed", "radius", "radius_delta"),
            {},
            omitted_field_defaults={"compat_flag": "0"},
        ),
    },
    "movement.move_limit_reset": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "movement.move_rand": {
        GEN_10: ArgLayout(("duration", "mode", "speed"), {}),
        GEN_12: ArgLayout(("duration", "mode", "speed"), {}),
        GEN_13: ArgLayout(("duration", "mode", "speed"), {}),
    },
    "movement.move_rand_rel": {
        GEN_10: ArgLayout(("duration", "mode", "speed"), {}),
        GEN_12: ArgLayout(("duration", "mode", "speed"), {}),
        GEN_13: ArgLayout(("duration", "mode", "speed"), {}),
    },
    "movement.move_boss": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "movement.move_boss_rel": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },

    "movement.ellipse.set": {
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
    },
    "movement.ellipse_rel.set": {
        GEN_10: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
        GEN_13: ArgLayout(("theta", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {"ellipse_mode": "0"}),
    },
    "movement.ellipse.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
    },
    "movement.ellipse_rel.tween": {
        GEN_10: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "ellipse_angle", "ellipse_ratio"), {}),
    },
    "movement.bezier": {
        GEN_10: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
        GEN_12: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
        GEN_13: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
    },
    "movement.bezier_rel": {
        GEN_10: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
        GEN_12: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
        GEN_13: ArgLayout(("duration", "x1", "y1", "x2", "y2", "x3", "y3"), {}),
    },
    "movement.move_vel_nm_time": {
        GEN_12: ArgLayout(("duration", "interpolation", "angle", "speed"), {}),
        GEN_13: ArgLayout(("duration", "interpolation", "angle", "speed"), {}),
    },
    "movement.move_dir": {
        GEN_OLD: ArgLayout(("angle", "speed"), {}),
        GEN_10: ArgLayout(("angle", "speed"), {}),
        GEN_12: ArgLayout(("angle", "speed"), {}),
        GEN_13: ArgLayout(("angle", "speed"), {}),
    },
    "movement.move_dir_time": {
        GEN_OLD: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_10: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_12: ArgLayout(("duration", "mode", "angle", "speed"), {}),
        GEN_13: ArgLayout(("duration", "mode", "angle", "speed"), {}),
    },
    "unit.set_hitbox": {
        GEN_OLD: ArgLayout(("width", "height"), {}),
        GEN_10: ArgLayout(("width", "height"), {}),
        GEN_12: ArgLayout(("width", "height"), {}),
        GEN_13: ArgLayout(("width", "height"), {}),
    },
    "unit.set_hurtbox": {
        GEN_OLD: ArgLayout(("width", "height"), {}),
        GEN_10: ArgLayout(("width", "height"), {}),
        GEN_12: ArgLayout(("width", "height"), {}),
        GEN_13: ArgLayout(("width", "height"), {}),
    },
    "unit.special_collision_flag": {
        GEN_12: ArgLayout(("enabled",), {}),
        GEN_13: ArgLayout(("enabled",), {}),
    },
    "unit.kill_rate": {
        GEN_13: ArgLayout(("weight",), {}),
    },
    "unit.spirit_drop_decay_frames": {
        GEN_13: ArgLayout(("frames",), {}),
    },
    "unit.spirit_drop_max_count": {
        GEN_13: ArgLayout(("count",), {}),
    },
    "flow.jmp": {
        GEN_OLD: ArgLayout(("time", "label"), {}),
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.jmp_eq": {
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.jmp_neq": {
        GEN_10: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_12: ArgLayout(("label", "time"), {"time": "0"}),
        GEN_13: ArgLayout(("label", "time"), {"time": "0"}),
    },
    "flow.nop": {
        GEN_OLD: ArgLayout((), {}),
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.delete": {
        GEN_OLD: ArgLayout((), {}),
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.kill_async": {
        GEN_10: ArgLayout(("slot",), {}),
        GEN_12: ArgLayout(("slot",), {"slot": "0"}),
        GEN_13: ArgLayout(("slot",), {"slot": "0"}),
    },
    "flow.kill_all_async": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.noti": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.notf": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.negi": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.negf": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "flow.square_sum": {
        GEN_10: ArgLayout(("var", "x", "y"), {}),
        GEN_12: ArgLayout(("var", "x", "y"), {}),
        GEN_13: ArgLayout(("var", "x", "y"), {}),
    },
    "flow.stack_sqrt": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "bullet.fire": {
        GEN_OLD: ArgLayout((), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "bullet.offset": {
        GEN_OLD: ArgLayout(("x", "y"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id", "x", "y"), {"et_id": "0"}),
    },
    "bullet.et_offset_rad": {
        GEN_10: ArgLayout(("et_id", "angle", "radius"), {"et_id": "0", "angle": "0.0f", "radius": "0.0f"}),
        GEN_12: ArgLayout(("et_id", "angle", "radius"), {"et_id": "0", "angle": "0.0f", "radius": "0.0f"}),
        GEN_13: ArgLayout(("et_id", "angle", "radius"), {"et_id": "0", "angle": "0.0f", "radius": "0.0f"}),
    },
    "bullet.et_offset_abs": {
        GEN_10: ArgLayout(("et_id", "x", "y"), {"et_id": "0", "x": "0.0f", "y": "0.0f"}),
        GEN_12: ArgLayout(("et_id", "x", "y"), {"et_id": "0", "x": "0.0f", "y": "0.0f"}),
        GEN_13: ArgLayout(("et_id", "x", "y"), {"et_id": "0", "x": "0.0f", "y": "0.0f"}),
    },
    "bullet.sound": {
        GEN_OLD: ArgLayout(("fire_sound", "transform_sound"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
        GEN_12: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
        GEN_13: ArgLayout(("et_id", "fire_sound", "transform_sound"), {"et_id": "0", "fire_sound": "-1", "transform_sound": "-1"}),
    },
    "bullet.transform": {
        GEN_OLD: ArgLayout(("slot", "mode", "channel", "a", "b", "r", "s"), {"et_id": "0"}),
        GEN_10: ArgLayout(("et_id", "slot", "channel", "mode", "a", "b", "r", "s"), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id", "slot", "channel", "mode", "a", "b", "r", "s"), {"et_id": "0"}),
        # TH13+ opcode 609 has explicit slot; opcode 611 is append-style and has no slot.
        GEN_13: ArgLayout(("et_id", "slot", "channel", "mode", "a", "b", "r", "s"), {"et_id": "0", "slot": "0"}),
    },
    "bullet.clear_all": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "bullet.copy": {
        GEN_10: ArgLayout(("dest", "src"), {}),
        GEN_12: ArgLayout(("dest", "src"), {}),
        GEN_13: ArgLayout(("dest", "src"), {}),
    },
    "bullet.cancel_radius": {
        GEN_OLD: ArgLayout((), {"radius": "0.0f"}),
        GEN_10: ArgLayout(("radius",), {"radius": "0.0f"}),
        GEN_12: ArgLayout(("radius",), {"radius": "0.0f"}),
        GEN_13: ArgLayout(("radius",), {"radius": "0.0f"}),
    },


    "laser.on": {
        GEN_10: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "laser.on_aimed": {
        GEN_10: ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0", "slot": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "laser.straight_on": {
        GEN_10: ArgLayout(("et_id", "slot", "sprite", "color", "angle", "speed", "length", "width", "start", "duration", "stop", "unknown"), {"et_id": "0", "slot": "0", "sprite": "0", "color": "0", "angle": "0.0f", "speed": "0.0f", "length": "128.0f", "width": "16.0f", "start": "0", "duration": "60", "stop": "0", "unknown": "0"}),
        GEN_12: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_13: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
    },
    "laser.new": {
        GEN_12: ArgLayout(("et_id", "init_length", "final_length", "unknown", "width"), {"et_id": "0", "init_length": "0.0f", "final_length": "0.0f", "unknown": "0.0f", "width": "16.0f"}),
        GEN_13: ArgLayout(("et_id", "init_length", "final_length", "unknown", "width"), {"et_id": "0", "init_length": "0.0f", "final_length": "0.0f", "unknown": "0.0f", "width": "16.0f"}),
    },
    "laser.timing": {
        GEN_12: ArgLayout(("et_id", "start", "duration", "stop", "graze_delay", "graze_speed"), {"et_id": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
        GEN_13: ArgLayout(("et_id", "start", "duration", "stop", "graze_delay", "graze_speed"), {"et_id": "0", "start": "0", "duration": "60", "stop": "0", "graze_delay": "0", "graze_speed": "0"}),
    },
    "laser.width": {
        GEN_12: ArgLayout(("et_id", "width"), {"et_id": "0", "width": "16.0f"}),
        GEN_13: ArgLayout(("et_id", "width"), {"et_id": "0", "width": "16.0f"}),
    },
    "laser.length": {
        GEN_12: ArgLayout(("et_id", "length"), {"et_id": "0", "length": "128.0f"}),
        GEN_13: ArgLayout(("et_id", "length"), {"et_id": "0", "length": "128.0f"}),
    },
    "laser.offset": {
        GEN_12: ArgLayout(("laser_id", "x", "y"), {"laser_id": "0", "x": "0.0f", "y": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "x", "y"), {"laser_id": "0", "x": "0.0f", "y": "0.0f"}),
    },
    "laser.trajectory": {
        GEN_12: ArgLayout(("laser_id", "speed", "angle"), {"laser_id": "0", "speed": "0.0f", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "x_speed", "y_speed"), {"laser_id": "0", "x_speed": "0.0f", "y_speed": "0.0f"}),
    },
    "laser.angle": {
        GEN_12: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
    },
    "laser.rotation": {
        GEN_12: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
        GEN_13: ArgLayout(("laser_id", "angle"), {"laser_id": "0", "angle": "0.0f"}),
    },
    "laser.end": {
        GEN_12: ArgLayout(("laser_id",), {"laser_id": "0"}),
        GEN_13: ArgLayout(("laser_id",), {"laser_id": "0"}),
    },
    "laser.curve_on": {
        GEN_12: ArgLayout(("et_id",), {"et_id": "0"}),
        GEN_13: ArgLayout(("et_id",), {"et_id": "0"}),
    },
    "anm.rotate": {
        GEN_OLD: ArgLayout(("angle",), {"slot": "0"}),
        GEN_12: ArgLayout(("slot", "angle"), {"slot": "0"}),
        GEN_13: ArgLayout(("slot", "angle"), {"slot": "0"}),
    },
    "anm.on_et": {
        GEN_10: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_12: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
        GEN_13: ArgLayout(("et_id", "slot"), {"et_id": "0", "slot": "0"}),
    },
    "unit.z_index": {
        GEN_OLD: ArgLayout(("layers",), {}),
        GEN_12: ArgLayout(("layers",), {}),
        GEN_13: ArgLayout(("layers",), {}),
    },
    "bullet.distance": {
        GEN_10: ArgLayout(("et_id", "distance"), {"et_id": "0", "distance": "0.0f"}),
        GEN_12: ArgLayout(("et_id", "distance"), {"et_id": "0", "distance": "0.0f"}),
        GEN_13: ArgLayout(("et_id", "distance"), {"et_id": "0", "distance": "0.0f"}),
    },
    "unit.hit_sound": {
        GEN_12: ArgLayout(("sound",), {"sound": "0"}),
        GEN_13: ArgLayout(("sound",), {"sound": "0"}),
    },
    "unit.fog": {
        GEN_10: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
        GEN_12: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
        GEN_13: ArgLayout(("radius", "color"), {"radius": "0.0f", "color": "0"}),
    },
    "unit.boss_wait": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.move_limit": {
        GEN_10: ArgLayout(("x", "y", "width", "height"), {}),
        GEN_12: ArgLayout(("x", "y", "width", "height"), {}),
        GEN_13: ArgLayout(("x", "y", "width", "height"), {}),
    },
    "movement.move_limit": {
        GEN_10: ArgLayout(("x", "y", "width", "height"), {}),
        GEN_12: ArgLayout(("x", "y", "width", "height"), {}),
        GEN_13: ArgLayout(("x", "y", "width", "height"), {}),
    },
    "unit.drop_clear": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.drop_extra": {
        GEN_10: ArgLayout(("type", "amount"), {}),
        GEN_12: ArgLayout(("type", "amount"), {}),
        GEN_13: ArgLayout(("type", "amount"), {}),
    },
    "unit.drop_area": {
        GEN_10: ArgLayout(("width", "height"), {}),
        GEN_12: ArgLayout(("width", "height"), {}),
        GEN_13: ArgLayout(("width", "height"), {}),
    },
    "unit.drop_items": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.drop_main": {
        GEN_10: ArgLayout(("type",), {}),
        GEN_12: ArgLayout(("type",), {}),
        GEN_13: ArgLayout(("type",), {}),
    },
    "boss.life_set": {
        GEN_10: ArgLayout(("life",), {}),
        GEN_12: ArgLayout(("life",), {}),
        GEN_13: ArgLayout(("life",), {}),
    },
    "boss.set_boss": {
        GEN_10: ArgLayout(("boss_id",), {}),
        GEN_12: ArgLayout(("boss_id",), {}),
        GEN_13: ArgLayout(("boss_id",), {}),
    },
    "boss.timer_reset": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.set_invuln": {
        GEN_10: ArgLayout(("time",), {}),
        GEN_12: ArgLayout(("time",), {}),
        GEN_13: ArgLayout(("time",), {}),
    },
    "unit.play_sound": {
        GEN_10: ArgLayout(("sound",), {}),
        GEN_12: ArgLayout(("sound",), {}),
        GEN_13: ArgLayout(("sound",), {}),
    },
    "unit.dialog_read": {
        GEN_10: ArgLayout(("msg",), {}),
        GEN_12: ArgLayout(("msg",), {}),
        GEN_13: ArgLayout(("msg",), {}),
    },
    "unit.dialog_wait": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "boss.spell_end": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "boss.set_chapter": {
        GEN_10: ArgLayout(("chapter",), {}),
        GEN_12: ArgLayout(("chapter",), {}),
        GEN_13: ArgLayout(("chapter",), {}),
    },
    "enemy.enm_kill_all": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.life_marker": {
        GEN_10: ArgLayout(("slot", "life", "color"), {}),
        GEN_12: ArgLayout(("slot", "life", "color"), {}),
        GEN_13: ArgLayout(("slot", "life", "color"), {}),
    },
    "unit.stars": {
        GEN_10: ArgLayout(("count",), {}),
        GEN_12: ArgLayout(("count",), {}),
        GEN_13: ArgLayout(("count",), {}),
    },
    "unit.death_wait": {
        GEN_10: ArgLayout((), {}),
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.stage_logo": {
        GEN_12: ArgLayout((), {}),
        GEN_13: ArgLayout((), {}),
    },
    "unit.unknown569": {
        GEN_13: ArgLayout(("value",), {"value": "0"}),
    },

    "unit.call_std": {
        GEN_10: ArgLayout(("mode",), {"mode": "0"}),
        GEN_12: ArgLayout((), {"mode": "0"}),
        GEN_13: ArgLayout(("mode",), {"mode": "0"}),
    },
    "flow.call_async": {
        GEN_OLD: ArgLayout(("slot", "sub"), {"slot": "0"}),
        GEN_10: ArgLayout(("sub",), {"slot": "0"}),
        GEN_12: ArgLayout(("sub",), {"slot": "0"}),
        GEN_13: ArgLayout(("sub",), {"slot": "0"}),
    },
    "flow.debug22": {
        GEN_12: ArgLayout((), {"mode": "0", "name": '""'}),
        GEN_13: ArgLayout(("mode", "name"), {"mode": "0", "name": '""'}),
    },
    "flow.float_time": {
        GEN_OLD: ArgLayout(("var", "duration", "curve", "mode", "initial", "final", "p1", "p2"), {"slot": "0"}),
        GEN_10: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
        GEN_12: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
        GEN_13: ArgLayout(("slot", "var", "duration", "mode", "initial", "final"), {"slot": "0"}),
    },
    "unit.et_protect_range": {
        GEN_OLD: ArgLayout(("radius",), {}),
        GEN_10: ArgLayout(("radius",), {}),
        GEN_12: ArgLayout(("radius",), {}),
        GEN_13: ArgLayout(("radius",), {}),
    },
    "boss.set_interrupt": {
        GEN_OLD: ArgLayout(("sub",), {"phase": "0", "life": "0", "time": "0"}),
        GEN_10: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
        GEN_12: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
        GEN_13: ArgLayout(("phase", "life", "time", "sub"), {"phase": "0", "life": "0", "time": "0"}),
    },
    "boss.set_timeout": {
        GEN_10: ArgLayout(("time", "sub"), {"time": "0"}),
        GEN_12: ArgLayout(("time", "sub"), {"time": "0"}),
        GEN_13: ArgLayout(("time", "sub"), {"time": "0"}),
    },
    "boss.spell": {
        GEN_OLD: ArgLayout(("phase", "spell_id", "score", "name", "user", "desc1", "desc2"), {"timeout": "0"}),
        GEN_10: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_12: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_13: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
    },
    "boss.spell_ex": {
        GEN_10: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_12: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
        GEN_13: ArgLayout(("phase", "timeout", "score", "name"), {"phase": "0", "timeout": "0", "score": "0", "name": '""'}),
    },
}

ARG_LAYOUT_OVERRIDES.update({
    ("enemy.create", GEN_10, 270): ArgLayout(("routine", "x", "y", "legacy_parameter", "health", "score_reward", "item_drop"), {}),
    ("enemy.create", GEN_12, 270): ArgLayout(("routine", "x", "y", "legacy_parameter", "health", "score_reward", "item_drop"), {}),
    ("enemy.create_func", GEN_10, 271): ArgLayout(("routine", "x", "y", "legacy_parameter", "health", "score_reward", "item_drop"), {}),
    ("enemy.create_func", GEN_12, 271): ArgLayout(("routine", "x", "y", "legacy_parameter", "health", "score_reward", "item_drop"), {}),
    ("movement.circle_rel.tween", GEN_10, 291): ArgLayout(("duration", "mode", "angular_speed", "radius", "radius_delta", "compat_flag"), {"compat_flag": "0"}),
    ("laser.on", GEN_10, 412): ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0"}),
    ("laser.on", GEN_10, 431): ArgLayout(("sprite", "color", "angle", "speed", "unknown1", "length1", "length2", "width"), {"et_id": "0"}),
    ("bullet.transform", GEN_13, 611): ArgLayout(("et_id", "channel", "mode", "a", "b", "r", "s"), {"slot": "0"}),
})

ARG_LAYOUT_GAME_OVERRIDES.update({
    # TH10 has a six-field form, while TH11's native ins_291 replaces
    # radius_delta with a trailing integer compatibility flag.
    ("movement.circle_rel.tween", "th11", 291): ArgLayout(
        ("duration", "mode", "angular_speed", "radius", "compat_flag"),
        {"compat_flag": "0", "radius_delta": "0.0f"},
        omitted_field_defaults={"radius_delta": "0.0f"},
    ),
})

# 旧作条件跳转把比较也塞在同一个 op 里；TH12+ 的 jmpEq/jmpNeq 只吃 VM 条件标志。
# 没有同步比较栈时不能安全一条指令转换。
UNSAFE_LAYOUT_OPS: dict[str, set[tuple[str, str]]] = {
    "flow.jmp_eq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_neq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_lss": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_leq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_gre": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
    "flow.jmp_geq": {(GEN_OLD, GEN_12), (GEN_OLD, GEN_13), (GEN_12, GEN_OLD), (GEN_13, GEN_OLD)},
}


def adapt_args_for_op_key(
    op_key: str,
    source_game: str,
    source_opcode: int,
    target: str,
    target_opcode: int,
    args: list[str],
    *,
    project_variables: bool = True,
) -> list[str] | None:
    source_gen = generation_for_game(source_game)
    target_gen = generation_for_game(target)
    if project_variables:
        values, _variable_issues = rewrite_argument_variables(
            source_game,
            target,
            args,
            use_kind=VariableUseKind.UNKNOWN,
        )
        if values is None:
            return None
    else:
        values = [str(arg) for arg in args]

    if (source_gen, target_gen) in UNSAFE_LAYOUT_OPS.get(op_key, set()):
        return None

    layouts = ARG_LAYOUTS.get(op_key)
    if not layouts:
        return adapt_special_args(op_key, source_gen, target_gen, values)
    source_layout = ARG_LAYOUT_GAME_OVERRIDES.get(
        (op_key, normalize_game_id(source_game), source_opcode),
        ARG_LAYOUT_OVERRIDES.get((op_key, source_gen, source_opcode), layouts.get(source_gen)),
    )
    target_layout = ARG_LAYOUT_GAME_OVERRIDES.get(
        (op_key, normalize_game_id(target), target_opcode),
        ARG_LAYOUT_OVERRIDES.get((op_key, target_gen, target_opcode), layouts.get(target_gen)),
    )
    if not source_layout or not target_layout:
        return None

    fields = fields_from_args(source_layout, values)
    if fields is None:
        return None
    for key, default in source_layout.defaults.items():
        fields.setdefault(key, default)
    for key, default in (target_layout.omitted_field_defaults or {}).items():
        if key in fields and not field_value_is_proven_default(fields[key], default):
            return None
    target_defaults = target_layout.defaults | (target_layout.target_only_defaults or {})
    target_fields = target_layout.fields
    if op_key == "bullet.transform" and target_gen == GEN_13 and target_opcode == 611:
        target_fields = ("et_id", "channel", "mode", "a", "b", "r", "s")
    if op_key == "laser.trajectory" and source_gen == GEN_12 and target_gen == GEN_13:
        speed = fields.get("speed", target_defaults.get("speed", "0.0f"))
        angle = fields.get("angle", target_defaults.get("angle", "0.0f"))
        fields["x_speed"] = f"({speed}) * cos({angle})"
        fields["y_speed"] = f"({speed}) * sin({angle})"
    result = [adapt_field_value(field, fields.get(field, target_defaults.get(field, "")), source_gen, target_gen) for field in target_fields]
    if op_key == "movement.move_vel_nm_time" and target_gen == GEN_12 and len(result) > 1:
        match = re.fullmatch(r"(-?\d+)", result[1].strip())
        if match:
            result[1] = f"{match.group(1)}.0f"
    return result


def adapt_special_args(op_key: str, source_gen: str, target_gen: str, values: list[str]) -> list[str] | None:
    if op_key == "flow.call" and values:
        result = list(values)
        result[0] = adapt_sub_value(result[0], source_gen, target_gen)
        return result
    return values


def adapt_field_value(field: str, value: str, source_gen: str, target_gen: str) -> str:
    if field in {"sub", "function"}:
        return adapt_sub_value(value, source_gen, target_gen)
    if field == "layers" and source_gen == GEN_12 and target_gen == GEN_13:
        match = re.fullmatch(r"(-?\d+)\.0f", str(value).strip())
        if match:
            return match.group(1)
    if field == "interpolation" and source_gen == GEN_12 and target_gen == GEN_13:
        match = re.fullmatch(r"(-?\d+)\.0f", str(value).strip())
        if match:
            return match.group(1)
    return value


def field_value_is_proven_default(value: str, default: str) -> bool:
    value_text = str(value).strip()
    default_text = str(default).strip()
    if value_text == default_text:
        return True
    numeric = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)[fF]?")
    if not numeric.fullmatch(value_text) or not numeric.fullmatch(default_text):
        return False
    return Decimal(value_text.rstrip("fF")) == Decimal(default_text.rstrip("fF"))


def adapt_sub_value(value: str, source_gen: str, target_gen: str) -> str:
    text = str(value).strip()
    if source_gen == GEN_OLD and target_gen in {GEN_10, GEN_12, GEN_13} and re.fullmatch(r"\d+", text):
        return f'"Sub{text}"'
    if target_gen == GEN_OLD:
        match = re.fullmatch(r"Sub(\d+)", text)
        if match:
            return match.group(1)
    return text

def fields_from_args(layout: ArgLayout, args: list[str]) -> dict[str, str] | None:
    if len(args) != len(layout.fields):
        return None
    return dict(zip(layout.fields, args))
