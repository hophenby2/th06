from __future__ import annotations

from pathlib import Path
import unittest

from ecl_ir.compat.backend import compile_ir_op_event
from ecl_ir.dialects.game_profile import profile_for_game
from ecl_ir.target.lowering import LoweringPlanner, LoweringStrategy
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.source.parser import parse_decl, parse_decl_text
from ecl_ir.canonical.semantic_ir import (
    Confidence,
    ExpressionIR,
    SemanticOperation,
    ValueType,
    VariableAccess,
    VariablePropagation,
    VariableStorageScope,
    VariableUseKind,
)
from ecl_ir.canonical.semantic_lifter import build_semantic_module
from ecl_ir.target.target_ir import CanonicalBackendEmitter, TargetAstBuilder
from ecl_ir.canonical.variable_ir import parse_expression, project_expression


ROOT = Path(__file__).resolve().parents[1]


def project(source: str, target: str, text: str, use: VariableUseKind = VariableUseKind.READ):
    return project_expression(parse_expression(source, text, use_kind=use), target)


class VariableIrTests(unittest.TestCase):
    def test_variable_ref_is_typed_and_schema_roundtrips(self) -> None:
        expression = parse_expression("th11", "[-9939.0f] * 0.8f")
        self.assertEqual(len(expression.variable_uses), 1)
        reference = expression.variable_uses[0].reference
        self.assertEqual(reference.semantic_id, "boss.primary.local.float.0")
        self.assertEqual(reference.value_type, ValueType.FLOAT32)
        self.assertEqual(reference.storage_type, ValueType.FLOAT32)
        self.assertEqual(reference.storage_scope, VariableStorageScope.BOSS_PROXY)
        self.assertEqual(reference.access, VariableAccess.READ_WRITE)
        self.assertEqual(reference.propagation, VariablePropagation.SHARED)
        self.assertEqual(reference.confidence, Confidence.DOCUMENTED)
        self.assertEqual(ExpressionIR.from_dict(expression.to_dict()), expression)

    def test_th08_exact_pairs_encode_without_generation_regexes(self) -> None:
        cases = {
            "[10000]": "[-9985]",
            "[10000.0f]": "[-9985.0f]",
            "[10016.0f]": "[-9981.0f]",
            "[10020.0f]": "[-9935.0f]",
            "[10032]": "[-10000]",
            "[10033.0f]": "[-9999.0f]",
            "[10035.0f]": "[-9987.0f]",
            "[10082.0f]": "[-9998.0f]",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                result = project("th08", "th15", source)
                self.assertEqual(result.issues, ())
                self.assertEqual(result.expression.text, expected)
                reverse = project("th15", "th08", expected)
                self.assertEqual(reverse.issues, ())
                self.assertEqual(reverse.expression.text, source)

    def test_game_specific_availability_and_numeric_collisions_are_rejected(self) -> None:
        unavailable = (
            ("th11", "th10", "[-9939.0f]", "variable.target_unavailable"),
            ("th17", "th12", "[-9922.0f]", "variable.target_unavailable"),
            ("th16", "th17", "[-9903]", "variable.semantic_collision"),
            ("th17", "th16", "[-9903]", "variable.semantic_collision"),
            ("th18", "th17", "[-9898]", "variable.target_unavailable"),
        )
        for source, target, text, code in unavailable:
            with self.subTest(source=source, target=target, text=text):
                result = project(source, target, text)
                self.assertIsNone(result.expression)
                self.assertEqual(result.issues[0].code, code)

        self.assertEqual(
            profile_for_game("th14").variable_dialect.specs[-9906].semantic_id,
            "entity.mirror_state",
        )
        self.assertEqual(
            profile_for_game("th14").variable_dialect.specs[-9906].confidence,
            Confidence.INFERRED,
        )
        self.assertEqual(
            profile_for_game("th18").variable_dialect.specs[-9898].semantic_id,
            "bullet.active_count",
        )

    def test_spell_practice_selection_projects_across_modern_games(self) -> None:
        games = ("th13", "th14", "th15", "th16", "th17", "th18")
        for source in games:
            reference = parse_expression(source, "[-9907]").variable_uses[0].reference
            with self.subTest(source=source, property="typed_reference"):
                self.assertEqual(reference.semantic_id, "game.spell.practice.selection_id")
                self.assertEqual(reference.storage_type, ValueType.INT32)
                self.assertEqual(reference.storage_scope, VariableStorageScope.ENGINE_GLOBAL)
                self.assertEqual(reference.access, VariableAccess.READ_ONLY)
                self.assertEqual(reference.propagation, VariablePropagation.SHARED)
                self.assertEqual(reference.confidence, Confidence.DOCUMENTED)
            for target in games:
                if source == target:
                    continue
                with self.subTest(source=source, target=target):
                    result = project(source, target, "[-9907]")
                    self.assertEqual(result.issues, ())
                    self.assertEqual(result.expression.text, "[-9907]")

        write = project("th14", "th15", "[-9907]", VariableUseKind.WRITE)
        self.assertIsNone(write.expression)
        self.assertEqual(write.issues[0].code, "variable.storage_or_access_mismatch")

    def test_modern_main_spell_practice_guard_survives_cross_game_lowering(self) -> None:
        program = parse_decl_text(
            """void main()
{
    unless ([-9907] >= 0) goto main_100 @ 0;
    return;
main_100:
    return;
}
""",
            "th14/st01.decl",
        )
        module = build_semantic_module(program)
        planner = LoweringPlanner.for_game(
            "th15",
            backend_emitter=CanonicalBackendEmitter(module, "th15"),
        )
        rendered = TargetAstBuilder(planner).build(module).render_decl()
        self.assertIn("unless ([-9907] >= 0) goto main_100 @ 0;", rendered)
        self.assertNotIn("variable.unconfirmed_semantics", rendered)

    def test_th07_does_not_borrow_the_th08_variable_table(self) -> None:
        th07 = project("th07", "th15", "[10004.0f]")
        self.assertIsNone(th07.expression)
        self.assertEqual(th07.issues[0].code, "variable.unconfirmed_semantics")

        th08 = parse_expression("th08", "[10004.0f]")
        self.assertEqual(
            th08.variable_uses[0].reference.semantic_id,
            "th08.entity.local.int.8",
        )
        self.assertEqual(
            parse_expression("th08", "[10036]").variable_uses[0].reference.semantic_id,
            "th08.entity.local.int.4",
        )

    def test_unknown_bracket_tokens_are_identity_only(self) -> None:
        expression = parse_expression("th12", "[-1]")
        self.assertEqual(len(expression.variable_uses), 1)
        self.assertEqual(expression.variable_uses[0].reference.confidence, Confidence.UNKNOWN)

        identity = project_expression(expression, "th12")
        self.assertEqual(identity.expression.text, "[-1]")
        cross_game = project_expression(expression, "th13")
        self.assertIsNone(cross_game.expression)
        self.assertEqual(
            cross_game.issues[0].code,
            "variable.unconfirmed_semantics",
        )

    def test_mutating_syntax_requires_target_write_access(self) -> None:
        program = parse_decl_text(
            """void Main()
{
    if ([10040]--) goto Done @ 0;
Done:
}
""",
            "th08/mutating-condition.decl",
        )
        module = build_semantic_module(program)
        condition = module.routines[0].body[0]
        self.assertEqual(
            condition.expressions[0].expression.variable_uses[0].kind,
            VariableUseKind.READ_WRITE,
        )
        decision = LoweringPlanner.for_game("th15").plan_node(condition, "Main")
        self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(
            decision.diagnostics[0].code,
            "variable.storage_or_access_mismatch",
        )

    def test_named_locals_and_routine_params_do_not_cross_the_first_gen_abi(self) -> None:
        program = parse_decl_text(
            """void Main(var A)
{
    var B;
    ins_83($A);
}
""",
            "th10/named-local.decl",
        )
        module = build_semantic_module(program)
        planner = LoweringPlanner.for_game(
            "th08",
            backend_emitter=CanonicalBackendEmitter(module, "th08"),
        )
        target = TargetAstBuilder(planner).build(module)
        self.assertIn(
            "syntax.routine_parameters.unsupported",
            {diagnostic.code for diagnostic in target.diagnostics},
        )
        self.assertEqual(target.routines[0].body[0].strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(target.routines[0].body[1].strategy, LoweringStrategy.UNSUPPORTED)
        rendered = target.render_decl()
        self.assertIn("variable.local_stack_abi_unsupported", rendered)
        self.assertIn("syntax.routine_parameters.unsupported", rendered)

    def test_named_routine_calls_do_not_cross_the_first_gen_abi(self) -> None:
        module = build_semantic_module(parse_decl(ROOT / "th10/stage01.decl"))
        calls = {
            node.provenance.span.start_line: node
            for routine in module.routines
            for node in routine.body
            if node.provenance.span.start_line in {9, 88}
        }
        self.assertEqual(calls[9].statement_kind, "call")
        self.assertEqual(calls[88].statement_kind, "async_call")

        for line, node in calls.items():
            with self.subTest(line=line):
                incompatible = LoweringPlanner.for_game("th08").plan_node(node, "fixture")
                self.assertEqual(incompatible.strategy, LoweringStrategy.UNSUPPORTED)
                self.assertEqual(
                    incompatible.diagnostics[0].code,
                    "routine.call_abi_unsupported",
                )
                self.assertIsNone(incompatible.target_text)

                compatible = LoweringPlanner.for_game("th11").plan_node(node, "fixture")
                self.assertEqual(compatible.strategy, LoweringStrategy.RAW)
                self.assertEqual(compatible.target_text, node.text)

    def test_structured_stack_syntax_does_not_cross_into_the_first_gen_abi(self) -> None:
        module = build_semantic_module(parse_decl(ROOT / "th10/stage01.decl"))
        expected = {
            84: "goto",
            100: "conditional_goto",
            101: "return",
            107: "assign",
            1792: "raw",
        }
        statements = {
            node.provenance.span.start_line: node
            for routine in module.routines
            for node in routine.body
            if node.provenance.span.start_line in expected
        }
        self.assertEqual(
            {line: node.statement_kind for line, node in statements.items()},
            expected,
        )

        for line, node in statements.items():
            with self.subTest(line=line, kind=node.statement_kind):
                incompatible = LoweringPlanner.for_game("th08").plan_node(node, "fixture")
                self.assertEqual(incompatible.strategy, LoweringStrategy.UNSUPPORTED)
                self.assertEqual(
                    incompatible.diagnostics[0].code,
                    "routine.structured_syntax_abi_unsupported",
                )

                compatible = LoweringPlanner.for_game("th11").plan_node(node, "fixture")
                self.assertEqual(compatible.strategy, LoweringStrategy.RAW)
                self.assertEqual(compatible.target_text, node.text)

        declarations = build_semantic_module(parse_decl(ROOT / "th10/stage07.decl")).top_level
        declaration = next(
            node for node in declarations if node.provenance.span.start_line == 4
        )
        self.assertEqual(declaration.statement_kind, "function_decl")
        incompatible = LoweringPlanner.for_game("th08").plan_node(declaration)
        self.assertEqual(incompatible.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(
            incompatible.diagnostics[0].code,
            "routine.structured_syntax_abi_unsupported",
        )

    def test_projection_preserves_use_kind_and_target_encoding_metadata(self) -> None:
        source = parse_expression(
            "th08",
            "[10000]",
            use_kind=VariableUseKind.WRITE,
        )
        result = project_expression(source, "th15")
        self.assertEqual(result.expression.text, "[-9985]")
        projected_use = result.expression.variable_uses[0]
        self.assertEqual(projected_use.kind, VariableUseKind.WRITE)
        self.assertEqual(projected_use.reference.source_encoding.game, "th15")

    def test_preemptive_backend_policy_receives_projected_variables(self) -> None:
        lowered = compile_ir_op_event(
            {
                "op_key": "flow.fset",
                "source_game": "th08",
                "source_opcode": 7,
                "args": ["[10018.0f]", "0.1f"],
            },
            "th15",
        )
        self.assertIn("ins_45([-9979.0f])", lowered or "")
        self.assertNotIn("[10018.0f]", lowered or "")

    def test_side_game_paths_select_their_variable_dialect(self) -> None:
        self.assertEqual(parse_decl_text("", "th16_5/test.decl").game, "th165")
        self.assertEqual(parse_decl_text("", "th18.5/test.decl").game, "th185")
        expression = parse_expression("th165", "[-9903]")
        self.assertEqual(expression.variable_uses[0].reference.semantic_id, "th16.subseason.selected")

    def test_stack_relative_parameters_do_not_cross_the_th13_abi_boundary(self) -> None:
        module = build_semantic_module(parse_decl(ROOT / "th17/default.decl"))
        node = next(
            node
            for routine in module.routines
            if routine.name == "test"
            for node in routine.body
            if node.provenance.span.start_line == 283
        )
        stack_uses = [
            use
            for operand in node.operands
            for use in operand.value.expression.stack_uses
        ]
        self.assertEqual([use.reference.offset for use in stack_uses], [-1, -2, -3])
        self.assertEqual(
            ExpressionIR.from_dict(node.operands[1].value.expression.to_dict()),
            node.operands[1].value.expression,
        )

        old_target = LoweringPlanner.for_game("th12").plan_node(node, "test")
        self.assertEqual(old_target.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(old_target.diagnostics[0].code, "stack.relative_abi_unsupported")

        modern_target = LoweringPlanner.for_game("th15").plan_node(node, "test")
        self.assertEqual(modern_target.strategy, LoweringStrategy.DIRECT)

    def test_selected_evaluation_placeholder_context_never_allows_a_write(self) -> None:
        read = project_expression(
            parse_expression(
                "th15",
                "[-1]",
                use_kind=VariableUseKind.READ,
            ),
            "th12",
            evaluation_stack_offsets=frozenset({-1}),
        )
        self.assertEqual(read.issues, ())
        self.assertEqual(read.expression.text, "[-1]")

        write = project_expression(
            parse_expression(
                "th15",
                "[-1]",
                use_kind=VariableUseKind.WRITE,
            ),
            "th12",
            evaluation_stack_offsets=frozenset({-1}),
        )
        self.assertIsNone(write.expression)
        self.assertEqual(write.issues[0].code, "stack.relative_abi_unsupported")

    def test_projection_rebuilds_missing_or_stale_expression_spans(self) -> None:
        operation = semantic_operation(
            "th17",
            404,
            ["[-9991.0f] + [-1.0f]", "0.1f"],
        )
        serialized = operation.to_dict()
        expression = serialized["operands"][0]["value"]["expression"]
        self.assertTrue(expression["variable_uses"])
        self.assertTrue(expression["stack_uses"])
        expression.pop("stack_uses")
        expression["variable_uses"][0]["start"] = 0
        expression["variable_uses"][0]["end"] = 1

        legacy = SemanticOperation.from_dict(serialized)
        self.assertFalse(legacy.operands[0].value.expression.stack_uses)
        decision = LoweringPlanner.for_game("th12").plan_node(legacy, "fixture")
        self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(
            decision.diagnostics[0].code,
            "stack.relative_abi_unsupported",
        )

    def test_syntax_rvalue_and_lvalue_share_the_typed_expression_path(self) -> None:
        program = parse_decl_text(
            """void Main()
{
    unless ([10042.0f] < 0.0f) goto Done @ 0;
    [10042.0f] = 1.0f;
Done:
}
""",
            "th08/variable-syntax.decl",
        )
        module = build_semantic_module(program)
        condition, assignment, _label = module.routines[0].body
        self.assertEqual(condition.expressions[0].role, "condition")
        self.assertEqual(assignment.expressions[0].role, "target")
        self.assertEqual(
            assignment.expressions[0].expression.variable_uses[0].kind,
            VariableUseKind.WRITE,
        )

        result = LoweringPlanner.for_game("th15").plan_module(module)
        condition_decision, assignment_decision, _label_decision = result.routines[0].decisions
        self.assertEqual(condition_decision.strategy, LoweringStrategy.RAW)
        self.assertIn("[-9995.0f]", condition_decision.target_text)
        self.assertEqual(assignment_decision.strategy, LoweringStrategy.UNSUPPORTED)
        self.assertEqual(
            assignment_decision.diagnostics[0].code,
            "variable.storage_or_access_mismatch",
        )

    def test_real_unavailable_variables_stop_before_backend_lowering(self) -> None:
        cases = (
            (ROOT / "th11/stage06boss.decl", "th10", "BossCard5", 1399),
            (ROOT / "th17/st07bs.decl", "th12", "BossCard5_at3", 1831),
        )
        for path, target, routine_name, line in cases:
            with self.subTest(path=path, target=target, line=line):
                module = build_semantic_module(parse_decl(path))
                node = next(
                    node
                    for routine in module.routines
                    if routine.name == routine_name
                    for node in routine.body
                    if node.provenance.span.start_line == line
                )
                decision = LoweringPlanner.for_game(target).plan_node(node, routine_name)
                self.assertEqual(decision.strategy, LoweringStrategy.UNSUPPORTED)
                self.assertEqual(decision.diagnostics[0].code, "variable.target_unavailable")


if __name__ == "__main__":
    unittest.main()
