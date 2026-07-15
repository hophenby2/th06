from __future__ import annotations

import unittest

from ecl_ir.dialects.game_profile import (
    CAP_LASER_CURVE,
    CAP_TRANSFORM_CURSOR_DECREMENT,
)
from ecl_ir.target.lowering import (
    DiagnosticSeverity,
    LoweringPlanner,
    LoweringPolicy,
    LoweringStrategy,
)
from ecl_ir.canonical.semantic_ir import (
    Confidence,
    DifficultyGuard,
    LoweringOwner,
    NodeId,
    NodeOwnership,
    OperandValue,
    Provenance,
    RawInstructionOp,
    SemanticModule,
    SemanticOperand,
    SemanticOperation,
    SemanticRoutine,
    SourceSpan,
    SyntaxStatement,
)


def provenance(game: str, line: int = 1, opcode: int | None = None) -> Provenance:
    return Provenance(
        game=game,
        routine="Test",
        span=SourceSpan("fixture.decl", line, line),
        opcode=opcode,
        confidence=Confidence.DOCUMENTED,
    )


def semantic_op(
    operation: str,
    node_id: str,
    *,
    source_game: str = "th15",
    annotations: dict[str, object] | None = None,
    owner: LoweringOwner = LoweringOwner.SEMANTIC,
) -> SemanticOperation:
    return SemanticOperation(
        node_id=NodeId(node_id),
        operation=operation,
        domain=operation.partition(".")[0],
        operands=[SemanticOperand("value", OperandValue.value("0"))],
        provenance=provenance(source_game),
        guard=DifficultyGuard(),
        annotations=annotations or {},
        ownership=NodeOwnership(owner),
    )


class LoweringPlannerTests(unittest.TestCase):
    def test_native_capability_is_direct_and_node_policy_is_ignored(self) -> None:
        node = semantic_op(
            "bullet.transform.append",
            "Test:1:0",
            annotations={
                # Old serialized policies must not steer canonical lowering.
                "lowering_policy": {"strategy": "drop", "targets": ["th15"]},
            },
        )

        decision = LoweringPlanner.for_game("th15").plan_node(node, "Test")

        self.assertEqual(decision.node_id, node.node_id)
        self.assertEqual(decision.strategy, LoweringStrategy.DIRECT)
        self.assertEqual(decision.rule, "bullet.transform.append")
        self.assertFalse(decision.diagnostics)

    def test_capability_fallback_and_unsupported_have_structured_diagnostics(self) -> None:
        curve = semantic_op("laser.activate_curve", "Test:2:0")
        permissive = LoweringPolicy(allow_lossy=True)
        curve_decision = LoweringPlanner.for_game(
            "th10",
            policy=permissive,
        ).plan_node(curve, "Test")

        self.assertEqual(curve_decision.strategy, LoweringStrategy.LOSSY)
        self.assertIn(CAP_LASER_CURVE, curve_decision.missing_capabilities)
        self.assertEqual(curve_decision.diagnostics[0].code, "capability.lossy_fallback")
        self.assertEqual(curve_decision.diagnostics[0].severity, DiagnosticSeverity.WARNING)

        decrement = semantic_op("bullet.transform.append_cursor.decrement", "Test:3:0")
        decrement_decision = LoweringPlanner.for_game(
            "th13",
            policy=permissive,
        ).plan_node(decrement, "Test")

        self.assertEqual(decrement_decision.strategy, LoweringStrategy.LOSSY)
        self.assertIn(CAP_TRANSFORM_CURSOR_DECREMENT, decrement_decision.missing_capabilities)
        self.assertEqual(decrement_decision.diagnostics[0].code, "capability.lossy_fallback")
        self.assertEqual(decrement_decision.diagnostics[0].node_id, decrement.node_id)

    def test_policy_can_forbid_lossy_fallback_without_changing_the_node(self) -> None:
        node = semantic_op("bullet.manager.reset", "Test:4:0")
        permissive = LoweringPlanner.for_game(
            "th06",
            policy=LoweringPolicy(allow_lossy=True),
        ).plan_node(node)
        strict = LoweringPlanner.for_game("th06").plan_node(node)

        self.assertEqual(permissive.strategy, LoweringStrategy.LOSSY)
        self.assertEqual(strict.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertIn("lossy fallbacks are disabled", strict.reason)

    def test_module_preserves_order_and_raw_uses_only_profile_compatibility(self) -> None:
        top_level = SyntaxStatement(
            node_id=NodeId("<module>:1:0"),
            statement_kind="include",
            text="#include \"common.eclh\"",
            attributes={},
            provenance=provenance("th13"),
        )
        first = semantic_op("flow.wait", "Test:2:0", source_game="th13")
        raw = RawInstructionOp(
            node_id=NodeId("Test:3:0"),
            opcode=900,
            args=["1"],
            provenance=provenance("th13", line=3, opcode=900),
            reason="unconfirmed_game_extension",
        )
        module = SemanticModule(
            source="fixture.decl",
            source_game="th13",
            profile="th13",
            top_level=[top_level],
            routines=[SemanticRoutine("Test", body=[first, raw])],
        )

        result = LoweringPlanner.for_game(
            "th15",
            policy=LoweringPolicy(preserve_raw_same_family=True),
        ).plan_module(module)

        self.assertEqual(
            [str(decision.node_id) for decision in result.decisions],
            ["<module>:1:0", "Test:2:0", "Test:3:0"],
        )
        self.assertEqual(result.decisions[0].strategy, LoweringStrategy.RAW)
        self.assertEqual(result.decisions[1].strategy, LoweringStrategy.DIRECT)
        self.assertEqual(result.decisions[2].strategy, LoweringStrategy.RAW)
        self.assertEqual(result.decisions[2].target_text, "ins_900(1);")
        self.assertEqual(result.decisions[2].diagnostics[0].code, "raw.same_family_passthrough")
        self.assertFalse(result.decisions[2].is_lossless)
        self.assertTrue(result.successful)

    def test_cross_family_raw_and_non_owner_are_not_silently_emitted(self) -> None:
        raw = RawInstructionOp(
            node_id=NodeId("Test:5:0"),
            opcode=900,
            args=[],
            provenance=provenance("th15", opcode=900),
        )
        wrong_owner = semantic_op(
            "flow.wait",
            "Test:6:0",
            owner=LoweringOwner.PATTERN,
        )

        raw_decision = LoweringPlanner.for_game("th12").plan_node(raw)
        owner_decision = LoweringPlanner.for_game("th15").plan_node(wrong_owner)

        self.assertEqual(raw_decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(raw_decision.diagnostics[0].code, "raw.incompatible_dialect")
        self.assertEqual(owner_decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(owner_decision.diagnostics[0].code, "ownership.wrong_lowerer")

    def test_backend_is_an_injected_compatibility_boundary(self) -> None:
        calls: list[tuple[NodeId, str]] = []

        def emitter(node: SemanticOperation, target: str) -> str:
            calls.append((node.node_id, target))
            return "ins_23(30);"

        node = semantic_op("flow.wait", "Test:7:0")
        planner = LoweringPlanner.for_game("th15", backend_emitter=emitter)
        decision = planner.plan_node(node)

        self.assertEqual(calls, [(node.node_id, "th15")])
        self.assertEqual(decision.strategy, LoweringStrategy.DIRECT)
        self.assertEqual(decision.target_text, "ins_23(30);")

    def test_duplicate_node_id_is_reported_at_module_scope(self) -> None:
        duplicate = "Test:8:0"
        module = SemanticModule(
            source="fixture.decl",
            source_game="th15",
            profile="th15",
            routines=[
                SemanticRoutine(
                    "Test",
                    body=[
                        semantic_op("flow.wait", duplicate),
                        semantic_op("flow.nop", duplicate),
                    ],
                )
            ],
        )

        result = LoweringPlanner.for_game("th15").plan_module(module)

        self.assertFalse(result.successful)
        self.assertEqual(result.decisions[0].strategy, LoweringStrategy.DIRECT)
        self.assertEqual(result.decisions[1].strategy, LoweringStrategy.UNSUPPORTED)
        self.assertIn("identity.duplicate_node_id", [item.code for item in result.diagnostics])


if __name__ == "__main__":
    unittest.main()
