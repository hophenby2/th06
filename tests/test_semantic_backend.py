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
from ecl_ir.source.parser import parse_decl
from ecl_ir.legacy.timeline_lifter import statement_to_event


class SemanticBackendTests(unittest.TestCase):
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
