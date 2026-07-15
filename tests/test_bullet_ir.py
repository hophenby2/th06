from __future__ import annotations

import unittest

from ecl_ir.analysis.bullet_ir import (
    EmitterFire,
    analyze_bullet_routine,
    iter_fire_actions,
)
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.canonical.semantic_ir import OperandState, SemanticRoutine


def analyze(game: str, specs: list[tuple[int, list[str], str | None]]):
    routine = SemanticRoutine("Test")
    for line, (opcode, args, difficulty) in enumerate(specs, 1):
        routine.body.append(
            semantic_operation(
                game,
                opcode,
                args,
                line,
                difficulty,
                routine="Test",
                source="fixture.decl",
            )
        )
    return analyze_bullet_routine(routine, game)


class BulletIrTests(unittest.TestCase):
    def test_early_games_use_independent_opcode_families(self) -> None:
        self.assertEqual(semantic_operation("th06", 67, []).operation, "bullet.macro.configure")
        self.assertEqual(semantic_operation("th07", 64, []).operation, "bullet.macro.configure")
        self.assertEqual(semantic_operation("th08", 96, []).operation, "bullet.macro.configure")
        self.assertNotEqual(semantic_operation("th06", 96, []).domain, "bullet")
        self.assertNotEqual(semantic_operation("th07", 96, []).domain, "bullet")

        th06_origin = semantic_operation("th06", 81, ["1.0f", "2.0f", "3.0f"])
        th07_origin = semantic_operation("th07", 78, ["1.0f", "2.0f", "3.0f"])
        self.assertEqual([operand.name for operand in th06_origin.operands], ["x", "y", "z"])
        self.assertEqual([operand.name for operand in th07_origin.operands], ["x", "y", "z"])

    def test_th07_transform_replace_is_last_write_wins(self) -> None:
        result = analyze(
            "th07",
            [
                (79, ["0", "2", "0", "1", "-1", "-1.0f", "-1.0f"], None),
                (79, ["0", "4", "1", "30", "-1", "0.1f", "-1.0f"], None),
            ],
        )
        program = result.final_states["N"]["0"].definition.transforms
        self.assertEqual(list(program.slots), [0])
        self.assertEqual(program.slots[0].mode, "4")
        self.assertEqual(program.slots[0].channel, "1")

    def test_th08_defer_enable_and_auto_schedule_are_distinct(self) -> None:
        macro = ["0", "3", "4", "2", "1.0f", "2.0f", "0.0f", "0.1f", "0"]
        result = analyze(
            "th08",
            [
                (107, [], None),
                (96, macro, None),
                (108, [], None),
                (106, ["30"], None),
            ],
        )
        fires = list(iter_fire_actions(result))
        self.assertEqual([fire.trigger for fire in fires], ["enable"])
        state = result.final_states["N"]["0"].definition
        self.assertIsNotNone(state.auto_fire)
        self.assertTrue(state.auto_fire.random_initial_delay)
        self.assertEqual(state.auto_fire.interval.source_text, "30")

        default_result = analyze("th08", [(96, macro, None)])
        self.assertEqual([fire.trigger for fire in iter_fire_actions(default_result)], ["macro_default"])

    def test_fire_captures_an_immutable_definition_snapshot(self) -> None:
        result = analyze(
            "th13",
            [
                (600, ["0"], None),
                (602, ["0", "1", "2"], None),
                (601, ["0"], None),
                (602, ["0", "9", "10"], None),
            ],
        )
        fire = next(iter_fire_actions(result))
        snapshot = fire.snapshot_for("N")
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.visual.bullet_type.source_text, "1")
        final = result.final_states["N"]["0"].definition
        self.assertEqual(final.visual.bullet_type.source_text, "9")

    def test_th12_only_opcode_509_writes_transform_slots(self) -> None:
        result = analyze(
            "th12",
            [
                (500, ["0"], None),
                (509, ["0", "0", "0", "4", "30", "-999999", "0.1f", "-999999.0f"], None),
                (510, [], None),
                (512, ["64.0f"], None),
                (521, ["0", "1.0f", "2.0f", "3.0f", "4.0f", "5.0f", "6.0f", "7.0f", "8.0f"], None),
                (522, ["0", "1", "2", "3", "4", "5", "6", "7", "8"], None),
            ],
        )
        program = result.final_states["N"]["0"].definition.transforms
        self.assertEqual(list(program.slots), [0])
        self.assertEqual(program.slots[0].source_opcode, 509)
        system_operations = [action.operation for action in result.actions if action.kind == "bullet_system_action"]
        self.assertEqual(system_operations, ["bullet.clear_all", "bullet.cancel_radius"])

    def test_append_copy_patch_and_cursor_share_one_transform_program(self) -> None:
        short = ["0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"]
        result = analyze(
            "th14",
            [
                (600, ["0"], None),
                (611, short, None),
                (600, ["1"], None),
                (611, ["1", *short[1:]], None),
                (611, ["1", "0", "4", "30", "-999999", "0.1f", "-999999.0f"], None),
                (614, ["0", "1"], None),
                (609, ["0", "3", "0", "4", "60", "-999999", "0.2f", "-999999.0f"], None),
                (611, ["0", "1", "8", "10", "-999999", "0.3f", "0.4f"], None),
                (640, ["0", "0", '"SubName"'], None),
                (641, ["0"], None),
            ],
        )
        program = result.final_states["N"]["0"].definition.transforms
        self.assertEqual(set(program.slots), {0, 1, 3})
        self.assertEqual(program.slots[1].mode, "8")
        self.assertEqual(program.slots[0].string_operand.source_text, '"SubName"')
        self.assertEqual(program.append_cursor, 1)
        self.assertEqual(program.contiguous_prefix(), (0, 1))

    def test_holes_preserve_later_slots_but_stop_normal_prefix(self) -> None:
        result = analyze(
            "th13",
            [
                (600, ["0"], None),
                (609, ["0", "0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"], None),
                (609, ["0", "2", "0", "4", "30", "-999999", "0.1f", "-999999.0f"], None),
            ],
        )
        program = result.final_states["N"]["0"].definition.transforms
        self.assertEqual(set(program.slots), {0, 2})
        self.assertEqual(program.contiguous_prefix(), (0,))
        self.assertTrue(program.to_dict()["has_hole_before_last_slot"])

    def test_contextual_sentinels_distinguish_keep_current_and_unused(self) -> None:
        canonical = semantic_operation(
            "th18",
            610,
            [
                "0", "0", "0", "8192", "1", "2", "3", "4",
                "-9999994.0f", "0.0f", "-9999994.0f", "0.0f",
            ],
        )
        canonical_operands = {operand.name: operand.value for operand in canonical.operands}
        self.assertEqual(canonical_operands["r"].state, OperandState.KEEP_CURRENT)
        self.assertEqual(canonical_operands["m"].state, OperandState.KEEP_CURRENT)

        result = analyze(
            "th18",
            [
                (600, ["0"], None),
                (
                    610,
                    [
                        "0", "0", "0", "8192", "1", "2", "3", "4",
                        "-9999994.0f", "0.0f", "-9999994.0f", "0.0f",
                    ],
                    None,
                ),
                (609, ["0", "1", "0", "2", "1", "-9999994", "-9999994.0f", "-9999994.0f"], None),
            ],
        )
        program = result.final_states["N"]["0"].definition.transforms
        long_operands = {operand.name: operand.value for operand in program.slots[0].operands}
        self.assertEqual(long_operands["r"].state, OperandState.KEEP_CURRENT)
        self.assertEqual(long_operands["m"].state, OperandState.KEEP_CURRENT)
        short_operands = {operand.name: operand.value for operand in program.slots[1].operands}
        self.assertEqual(short_operands["b"].state, OperandState.UNUSED)
        self.assertEqual(short_operands["r"].state, OperandState.UNUSED)
        self.assertEqual(short_operands["r"].source_text, "-9999994.0f")

        th10_accel = semantic_operation(
            "th10",
            409,
            ["0", "0", "0", "16", "60", "-999999", "0.1f", "-999999.0f"],
        )
        th10_values = {operand.name: operand.value for operand in th10_accel.operands}
        self.assertEqual(th10_accel.annotations["transform_mode"], "accel")
        self.assertEqual(th10_values["s"].state, OperandState.KEEP_CURRENT)

        th12_delete = semantic_operation(
            "th12",
            509,
            ["0", "0", "0", "8192", "60", "-999999", "-999999.0f", "-999999.0f"],
        )
        th12_values = {operand.name: operand.value for operand in th12_delete.operands}
        self.assertEqual(th12_delete.annotations["transform_mode"], "delete")
        self.assertEqual(th12_values["r"].state, OperandState.UNUSED)

    def test_difficulty_guards_mutate_independent_state_lanes(self) -> None:
        result = analyze(
            "th13",
            [
                (600, ["0"], None),
                (602, ["0", "7", "8"], "E"),
                (601, ["0"], None),
            ],
        )
        fire = next(action for action in result.actions if isinstance(action, EmitterFire))
        self.assertEqual(fire.snapshot_for("E").visual.bullet_type.source_text, "7")
        self.assertIsNone(fire.snapshot_for("N").visual.bullet_type)


if __name__ == "__main__":
    unittest.main()
