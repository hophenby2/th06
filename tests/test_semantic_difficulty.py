from __future__ import annotations

from dataclasses import replace
import unittest

from ecl_ir.analysis.bullet_ir import active_difficulty_lanes
from ecl_ir.target.lowering import (
    BackendEmission,
    LoweringPlanner,
    LoweringPolicy,
    LoweringStrategy,
)
from ecl_ir.source.parser import (
    DifficultySelectionCandidate,
    find_difficulty_selection_candidates,
    parse_decl,
    parse_decl_text,
)
from ecl_ir.canonical.semantic_ir import (
    DifficultyGuard,
    SemanticModule,
    SemanticOperation,
    SelectionKind,
    SyntaxStatement,
)
from ecl_ir.canonical.semantic_lifter import build_semantic_module
from ecl_ir.target.target_ir import CanonicalBackendEmitter, TargetAstBuilder, target_difficulty_guard


def operation_at(module: SemanticModule, routine_name: str, line: int) -> SemanticOperation:
    routine = next(routine for routine in module.routines if routine.name == routine_name)
    return next(
        node
        for node in routine.body
        if isinstance(node, SemanticOperation) and node.provenance.span.start_line == line
    )


class SemanticDifficultyTests(unittest.TestCase):
    def test_selection_candidates_require_a_complete_uninterrupted_table(self) -> None:
        valid_source = """void Main()
{
!E
    10;
!N
    20;
!*
    ins_23([-1]);
}
"""
        self.assertEqual(
            find_difficulty_selection_candidates(valid_source),
            (DifficultySelectionCandidate((4, 6), 8),),
        )
        inline_consumer = valid_source.replace("!*\n    ins_23([-1]);", "!* ins_23([-1]);")
        self.assertEqual(
            find_difficulty_selection_candidates(inline_consumer),
            (DifficultySelectionCandidate((4, 6), 7),),
        )
        inline_program = parse_decl_text(inline_consumer, "th13/inline-selection.decl")
        inline_instruction = inline_program.functions[0].statements[-1]
        self.assertEqual(
            inline_instruction.attrs["difficulty_literals"],
            [{"E": "10", "N": "20"}],
        )

        program = parse_decl("th10/stage04.decl")
        routine = next(function for function in program.functions if function.name == "Boss3_at3")
        by_line = {statement.line_no: statement for statement in routine.statements}
        self.assertEqual(by_line[425].text, "%A;")
        self.assertEqual(by_line[431].text, "%A;")
        self.assertEqual(
            [by_line[line].difficulty for line in (425, 427, 428, 429)],
            ["EN", "EN", "EN", "EN"],
        )
        self.assertEqual(
            [by_line[line].difficulty for line in (431, 433, 434, 435)],
            ["HL", "HL", "HL", "HL"],
        )

    def test_rank_markers_follow_thecl_persistent_and_scoped_state(self) -> None:
        program = parse_decl_text(
            """sub Main()
{
!L    ins_1(0);
    ins_1(0);
!*    ins_1(0);
    ins_1(0);
!H:   ins_1(0);
    ins_1(0);
!N:
    ins_1(0);
    ins_1(0);
}
""",
            "th06/rank-state.decl",
        )
        self.assertEqual(
            [statement.difficulty for statement in program.functions[0].statements],
            ["L", "L", "*", None, "H", None, "N", None],
        )

        module = build_semantic_module(program)
        planner = LoweringPlanner.for_game(
            "th06",
            backend_emitter=CanonicalBackendEmitter(module, "th06"),
        )
        rendered = TargetAstBuilder(planner).build(module).render_decl()
        self.assertIn(
            "!L\n    ins_1(0);\n    ins_1(0);\n"
            "    !*\n    ins_1(0);\n    ins_1(0);\n"
            "    !H\n    ins_1(0);\n    !*\n    ins_1(0);",
            rendered,
        )

    def test_timeline_rank_state_resets_at_each_region(self) -> None:
        program = parse_decl_text(
            """timeline Timeline0()
{
!L    ins_1(0);
}
timeline Timeline1()
{
    ins_1(0);
}
""",
            "th08/timeline-rank-state.decl",
        )
        timeline_instructions = [
            statement
            for statement in program.top_level
            if statement.kind == "instruction"
        ]
        self.assertEqual(
            [statement.difficulty for statement in timeline_instructions],
            ["L", None],
        )

    def test_real_eight_lane_markers_survive_target_normalization(self) -> None:
        th13 = build_semantic_module(parse_decl("th13/st05bs.decl"))
        overdrive = operation_at(th13, "BossCard4Ship_at", 894)
        self.assertEqual(overdrive.guard.raw, "O67")
        self.assertEqual(overdrive.guard.mask, ("O", "6", "7"))
        self.assertEqual(active_difficulty_lanes(overdrive.guard), ("O", "6", "7"))
        self.assertEqual(
            target_difficulty_guard(overdrive.guard, "fourth", "th15").raw,
            "O67",
        )

        th08 = build_semantic_module(parse_decl("th08/ecldata8.decl"))
        legacy_overdrive = operation_at(th08, "Sub53", 1159)
        unused_lanes = operation_at(th08, "Sub53", 1160)
        self.assertEqual(legacy_overdrive.guard.mask, ("E", "N", "H", "L", "O", "7"))
        self.assertEqual(unused_lanes.guard.mask, ("E", "N", "H", "L", "6", "7"))
        self.assertEqual(
            target_difficulty_guard(legacy_overdrive.guard, "fourth", "th15").raw,
            "ENHLO7",
        )
        self.assertEqual(
            target_difficulty_guard(unused_lanes.guard, "fourth", "th15").raw,
            "ENHL67",
        )

        numeric = DifficultyGuard.from_marker("01234567")
        self.assertEqual(numeric.mask, ("E", "N", "H", "L", "X", "O", "6", "7"))
        self.assertEqual(
            target_difficulty_guard(numeric, "fourth", "th185").raw,
            "01234567",
        )

    def test_real_difficulty_literal_table_is_typed_and_roundtrips(self) -> None:
        module = build_semantic_module(parse_decl("th13/st03bs.decl"))
        operation = operation_at(module, "Boss1_at2", 131)

        self.assertEqual(operation.encoded_args()[-2:], ["[-1.0f]", "[-2.0f]"])
        self.assertEqual(len(operation.selected_values), 1)
        selected = operation.selected_values[0]
        self.assertEqual(selected.selector, SelectionKind.DIFFICULTY)
        self.assertEqual(
            [(case.guard.raw, case.value.text) for case in selected.cases],
            [
                ("E", "0.016667f"),
                ("N", "0.016667f"),
                ("H", "0.0125f"),
                ("LO", "0.0125f"),
            ],
        )
        self.assertEqual(selected.cases[-1].guard.mask, ("L", "O"))

        restored = SemanticModule.from_dict(module.to_dict())
        self.assertEqual(restored.to_dict(), module.to_dict())

        decision = LoweringPlanner.with_compat_backend("th15").plan_node(
            operation,
            "Boss1_at2",
        )
        self.assertEqual(decision.strategy, LoweringStrategy.DIRECT)
        self.assertIn("!LO\n0.0125f;\n!*", decision.target_text or "")
        self.assertTrue((decision.target_text or "").endswith(
            "ins_609(1, 2, 0, 4, 240, -999999, [-1.0f], [-2.0f]);"
        ))

        # Only [-1] belongs to this selection. The unrelated TH13+ [-2]
        # routine-stack reference remains unsafe for a TH12 target.
        old_target = LoweringPlanner.with_compat_backend("th12").plan_node(
            operation,
            "Boss1_at2",
        )
        self.assertEqual(old_target.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(old_target.diagnostics[-1].code, "stack.relative_abi_unsupported")

        identity = LoweringPlanner.with_compat_backend("th13").plan_node(
            operation,
            "Boss1_at2",
        )
        self.assertEqual(identity.strategy, LoweringStrategy.DIRECT)
        self.assertIn("!E\n0.016667f;", identity.target_text or "")
        self.assertTrue((identity.target_text or "").endswith(
            "ins_609(1, 2, 0, 4, 240, -999999, [-1.0f], [-2.0f]);"
        ))

    def test_syntax_consumers_own_and_restore_selected_values(self) -> None:
        module = build_semantic_module(parse_decl("th17/st06bs.decl"))
        routine = next(routine for routine in module.routines if routine.name == "BossCard1")
        call = next(
            node
            for node in routine.body
            if isinstance(node, SyntaxStatement) and node.provenance.span.start_line == 849
        )
        self.assertEqual(call.statement_kind, "call")
        self.assertEqual(len(call.selected_values), 3)
        self.assertEqual(
            [case.value.text for case in call.selected_values[-1].cases],
            ["5", "8", "12", "14"],
        )

        restored = SemanticModule.from_dict(module.to_dict())
        restored_call = next(
            node
            for restored_routine in restored.routines
            if restored_routine.name == "BossCard1"
            for node in restored_routine.body
            if node.provenance.span.start_line == 849
        )
        self.assertEqual(restored_call.to_dict(), call.to_dict())

        identity = LoweringPlanner.for_game("th17").plan_node(call, "BossCard1")
        self.assertEqual(identity.strategy, LoweringStrategy.RAW)
        self.assertEqual((identity.target_text or "").count("!*"), 3)
        self.assertIn("!LO\n14;\n!*\n@Boss1Card_at", identity.target_text or "")

        cross_game = LoweringPlanner.for_game("th18").plan_node(call, "BossCard1")
        self.assertEqual(cross_game.strategy, LoweringStrategy.RAW)
        self.assertEqual((cross_game.target_text or "").count("!*"), 3)
        self.assertTrue((cross_game.target_text or "").endswith(call.text))

        old_spelling = LoweringPlanner.for_game("th12").plan_node(call, "BossCard1")
        self.assertEqual(old_spelling.strategy, LoweringStrategy.RAW)
        self.assertEqual((old_spelling.target_text or "").count("!L5"), 3)
        self.assertNotIn("!LO", old_spelling.target_text or "")

    def test_cross_generation_selection_preserves_the_proven_consumer_slot(self) -> None:
        module = build_semantic_module(
            parse_decl_text(
                """void Main()
{
!E
    90;
!N
    90;
!H
    30;
!LO
    30;
!*
    ins_23([-1]);
}
""",
                "th15/selection.decl",
            )
        )
        operation = module.routines[0].body[0]
        planner = LoweringPlanner.for_game(
            "th12",
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        )
        decision = planner.plan_node(operation, "Main")
        self.assertEqual(decision.strategy, LoweringStrategy.DIRECT)
        self.assertIn("!L5\n30;\n!*", decision.target_text or "")
        self.assertTrue((decision.target_text or "").endswith("ins_83([-1]);"))

        class CommentOnlyPlaceholderEmitter:
            def __call__(self, _node, _target):
                return BackendEmission("// removed source argument [-1]\nins_83(30);")

        dropped = LoweringPlanner.for_game(
            "th12",
            backend_emitter=CommentOnlyPlaceholderEmitter(),
        ).plan_node(operation, "Main")
        self.assertEqual(dropped.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(dropped.diagnostics[-1].code, "value_selection.unsupported")
        self.assertEqual(
            dropped.diagnostics[-1].details["missing_target_placeholders"],
            [-1],
        )

        class DelayedConsumerEmitter:
            def __call__(self, _node, _target):
                return BackendEmission("ins_1();\nins_83([-1]);")

        delayed = LoweringPlanner.for_game(
            "th12",
            backend_emitter=DelayedConsumerEmitter(),
        ).plan_node(operation, "Main")
        self.assertEqual(delayed.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(delayed.diagnostics[-1].code, "value_selection.unsupported")
        self.assertIn("first emitted executable statement", delayed.reason)
        self.assertEqual(
            delayed.diagnostics[-1].details["first_statement_placeholders"],
            [],
        )
        self.assertEqual(
            delayed.diagnostics[-1].details["target_placeholders"],
            [-1],
        )

    def test_real_multi_slot_operation_keeps_push_order_and_target_spelling(self) -> None:
        module = build_semantic_module(parse_decl("th13/st04bs.decl"))
        operation = operation_at(module, "Boss1_at", 110)
        self.assertEqual(len(operation.selected_values), 2)
        self.assertEqual(operation.encoded_args(), ["0", "[-1.0f]", "[-2.0f]"])

        decision = LoweringPlanner.for_game(
            "th12",
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        ).plan_node(operation, "Boss1_at")
        self.assertEqual(decision.strategy, LoweringStrategy.DIRECT)
        text = decision.target_text or ""
        first_table = text.index("0.523599f;")
        second_table = text.index("[-9987.0f] * 0.017453292f;")
        consumer = text.index("ins_504(0, [-1.0f], [-2.0f]);")
        self.assertLess(first_table, second_table)
        self.assertLess(second_table, consumer)
        self.assertEqual(text.count("!L5"), 2)

    def test_argument_adaptation_must_not_drop_a_selected_placeholder(self) -> None:
        module = build_semantic_module(
            parse_decl_text(
                """void Main()
{
!E
    1;
!N
    2;
!H
    3;
!LO
    4;
!*
    ins_270("Foo", 0.0f, 0.0f, [-1], 100, 0, 0);
}
""",
                "th10/selection-drop.decl",
            )
        )
        operation = module.routines[0].body[0]
        decision = LoweringPlanner.for_game(
            "th15",
            backend_emitter=CanonicalBackendEmitter(module, "th15"),
        ).plan_node(operation, "Main")
        self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(decision.diagnostics[-1].code, "value_selection.unsupported")
        self.assertIn("adaptation removed", decision.reason)
        self.assertEqual(
            decision.diagnostics[-1].details["missing_target_placeholders"],
            [-1],
        )

    def test_selected_values_require_stack_expression_syntax_on_both_sides(self) -> None:
        module = build_semantic_module(parse_decl("th15/st01.decl"))
        operation = operation_at(module, "GirlA01_at", 38)
        decision = LoweringPlanner.with_compat_backend("th08").plan_node(
            operation,
            "GirlA01_at",
        )
        self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(decision.diagnostics[-1].code, "value_selection.unsupported")
        self.assertIn("stack-expression syntax", decision.reason)

    def test_syntax_emitter_must_preserve_every_selected_placeholder(self) -> None:
        module = build_semantic_module(parse_decl("th17/st06bs.decl"))
        call = next(
            node
            for routine in module.routines
            if routine.name == "BossCard1"
            for node in routine.body
            if isinstance(node, SyntaxStatement) and node.provenance.span.start_line == 849
        )

        class DroppingSyntaxEmitter:
            def emit_syntax(self, _node, _projected_text, _target_game):
                return "@Boss1Card_at(5, 6, %A, 2.0f);"

        decision = LoweringPlanner.for_game(
            "th18",
            backend_emitter=DroppingSyntaxEmitter(),
        ).plan_node(call, "BossCard1")
        self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(decision.diagnostics[-1].code, "value_selection.unsupported")
        self.assertEqual(
            decision.diagnostics[-1].details["missing_target_placeholders"],
            [-3, -2, -1],
        )

    def test_raw_selected_values_still_require_passthrough_policy_and_proof(self) -> None:
        module = build_semantic_module(
            parse_decl_text(
                """void Main()
{
!E
    1;
!N
    2;
!H
    3;
!LO
    4;
!*
    ins_9999([-1]);
}
""",
                "th10/raw-selection.decl",
            )
        )
        raw = module.routines[0].body[0]
        blocked = LoweringPlanner.for_game("th11").plan_node(raw, "Main")
        self.assertEqual(blocked.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(blocked.diagnostics[-1].code, "raw.incompatible_dialect")

        policy = LoweringPolicy(preserve_raw_same_family=True)
        preserved = LoweringPlanner.for_game("th11", policy=policy).plan_node(raw, "Main")
        self.assertEqual(preserved.strategy, LoweringStrategy.RAW)
        self.assertIn("!L5\n4;\n!*\nins_9999([-1]);", preserved.target_text or "")

        malformed = replace(raw, args=["0"])
        rejected = LoweringPlanner.for_game("th11", policy=policy).plan_node(
            malformed,
            "Main",
        )
        self.assertEqual(rejected.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(rejected.diagnostics[-1].code, "value_selection.unsupported")
        self.assertEqual(
            rejected.diagnostics[-1].details["missing_source_placeholders"],
            [-1],
        )


if __name__ == "__main__":
    unittest.main()
