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


if __name__ == "__main__":
    unittest.main()
