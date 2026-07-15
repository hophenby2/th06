from __future__ import annotations

import unittest

from ecl_ir.target.lowering import LoweringPlanner
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.canonical.semantic_ir import SemanticModule, SemanticRoutine
from ecl_ir.dialects.semantics import (
    bullet_shape_can_encode,
    bullet_shape_semantic,
    encode_bullet_shape,
)
from ecl_ir.target.target_ir import CanonicalBackendEmitter, TargetAstBuilder


def lower_visual(source_game: str, shape: str, target: str):
    operation = semantic_operation(
        source_game,
        602 if source_game.startswith("th1") and source_game not in {"th10", "th11", "th12"} else {
            "th10": 402,
            "th11": 402,
            "th12": 502,
        }[source_game],
        ["0", shape, "3"],
        1,
        routine="Main",
    )
    module = SemanticModule(
        source="fixture.decl",
        source_game=source_game,
        profile=source_game,
        routines=[SemanticRoutine("Main", body=[operation])],
    )
    planner = LoweringPlanner.for_game(
        target,
        backend_emitter=CanonicalBackendEmitter(module, target),
    )
    return TargetAstBuilder(planner).build(module).routines[0].body[0]


class BulletShapeTests(unittest.TestCase):
    def test_early_game_catalogs_are_not_a_shared_numeric_generation(self) -> None:
        self.assertEqual(bullet_shape_semantic("th06", "6"), "orb_medium")
        self.assertEqual(bullet_shape_semantic("th07", "6"), "scale")
        self.assertEqual(bullet_shape_semantic("th08", "1"), "orb_ring")
        self.assertEqual(encode_bullet_shape("orb_ring", "th15"), "6")
        self.assertEqual(encode_bullet_shape("butterfly", "th15"), "22")
        self.assertFalse(bullet_shape_can_encode("legacy_knife", "th15"))

    def test_pre_th15_shape_shift_is_game_specific(self) -> None:
        self.assertEqual(bullet_shape_semantic("th14", "24"), "light_flame")
        self.assertEqual(encode_bullet_shape("light_flame", "th15"), "25")
        self.assertEqual(bullet_shape_semantic("th15", "24"), "big_star_reverse")
        self.assertFalse(bullet_shape_can_encode("big_star_reverse", "th14"))

        self.assertEqual(bullet_shape_semantic("th15", "34"), "drop")
        self.assertEqual(encode_bullet_shape("drop", "th12"), "28")

    def test_canonical_visual_lowering_uses_the_target_catalog(self) -> None:
        shifted = lower_visual("th14", "24", "th15")
        self.assertEqual(shifted.strategy.value, "direct")
        self.assertEqual(shifted.lines, ("ins_602(0, 25, 3);",))

        unsupported = lower_visual("th15", "24", "th14")
        self.assertEqual(unsupported.strategy.value, "unsupported")
        self.assertEqual(
            unsupported.diagnostics[-1].code,
            "backend.bullet_shape.unsupported",
        )


if __name__ == "__main__":
    unittest.main()
