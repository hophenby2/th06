from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .reference import opcode_reference, opcode_signature

TH13PLUS_GAMES = {"th13", "th14", "th143", "th15", "th16", "th165", "th17", "th18", "th185"}
TH10_TH11_GAMES = {"th10", "th11"}
TH12_GAMES = {"th12", "th125", "th128"}
OLD_GAMES = {"th06", "th07", "th08"}

GEN_TH06_TH08 = "th06_th08"
GEN_TH10_TH11 = "th10_th11"
GEN_TH12 = "th12"
GEN_TH13_PLUS = "th13_plus"
GEN_UNKNOWN = "unknown"


@dataclass(frozen=True)
class RawOpcodeMap:
    target_opcode: int
    arg_order: tuple[int, ...] | None = None
    semantic: str = ""


@dataclass(frozen=True)
class SemanticOpcode:
    semantic: str
    opcodes: dict[str, int]
    arg_order: dict[tuple[str, str], tuple[int, ...]] | None = None
    unsupported_targets: dict[str, str] | None = None

    def map_between(self, source_generation: str, target_generation: str) -> RawOpcodeMap | None:
        source_opcode = self.opcodes.get(source_generation)
        target_opcode = self.opcodes.get(target_generation)
        if source_opcode is None or target_opcode is None:
            return None
        if self.unsupported_targets and target_generation in self.unsupported_targets:
            return None
        order = None
        if self.arg_order:
            order = self.arg_order.get((source_generation, target_generation))
        return RawOpcodeMap(target_opcode, order, self.semantic)


@dataclass(frozen=True)
class SemanticValue:
    semantic: str
    values: dict[str, str]
    aliases: tuple[str, ...] = ()
    lossy_targets: tuple[str, ...] = ()

    def encode(self, generation: str) -> str | None:
        return self.values.get(generation)


def generation_for_game(game: str) -> str:
    if game in TH13PLUS_GAMES:
        return GEN_TH13_PLUS
    if game in TH12_GAMES:
        return GEN_TH12
    if game in TH10_TH11_GAMES:
        return GEN_TH10_TH11
    if game in OLD_GAMES:
        return GEN_TH06_TH08
    return GEN_UNKNOWN


def bullet_transform_generation_for_game(game: str) -> str:
    if game == "th11":
        return GEN_TH12
    return generation_for_game(game)


def lifted_raw_coverage_policy(kind: str, source_game: str, target: str, family: str = "") -> str:
    source_generation = generation_for_game(source_game)
    target_generation = generation_for_game(target)
    if kind == "EnemyVisual":
        return "all"
    if kind == "UnitFlag":
        return "all"
    if kind == "Mode":
        return "metadata"
    if kind != "BulletEmitter":
        return "default"
    if family == "th12" and source_generation == GEN_TH12 and target_generation == GEN_TH13_PLUS:
        return "contiguous_setup_prefix"
    if family == "th10_slot" and source_generation == GEN_TH10_TH11 and target_generation == GEN_TH12:
        return "contiguous_setup_prefix"
    return "default"


# Opcode semantics are registered by meaning first, then encoded per generation.
SEMANTIC_OPCODES: tuple[SemanticOpcode, ...] = (
    SemanticOpcode("flow.nop", {GEN_TH13_PLUS: 0, GEN_TH12: 0, GEN_TH10_TH11: 0}),
    SemanticOpcode("flow.kill_async", {GEN_TH13_PLUS: 17, GEN_TH12: 17, GEN_TH10_TH11: 17}),
    SemanticOpcode("flow.kill_all_async", {GEN_TH13_PLUS: 21, GEN_TH12: 21, GEN_TH10_TH11: 21}),
    SemanticOpcode("flow.wait", {GEN_TH13_PLUS: 23, GEN_TH12: 83, GEN_TH10_TH11: 83}),
    # TH10/11 docs omit these stack VM opcodes, but original scripts use them
    # with the same ABI as TH12 and TH13+ for arithmetic, comparisons, and
    # helper math. Keep them semantic so loops like Ecl_EtBreak keep mutating
    # their counters after cross-generation lowering.
    SemanticOpcode("flow.seti", {GEN_TH13_PLUS: 43, GEN_TH12: 43, GEN_TH10_TH11: 43}),
    SemanticOpcode("flow.setf", {GEN_TH13_PLUS: 45, GEN_TH12: 45, GEN_TH10_TH11: 45}),
    SemanticOpcode("flow.addi", {GEN_TH13_PLUS: 50, GEN_TH12: 50, GEN_TH10_TH11: 50}),
    SemanticOpcode("flow.addf", {GEN_TH13_PLUS: 51, GEN_TH12: 51, GEN_TH10_TH11: 51}),
    SemanticOpcode("flow.subi", {GEN_TH13_PLUS: 52, GEN_TH12: 52, GEN_TH10_TH11: 52}),
    SemanticOpcode("flow.subf", {GEN_TH13_PLUS: 53, GEN_TH12: 53, GEN_TH10_TH11: 53}),
    SemanticOpcode("flow.muli", {GEN_TH13_PLUS: 54, GEN_TH12: 54, GEN_TH10_TH11: 54}),
    SemanticOpcode("flow.mulf", {GEN_TH13_PLUS: 55, GEN_TH12: 55, GEN_TH10_TH11: 55}),
    SemanticOpcode("flow.divi", {GEN_TH13_PLUS: 56, GEN_TH12: 56, GEN_TH10_TH11: 56}),
    SemanticOpcode("flow.divf", {GEN_TH13_PLUS: 57, GEN_TH12: 57, GEN_TH10_TH11: 57}),
    SemanticOpcode("flow.modi", {GEN_TH13_PLUS: 58, GEN_TH12: 58, GEN_TH10_TH11: 58}),
    SemanticOpcode("flow.eqi", {GEN_TH13_PLUS: 59, GEN_TH12: 59, GEN_TH10_TH11: 59}),
    SemanticOpcode("flow.eqf", {GEN_TH13_PLUS: 60, GEN_TH12: 60, GEN_TH10_TH11: 60}),
    SemanticOpcode("flow.neqi", {GEN_TH13_PLUS: 61, GEN_TH12: 61, GEN_TH10_TH11: 61}),
    SemanticOpcode("flow.neqf", {GEN_TH13_PLUS: 62, GEN_TH12: 62, GEN_TH10_TH11: 62}),
    SemanticOpcode("flow.lessi", {GEN_TH13_PLUS: 63, GEN_TH12: 63, GEN_TH10_TH11: 63}),
    SemanticOpcode("flow.lessf", {GEN_TH13_PLUS: 64, GEN_TH12: 64, GEN_TH10_TH11: 64}),
    SemanticOpcode("flow.leqi", {GEN_TH13_PLUS: 65, GEN_TH12: 65, GEN_TH10_TH11: 65}),
    SemanticOpcode("flow.leqf", {GEN_TH13_PLUS: 66, GEN_TH12: 66, GEN_TH10_TH11: 66}),
    SemanticOpcode("flow.greateri", {GEN_TH13_PLUS: 67, GEN_TH12: 67, GEN_TH10_TH11: 67}),
    SemanticOpcode("flow.greaterf", {GEN_TH13_PLUS: 68, GEN_TH12: 68, GEN_TH10_TH11: 68}),
    SemanticOpcode("flow.geqi", {GEN_TH13_PLUS: 69, GEN_TH12: 69, GEN_TH10_TH11: 69}),
    SemanticOpcode("flow.geqf", {GEN_TH13_PLUS: 70, GEN_TH12: 70, GEN_TH10_TH11: 70}),
    SemanticOpcode("flow.noti", {GEN_TH13_PLUS: 71, GEN_TH12: 71, GEN_TH10_TH11: 71}),
    SemanticOpcode("flow.notf", {GEN_TH13_PLUS: 72, GEN_TH12: 72, GEN_TH10_TH11: 72}),
    SemanticOpcode("flow.deci", {GEN_TH13_PLUS: 78, GEN_TH12: 78, GEN_TH10_TH11: 78}),
    SemanticOpcode("flow.stack_sin", {GEN_TH13_PLUS: 79, GEN_TH12: 79, GEN_TH10_TH11: 79}),
    SemanticOpcode("flow.stack_cos", {GEN_TH13_PLUS: 80, GEN_TH12: 80, GEN_TH10_TH11: 80}),
    SemanticOpcode("flow.circle_pos", {GEN_TH13_PLUS: 81, GEN_TH12: 81, GEN_TH10_TH11: 81}),
    SemanticOpcode("flow.valid_rad", {GEN_TH13_PLUS: 82, GEN_TH12: 82, GEN_TH10_TH11: 82}),
    SemanticOpcode("flow.negi", {GEN_TH13_PLUS: 83, GEN_TH12: 84, GEN_TH10_TH11: 84}),
    SemanticOpcode("flow.negf", {GEN_TH13_PLUS: 84, GEN_TH12: 85, GEN_TH10_TH11: 85}),
    SemanticOpcode("flow.square_sum", {GEN_TH13_PLUS: 85, GEN_TH12: 86, GEN_TH10_TH11: 86}),
    SemanticOpcode("flow.stack_sqrt", {GEN_TH13_PLUS: 88, GEN_TH12: 88, GEN_TH10_TH11: 88}),
    SemanticOpcode("flow.get_angle", {GEN_TH13_PLUS: 87, GEN_TH12: 87, GEN_TH10_TH11: 87}),
    SemanticOpcode("enemy.create", {GEN_TH13_PLUS: 300, GEN_TH12: 256, GEN_TH10_TH11: 256}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_abs", {GEN_TH13_PLUS: 301, GEN_TH12: 257, GEN_TH10_TH11: 257}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("animation.select", {GEN_TH13_PLUS: 302, GEN_TH12: 258}, {(GEN_TH13_PLUS, GEN_TH12): (0,)}),
    SemanticOpcode("animation.set_sprite", {GEN_TH13_PLUS: 303, GEN_TH12: 259}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("enemy.create_mirror", {GEN_TH13_PLUS: 304, GEN_TH12: 260, GEN_TH10_TH11: 260}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_abs_mirror", {GEN_TH13_PLUS: 305, GEN_TH12: 261, GEN_TH10_TH11: 261}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("animation.set_main", {GEN_TH13_PLUS: 306, GEN_TH12: 262}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("animation.play", {GEN_TH13_PLUS: 307, GEN_TH12: 263}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("animation.play_abs", {GEN_TH13_PLUS: 308, GEN_TH12: 264}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("enemy.create_func", {GEN_TH13_PLUS: 309, GEN_TH12: 265, GEN_TH10_TH11: 265}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_abs_func", {GEN_TH13_PLUS: 310, GEN_TH12: 266, GEN_TH10_TH11: 266}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_mirror_func", {GEN_TH13_PLUS: 311, GEN_TH12: 267, GEN_TH10_TH11: 267}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_abs_mirror_func", {GEN_TH13_PLUS: 312, GEN_TH12: 268, GEN_TH10_TH11: 268}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.byakuren_butterfly", {GEN_TH12: 281}),
    SemanticOpcode("movement.position.set", {GEN_TH13_PLUS: 400, GEN_TH12: 300, GEN_TH10_TH11: 280}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.position.tween", {GEN_TH13_PLUS: 401, GEN_TH12: 301, GEN_TH10_TH11: 281}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.position_rel.set", {GEN_TH13_PLUS: 402, GEN_TH12: 302, GEN_TH10_TH11: 282}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.position_rel.tween", {GEN_TH13_PLUS: 403, GEN_TH12: 303, GEN_TH10_TH11: 283}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.velocity.set", {GEN_TH13_PLUS: 404, GEN_TH12: 304, GEN_TH10_TH11: 284}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.velocity.tween", {GEN_TH13_PLUS: 405, GEN_TH12: 305, GEN_TH10_TH11: 285}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.velocity_rel.set", {GEN_TH13_PLUS: 406, GEN_TH12: 306, GEN_TH10_TH11: 286}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.velocity_rel.tween", {GEN_TH13_PLUS: 407, GEN_TH12: 307, GEN_TH10_TH11: 287}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.circle.set", {GEN_TH13_PLUS: 408, GEN_TH12: 308, GEN_TH10_TH11: 288}),
    SemanticOpcode("movement.circle.tween", {GEN_TH13_PLUS: 409, GEN_TH12: 309, GEN_TH10_TH11: 289}),
    SemanticOpcode("movement.circle_rel.set", {GEN_TH13_PLUS: 410, GEN_TH12: 310, GEN_TH10_TH11: 290}),
    SemanticOpcode("movement.circle_rel.tween", {GEN_TH13_PLUS: 411, GEN_TH12: 311, GEN_TH10_TH11: 291}),
    SemanticOpcode("movement.move_rand", {GEN_TH13_PLUS: 412, GEN_TH12: 312, GEN_TH10_TH11: 292}),
    SemanticOpcode("movement.move_rand_rel", {GEN_TH13_PLUS: 413, GEN_TH12: 313, GEN_TH10_TH11: 293}),
    SemanticOpcode("movement.move_boss", {GEN_TH13_PLUS: 414, GEN_TH12: 314, GEN_TH10_TH11: 294}),
    SemanticOpcode("movement.move_boss_rel", {GEN_TH13_PLUS: 415, GEN_TH12: 315, GEN_TH10_TH11: 295}),
    SemanticOpcode("movement.ellipse.set", {GEN_TH13_PLUS: 420, GEN_TH12: 320, GEN_TH10_TH11: 300}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("movement.ellipse.tween", {GEN_TH13_PLUS: 421, GEN_TH12: 321, GEN_TH10_TH11: 301}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.ellipse_rel.set", {GEN_TH13_PLUS: 422, GEN_TH12: 322, GEN_TH10_TH11: 302}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("movement.ellipse_rel.tween", {GEN_TH13_PLUS: 423, GEN_TH12: 323, GEN_TH10_TH11: 303}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.mirror_mode", {GEN_TH13_PLUS: 424, GEN_TH12: 324}, {(GEN_TH13_PLUS, GEN_TH12): (0,)}),
    SemanticOpcode("movement.bezier", {GEN_TH13_PLUS: 425, GEN_TH12: 325, GEN_TH10_TH11: 305}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.bezier_rel", {GEN_TH13_PLUS: 426, GEN_TH12: 326, GEN_TH10_TH11: 306}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.reset", {GEN_TH13_PLUS: 427, GEN_TH12: 327}, {(GEN_TH13_PLUS, GEN_TH12): ()}),
    SemanticOpcode("unit.set_hurtbox", {GEN_TH13_PLUS: 500, GEN_TH12: 400, GEN_TH10_TH11: 320}),
    SemanticOpcode("unit.set_hitbox", {GEN_TH13_PLUS: 501, GEN_TH12: 401, GEN_TH10_TH11: 321}),
    SemanticOpcode("unit.flag_set", {GEN_TH13_PLUS: 502, GEN_TH12: 402, GEN_TH10_TH11: 322}),
    SemanticOpcode("unit.flag_clear", {GEN_TH13_PLUS: 503, GEN_TH12: 403, GEN_TH10_TH11: 323}),
    SemanticOpcode("movement.move_limit", {GEN_TH13_PLUS: 504, GEN_TH12: 404, GEN_TH10_TH11: 324}),
    SemanticOpcode("movement.move_limit_reset", {GEN_TH13_PLUS: 505, GEN_TH12: 405, GEN_TH10_TH11: 325}),
    SemanticOpcode("unit.drop_clear", {GEN_TH13_PLUS: 506, GEN_TH12: 406, GEN_TH10_TH11: 326}),
    SemanticOpcode("unit.drop_extra", {GEN_TH13_PLUS: 507, GEN_TH12: 407, GEN_TH10_TH11: 327}),
    SemanticOpcode("unit.drop_area", {GEN_TH13_PLUS: 508, GEN_TH12: 408, GEN_TH10_TH11: 328}),
    SemanticOpcode("unit.drop_items", {GEN_TH13_PLUS: 509, GEN_TH12: 409, GEN_TH10_TH11: 329}),
    SemanticOpcode("unit.drop_main", {GEN_TH13_PLUS: 510, GEN_TH12: 410, GEN_TH10_TH11: 330}),
    SemanticOpcode("boss.life_set", {GEN_TH13_PLUS: 511, GEN_TH12: 411, GEN_TH10_TH11: 331}),
    SemanticOpcode("boss.set_boss", {GEN_TH13_PLUS: 512, GEN_TH12: 412, GEN_TH10_TH11: 332}),
    SemanticOpcode("boss.timer_reset", {GEN_TH13_PLUS: 513, GEN_TH12: 413, GEN_TH10_TH11: 333}),
    SemanticOpcode("boss.set_interrupt", {GEN_TH13_PLUS: 514, GEN_TH12: 414, GEN_TH10_TH11: 334}),
    SemanticOpcode("unit.set_invuln", {GEN_TH13_PLUS: 515, GEN_TH12: 415, GEN_TH10_TH11: 335}),
    SemanticOpcode("unit.play_sound", {GEN_TH13_PLUS: 516, GEN_TH12: 416, GEN_TH10_TH11: 336}),
    *tuple(SemanticOpcode(f"unit.property.{op - 500:02d}", {GEN_TH13_PLUS: op, GEN_TH12: op - 100}) for op in range(517, 518)),
    SemanticOpcode("unit.dialog_read", {GEN_TH13_PLUS: 518, GEN_TH12: 418, GEN_TH10_TH11: 338}),
    SemanticOpcode("unit.dialog_wait", {GEN_TH13_PLUS: 519, GEN_TH12: 419, GEN_TH10_TH11: 339}),
    SemanticOpcode("unit.boss_wait", {GEN_TH13_PLUS: 520, GEN_TH12: 420, GEN_TH10_TH11: 340}),
    SemanticOpcode("boss.set_timeout", {GEN_TH13_PLUS: 521, GEN_TH12: 421, GEN_TH10_TH11: 341}),
    SemanticOpcode("boss.spell_ex", {GEN_TH13_PLUS: 522, GEN_TH12: 422, GEN_TH10_TH11: 342}),
    SemanticOpcode("boss.spell_end", {GEN_TH13_PLUS: 523, GEN_TH12: 423, GEN_TH10_TH11: 343}),
    SemanticOpcode("boss.set_chapter", {GEN_TH13_PLUS: 524, GEN_TH12: 424, GEN_TH10_TH11: 344}),
    SemanticOpcode("enemy.enm_kill_all", {GEN_TH13_PLUS: 525, GEN_TH12: 425, GEN_TH10_TH11: 345}),
    SemanticOpcode("unit.et_protect_range", {GEN_TH13_PLUS: 526, GEN_TH12: 426, GEN_TH10_TH11: 346}),
    SemanticOpcode("unit.life_marker", {GEN_TH13_PLUS: 527, GEN_TH12: 427, GEN_TH10_TH11: 347}),
    SemanticOpcode("boss.spell_unused", {GEN_TH13_PLUS: 528}),
    SemanticOpcode("unit.property.28", {GEN_TH13_PLUS: 528, GEN_TH12: 428}),
    SemanticOpcode("unit.property.29", {GEN_TH13_PLUS: 529, GEN_TH12: 429}),
    SemanticOpcode("unit.property.30", {GEN_TH13_PLUS: 530, GEN_TH12: 430}),
    SemanticOpcode("unit.rank_f2", {GEN_TH13_PLUS: 531, GEN_TH12: 431}),
    SemanticOpcode("unit.property.32", {GEN_TH13_PLUS: 532, GEN_TH12: 432}),
    SemanticOpcode("unit.property.33", {GEN_TH13_PLUS: 533, GEN_TH12: 433}),
    SemanticOpcode("unit.property.34", {GEN_TH13_PLUS: 534, GEN_TH12: 434}),
    SemanticOpcode("unit.diff_i", {GEN_TH13_PLUS: 535, GEN_TH12: 435}),
    SemanticOpcode("unit.diff_f", {GEN_TH13_PLUS: 536, GEN_TH12: 436}),
    SemanticOpcode("boss.spell", {GEN_TH13_PLUS: 537, GEN_TH12: 437, GEN_TH10_TH11: 357}),
    SemanticOpcode("boss.spell2", {GEN_TH13_PLUS: 538, GEN_TH12: 438}),
    SemanticOpcode("boss.spell3", {GEN_TH13_PLUS: 539, GEN_TH12: 439, GEN_TH10_TH11: 359}),
    SemanticOpcode("unit.stars", {GEN_TH13_PLUS: 540, GEN_TH12: 440, GEN_TH10_TH11: 360}),
    SemanticOpcode("unit.property.42", {GEN_TH13_PLUS: 542, GEN_TH12: 442}),
    SemanticOpcode("unit.property.43", {GEN_TH13_PLUS: 543, GEN_TH12: 443}),
    SemanticOpcode("unit.property.44", {GEN_TH13_PLUS: 544, GEN_TH12: 444}),
    SemanticOpcode("unit.laser_cancel", {GEN_TH13_PLUS: 545, GEN_TH12: 445}),
    SemanticOpcode("unit.bomb_shield", {GEN_TH13_PLUS: 546, GEN_TH12: 446}),
    SemanticOpcode("unit.game_speed", {GEN_TH13_PLUS: 547, GEN_TH12: 447}),
    SemanticOpcode("unit.property.48", {GEN_TH13_PLUS: 548, GEN_TH12: 448}),
    SemanticOpcode("unit.property.49", {GEN_TH13_PLUS: 549, GEN_TH12: 449}),
    SemanticOpcode("unit.effect.53", {GEN_TH13_PLUS: 553, GEN_TH12: 453}),
    SemanticOpcode("unit.effect.54", {GEN_TH13_PLUS: 554, GEN_TH12: 454}),
    SemanticOpcode("unit.effect.55", {GEN_TH13_PLUS: 555, GEN_TH12: 455}),
    SemanticOpcode("unit.effect.56", {GEN_TH13_PLUS: 556, GEN_TH12: 456}),
    *tuple(SemanticOpcode(f"bullet.emitter.{op - 600:02d}", {GEN_TH13_PLUS: op, GEN_TH12: op - 100, GEN_TH10_TH11: op - 200}) for op in range(600, 610)),
    SemanticOpcode("bullet.clear_all", {GEN_TH13_PLUS: 613, GEN_TH12: 510, GEN_TH10_TH11: 410}),
    SemanticOpcode("bullet.copy", {GEN_TH13_PLUS: 614, GEN_TH12: 511, GEN_TH10_TH11: 411}),
    SemanticOpcode("bullet.speed_by_difficulty", {GEN_TH13_PLUS: 624, GEN_TH12: 521, GEN_TH10_TH11: 424}),
    SemanticOpcode("bullet.count_by_difficulty", {GEN_TH13_PLUS: 625, GEN_TH12: 522, GEN_TH10_TH11: 425}),
)

UNSUPPORTED_SEMANTIC_OPCODES: dict[tuple[str, int, str], str] = {
    (GEN_TH13_PLUS, 569, GEN_TH12): "pointdevice/LoLK-specific unit flag, no TH12 equivalent",
    (GEN_TH13_PLUS, 610, GEN_TH12): "bullet clear/transform opcode is not TH12 opcode 510; parameter formats differ",
    (GEN_TH13_PLUS, 630, GEN_TH12): "TH12 opcode 527 has no compile-time args in thtk format table",
    (GEN_TH13_PLUS, 1001, GEN_TH12): "game-specific opcode, no TH12 equivalent",
    (GEN_TH13_PLUS, 1002, GEN_TH12): "game-specific opcode, no TH12 equivalent",
    (GEN_TH12, 452, GEN_TH13_PLUS): "unit effect opcode parameter formats differ",
}

def _with_th10_th11_aliases() -> tuple[SemanticOpcode, ...]:
    expanded: list[SemanticOpcode] = []
    for opcode_semantic in SEMANTIC_OPCODES:
        opcodes = dict(opcode_semantic.opcodes)
        if GEN_TH12 in opcodes and GEN_TH10_TH11 not in opcodes and opcode_semantic.semantic.startswith(("animation.", "enemy.")):
            opcodes[GEN_TH10_TH11] = opcodes[GEN_TH12]
        expanded.append(SemanticOpcode(opcode_semantic.semantic, opcodes, opcode_semantic.arg_order, opcode_semantic.unsupported_targets))
    return tuple(expanded)


SEMANTIC_OPCODES = _with_th10_th11_aliases()

OPCODE_BY_SOURCE_TARGET: dict[tuple[str, str, int], RawOpcodeMap] = {}
for opcode_semantic in SEMANTIC_OPCODES:
    for source_generation, source_opcode in opcode_semantic.opcodes.items():
        for target_generation in opcode_semantic.opcodes:
            if source_generation == target_generation:
                continue
            raw_map = opcode_semantic.map_between(source_generation, target_generation)
            if raw_map is not None:
                OPCODE_BY_SOURCE_TARGET[(source_generation, target_generation, source_opcode)] = raw_map


REFERENCE_GAME_BY_GENERATION = {
    GEN_TH06_TH08: "th08",
    GEN_TH10_TH11: "th10",
    GEN_TH12: "th12",
    GEN_TH13_PLUS: "th15",
}


def reference_semantic_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def compatible_reference_signature(source_game: str, target_game: str, source_opcode: int, target_opcode: int) -> bool:
    source_signature = opcode_signature(source_game, source_opcode)
    target_signature = opcode_signature(target_game, target_opcode)
    return source_signature == target_signature


def add_reference_name_opcode_maps() -> None:
    reference = opcode_reference()
    by_generation_name: dict[str, dict[str, list[int]]] = {}
    for generation, game in REFERENCE_GAME_BY_GENERATION.items():
        table = reference.get(game, {})
        name_map: dict[str, list[int]] = {}
        for opcode, info in table.items():
            if not info.name or info.name.startswith(("unknown", "debug")):
                continue
            name_map.setdefault(info.name, []).append(opcode)
        by_generation_name[generation] = name_map
    for source_generation, source_game in REFERENCE_GAME_BY_GENERATION.items():
        for target_generation, target_game in REFERENCE_GAME_BY_GENERATION.items():
            if source_generation == target_generation:
                continue
            if target_generation == GEN_TH06_TH08 or source_generation == GEN_TH06_TH08:
                continue
            target_names = by_generation_name.get(target_generation, {})
            for name, source_opcodes in by_generation_name.get(source_generation, {}).items():
                target_opcodes = target_names.get(name)
                if not target_opcodes:
                    continue
                for source_opcode in source_opcodes:
                    for target_opcode in target_opcodes:
                        key = (source_generation, target_generation, source_opcode)
                        if key in OPCODE_BY_SOURCE_TARGET:
                            continue
                        if (source_generation, source_opcode, target_generation) in UNSUPPORTED_SEMANTIC_OPCODES:
                            continue
                        if not compatible_reference_signature(source_game, target_game, source_opcode, target_opcode):
                            continue
                        OPCODE_BY_SOURCE_TARGET[key] = RawOpcodeMap(target_opcode, None, f"ref.{reference_semantic_name(name)}")


add_reference_name_opcode_maps()


BULLET_SHAPES: tuple[SemanticValue, ...] = (
    SemanticValue("point", {GEN_TH13_PLUS: "0", GEN_TH12: "0", GEN_TH10_TH11: "0", GEN_TH06_TH08: "0"}),
    SemanticValue("point_highlight", {GEN_TH13_PLUS: "1", GEN_TH12: "1", GEN_TH06_TH08: "0"}),
    SemanticValue("grape", {GEN_TH13_PLUS: "2", GEN_TH12: "2", GEN_TH10_TH11: "24"}),
    SemanticValue("particle", {GEN_TH13_PLUS: "3"}),
    SemanticValue("orb_small", {GEN_TH13_PLUS: "4", GEN_TH12: "3", GEN_TH10_TH11: "1", GEN_TH06_TH08: "3"}),
    SemanticValue("orb_small_highlight", {GEN_TH13_PLUS: "5", GEN_TH12: "4", GEN_TH06_TH08: "3"}),
    SemanticValue("orb_ring", {GEN_TH13_PLUS: "6", GEN_TH12: "5", GEN_TH10_TH11: "2", GEN_TH06_TH08: "6"}),
    SemanticValue("orb_ring_highlight", {GEN_TH13_PLUS: "7", GEN_TH12: "6", GEN_TH06_TH08: "6"}),
    SemanticValue("rice", {GEN_TH13_PLUS: "8", GEN_TH12: "7", GEN_TH10_TH11: "3", GEN_TH06_TH08: "7"}),
    SemanticValue("chain", {GEN_TH13_PLUS: "9", GEN_TH12: "8", GEN_TH10_TH11: "4", GEN_TH06_TH08: "8"}),
    SemanticValue("needle", {GEN_TH13_PLUS: "10", GEN_TH12: "9", GEN_TH10_TH11: "5", GEN_TH06_TH08: "9"}),
    SemanticValue("amulet", {GEN_TH13_PLUS: "11", GEN_TH12: "10", GEN_TH10_TH11: "6", GEN_TH06_TH08: "10"}),
    SemanticValue("scale", {GEN_TH13_PLUS: "12", GEN_TH12: "11", GEN_TH10_TH11: "7", GEN_TH06_TH08: "11"}),
    SemanticValue("bell", {GEN_TH13_PLUS: "13", GEN_TH12: "12", GEN_TH10_TH11: "8", GEN_TH06_TH08: "9"}),
    SemanticValue("cancel_effect", {GEN_TH13_PLUS: "14", GEN_TH12: "13", GEN_TH10_TH11: "9", GEN_TH06_TH08: "13"}),
    SemanticValue("bacillus", {GEN_TH13_PLUS: "15", GEN_TH12: "14", GEN_TH10_TH11: "10", GEN_TH06_TH08: "14"}),
    SemanticValue("small_star", {GEN_TH13_PLUS: "16", GEN_TH12: "15", GEN_TH10_TH11: "11", GEN_TH06_TH08: "8"}),
    SemanticValue("coin", {GEN_TH13_PLUS: "17", GEN_TH12: "16", GEN_TH10_TH11: "23", GEN_TH06_TH08: "16"}),
    SemanticValue("orb_medium", {GEN_TH13_PLUS: "18", GEN_TH12: "17", GEN_TH10_TH11: "12", GEN_TH06_TH08: "8"}),
    SemanticValue("orb_medium_highlight", {GEN_TH13_PLUS: "19", GEN_TH12: "18", GEN_TH10_TH11: "19", GEN_TH06_TH08: "8"}),
    SemanticValue("ellipse", {GEN_TH13_PLUS: "20", GEN_TH12: "19", GEN_TH10_TH11: "13", GEN_TH06_TH08: "19"}),
    SemanticValue("ellipse_highlight", {GEN_TH13_PLUS: "20", GEN_TH12: "19", GEN_TH10_TH11: "20"}, lossy_targets=(GEN_TH13_PLUS, GEN_TH12)),
    SemanticValue("knife", {GEN_TH13_PLUS: "21", GEN_TH12: "20", GEN_TH10_TH11: "14", GEN_TH06_TH08: "20"}),
    SemanticValue("knife_highlight", {GEN_TH13_PLUS: "21", GEN_TH12: "20", GEN_TH10_TH11: "21"}, lossy_targets=(GEN_TH13_PLUS, GEN_TH12)),
    SemanticValue("butterfly", {GEN_TH13_PLUS: "22", GEN_TH12: "21", GEN_TH10_TH11: "15", GEN_TH06_TH08: "21"}),
    SemanticValue("butterfly_highlight", {GEN_TH13_PLUS: "22", GEN_TH12: "21", GEN_TH10_TH11: "22"}, lossy_targets=(GEN_TH13_PLUS, GEN_TH12)),
    SemanticValue("big_star", {GEN_TH13_PLUS: "23", GEN_TH12: "22", GEN_TH10_TH11: "16", GEN_TH06_TH08: "8"}),
    SemanticValue("big_star_reverse", {GEN_TH13_PLUS: "24", GEN_TH12: "22", GEN_TH06_TH08: "8"}, lossy_targets=(GEN_TH12, GEN_TH06_TH08)),
    SemanticValue("light_orb", {GEN_TH13_PLUS: "33", GEN_TH12: "23", GEN_TH10_TH11: "18"}),
    SemanticValue("light_flame", {GEN_TH13_PLUS: "25", GEN_TH12: "24", GEN_TH10_TH11: "25"}),
    SemanticValue("blue_flame", {GEN_TH13_PLUS: "27"}),
    SemanticValue("yellow_flame", {GEN_TH13_PLUS: "28"}),
    SemanticValue("heart", {GEN_TH13_PLUS: "29", GEN_TH12: "25", GEN_TH10_TH11: "27", GEN_TH06_TH08: "25"}),
    SemanticValue("orb_medium_pulse", {GEN_TH13_PLUS: "30"}),
    SemanticValue("arrow", {GEN_TH13_PLUS: "31"}),
    SemanticValue("orb_large", {GEN_TH13_PLUS: "32", GEN_TH12: "26", GEN_TH10_TH11: "17"}),
    SemanticValue("drop", {GEN_TH13_PLUS: "34", GEN_TH12: "28"}),
    SemanticValue("rose", {GEN_TH13_PLUS: "34", GEN_TH12: "27"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("purple_flame", {GEN_TH13_PLUS: "26", GEN_TH12: "29"}),
    SemanticValue("rice_spinning", {GEN_TH13_PLUS: "35", GEN_TH10_TH11: "26"}),
    SemanticValue("needle_spinning", {GEN_TH13_PLUS: "36"}),
    SemanticValue("small_star_reverse", {GEN_TH13_PLUS: "37"}),
    SemanticValue("laser_segment", {GEN_TH13_PLUS: "38", GEN_TH12: "30"}),
)
BULLET_SHAPE_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for shape in BULLET_SHAPES:
    for generation, value in shape.values.items():
        BULLET_SHAPE_BY_GENERATION_VALUE.setdefault((generation, value), shape)
BULLET_SHAPE_BY_SEMANTIC = {shape.semantic: shape for shape in BULLET_SHAPES}

_MODERN_BASE_BULLET_SHAPES = {
    "0": "point",
    "1": "point_highlight",
    "2": "grape",
    "3": "particle",
    "4": "orb_small",
    "5": "orb_small_highlight",
    "6": "orb_ring",
    "7": "orb_ring_highlight",
    "8": "rice",
    "9": "chain",
    "10": "needle",
    "11": "amulet",
    "12": "scale",
    "13": "bell",
    "14": "cancel_effect",
    "15": "bacillus",
    "16": "small_star",
    "17": "coin",
    "18": "orb_medium",
    "19": "orb_medium_highlight",
    "20": "ellipse",
    "21": "knife",
    "22": "butterfly",
    "23": "big_star",
}

_PRE_TH15_BULLET_SHAPES = {
    **_MODERN_BASE_BULLET_SHAPES,
    "24": "light_flame",
    "25": "purple_flame",
    "26": "blue_flame",
    "27": "yellow_flame",
    "28": "heart",
    "29": "orb_medium_pulse",
    "30": "arrow",
    "31": "orb_large",
    "32": "light_orb",
    "33": "drop",
    "34": "rice_spinning",
    "35": "needle_spinning",
    "36": "small_star_reverse",
    "37": "laser_segment",
}

BULLET_SHAPE_CATALOG_BY_GAME: dict[str, dict[str, str]] = {
    "th06": {
        "0": "point", "1": "orb_ring", "2": "rice", "3": "orb_small",
        "4": "chain", "5": "needle", "6": "orb_medium", "7": "legacy_fire",
        "8": "knife", "9": "orb_large",
    },
    "th07": {
        "0": "point", "1": "orb_ring", "2": "rice", "3": "orb_small",
        "4": "chain", "5": "needle", "6": "scale", "7": "orb_medium",
        "8": "butterfly", "9": "legacy_knife", "10": "orb_large",
    },
    "th08": {
        "0": "point", "1": "orb_ring", "2": "rice", "3": "orb_small",
        "4": "chain", "5": "needle", "6": "scale", "7": "orb_medium",
        "8": "butterfly", "9": "legacy_knife", "10": "orb_large", "11": "amulet",
        "12": "small_star", "13": "small_star_reverse", "14": "big_star",
        "15": "big_star_reverse", "16": "bell", "17": "bacillus",
        "18": "ellipse", "19": "light_flame", "20": "knife",
    },
    "th13": _PRE_TH15_BULLET_SHAPES,
    "th14": _PRE_TH15_BULLET_SHAPES,
    "th143": _PRE_TH15_BULLET_SHAPES,
}
BULLET_SHAPE_ENCODING_BY_GAME: dict[str, dict[str, str]] = {
    game: {semantic: value for value, semantic in catalog.items()}
    for game, catalog in BULLET_SHAPE_CATALOG_BY_GAME.items()
}

DROP_TYPES: tuple[SemanticValue, ...] = (
    SemanticValue("none", {GEN_TH13_PLUS: "0", GEN_TH12: "0", GEN_TH10_TH11: "0"}),
    SemanticValue("point", {GEN_TH13_PLUS: "1", GEN_TH12: "1", GEN_TH10_TH11: "1"}),
    SemanticValue("blue_point", {GEN_TH13_PLUS: "2", GEN_TH12: "2", GEN_TH10_TH11: "2"}),
    SemanticValue("power_large", {GEN_TH13_PLUS: "3", GEN_TH12: "3", GEN_TH10_TH11: "3"}),
    SemanticValue("life_piece", {GEN_TH13_PLUS: "5", GEN_TH12: "6"}),
    SemanticValue("bomb_piece", {GEN_TH13_PLUS: "6", GEN_TH12: "5"}),
    SemanticValue("full_power", {GEN_TH13_PLUS: "8", GEN_TH12: "8", GEN_TH10_TH11: "8"}),
    SemanticValue("max_point_small", {GEN_TH13_PLUS: "9", GEN_TH12: "9"}),
    SemanticValue("max_point_medium", {GEN_TH13_PLUS: "10", GEN_TH12: "9"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("max_point_large", {GEN_TH13_PLUS: "11", GEN_TH12: "9"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("spirit_bomb_piece", {GEN_TH13_PLUS: "12", GEN_TH12: "5"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("score_30", {GEN_TH13_PLUS: "12", GEN_TH12: "9"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("score_40", {GEN_TH13_PLUS: "13", GEN_TH12: "9"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("score_50", {GEN_TH13_PLUS: "14", GEN_TH12: "9"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("spirit_bomb_piece_alt", {GEN_TH13_PLUS: "15", GEN_TH12: "5"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("fixed_red", {GEN_TH13_PLUS: "1", GEN_TH12: "10"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("fixed_blue", {GEN_TH13_PLUS: "2", GEN_TH12: "11"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("fixed_green", {GEN_TH13_PLUS: "1", GEN_TH12: "12"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("changing_red", {GEN_TH13_PLUS: "1", GEN_TH12: "13"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("changing_blue", {GEN_TH13_PLUS: "2", GEN_TH12: "14"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("changing_green", {GEN_TH13_PLUS: "1", GEN_TH12: "15"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("ufo_red_bundle", {GEN_TH13_PLUS: "1", GEN_TH12: "16"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("ufo_blue_bundle", {GEN_TH13_PLUS: "2", GEN_TH12: "17"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("ufo_red_blue_bundle", {GEN_TH13_PLUS: "1", GEN_TH12: "18"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("wolf_spirit", {GEN_TH13_PLUS: "16", GEN_TH12: "10"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("otter_spirit", {GEN_TH13_PLUS: "17", GEN_TH12: "11"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("eagle_spirit", {GEN_TH13_PLUS: "18", GEN_TH12: "12"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("red_spirit", {GEN_TH13_PLUS: "19", GEN_TH12: "13"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("blue_spirit", {GEN_TH13_PLUS: "20", GEN_TH12: "14"}, lossy_targets=(GEN_TH12,)),
    SemanticValue("green_spirit", {GEN_TH13_PLUS: "21", GEN_TH12: "15"}, lossy_targets=(GEN_TH12,)),
)
DROP_TYPE_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for drop in DROP_TYPES:
    for generation, value in drop.values.items():
        DROP_TYPE_BY_GENERATION_VALUE.setdefault((generation, value), drop)
DROP_TYPE_BY_SEMANTIC = {drop.semantic: drop for drop in DROP_TYPES}

BULLET_TRANSFORM_MODES: tuple[SemanticValue, ...] = (
    SemanticValue("spawn_step", {GEN_TH13_PLUS: "1", GEN_TH12: "1", GEN_TH10_TH11: "1"}),
    SemanticValue("set_mist", {GEN_TH13_PLUS: "2", GEN_TH12: "2"}),
    SemanticValue("legacy_unknown_2", {GEN_TH10_TH11: "2"}),
    SemanticValue("accel", {GEN_TH13_PLUS: "4", GEN_TH12: "4", GEN_TH10_TH11: "16"}),
    SemanticValue("legacy_unknown_4", {GEN_TH10_TH11: "4"}),
    SemanticValue("legacy_unknown_8", {GEN_TH10_TH11: "8"}),
    SemanticValue("tangent_accel", {GEN_TH13_PLUS: "8", GEN_TH12: "8", GEN_TH10_TH11: "32"}),
    SemanticValue("pause_then_relative_velocity", {GEN_TH13_PLUS: "16", GEN_TH12: "16", GEN_TH10_TH11: "64"}),
    SemanticValue("pause_then_aimed_velocity", {GEN_TH13_PLUS: "16", GEN_TH12: "32", GEN_TH10_TH11: "128"}),
    SemanticValue("pause_then_velocity", {GEN_TH13_PLUS: "16", GEN_TH12: "64", GEN_TH10_TH11: "256"}),
    SemanticValue("sound", {GEN_TH13_PLUS: "2048", GEN_TH12: "16384", GEN_TH10_TH11: "512"}),
    SemanticValue("bounce_all", {GEN_TH10_TH11: "1024"}),
    SemanticValue("bounce_no_bottom", {GEN_TH10_TH11: "2048"}),
    SemanticValue("bounce", {GEN_TH13_PLUS: "64", GEN_TH12: "256"}),
    SemanticValue("uncancelable_time", {GEN_TH13_PLUS: "128", GEN_TH12: "512", GEN_TH10_TH11: "4096"}),
    SemanticValue("offscreen_time", {GEN_TH13_PLUS: "256", GEN_TH12: "1024", GEN_TH10_TH11: "8192"}),
    SemanticValue("shape_change", {GEN_TH13_PLUS: "512", GEN_TH12: "2048", GEN_TH10_TH11: "16384"}),
    SemanticValue("wait_next", {GEN_TH13_PLUS: "-2147483648", GEN_TH12: "4096", GEN_TH10_TH11: "32768"}),
    SemanticValue("delete", {GEN_TH13_PLUS: "1024", GEN_TH12: "8192", GEN_TH10_TH11: "65536"}),
    SemanticValue("legacy_unknown_131072", {GEN_TH12: "131072", GEN_TH10_TH11: "131072"}),
    SemanticValue("legacy_unknown_262144", {GEN_TH12: "262144", GEN_TH10_TH11: "262144"}),
    SemanticValue("spawn_bullet_legacy", {GEN_TH12: "524288", GEN_TH10_TH11: "524288"}),
    SemanticValue("spawn_bullet_layers_legacy", {GEN_TH12: "1048576"}),
    SemanticValue("th12_jump_related", {GEN_TH12: "2097152"}),
    SemanticValue("wall_pass_horizontal", {GEN_TH10_TH11: "1048576"}),
    SemanticValue("bounce_bottom", {GEN_TH10_TH11: "2097152"}),
    SemanticValue("jump", {GEN_TH13_PLUS: "65536", GEN_TH12: "4194304", GEN_TH10_TH11: "4194304"}),
    SemanticValue("legacy_ds_unknown_8388608", {GEN_TH12: "8388608", GEN_TH10_TH11: "8388608"}),
    SemanticValue("shape_change_no_mist", {GEN_TH12: "16777216", GEN_TH10_TH11: "16777216"}),
    SemanticValue("legacy_turn_unknown", {GEN_TH12: "33554432", GEN_TH10_TH11: "33554432"}),
    SemanticValue("legacy_unknown_67108864", {GEN_TH12: "67108864", GEN_TH10_TH11: "67108864"}),
    SemanticValue("bounce_horizontal", {GEN_TH10_TH11: "134217728"}),
    SemanticValue("independent_velocity", {GEN_TH13_PLUS: "524288", GEN_TH12: "134217728"}),
    SemanticValue("highlight", {GEN_TH13_PLUS: "1048576", GEN_TH12: "268435456", GEN_TH10_TH11: "268435456"}),
    SemanticValue("velocity_over_time", {GEN_TH13_PLUS: "2097152", GEN_TH12: "536870912", GEN_TH10_TH11: "536870912"}),
    SemanticValue("legacy_ds_unknown_1073741824", {GEN_TH10_TH11: "1073741824"}),
    SemanticValue("spawn_bullet_advanced", {GEN_TH13_PLUS: "8192"}),
    SemanticValue("spawn_laser_attributes", {GEN_TH13_PLUS: "16384"}),
    SemanticValue("move_to_restore_speed", {GEN_TH13_PLUS: "131072"}),
    SemanticValue("set_velocity_immediate", {GEN_TH13_PLUS: "262144"}),
    SemanticValue("scale", {GEN_TH13_PLUS: "4194304"}),
    SemanticValue("mark_direction", {GEN_TH13_PLUS: "8388608"}),
    SemanticValue("spawn_familiar", {GEN_TH13_PLUS: "16777216"}),
    SemanticValue("layer", {GEN_TH13_PLUS: "33554432"}),
    SemanticValue("spawn_delay", {GEN_TH13_PLUS: "67108864"}),
    SemanticValue("spawn_laser", {GEN_TH13_PLUS: "134217728"}),
    SemanticValue("hitbox_radius", {GEN_TH13_PLUS: "536870912"}),
    SemanticValue("homing_velocity_blend", {GEN_TH13_PLUS: "1073741824"}),
    SemanticValue("wall_pass", {GEN_TH13_PLUS: "4096"}),
)
BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for mode in BULLET_TRANSFORM_MODES:
    for generation, value in mode.values.items():
        BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE.setdefault((generation, value), mode)
BULLET_TRANSFORM_MODE_BY_SEMANTIC = {mode.semantic: mode for mode in BULLET_TRANSFORM_MODES}

SPECIAL_BULLET_TRANSFORM_MODE_ENCODINGS: dict[tuple[str, str], str] = {
    ("bounce_all", GEN_TH12): "256",
    ("bounce_no_bottom", GEN_TH12): "256",
    ("bounce_bottom", GEN_TH12): "256",
    ("bounce_horizontal", GEN_TH12): "256",
    ("bounce_all", GEN_TH13_PLUS): "64",
    ("bounce_no_bottom", GEN_TH13_PLUS): "64",
    ("bounce_bottom", GEN_TH13_PLUS): "64",
    ("bounce_horizontal", GEN_TH13_PLUS): "64",
    ("wall_pass_horizontal", GEN_TH13_PLUS): "4096",
}

UNSUPPORTED_BULLET_TRANSFORM_MODE_REASONS: dict[tuple[str, str, str], str] = {
    (
        GEN_TH12,
        GEN_TH13_PLUS,
        "2097152",
    ): "TH12 etEx mode 2097152 is jump-related and is not TH13+ mode 2097152; direct mapping can jump into invalid TH13+ transform slots",
}

SPREAD_STYLES: tuple[SemanticValue, ...] = (
    SemanticValue("fan.aimed", {GEN_TH13_PLUS: "0", GEN_TH10_TH11: "0"}),
    SemanticValue("fan.fixed", {GEN_TH13_PLUS: "1", GEN_TH10_TH11: "1"}),
    SemanticValue("random_angle", {GEN_TH13_PLUS: "6", GEN_TH10_TH11: "6"}),
    SemanticValue("random_speed", {GEN_TH13_PLUS: "7", GEN_TH10_TH11: "7"}),
    SemanticValue("random_angle_speed", {GEN_TH13_PLUS: "8", GEN_TH10_TH11: "8"}),
    SemanticValue("single_flower.left.aimed", {GEN_TH13_PLUS: "2", GEN_TH12: "4", GEN_TH10_TH11: "2"}),
    SemanticValue("single_flower.left.fixed", {GEN_TH13_PLUS: "3", GEN_TH12: "5", GEN_TH10_TH11: "3"}),
    SemanticValue("single_flower.offset_left.aimed", {GEN_TH13_PLUS: "4", GEN_TH10_TH11: "4"}),
    SemanticValue("single_flower.offset_left.fixed", {GEN_TH13_PLUS: "5", GEN_TH10_TH11: "5"}),
    SemanticValue("single_flower.right.aimed", {GEN_TH12: "2"}),
    SemanticValue("single_flower.right.fixed", {GEN_TH12: "3"}),
    SemanticValue("double_flower.aimed", {GEN_TH13_PLUS: "9", GEN_TH12: "4", GEN_TH10_TH11: "4"}, lossy_targets=(GEN_TH12, GEN_TH10_TH11)),
    SemanticValue("double_flower.fixed", {GEN_TH13_PLUS: "10", GEN_TH12: "5", GEN_TH10_TH11: "5"}, lossy_targets=(GEN_TH12, GEN_TH10_TH11)),
)
SPREAD_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for style in SPREAD_STYLES:
    for generation, value in style.values.items():
        SPREAD_BY_GENERATION_VALUE.setdefault((generation, value), style)
SPREAD_BY_SEMANTIC = {style.semantic: style for style in SPREAD_STYLES}


def plain(value: Any, default: str = "") -> str:
    if isinstance(value, dict):
        return str(value.get("placeholder", default))
    if value in (None, ""):
        return default
    return str(value)


def bullet_shape_semantic(game: str, shape: Any) -> str:
    raw = plain(shape).strip()
    game_catalog = BULLET_SHAPE_CATALOG_BY_GAME.get(game)
    if game_catalog is not None:
        return game_catalog.get(raw, f"raw:{raw}")
    semantic = BULLET_SHAPE_BY_GENERATION_VALUE.get((generation_for_game(game), raw))
    if semantic:
        return semantic.semantic
    return f"raw:{raw}"


def encode_bullet_shape(semantic: str, target: str, fallback: Any = None) -> str:
    if semantic.startswith("raw:"):
        return semantic[4:]
    game_encoding = BULLET_SHAPE_ENCODING_BY_GAME.get(target)
    if game_encoding is not None:
        return game_encoding.get(semantic, plain(fallback, "0"))
    shape = BULLET_SHAPE_BY_SEMANTIC.get(semantic)
    if shape:
        encoded = shape.encode(generation_for_game(target))
        if encoded is not None:
            return encoded
    return plain(fallback, "0")


def bullet_shape_can_encode(semantic: str, target: str) -> bool:
    if semantic.startswith("raw:"):
        return False
    game_encoding = BULLET_SHAPE_ENCODING_BY_GAME.get(target)
    if game_encoding is not None:
        return semantic in game_encoding
    shape = BULLET_SHAPE_BY_SEMANTIC.get(semantic)
    return bool(shape and shape.encode(generation_for_game(target)) is not None)


def bullet_shape_is_lossy(semantic: str, target: str) -> bool:
    shape = BULLET_SHAPE_BY_SEMANTIC.get(semantic)
    return bool(shape and generation_for_game(target) in shape.lossy_targets)


def drop_type_semantic(game: str, value: Any) -> str:
    raw = plain(value).strip()
    semantic = DROP_TYPE_BY_GENERATION_VALUE.get((generation_for_game(game), raw))
    if semantic:
        return semantic.semantic
    return f"raw:{raw}"


def encode_drop_type(semantic: str, target: str, fallback: Any = None) -> str:
    if semantic.startswith("raw:"):
        return semantic[4:]
    drop = DROP_TYPE_BY_SEMANTIC.get(semantic)
    if drop:
        encoded = drop.encode(generation_for_game(target))
        if encoded is not None:
            return encoded
    return plain(fallback, "0")


def bullet_transform_mode_semantic(game: str, mode: Any) -> str:
    raw = plain(mode).strip()
    semantic = BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE.get((bullet_transform_generation_for_game(game), raw))
    if semantic:
        return semantic.semantic
    for candidate in BULLET_TRANSFORM_MODES:
        if raw in candidate.aliases:
            return candidate.semantic
    return f"raw:{raw}"


def encode_bullet_transform_mode(semantic: str, target: str, fallback: Any = None) -> str:
    if semantic.startswith("raw:"):
        return semantic[4:]
    target_generation = bullet_transform_generation_for_game(target)
    special = SPECIAL_BULLET_TRANSFORM_MODE_ENCODINGS.get((semantic, target_generation))
    if special is not None:
        return special
    mode = BULLET_TRANSFORM_MODE_BY_SEMANTIC.get(semantic)
    if mode:
        encoded = mode.encode(target_generation)
        if encoded is not None:
            return encoded
    return plain(fallback, "0")


def bullet_transform_mode_can_encode(semantic: str, target: str) -> bool:
    if semantic.startswith("raw:"):
        return False
    target_generation = bullet_transform_generation_for_game(target)
    if (semantic, target_generation) in SPECIAL_BULLET_TRANSFORM_MODE_ENCODINGS:
        return True
    mode = BULLET_TRANSFORM_MODE_BY_SEMANTIC.get(semantic)
    return bool(mode and mode.encode(target_generation) is not None)


def remap_bullet_transform_mode(source_game: str, target: str, mode: Any) -> str:
    return encode_bullet_transform_mode(bullet_transform_mode_semantic(source_game, mode), target, mode)


def unsupported_bullet_transform_mode_reason(source_game: str, target: str, mode: Any) -> str | None:
    return UNSUPPORTED_BULLET_TRANSFORM_MODE_REASONS.get(
        (bullet_transform_generation_for_game(source_game), generation_for_game(target), plain(mode).strip())
    )


def remap_shape_change_arg(source_game: str, target: str, mode: Any, shape: Any) -> str:
    if bullet_transform_mode_semantic(source_game, mode) != "shape_change":
        return str(shape)
    return encode_bullet_shape(bullet_shape_semantic(source_game, shape), target, shape)


def flag_profile_for_game(game: str) -> str:
    if game == "th10":
        return "th10"
    if game == "th11":
        return "th11"
    if game == "th12":
        return "th12"
    if game == "th13":
        return "th13"
    if game in TH13PLUS_GAMES:
        return "th14_plus"
    return "unknown"


UNIT_FLAG_SEMANTICS_BY_PROFILE: dict[str, dict[int, str]] = {
    "th10": {
        0x00000001: "no_hurtbox",
        0x00000002: "no_body_collision",
        0x00000004: "persist_lr_offscreen",
        0x00000008: "invincible_hide_boss_bar",
        0x00000010: "hidden_or_noninteractive",
        0x00000020: "legacy_th10_blank",
        0x00000040: "no_global_clear",
        0x00000080: "force_global_clear",
        0x00000100: "entered_screen_internal",
        0x00000200: "move_bounds_internal",
        0x00000400: "tested_internal",
        0x00000800: "movement_mirror_internal",
        0x00001000: "horizontal_anim_internal",
        0x00002000: "nonboss_hidden_strip_internal",
        0x00004000: "special_unit_no_force_clear",
        0x00008000: "boss_mode_internal",
        0x00010000: "no_miss_marker",
        0x00020000: "delete_pending_internal",
        0x00040000: "movement_unknown_internal",
        0x00080000: "legacy_364_unknown",
        0x00100000: "bomb_immune",
        0x00200000: "bomb_immune_cleanup_internal",
    },
    "th11": {
        0x00000001: "no_hurtbox",
        0x00000002: "no_body_collision",
        0x00000004: "persist_lr_offscreen",
        0x00000008: "persist_tb_offscreen",
        0x00000010: "invincible_hide_boss_bar",
        0x00000020: "hidden_or_noninteractive",
        0x00000040: "boss_initial_unknown",
        0x00000080: "no_global_clear",
        0x00000100: "force_global_clear",
        0x00000200: "graze_like_laser",
        0x00000400: "no_clear_dialog_death",
        0x00000800: "clear_effect_vulnerable",
        0x00001000: "entered_screen_internal",
        0x00002000: "move_bounds_internal",
        0x00004000: "tested_internal",
        0x00008000: "movement_mirror_internal",
        0x00010000: "horizontal_anim_internal",
        0x00020000: "nonboss_hidden_strip_internal",
        0x00040000: "special_unit_no_force_clear",
        0x00080000: "boss_mode_internal",
        0x00100000: "no_miss_marker",
        0x00200000: "delete_pending_internal",
        0x00400000: "movement_unknown_internal",
        0x00800000: "legacy_364_unknown",
        0x01000000: "bomb_immune",
        0x02000000: "bomb_immune_cleanup_internal",
        0x08000000: "legacy_369_unknown",
    },
    "th12": {
        0x00000001: "no_hurtbox",
        0x00000002: "no_body_collision",
        0x00000004: "persist_lr_offscreen",
        0x00000008: "persist_tb_offscreen",
        0x00000010: "invincible_hide_boss_bar",
        0x00000020: "hidden_or_noninteractive",
        0x00000040: "boss_initial_unknown",
        0x00000080: "no_global_clear",
        0x00000100: "force_global_clear",
        0x00000200: "graze_like_laser",
        0x00000400: "no_clear_dialog_death",
        0x00000800: "clear_effect_vulnerable",
        0x00008000: "entered_screen_internal",
        0x00010000: "move_bounds_internal",
        0x00020000: "tested_internal",
        0x00040000: "movement_mirror_internal",
        0x00080000: "horizontal_anim_internal",
        0x00100000: "nonboss_hidden_strip_internal",
        0x00200000: "special_unit_no_force_clear",
        0x00400000: "boss_mode_internal",
        0x00800000: "no_miss_marker",
        0x01000000: "delete_pending_internal",
        0x02000000: "movement_unknown_internal",
        0x04000000: "legacy_444_unknown",
        0x08000000: "bomb_immune",
        0x10000000: "bomb_immune_cleanup_internal",
        0x20000000: "engine_internal",
        0x40000000: "legacy_449_unknown",
    },
    "th13": {
        0x00000001: "no_hurtbox",
        0x00000002: "no_body_collision",
        0x00000004: "persist_lr_offscreen",
        0x00000008: "persist_tb_offscreen",
        0x00000010: "invincible_hide_boss_bar",
        0x00000020: "hidden_or_noninteractive",
        0x00000040: "boss_initial_unknown",
        0x00000080: "no_global_clear",
        0x00000100: "force_global_clear",
        0x00000200: "graze_like_laser",
        0x00000400: "no_clear_dialog_death",
        0x00000800: "clear_effect_vulnerable",
        0x00040000: "move_bounds_internal",
        0x00080000: "tested_internal",
        0x00100000: "movement_mirror_internal",
        0x00200000: "horizontal_anim_internal",
        0x00400000: "nonboss_hidden_strip_internal",
        0x00800000: "special_unit_no_force_clear",
        0x01000000: "boss_mode_internal",
        0x02000000: "no_miss_marker",
        0x04000000: "delete_pending_internal",
        0x08000000: "movement_unknown_internal",
        0x10000000: "legacy_544_unknown",
        0x20000000: "bomb_immune",
        0x40000000: "legacy_546_clear_unknown",
        0x80000000: "engine_internal",
    },
    "th14_plus": {
        0x00000001: "no_hurtbox",
        0x00000002: "no_body_collision",
        0x00000004: "persist_lr_offscreen",
        0x00000008: "persist_tb_offscreen",
        0x00000010: "invincible_hide_boss_bar",
        0x00000020: "hidden_or_noninteractive",
        0x00000040: "boss_initial_unknown",
        0x00000080: "no_global_clear",
        0x00000100: "force_global_clear",
        0x00000200: "graze_like_laser",
        0x00000400: "no_clear_dialog_death",
        0x00000800: "clear_effect_vulnerable",
        0x00001000: "rect_collision_gzz",
        0x00020000: "move_bounds_internal",
        0x00040000: "tested_internal",
        0x00080000: "movement_mirror_internal",
        0x00100000: "horizontal_anim_internal",
        0x00200000: "nonboss_hidden_strip_internal",
        0x00400000: "special_unit_no_force_clear",
        0x00800000: "boss_mode_internal",
        0x01000000: "no_miss_marker",
        0x02000000: "delete_pending_internal",
        0x04000000: "movement_unknown_internal",
        0x08000000: "familiar_ignore_reimu_homing",
        0x10000000: "bomb_immune",
        0x20000000: "legacy_546_clear_unknown",
        0x40000000: "engine_internal",
        0x80000000: "familiar_hit_flash_purple",
    },
}

UNIT_FLAG_VALUE_BY_PROFILE_SEMANTIC: dict[tuple[str, str], int] = {}
for profile, flags in UNIT_FLAG_SEMANTICS_BY_PROFILE.items():
    for value, semantic in flags.items():
        UNIT_FLAG_VALUE_BY_PROFILE_SEMANTIC.setdefault((profile, semantic), value)

LOSSY_UNIT_FLAG_TARGETS: dict[str, str | None] = {
    "legacy_th10_blank": None,
}


def parse_int_mask(value: Any) -> int | None:
    raw = plain(value).strip()
    if not raw:
        return None
    try:
        return int(raw, 0)
    except ValueError:
        return None


def unit_flag_components(game: str, raw_flag: Any) -> list[dict[str, Any]]:
    profile = flag_profile_for_game(game)
    mask = parse_int_mask(raw_flag)
    if mask is None:
        return [{"source_value": plain(raw_flag), "semantic": f"expr:{plain(raw_flag)}", "profile": profile}]
    table = UNIT_FLAG_SEMANTICS_BY_PROFILE.get(profile, {})
    components: list[dict[str, Any]] = []
    remaining = mask
    bit = 1
    while remaining:
        if remaining & bit:
            semantic = table.get(bit, f"raw_bit:{bit}")
            components.append({"source_value": bit, "semantic": semantic, "profile": profile})
            remaining &= ~bit
        bit <<= 1
    if not components:
        components.append({"source_value": 0, "semantic": "none", "profile": profile})
    return components


def encode_unit_flag_semantic(semantic: str, target: str) -> int | None:
    if semantic in LOSSY_UNIT_FLAG_TARGETS:
        return LOSSY_UNIT_FLAG_TARGETS[semantic]
    profile = flag_profile_for_game(target)
    encoded = UNIT_FLAG_VALUE_BY_PROFILE_SEMANTIC.get((profile, semantic))
    if encoded is not None:
        return encoded
    if semantic.startswith("raw_bit:"):
        try:
            return int(semantic.split(":", 1)[1], 0)
        except ValueError:
            return None
    return None


def unit_flag_semantics(game: str, op_key: str, raw_flag: Any, function: str) -> dict[str, Any]:
    components = unit_flag_components(game, raw_flag)
    return {
        "op_key": op_key,
        "raw_flag": plain(raw_flag),
        "profile": flag_profile_for_game(game),
        "function": function,
        "components": components,
        "names": [component["semantic"] for component in components],
    }


def remap_unit_flag_mask(source_game: str, target: str, raw_flag: Any) -> dict[str, Any]:
    components = unit_flag_components(source_game, raw_flag)
    target_mask = 0
    emitted: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    for component in components:
        semantic = str(component.get("semantic", ""))
        encoded = encode_unit_flag_semantic(semantic, target)
        mapped = dict(component)
        mapped["target_value"] = encoded
        if encoded is None or encoded == 0:
            dropped.append(mapped)
        else:
            target_mask |= encoded
            emitted.append(mapped)
    return {
        "source": plain(raw_flag),
        "source_profile": flag_profile_for_game(source_game),
        "target_profile": flag_profile_for_game(target),
        "target_mask": target_mask,
        "target_flag": str(target_mask) if target_mask else "drop",
        "components": components,
        "emitted": emitted,
        "dropped": dropped,
    }


def spread_semantic(game: str, style: Any) -> dict[str, Any]:
    raw = plain(style).strip()
    generation = generation_for_game(game)
    style_semantic = SPREAD_BY_GENERATION_VALUE.get((generation, raw))
    if style_semantic:
        parts = style_semantic.semantic.split(".")
        if parts[0] == "double_flower":
            return {
                "semantic": style_semantic.semantic,
                "spread_family": "double_flower",
                "target_biases": ["left", "right"],
                "aimed": parts[1] == "aimed",
                "source_raw": raw,
            }
        if parts[0] == "single_flower":
            return {
                "semantic": style_semantic.semantic,
                "spread_family": "single_flower",
                "bias": parts[1],
                "aimed": parts[2] == "aimed",
                "source_raw": raw,
            }
        return {
            "semantic": style_semantic.semantic,
            "spread_family": parts[0],
            "source_raw": raw,
            "aimed": parts[-1] == "aimed",
        }
    return {"semantic": f"raw:{raw}", "spread_family": "raw", "raw": raw, "aimed": raw in {"0", "2", "4", "9"}}


def spread_semantic_key(spread: dict[str, Any]) -> str:
    semantic = spread.get("semantic")
    if isinstance(semantic, str) and semantic:
        return semantic
    family = spread.get("spread_family")
    aimed = "aimed" if bool(spread.get("aimed")) else "fixed"
    if family == "double_flower":
        return f"double_flower.{aimed}"
    if family == "single_flower":
        return f"single_flower.{spread.get('bias', 'left')}.{aimed}"
    return f"raw:{spread.get('raw', '')}"


def encode_spread_style(spread: dict[str, Any], target: str, fallback: Any = None) -> str:
    semantic = spread_semantic_key(spread)
    if semantic.startswith("raw:"):
        return semantic[4:] or plain(fallback, "1")
    style = SPREAD_BY_SEMANTIC.get(semantic)
    if style:
        encoded = style.encode(generation_for_game(target))
        if encoded is not None:
            return encoded
    return plain(fallback, "1")


def th12_double_flower_pair(spread: dict[str, Any]) -> tuple[str, str] | None:
    # TH12 has no native double-flower style. Preserve the semantic by emitting two
    # single-flower emitters, not by pretending style 9/10 exists in TH12.
    if spread.get("spread_family") != "double_flower":
        return None
    aimed = bool(spread.get("aimed"))
    return ("4", "2") if aimed else ("5", "3")


def opcode_map_for(source_game: str, target: str, source_opcode: int) -> RawOpcodeMap | None:
    return OPCODE_BY_SOURCE_TARGET.get((generation_for_game(source_game), generation_for_game(target), source_opcode))


def boss_phase_prefix_ops(op_key: str, target: str) -> list[str]:
    if generation_for_game(target) == GEN_TH13_PLUS and op_key == "boss.set_interrupt":
        return ["[-9947] = 1;"]
    return []


def unsupported_opcode_reason(source_game: str, target: str, source_opcode: int) -> str | None:
    return UNSUPPORTED_SEMANTIC_OPCODES.get((generation_for_game(source_game), source_opcode, generation_for_game(target)))


def remap_raw_arg_by_semantic(source_game: str, target: str, source_opcode: int, target_opcode: int, args: list[str]) -> list[str]:
    mapped = args[:]
    source_generation = generation_for_game(source_game)
    target_generation = generation_for_game(target)
    semantic_map = opcode_map_for(source_game, target, source_opcode)
    semantic_key = semantic_map.semantic if semantic_map is not None else ""
    if source_generation == GEN_TH13_PLUS and target_generation == GEN_TH12 and source_opcode == 302 and target_opcode == 258 and len(mapped) == 1:
        # ANM bank ids moved by one between these generations for the stage files we lower.
        if mapped[0] == "2":
            mapped[0] = "1"
        elif mapped[0] == "3":
            mapped[0] = "2"
    elif source_opcode in {256, 257, 260, 261, 265, 266, 267, 268, 270, 271, 300, 301, 304, 305, 309, 310, 311, 312} and source_opcode != target_opcode and len(mapped) >= 6:
        mapped[5] = remap_create_item_policy(source_game, target, mapped[5])
    elif semantic_key == "bullet.emitter.02" and source_opcode != target_opcode and len(mapped) >= 3:
        mapped[1] = encode_bullet_shape(bullet_shape_semantic(source_game, mapped[1]), target, mapped[1])
    elif semantic_key == "bullet.emitter.07" and source_opcode != target_opcode and len(mapped) >= 2:
        mapped[1] = encode_spread_style(spread_semantic(source_game, mapped[1]), target, mapped[1])
    elif semantic_key == "bullet.emitter.09" and source_opcode != target_opcode and len(mapped) >= 5:
        source_mode = mapped[3]
        mapped[3] = remap_bullet_transform_mode(source_game, target, source_mode)
        mapped[4] = remap_shape_change_arg(source_game, target, source_mode, mapped[4])
        if source_generation == GEN_TH12 and target_generation == GEN_TH13_PLUS:
            for index in range(6, len(mapped)):
                if mapped[index] == "-999.0f":
                    mapped[index] = "-999999.0f"
    if semantic_key in {"unit.drop_extra", "unit.drop_main"} and source_opcode != target_opcode:
        drop_type_index = 0
        if len(mapped) > drop_type_index:
            mapped[drop_type_index] = remap_drop_type(source_game, target, mapped[drop_type_index])
    return mapped


def remap_drop_type(source_game: str, target: str, value: str) -> str:
    text = str(value).strip()
    if generation_for_game(source_game) == generation_for_game(target):
        return text
    return encode_drop_type(drop_type_semantic(source_game, text), target, text)


def remap_create_item_policy(source_game: str, target: str, value: str) -> str:
    text = str(value).strip()
    if generation_for_game(source_game) == generation_for_game(target):
        return text
    return encode_drop_type(drop_type_semantic(source_game, text), target, text)
