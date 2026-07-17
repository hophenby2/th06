from __future__ import annotations

import unittest
from types import SimpleNamespace

from ecl_ir.compat.backend import (
    compile_ir_op_emission,
    compile_ir_op_event,
    normalize_backend_event,
    object_ir_events,
)
from ecl_ir.commands.main import covered_lines_for_lifted_object, emit_timeline_event
from ecl_ir.target.lowering import LoweringStrategy
from ecl_ir.source.model import Instruction, Statement
from ecl_ir.legacy.object_lifter import lift_all_objects
from ecl_ir.canonical.op_ir import op_event, semantic_operation, target_opcode_for_op_key
from ecl_ir.dialects.reference import is_opcode_supported, opcode_signature
from ecl_ir.source.parser import parse_decl
from ecl_ir.legacy.timeline_lifter import statement_to_event


class SemanticBackendTests(unittest.TestCase):
    def test_th11_inherits_alcostg_movement_formats_used_by_original_ecl(self) -> None:
        self.assertTrue(is_opcode_supported("th11", 302))
        self.assertEqual(opcode_signature("th11", 302), "ffffff")
        self.assertTrue(is_opcode_supported("th11", 303))
        self.assertEqual(opcode_signature("th11", 303), "ffffff")
        self.assertFalse(is_opcode_supported("th10", 302))

    def test_ellipse_rel_uses_shared_six_field_form_th11_and_newer(self) -> None:
        args = ["0.0f", "0.1f", "32.0f", "0.0f", "1.0f", "0.5f"]
        modern = semantic_operation("th18", 422, args)
        legacy = semantic_operation("th11", 302, args)

        self.assertEqual(
            [operand.name for operand in modern.operands],
            [
                "theta",
                "angular_speed",
                "radius",
                "radius_delta",
                "ellipse_angle",
                "ellipse_ratio",
            ],
        )
        self.assertEqual(
            compile_ir_op_event(modern, "th11"),
            f"ins_302({', '.join(args)});",
        )
        self.assertEqual(
            compile_ir_op_event(legacy, "th15"),
            f"ins_422({', '.join(args)});",
        )

    def test_bezier_coordinates_are_not_normalized_as_interpolation_mode(self) -> None:
        args = ["120", "1.0f", "2.0f", "3.0f", "4.0f", "5.0f", "6.0f"]
        bezier = semantic_operation("th13", 425, args)

        self.assertEqual(
            compile_ir_op_event(bezier, "th12"),
            f"ins_325({', '.join(args)});",
        )
        self.assertEqual(
            compile_ir_op_event(bezier, "th11"),
            f"ins_305({', '.join(args)});",
        )
        unsupported = compile_ir_op_emission(bezier, "th10")
        self.assertIsNotNone(unsupported)
        self.assertEqual(unsupported.strategy, LoweringStrategy.UNSUPPORTED)

    def test_move_vel_nm_time_projects_th12_float_mode_to_modern_int_mode(self) -> None:
        th12 = semantic_operation("th12", 329, ["60", "0.0f", "0.1f", "1.0f"])
        modern = semantic_operation("th13", 429, ["60", "0", "0.1f", "1.0f"])

        self.assertEqual(
            [operand.name for operand in th12.operands],
            ["duration", "interpolation", "angle", "speed"],
        )
        self.assertEqual(
            compile_ir_op_event(th12, "th15"),
            "ins_429(60, 0, 0.1f, 1.0f);",
        )
        self.assertEqual(
            compile_ir_op_event(modern, "th12"),
            "ins_329(60, 0.0f, 0.1f, 1.0f);",
        )

    def test_et_offsets_use_the_verified_th11_layout(self) -> None:
        radial = semantic_operation("th11", 437, ["1", "0.25f", "80.0f"])
        absolute = semantic_operation("th14", 628, ["1", "32.0f", "48.0f"])

        self.assertEqual(
            compile_ir_op_event(radial, "th12"),
            "ins_523(1, 0.25f, 80.0f);",
        )
        self.assertEqual(
            compile_ir_op_event(absolute, "th11"),
            "ins_439(1, 32.0f, 48.0f);",
        )
        unsupported = compile_ir_op_emission(absolute, "th10")
        self.assertIsNotNone(unsupported)
        self.assertEqual(unsupported.strategy, LoweringStrategy.UNSUPPORTED)

    def test_native_distance_maple_and_anm_reset_are_not_policy_dropped(self) -> None:
        distance = semantic_operation("th14", 627, ["1", "20.0f"])
        maple = semantic_operation(
            "th13",
            321,
            ['"MapleEnemy"', "0", "0", "100", "1000", "0"],
        )
        reset = semantic_operation("th14", 318, [])

        self.assertEqual(
            compile_ir_op_event(distance, "th11"),
            "ins_438(1, 20.0f);",
        )
        self.assertEqual(
            compile_ir_op_event(maple, "th12"),
            'ins_280("MapleEnemy", 0, 0, 100, 1000, 0);',
        )
        self.assertEqual(compile_ir_op_event(reset, "th12"), "ins_276();")
        for node, target in ((distance, "th10"), (maple, "th11"), (reset, "th10")):
            with self.subTest(operation=node.operation, target=target):
                unsupported = compile_ir_op_emission(node, target)
                self.assertIsNotNone(unsupported)
                self.assertEqual(unsupported.strategy, LoweringStrategy.UNSUPPORTED)

    def test_non_equivalent_or_unavailable_movement_forms_stay_unsupported(self) -> None:
        cases = (
            (semantic_operation("th15", 441, ["120", "7", "0.1f"]), "th13"),
            (semantic_operation("th15", 445, ["120", "1", "2.0f"]), "th12"),
            (semantic_operation("th13", 433, ["1"]), "th12"),
            (semantic_operation("th13", 429, ["60", "0", "0.1f", "1.0f"]), "th10"),
            (
                semantic_operation(
                    "th15",
                    423,
                    ["60", "0", "0.1f", "32.0f", "0.0f", "1.0f", "0.5f"],
                ),
                "th11",
            ),
            (
                semantic_operation(
                    "th13",
                    409,
                    ["120", "0", "0.1f", "32.0f", "0.0f"],
                ),
                "th10",
            ),
        )
        for node, target in cases:
            with self.subTest(operation=node.operation, target=target):
                emission = compile_ir_op_emission(node, target)
                self.assertIsNotNone(emission)
                self.assertEqual(emission.strategy, LoweringStrategy.UNSUPPORTED)

    def test_circle_tween_uses_only_abi_equivalent_target_forms(self) -> None:
        absolute = semantic_operation(
            "th13",
            409,
            ["120", "0", "0.1f", "32.0f", "0.0f"],
        )
        relative = semantic_operation(
            "th12",
            311,
            ["120", "9", "0.1f", "32.0f", "0.0f"],
        )

        self.assertEqual(
            compile_ir_op_event(absolute, "th11"),
            "ins_289(120, 0, 0.1f, 32.0f, 0.0f);",
        )
        self.assertEqual(
            compile_ir_op_event(relative, "th10"),
            "ins_291(120, 9, 0.1f, 32.0f, 0.0f, 0);",
        )
        self.assertEqual(
            compile_ir_op_event(relative, "th11"),
            "ins_291(120, 9, 0.1f, 32.0f, 0);",
        )

        th11_relative = semantic_operation(
            "th11",
            291,
            ["120", "9", "0.1f", "32.0f", "0"],
        )
        self.assertEqual(
            [operand.name for operand in th11_relative.operands],
            ["duration", "interpolation", "angular_speed", "radius", "compat_flag"],
        )
        th10_relative = semantic_operation(
            "th10",
            291,
            ["120", "9", "0.1f", "32.0f", "0.0f", "0"],
        )
        self.assertEqual(
            [operand.name for operand in th10_relative.operands],
            [
                "duration",
                "interpolation",
                "angular_speed",
                "radius",
                "radius_delta",
                "compat_flag",
            ],
        )
        self.assertEqual(
            compile_ir_op_event(th11_relative, "th10"),
            "ins_291(120, 9, 0.1f, 32.0f, 0.0f, 0);",
        )
        self.assertEqual(
            compile_ir_op_event(th11_relative, "th12"),
            "ins_311(120, 9, 0.1f, 32.0f, 0.0f);",
        )

        for radius_delta in ("1.0f", "0.0f + 0.0f"):
            incompatible = semantic_operation(
                "th12",
                311,
                ["120", "9", "0.1f", "32.0f", radius_delta],
            )
            with self.subTest(radius_delta=radius_delta):
                emission = compile_ir_op_emission(incompatible, "th11")
                self.assertIsNotNone(emission)
                self.assertEqual(emission.strategy, LoweringStrategy.UNSUPPORTED)

        non_default_compat = semantic_operation(
            "th11",
            291,
            ["120", "9", "0.1f", "32.0f", "1"],
        )
        emission = compile_ir_op_emission(non_default_compat, "th12")
        self.assertIsNotNone(emission)
        self.assertEqual(emission.strategy, LoweringStrategy.UNSUPPORTED)

    def test_typed_and_schema_v1_events_lower_identically(self) -> None:
        cases = [
            ("th08", 21, ["[-10000]", "1"], "th12"),
            ("th10", 412, ["0", "1", "0.0f", "1.0f", "60", "0", "4.0f", "16.0f"], "th12"),
            ("th13", 0, [], "th12"),
        ]
        for source, opcode, args, target in cases:
            with self.subTest(source=source, opcode=opcode, target=target):
                legacy = compile_ir_op_event(op_event(source, opcode, args), target)
                typed = compile_ir_op_event(semantic_operation(source, opcode, args), target)
                self.assertEqual(legacy, typed)

    def test_normalization_preserves_opcode_zero_and_prefers_operations(self) -> None:
        typed = semantic_operation("th13", 0, []).to_dict()
        self.assertEqual(normalize_backend_event(typed)["source_opcode"], 0)

        obj = SimpleNamespace(
            game="th13",
            fields={
                "operations": [typed],
                "ir_ops": [{"op_key": "wrong.legacy", "args": [], "source_opcode": 999}],
            },
            raw=[],
        )
        events = object_ir_events(obj)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["op_key"], "flow.nop")

    def test_target_opcode_lookup_never_borrows_a_same_generation_number(self) -> None:
        source = semantic_operation("th15", 324, ["1"])
        target = semantic_operation("th17", 324, [])
        self.assertEqual(source.operation, "enemy.enm324")
        self.assertEqual(target.operation, "enemy.enm_pos2")
        self.assertIsNone(target_opcode_for_op_key(source.operation, "th17"))
        self.assertEqual(target_opcode_for_op_key(target.operation, "th17"), 324)

        emission = compile_ir_op_emission(source, "th17")
        self.assertIsNotNone(emission)
        self.assertEqual(emission.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertNotIn("ins_324", emission.text)

    def test_evidence_backed_reused_opcodes_have_game_scoped_semantics(self) -> None:
        cases = [
            ("th12", 444, ["1"], "unit.special_collision_flag", "enabled", "th15", "ins_544(1);"),
            ("th15", 544, ["0"], "unit.special_collision_flag", "enabled", "th12", "ins_444(0);"),
            ("th15", 569, ["6"], "unit.kill_rate", "weight", "th17", "ins_569(6);"),
            (
                "th13",
                1001,
                ["120"],
                "unit.spirit_drop_decay_frames",
                "frames",
                "th15",
                "ins_1001(120);",
            ),
            (
                "th15",
                1002,
                ["5"],
                "unit.spirit_drop_max_count",
                "count",
                "th14",
                "ins_1002(5);",
            ),
        ]
        for source, opcode, args, operation, operand, target, expected in cases:
            with self.subTest(source=source, opcode=opcode, target=target):
                node = semantic_operation(source, opcode, args)
                self.assertEqual(node.operation, operation)
                self.assertEqual([item.name for item in node.operands], [operand])
                self.assertEqual(node.provenance.confidence.value, "documented")
                self.assertEqual(compile_ir_op_event(node, target), expected)

        self.assertIsNone(target_opcode_for_op_key("unit.special_collision_flag", "th11"))
        self.assertIsNone(target_opcode_for_op_key("unit.kill_rate", "th14"))
        self.assertIsNone(
            target_opcode_for_op_key("unit.spirit_drop_decay_frames", "th16")
        )
        self.assertIsNone(
            target_opcode_for_op_key("unit.spirit_drop_max_count", "th17")
        )

    def test_game_specific_opcode_reuse_is_not_treated_as_an_alias(self) -> None:
        th11_debug = semantic_operation("th11", 500, ["100"])
        th12_emitter = semantic_operation("th12", 500, ["0"])
        th13_hurtbox = semantic_operation("th13", 500, ["24.0f", "24.0f"])
        th13_debug = semantic_operation("th13", 900, ["4"])
        th16_season = semantic_operation("th16", 1001, ["200"])
        th17_spec = semantic_operation("th17", 1001, ["1"])
        th18_timed_drop = semantic_operation("th18", 573, ["1", "1"])

        self.assertTrue(th11_debug.operation.startswith("raw."))
        self.assertEqual(th12_emitter.operation, "bullet.manager.reset")
        self.assertEqual(th13_hurtbox.operation, "unit.set_hurtbox")
        self.assertTrue(th13_debug.operation.startswith("raw."))
        self.assertEqual(th13_debug.provenance.confidence.value, "unknown")
        self.assertNotEqual(th16_season.operation, "unit.spirit_drop_decay_frames")
        self.assertNotEqual(th17_spec.operation, "unit.spirit_drop_decay_frames")
        self.assertNotEqual(th18_timed_drop.operation, "unit.kill_rate")

        for node, target in (
            (th11_debug, "th15"),
            (th16_season, "th15"),
            (th18_timed_drop, "th17"),
        ):
            with self.subTest(operation=node.operation, target=target):
                emission = compile_ir_op_emission(node, target)
                self.assertIsNotNone(emission)
                self.assertEqual(emission.strategy, LoweringStrategy.UNSUPPORTED)

    def test_enemy_create_target_form_is_selected_by_typed_arity(self) -> None:
        normal_args = ['"Girl"', "1.0f", "2.0f", "100", "1000", "1"]
        normal = semantic_operation("th15", 300, normal_args)

        self.assertEqual(normal.operation, "enemy.create")
        self.assertEqual(target_opcode_for_op_key(normal.operation, "th12"), 256)
        self.assertEqual(
            compile_ir_op_event(normal, "th12"),
            f"ins_256({', '.join(normal_args)});",
        )

    def test_legacy_extended_enemy_create_keeps_its_typed_form(self) -> None:
        extended_args = [
            '"DiveEnemy"',
            "1.0f",
            "2.0f",
            "-1073741824",
            "100",
            "1000",
            "1",
        ]
        create = semantic_operation("th10", 270, extended_args)
        create_func = semantic_operation("th11", 271, extended_args)

        self.assertEqual(create.operation, "enemy.create")
        self.assertEqual(create_func.operation, "enemy.create_func")
        self.assertEqual(
            [operand.name for operand in create.operands],
            [
                "routine",
                "x",
                "y",
                "legacy_parameter",
                "health",
                "score_reward",
                "item_drop",
            ],
        )
        self.assertEqual(
            compile_ir_op_event(create, "th12"),
            f"ins_270({', '.join(extended_args)});",
        )
        self.assertEqual(
            compile_ir_op_event(create_func, "th12"),
            f"ins_271({', '.join(extended_args)});",
        )
        self.assertEqual(
            compile_ir_op_event(create, "th15"),
            'ins_300("DiveEnemy", 1.0f, 2.0f, 100, 1000, 1);',
        )

        th12_drop = semantic_operation(
            "th12",
            270,
            ['"DiveEnemy"', "1.0f", "2.0f", "0", "100", "1000", "5"],
        )
        self.assertEqual(
            compile_ir_op_event(th12_drop, "th15"),
            'ins_300("DiveEnemy", 1.0f, 2.0f, 100, 1000, 6);',
        )

    def test_th13_reused_opcodes_dispatch_by_semantics(self) -> None:
        cases = [
            (401, ["60", "12", "0.0f", "128.0f"], "movement.position.tween", "ins_301("),
            (502, ["1"], "unit.flag_set", "ins_402("),
            (503, ["1"], "unit.flag_clear", "ins_403("),
        ]
        for opcode, args, operation, target_text in cases:
            with self.subTest(opcode=opcode):
                text = f"ins_{opcode}({', '.join(args)});"
                statement = Statement(
                    "instruction",
                    text,
                    1,
                    text,
                    None,
                    {"opcode": opcode, "args": args},
                )
                event = statement_to_event(statement, "th13", "Test", "fixture.decl")
                self.assertEqual(event["semantic_op"]["operation"], operation)
                lowered = "\n".join(emit_timeline_event(event, "th13", "th12"))
                self.assertIn(target_text, lowered)
                self.assertNotIn("dynamic bullet", lowered)

    def test_canonical_transform_replace_selects_target_replace_form(self) -> None:
        operation = semantic_operation(
            "th12",
            509,
            ["0", "2", "1", "4", "30", "-999999", "0.1f", "-999999.0f"],
        )
        lowered = compile_ir_op_event(operation, "th15")
        self.assertEqual(
            lowered,
            "ins_609(0, 2, 1, 4, 30, -999999, 0.1f, -999999.0f);",
        )

    def test_transform_sentinels_are_encoded_for_the_target_profile(self) -> None:
        th08 = semantic_operation(
            "th08",
            111,
            ["0", "2", "1", "30", "-1", "-1.0f", "-1.0f"],
        )
        self.assertEqual(
            compile_ir_op_event(th08, "th15"),
            "ins_609(0, 0, 1, 2, 30, -999999, -999999.0f, -999999.0f);",
        )

        th18 = semantic_operation(
            "th18",
            609,
            ["0", "0", "0", "2", "1", "-9999994", "-9999994.0f", "-9999994.0f"],
        )
        self.assertEqual(
            compile_ir_op_event(th18, "th15"),
            "ins_609(0, 0, 0, 2, 1, -999999, -999999.0f, -999999.0f);",
        )

    def test_early_game_macro_modes_select_the_matching_target_opcode(self) -> None:
        macro_args = ["0", "3", "4", "2", "1.0f", "2.0f", "0.0f", "0.1f", "0"]
        macro_starts = {"th06": 67, "th07": 64, "th08": 96}

        for source_game, source_start in macro_starts.items():
            for target_game, target_start in macro_starts.items():
                for mode_index in range(9):
                    with self.subTest(source=source_game, target=target_game, mode=mode_index):
                        operation = semantic_operation(
                            source_game,
                            source_start + mode_index,
                            macro_args,
                        )
                        self.assertEqual(
                            compile_ir_op_event(operation, target_game),
                            f"ins_{target_start + mode_index}({', '.join(macro_args)});",
                        )

    def test_th13_unit_flags_are_owned_by_unit_objects(self) -> None:
        program = parse_decl("th13/st07mbs.decl")
        objects = lift_all_objects(program)
        owned = []
        for obj in objects:
            if getattr(obj, "kind", "") != "UnitFlag":
                continue
            for instruction in getattr(obj, "raw", []):
                if instruction.opcode in {502, 503}:
                    covered = covered_lines_for_lifted_object(obj, program.game, "th12")
                    owned.append(instruction.line_no in covered)
        self.assertTrue(owned)
        self.assertTrue(all(owned))


if __name__ == "__main__":
    unittest.main()
