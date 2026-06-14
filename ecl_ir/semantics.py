from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .reference import opcode_reference, opcode_signature

TH13PLUS_GAMES = {"th13", "th14", "th15", "th16", "th17", "th18"}
TH10_TH11_GAMES = {"th10", "th11"}
TH12_GAMES = {"th12"}
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


def lifted_raw_coverage_policy(kind: str, source_game: str, target: str, family: str = "") -> str:
    source_generation = generation_for_game(source_game)
    target_generation = generation_for_game(target)
    if kind == "BulletEmitter" and family == "th12" and source_generation == GEN_TH12 and target_generation == GEN_TH13_PLUS:
        return "contiguous_setup_prefix"
    return "default"


# Opcode semantics are registered by meaning first, then encoded per generation.
SEMANTIC_OPCODES: tuple[SemanticOpcode, ...] = (
    SemanticOpcode("enemy.create", {GEN_TH13_PLUS: 300, GEN_TH12: 256}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_async", {GEN_TH13_PLUS: 301, GEN_TH12: 257}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("animation.select", {GEN_TH13_PLUS: 302, GEN_TH12: 258}, {(GEN_TH13_PLUS, GEN_TH12): (0,)}),
    SemanticOpcode("animation.set_sprite", {GEN_TH13_PLUS: 303, GEN_TH12: 259}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("enemy.create_main", {GEN_TH13_PLUS: 304, GEN_TH12: 260}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_async_main", {GEN_TH13_PLUS: 305, GEN_TH12: 261}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("animation.set_main", {GEN_TH13_PLUS: 306, GEN_TH12: 262}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("animation.play", {GEN_TH13_PLUS: 307, GEN_TH12: 263}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("animation.play_abs", {GEN_TH13_PLUS: 308, GEN_TH12: 264}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("enemy.create_func", {GEN_TH13_PLUS: 309, GEN_TH12: 265}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_async_func", {GEN_TH13_PLUS: 310, GEN_TH12: 266}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_main_func", {GEN_TH13_PLUS: 311, GEN_TH12: 267}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.create_async_main_func", {GEN_TH13_PLUS: 312, GEN_TH12: 268}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("enemy.byakuren_butterfly", {GEN_TH12: 281}),
    SemanticOpcode("movement.position.set", {GEN_TH13_PLUS: 400, GEN_TH12: 300}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.position.tween", {GEN_TH13_PLUS: 401, GEN_TH12: 301}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.position_rel.set", {GEN_TH13_PLUS: 402, GEN_TH12: 302}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.position_rel.tween", {GEN_TH13_PLUS: 403, GEN_TH12: 303}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.velocity.set", {GEN_TH13_PLUS: 404, GEN_TH12: 304}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.velocity.tween", {GEN_TH13_PLUS: 405, GEN_TH12: 305}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.velocity_rel.set", {GEN_TH13_PLUS: 406, GEN_TH12: 306}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1)}),
    SemanticOpcode("movement.velocity_rel.tween", {GEN_TH13_PLUS: 407, GEN_TH12: 307}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3)}),
    SemanticOpcode("movement.ellipse.set", {GEN_TH13_PLUS: 420, GEN_TH12: 320}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("movement.ellipse.tween", {GEN_TH13_PLUS: 421, GEN_TH12: 321}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.ellipse_rel.set", {GEN_TH13_PLUS: 422, GEN_TH12: 322}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5)}),
    SemanticOpcode("movement.ellipse_rel.tween", {GEN_TH13_PLUS: 423, GEN_TH12: 323}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.mirror_mode", {GEN_TH13_PLUS: 424, GEN_TH12: 324}, {(GEN_TH13_PLUS, GEN_TH12): (0,)}),
    SemanticOpcode("movement.bezier", {GEN_TH13_PLUS: 425, GEN_TH12: 325}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.bezier_rel", {GEN_TH13_PLUS: 426, GEN_TH12: 326}, {(GEN_TH13_PLUS, GEN_TH12): (0, 1, 2, 3, 4, 5, 6)}),
    SemanticOpcode("movement.reset", {GEN_TH13_PLUS: 427, GEN_TH12: 327}, {(GEN_TH13_PLUS, GEN_TH12): ()}),
    *tuple(SemanticOpcode(f"unit.property.{op - 500:02d}", {GEN_TH13_PLUS: op, GEN_TH12: op - 100}) for op in range(500, 511)),
    SemanticOpcode("boss.life_set", {GEN_TH13_PLUS: 511, GEN_TH12: 411}),
    SemanticOpcode("boss.set_boss", {GEN_TH13_PLUS: 512, GEN_TH12: 412}),
    SemanticOpcode("boss.timer_reset", {GEN_TH13_PLUS: 513, GEN_TH12: 413}),
    SemanticOpcode("boss.set_interrupt", {GEN_TH13_PLUS: 514, GEN_TH12: 414}),
    *tuple(SemanticOpcode(f"unit.property.{op - 500:02d}", {GEN_TH13_PLUS: op, GEN_TH12: op - 100}) for op in range(515, 519)),
    SemanticOpcode("unit.dialog_wait", {GEN_TH13_PLUS: 519, GEN_TH12: 419}),
    SemanticOpcode("unit.boss_wait", {GEN_TH13_PLUS: 520, GEN_TH12: 420}),
    SemanticOpcode("boss.set_timeout", {GEN_TH13_PLUS: 521, GEN_TH12: 421}),
    SemanticOpcode("unit.property.22", {GEN_TH13_PLUS: 522, GEN_TH12: 422}),
    SemanticOpcode("boss.spell_end", {GEN_TH13_PLUS: 523, GEN_TH12: 423}),
    SemanticOpcode("boss.set_chapter", {GEN_TH13_PLUS: 524, GEN_TH12: 424}),
    SemanticOpcode("enemy.enm_kill_all", {GEN_TH13_PLUS: 525, GEN_TH12: 425}),
    SemanticOpcode("unit.property.27", {GEN_TH13_PLUS: 527, GEN_TH12: 427}),
    SemanticOpcode("unit.property.28", {GEN_TH13_PLUS: 528, GEN_TH12: 428}),
    SemanticOpcode("unit.property.29", {GEN_TH13_PLUS: 529, GEN_TH12: 429}),
    SemanticOpcode("unit.property.30", {GEN_TH13_PLUS: 530, GEN_TH12: 430}),
    SemanticOpcode("unit.property.31", {GEN_TH13_PLUS: 531, GEN_TH12: 431}),
    SemanticOpcode("unit.property.32", {GEN_TH13_PLUS: 532, GEN_TH12: 432}),
    SemanticOpcode("unit.property.33", {GEN_TH13_PLUS: 533, GEN_TH12: 433}),
    SemanticOpcode("unit.property.34", {GEN_TH13_PLUS: 534, GEN_TH12: 434}),
    SemanticOpcode("unit.diff_i", {GEN_TH13_PLUS: 535, GEN_TH12: 435}),
    SemanticOpcode("unit.diff_f", {GEN_TH13_PLUS: 536, GEN_TH12: 436}),
    SemanticOpcode("boss.spell", {GEN_TH13_PLUS: 537, GEN_TH12: 437}),
    SemanticOpcode("boss.spell2", {GEN_TH13_PLUS: 538, GEN_TH12: 438}),
    SemanticOpcode("boss.spell3", {GEN_TH13_PLUS: 539, GEN_TH12: 439}),
    SemanticOpcode("unit.stars", {GEN_TH13_PLUS: 540, GEN_TH12: 440}),
    SemanticOpcode("unit.property.42", {GEN_TH13_PLUS: 542, GEN_TH12: 442}),
    SemanticOpcode("unit.property.43", {GEN_TH13_PLUS: 543, GEN_TH12: 443}),
    SemanticOpcode("unit.property.44", {GEN_TH13_PLUS: 544, GEN_TH12: 444}),
    SemanticOpcode("unit.laser_cancel", {GEN_TH13_PLUS: 545, GEN_TH12: 445}),
    SemanticOpcode("unit.property.46", {GEN_TH13_PLUS: 546, GEN_TH12: 446}),
    SemanticOpcode("unit.property.47", {GEN_TH13_PLUS: 547, GEN_TH12: 447}),
    SemanticOpcode("unit.property.48", {GEN_TH13_PLUS: 548, GEN_TH12: 448}),
    SemanticOpcode("unit.property.49", {GEN_TH13_PLUS: 549, GEN_TH12: 449}),
    SemanticOpcode("unit.effect.53", {GEN_TH13_PLUS: 553, GEN_TH12: 453}),
    SemanticOpcode("unit.effect.54", {GEN_TH13_PLUS: 554, GEN_TH12: 454}),
    SemanticOpcode("unit.effect.55", {GEN_TH13_PLUS: 555, GEN_TH12: 455}),
    SemanticOpcode("unit.effect.56", {GEN_TH13_PLUS: 556, GEN_TH12: 456}),
    *tuple(SemanticOpcode(f"bullet.emitter.{op - 600:02d}", {GEN_TH13_PLUS: op, GEN_TH12: op - 100}) for op in range(600, 610)),
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
    SemanticValue("point_highlight", {GEN_TH13_PLUS: "1", GEN_TH12: "1", GEN_TH10_TH11: "1", GEN_TH06_TH08: "0"}),
    SemanticValue("grape", {GEN_TH13_PLUS: "2", GEN_TH12: "2", GEN_TH10_TH11: "2", GEN_TH06_TH08: "2"}),
    SemanticValue("orb_small", {GEN_TH13_PLUS: "4", GEN_TH12: "3", GEN_TH10_TH11: "3", GEN_TH06_TH08: "3"}),
    SemanticValue("orb_small_highlight", {GEN_TH13_PLUS: "5", GEN_TH12: "4", GEN_TH10_TH11: "4", GEN_TH06_TH08: "3"}),
    SemanticValue("orb_ring", {GEN_TH13_PLUS: "6", GEN_TH12: "5", GEN_TH10_TH11: "5", GEN_TH06_TH08: "6"}),
    SemanticValue("orb_ring_highlight", {GEN_TH13_PLUS: "7", GEN_TH12: "6", GEN_TH10_TH11: "6", GEN_TH06_TH08: "6"}),
    SemanticValue("rice", {GEN_TH13_PLUS: "8", GEN_TH12: "7", GEN_TH10_TH11: "7", GEN_TH06_TH08: "7"}),
    SemanticValue("chain", {GEN_TH13_PLUS: "9", GEN_TH12: "8", GEN_TH10_TH11: "8", GEN_TH06_TH08: "8"}),
    SemanticValue("needle", {GEN_TH13_PLUS: "10", GEN_TH12: "9", GEN_TH10_TH11: "9", GEN_TH06_TH08: "9"}),
    SemanticValue("amulet", {GEN_TH13_PLUS: "11", GEN_TH12: "10", GEN_TH10_TH11: "10", GEN_TH06_TH08: "10"}),
    SemanticValue("scale", {GEN_TH13_PLUS: "12", GEN_TH12: "11", GEN_TH10_TH11: "11", GEN_TH06_TH08: "11"}),
    SemanticValue("bell", {GEN_TH13_PLUS: "13", GEN_TH12: "12", GEN_TH10_TH11: "12", GEN_TH06_TH08: "9"}),
    SemanticValue("cancel_effect", {GEN_TH13_PLUS: "14", GEN_TH12: "13", GEN_TH10_TH11: "13", GEN_TH06_TH08: "13"}),
    SemanticValue("bacillus", {GEN_TH13_PLUS: "15", GEN_TH12: "14", GEN_TH10_TH11: "14", GEN_TH06_TH08: "14"}),
    SemanticValue("small_star", {GEN_TH13_PLUS: "16", GEN_TH12: "15", GEN_TH10_TH11: "15", GEN_TH06_TH08: "8"}),
    SemanticValue("coin", {GEN_TH13_PLUS: "17", GEN_TH12: "16", GEN_TH10_TH11: "16", GEN_TH06_TH08: "16"}),
    SemanticValue("orb_medium", {GEN_TH13_PLUS: "18", GEN_TH12: "17", GEN_TH10_TH11: "17", GEN_TH06_TH08: "8"}),
    SemanticValue("orb_medium_highlight", {GEN_TH13_PLUS: "19", GEN_TH12: "18", GEN_TH10_TH11: "18", GEN_TH06_TH08: "8"}),
    SemanticValue("ellipse", {GEN_TH13_PLUS: "20", GEN_TH12: "19", GEN_TH10_TH11: "19", GEN_TH06_TH08: "19"}),
    SemanticValue("knife", {GEN_TH13_PLUS: "21", GEN_TH12: "20", GEN_TH10_TH11: "20", GEN_TH06_TH08: "20"}),
    SemanticValue("butterfly", {GEN_TH13_PLUS: "22", GEN_TH12: "21", GEN_TH10_TH11: "21", GEN_TH06_TH08: "21"}),
    SemanticValue("big_star", {GEN_TH13_PLUS: "23", GEN_TH12: "22", GEN_TH10_TH11: "22", GEN_TH06_TH08: "8"}),
    SemanticValue("big_star_reverse", {GEN_TH13_PLUS: "24", GEN_TH12: "22", GEN_TH10_TH11: "22", GEN_TH06_TH08: "8"}, lossy_targets=(GEN_TH12, GEN_TH10_TH11, GEN_TH06_TH08)),
    SemanticValue("light_orb", {GEN_TH13_PLUS: "33", GEN_TH12: "23"}),
    SemanticValue("light_flame", {GEN_TH13_PLUS: "25", GEN_TH12: "24"}),
    SemanticValue("heart", {GEN_TH13_PLUS: "29", GEN_TH12: "25", GEN_TH10_TH11: "25", GEN_TH06_TH08: "25"}),
    SemanticValue("orb_large", {GEN_TH13_PLUS: "32", GEN_TH12: "26"}),
    SemanticValue("rose", {GEN_TH13_PLUS: "34", GEN_TH12: "27"}, lossy_targets=(GEN_TH13_PLUS,)),
    SemanticValue("drop", {GEN_TH13_PLUS: "34", GEN_TH12: "28"}),
    SemanticValue("purple_flame", {GEN_TH13_PLUS: "26", GEN_TH12: "29"}),
    SemanticValue("laser_segment", {GEN_TH13_PLUS: "38", GEN_TH12: "30"}),
)
BULLET_SHAPE_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for shape in BULLET_SHAPES:
    for generation, value in shape.values.items():
        BULLET_SHAPE_BY_GENERATION_VALUE.setdefault((generation, value), shape)
BULLET_SHAPE_BY_SEMANTIC = {shape.semantic: shape for shape in BULLET_SHAPES}

BULLET_TRANSFORM_MODES: tuple[SemanticValue, ...] = (
    SemanticValue("spawn_step", {GEN_TH13_PLUS: "1", GEN_TH12: "1"}),
    SemanticValue("set_mist", {GEN_TH13_PLUS: "2", GEN_TH12: "2"}),
    SemanticValue("accel", {GEN_TH13_PLUS: "4", GEN_TH12: "4"}),
    SemanticValue("tangent_accel", {GEN_TH13_PLUS: "8", GEN_TH12: "8"}),
    SemanticValue("pause_then_velocity", {GEN_TH13_PLUS: "16", GEN_TH12: "64"}),
    SemanticValue("pause_then_relative_velocity", {GEN_TH12: "16"}),
    SemanticValue("pause_then_aimed_velocity", {GEN_TH12: "32"}),
    SemanticValue("bounce", {GEN_TH13_PLUS: "64", GEN_TH12: "256"}),
    SemanticValue("uncancelable_time", {GEN_TH13_PLUS: "128", GEN_TH12: "512"}),
    SemanticValue("offscreen_time", {GEN_TH13_PLUS: "256", GEN_TH12: "1024"}),
    SemanticValue("shape_change", {GEN_TH13_PLUS: "512", GEN_TH12: "2048"}),
    SemanticValue("delete", {GEN_TH13_PLUS: "1024", GEN_TH12: "8192"}),
    SemanticValue("sound", {GEN_TH13_PLUS: "2048", GEN_TH12: "16384"}),
    SemanticValue("wait_next", {GEN_TH13_PLUS: "-2147483648", GEN_TH12: "4096"}),
    SemanticValue("jump", {GEN_TH13_PLUS: "65536", GEN_TH12: "4194304"}),
    SemanticValue("independent_velocity", {GEN_TH13_PLUS: "524288", GEN_TH12: "134217728"}),
    SemanticValue("highlight", {GEN_TH13_PLUS: "1048576", GEN_TH12: "268435456"}),
    SemanticValue("velocity_over_time", {GEN_TH13_PLUS: "2097152", GEN_TH12: "536870912"}),
)
BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE: dict[tuple[str, str], SemanticValue] = {}
for mode in BULLET_TRANSFORM_MODES:
    for generation, value in mode.values.items():
        BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE.setdefault((generation, value), mode)
BULLET_TRANSFORM_MODE_BY_SEMANTIC = {mode.semantic: mode for mode in BULLET_TRANSFORM_MODES}

UNSUPPORTED_BULLET_TRANSFORM_MODE_REASONS: dict[tuple[str, str, str], str] = {
    (
        GEN_TH12,
        GEN_TH13_PLUS,
        "2097152",
    ): "TH12 etEx mode 2097152 is not TH13+ mode 2097152; the TH13+ value is velocity-over-time and corrupts TH12 transform chains",
}

SPREAD_STYLES: tuple[SemanticValue, ...] = (
    SemanticValue("single_flower.right.aimed", {GEN_TH12: "2", GEN_TH10_TH11: "2"}),
    SemanticValue("single_flower.right.fixed", {GEN_TH12: "3", GEN_TH10_TH11: "3"}),
    SemanticValue("single_flower.left.aimed", {GEN_TH13_PLUS: "2", GEN_TH12: "4", GEN_TH10_TH11: "4"}),
    SemanticValue("single_flower.left.fixed", {GEN_TH13_PLUS: "3", GEN_TH12: "5", GEN_TH10_TH11: "5"}),
    SemanticValue("single_flower.offset_left.aimed", {GEN_TH13_PLUS: "4", GEN_TH12: "4", GEN_TH10_TH11: "4"}, lossy_targets=(GEN_TH12, GEN_TH10_TH11)),
    SemanticValue("single_flower.offset_left.fixed", {GEN_TH13_PLUS: "5", GEN_TH12: "5", GEN_TH10_TH11: "5"}, lossy_targets=(GEN_TH12, GEN_TH10_TH11)),
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
    semantic = BULLET_SHAPE_BY_GENERATION_VALUE.get((generation_for_game(game), raw))
    if semantic:
        return semantic.semantic
    return f"raw:{raw}"


def encode_bullet_shape(semantic: str, target: str, fallback: Any = None) -> str:
    if semantic.startswith("raw:"):
        return semantic[4:]
    shape = BULLET_SHAPE_BY_SEMANTIC.get(semantic)
    if shape:
        encoded = shape.encode(generation_for_game(target))
        if encoded is not None:
            return encoded
    return plain(fallback, "0")


def bullet_transform_mode_semantic(game: str, mode: Any) -> str:
    raw = plain(mode).strip()
    semantic = BULLET_TRANSFORM_MODE_BY_GENERATION_VALUE.get((generation_for_game(game), raw))
    if semantic:
        return semantic.semantic
    return f"raw:{raw}"


def encode_bullet_transform_mode(semantic: str, target: str, fallback: Any = None) -> str:
    if semantic.startswith("raw:"):
        return semantic[4:]
    mode = BULLET_TRANSFORM_MODE_BY_SEMANTIC.get(semantic)
    if mode:
        encoded = mode.encode(generation_for_game(target))
        if encoded is not None:
            return encoded
    return plain(fallback, "0")


def remap_bullet_transform_mode(source_game: str, target: str, mode: Any) -> str:
    return encode_bullet_transform_mode(bullet_transform_mode_semantic(source_game, mode), target, mode)


def unsupported_bullet_transform_mode_reason(source_game: str, target: str, mode: Any) -> str | None:
    return UNSUPPORTED_BULLET_TRANSFORM_MODE_REASONS.get(
        (generation_for_game(source_game), generation_for_game(target), plain(mode).strip())
    )


def remap_shape_change_arg(source_game: str, target: str, mode: Any, shape: Any) -> str:
    if bullet_transform_mode_semantic(source_game, mode) != "shape_change":
        return str(shape)
    return encode_bullet_shape(bullet_shape_semantic(source_game, shape), target, shape)


def th13_append_transform_to_th12_509(args: list[object], index: int, source_game: str = "th15") -> list[str] | None:
    if len(args) != 7:
        return None
    et_id, channel, mode, a, b, r, s = [str(arg) for arg in args]
    mapped_mode = remap_bullet_transform_mode(source_game, "th12", mode)
    a = remap_shape_change_arg(source_game, "th12", mode, a)
    # TH13+ ins_611 appends a transform and omits the transform index.
    # TH12 ins_509 needs that index explicitly: et, index, channel, mode, a, b, r, s.
    return [et_id, str(index), channel, mapped_mode, a, b, r, s]


def th13_transform_set_to_th12_509(args: list[object], source_game: str = "th15") -> list[str] | None:
    if len(args) != 8:
        return None
    converted = [str(arg) for arg in args]
    converted[3] = remap_bullet_transform_mode(source_game, "th12", converted[3])
    converted[4] = remap_shape_change_arg(source_game, "th12", args[3], converted[4])
    return converted


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
    if source_generation == GEN_TH13_PLUS and target_generation == GEN_TH12 and source_opcode == 302 and target_opcode == 258 and len(mapped) == 1:
        # ANM bank ids moved by one between these generations for the stage files we lower.
        if mapped[0] == "2":
            mapped[0] = "1"
        elif mapped[0] == "3":
            mapped[0] = "2"
    elif source_opcode in {602, 502} and source_opcode != target_opcode and len(mapped) >= 3:
        mapped[1] = encode_bullet_shape(bullet_shape_semantic(source_game, mapped[1]), target, mapped[1])
    elif source_opcode in {607, 507} and source_opcode != target_opcode and len(mapped) >= 2:
        mapped[1] = encode_spread_style(spread_semantic(source_game, mapped[1]), target, mapped[1])
    elif source_opcode in {609, 509} and source_opcode != target_opcode and len(mapped) >= 5:
        source_mode = mapped[3]
        mapped[3] = remap_bullet_transform_mode(source_game, target, source_mode)
        mapped[4] = remap_shape_change_arg(source_game, target, source_mode, mapped[4])
        if source_generation == GEN_TH12 and target_generation == GEN_TH13_PLUS:
            for index in range(6, len(mapped)):
                if mapped[index] == "-999.0f":
                    mapped[index] = "-999999.0f"
    return mapped
