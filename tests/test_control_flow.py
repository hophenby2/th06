from __future__ import annotations

import unittest

from ecl_ir.analysis.bullet_ir import analyze_bullet_routine
from ecl_ir.analysis.control_flow import analyze_routine_control_flow
from ecl_ir.target.lowering import LoweringPlanner, LoweringPolicy
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.canonical.semantic_ir import (
    Confidence,
    NodeId,
    Provenance,
    SemanticModule,
    SemanticRoutine,
    SourceSpan,
    SyntaxStatement,
)
from ecl_ir.target.target_ir import CanonicalBackendEmitter, TargetAstBuilder


def syntax(kind: str, line: int, text: str, **attributes: str) -> SyntaxStatement:
    return SyntaxStatement(
        node_id=NodeId.for_statement("Loop", line),
        statement_kind=kind,
        text=text,
        attributes=attributes,
        provenance=Provenance(
            game="th15",
            routine="Loop",
            span=SourceSpan("fixture.decl", line, line),
            raw=text,
            confidence=Confidence.DOCUMENTED,
        ),
    )


class ControlFlowTests(unittest.TestCase):
    def test_cfg_marks_the_full_strongly_connected_loop_region(self) -> None:
        label = syntax("label", 1, "again:", name="again")
        append = semantic_operation(
            "th15",
            611,
            ["0", "0", "4", "60", "-999999", "0.1f", "-999999.0f"],
            2,
            routine="Loop",
        )
        branch = syntax(
            "conditional_goto",
            3,
            "if ($A--) goto again @ 0;",
            condition_type="if",
            condition="$A--",
            label="again",
            time="0",
        )
        routine = SemanticRoutine("Loop", body=[label, append, branch])

        flow = analyze_routine_control_flow(routine)

        self.assertEqual(
            flow.cyclic_node_ids,
            frozenset({"Loop:1:0", "Loop:2:0", "Loop:3:0"}),
        )
        bullet = analyze_bullet_routine(routine, "th15")
        self.assertEqual(bullet.resolved_transform_indices["Loop:2:0"], {lane: None for lane in ("E", "N", "H", "L", "X", "O", "6", "7")})
        self.assertEqual(
            bullet.diagnostics[-1]["code"],
            "bullet.transform.append.cyclic_control_flow",
        )

    def test_cyclic_append_is_not_materialized_for_indexed_target(self) -> None:
        label = syntax("label", 1, "again:", name="again")
        append = semantic_operation(
            "th15",
            611,
            ["0", "0", "4", "60", "-999999", "0.1f", "-999999.0f"],
            2,
            routine="Loop",
        )
        branch = syntax(
            "conditional_goto",
            3,
            "if ($A--) goto again @ 0;",
            condition_type="if",
            condition="$A--",
            label="again",
            time="0",
        )
        module = SemanticModule(
            source="fixture.decl",
            source_game="th15",
            profile="th15",
            routines=[SemanticRoutine("Loop", body=[label, append, branch])],
        )
        planner = LoweringPlanner.for_game(
            "th12",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        )

        target = TargetAstBuilder(planner).build(module)
        decision = target.routines[0].body[1]

        self.assertEqual(decision.strategy.value, "unsupported")
        self.assertEqual(
            decision.diagnostics[-1].code,
            "backend.transform_append_index_join",
        )
        self.assertEqual(
            decision.diagnostics[-1].details["resolved_indices"],
            {lane: None for lane in ("E", "N", "H", "L", "X", "O", "6", "7")},
        )

    def test_reset_barrier_stabilizes_append_indices_inside_loop(self) -> None:
        label = syntax("label", 1, "again:", name="again")
        reset = semantic_operation("th15", 600, ["$A"], 2, routine="Loop")
        first = semantic_operation(
            "th15",
            611,
            ["$A", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"],
            3,
            routine="Loop",
        )
        second = semantic_operation(
            "th15",
            611,
            ["$A", "0", "4", "60", "-999999", "0.1f", "-999999.0f"],
            4,
            routine="Loop",
        )
        branch = syntax(
            "conditional_goto",
            5,
            "if ($B--) goto again @ 0;",
            condition_type="if",
            condition="$B--",
            label="again",
            time="0",
        )
        routine = SemanticRoutine("Loop", body=[label, reset, first, second, branch])

        bullet = analyze_bullet_routine(routine, "th15")

        self.assertEqual(
            bullet.resolved_transform_indices["Loop:3:0"],
            {lane: 0 for lane in ("E", "N", "H", "L", "X", "O", "6", "7")},
        )
        self.assertEqual(
            bullet.resolved_transform_indices["Loop:4:0"],
            {lane: 1 for lane in ("E", "N", "H", "L", "X", "O", "6", "7")},
        )
        self.assertFalse(bullet.diagnostics)

        module = SemanticModule(
            source="fixture.decl",
            source_game="th15",
            profile="th15",
            routines=[routine],
        )
        planner = LoweringPlanner.for_game(
            "th12",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        )
        rendered = TargetAstBuilder(planner).build(module).render_decl()
        self.assertIn("ins_509($A, 0, 0, 2", rendered)
        self.assertIn("ins_509($A, 1, 0, 4", rendered)

    def test_manager_copy_preserves_the_destination_append_cursor(self) -> None:
        label = syntax("label", 1, "again:", name="again")
        reset_destination = semantic_operation("th15", 600, ["0"], 2, routine="Loop")
        destination_append = semantic_operation(
            "th15",
            611,
            ["0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"],
            3,
            routine="Loop",
        )
        reset_source = semantic_operation("th15", 600, ["1"], 4, routine="Loop")
        source_append_1 = semantic_operation(
            "th15",
            611,
            ["1", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"],
            5,
            routine="Loop",
        )
        source_append_2 = semantic_operation(
            "th15",
            611,
            ["1", "0", "4", "60", "-999999", "0.1f", "-999999.0f"],
            6,
            routine="Loop",
        )
        copy = semantic_operation("th15", 614, ["0", "1"], 7, routine="Loop")
        after_copy = semantic_operation(
            "th15",
            611,
            ["0", "0", "8", "60", "-999999", "0.2f", "0.3f"],
            8,
            routine="Loop",
        )
        branch = syntax(
            "conditional_goto",
            9,
            "if ($A--) goto again @ 0;",
            condition_type="if",
            condition="$A--",
            label="again",
            time="0",
        )
        routine = SemanticRoutine(
            "Loop",
            body=[
                label,
                reset_destination,
                destination_append,
                reset_source,
                source_append_1,
                source_append_2,
                copy,
                after_copy,
                branch,
            ],
        )

        bullet = analyze_bullet_routine(routine, "th15")

        self.assertEqual(
            bullet.resolved_transform_indices["Loop:8:0"],
            {lane: 1 for lane in ("E", "N", "H", "L", "X", "O", "6", "7")},
        )

    def test_branch_divergent_append_cursor_stays_unresolved(self) -> None:
        label = syntax("label", 1, "again:", name="again")
        reset = semantic_operation("th15", 600, ["0"], 2, routine="Loop")
        skip = syntax(
            "conditional_goto",
            3,
            "if ($A) goto skip @ 0;",
            condition_type="if",
            condition="$A",
            label="skip",
            time="0",
        )
        optional_append = semantic_operation(
            "th15",
            611,
            ["0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"],
            4,
            routine="Loop",
        )
        skip_label = syntax("label", 5, "skip:", name="skip")
        joined_append = semantic_operation(
            "th15",
            611,
            ["0", "0", "4", "60", "-999999", "0.1f", "-999999.0f"],
            6,
            routine="Loop",
        )
        branch = syntax(
            "conditional_goto",
            7,
            "if ($B--) goto again @ 0;",
            condition_type="if",
            condition="$B--",
            label="again",
            time="0",
        )
        routine = SemanticRoutine(
            "Loop",
            body=[label, reset, skip, optional_append, skip_label, joined_append, branch],
        )

        bullet = analyze_bullet_routine(routine, "th15")

        self.assertEqual(
            bullet.resolved_transform_indices["Loop:6:0"],
            {lane: None for lane in ("E", "N", "H", "L", "X", "O", "6", "7")},
        )
        self.assertTrue(
            any(
                item["source_node_id"] == "Loop:6:0"
                and item["code"] == "bullet.transform.append.cyclic_control_flow"
                for item in bullet.diagnostics
            )
        )


if __name__ == "__main__":
    unittest.main()
