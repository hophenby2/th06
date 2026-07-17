from __future__ import annotations

import unittest

from ecl_ir.target.lowering import LoweringPlanner, LoweringPolicy
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.source.parser import parse_decl
from ecl_ir.canonical.semantic_ir import (
    Confidence,
    NodeId,
    Provenance,
    RawInstructionOp,
    SemanticModule,
    SemanticRoutine,
    SourceSpan,
    SyntaxStatement,
)
from ecl_ir.canonical.semantic_lifter import build_semantic_module
from ecl_ir.target.target_ir import (
    CanonicalBackendEmitter,
    TargetAstBuilder,
    decode_legacy_macro_random_ranges,
)


class TargetIrTests(unittest.TestCase):
    def test_target_statement_does_not_split_in_string_control_bytes(self) -> None:
        raw = 'ins_999("a\x1cb\x0cc\x0bd\re");'
        operation = semantic_operation(
            "th08",
            999,
            ['"a\x1cb\x0cc\x0bd\re"'],
            1,
            routine="Main",
            raw=raw,
        )
        module = SemanticModule(
            source="source.decl",
            source_game="th08",
            profile="th08",
            routines=[SemanticRoutine("Main", body=[operation])],
        )
        planner = LoweringPlanner.for_game(
            "th08",
            backend_emitter=CanonicalBackendEmitter(module, "th08"),
        )

        statement = TargetAstBuilder(planner).build(module).routines[0].body[0]

        self.assertEqual(statement.lines, (raw,))

    def test_anm_resource_numbers_require_verified_cross_game_context(self) -> None:
        cases = (
            ("th10/stage01.decl", 8, "th15", "anm.set_main", "ins_262(1, 45);"),
            ("th08/ecldata8.decl", 4, "th15", "anm.set", None),
        )
        for path, line, target_game, operation, identity_text in cases:
            with self.subTest(path=path, line=line, target=target_game):
                module = build_semantic_module(parse_decl(path))
                node = next(
                    node
                    for routine in module.routines
                    for node in routine.body
                    if node.provenance.span.start_line == line
                )
                self.assertEqual(node.operation, operation)
                decision = LoweringPlanner.for_game(target_game).plan_node(
                    node,
                    node.provenance.routine,
                )
                self.assertEqual(decision.strategy.value, "unsupported")
                self.assertEqual(
                    decision.diagnostics[0].code,
                    "anm.resource_context_unresolved",
                )
                if identity_text is not None:
                    identity = LoweringPlanner.with_compat_backend(
                        node.provenance.game
                    ).plan_node(node, node.provenance.routine)
                    self.assertEqual(identity.target_text, identity_text)

        module = build_semantic_module(parse_decl("th15/st05.decl"))
        layer = next(
            node
            for routine in module.routines
            for node in routine.body
            if node.provenance.span.start_line == 24
        )
        self.assertEqual(layer.operation, "anm.layer")
        decision = LoweringPlanner.for_game(
            "th16",
            backend_emitter=CanonicalBackendEmitter(module, "th16"),
        ).plan_node(layer, layer.provenance.routine)
        self.assertEqual(decision.strategy.value, "direct")
        self.assertEqual(decision.target_text, "ins_336(0, 6);")

    def test_target_ast_preserves_order_and_unsupported_source(self) -> None:
        first = semantic_operation("th12", 0, [], 1, routine="Main", raw="ins_0();")
        raw = RawInstructionOp(
            node_id=NodeId("Main:2:0"),
            opcode=999,
            args=["1"],
            provenance=Provenance(
                game="th12",
                routine="Main",
                span=SourceSpan("source.decl", 2, 2),
                opcode=999,
                raw="ins_999(1);",
                confidence=Confidence.UNKNOWN,
            ),
        )
        module = SemanticModule(
            source="source.decl",
            source_game="th12",
            profile="th12",
            routines=[SemanticRoutine("Main", body=[first, raw])],
        )
        target = TargetAstBuilder(LoweringPlanner.with_compat_backend("th15")).build(module)
        self.assertEqual([statement.source_node_id for statement in target.routines[0].body], ["Main:1:0", "Main:2:0"])
        rendered = target.render_decl()
        self.assertIn("ins_0();", rendered)
        self.assertIn("raw.incompatible_dialect", rendered)
        self.assertIn("ins_999(1);", rendered)
        self.assertTrue(rendered.rstrip().endswith("}"))

    def test_cross_game_raw_requires_opt_in_and_renders_its_warning(self) -> None:
        raw = RawInstructionOp(
            node_id=NodeId("Main:1:0"),
            opcode=569,
            args=["-1"],
            provenance=Provenance(
                game="th15",
                routine="Main",
                span=SourceSpan("source.decl", 1, 1),
                opcode=569,
                raw="ins_569(-1);",
                confidence=Confidence.UNKNOWN,
            ),
        )
        module = SemanticModule(
            source="source.decl",
            source_game="th15",
            profile="th15",
            routines=[SemanticRoutine("Main", body=[raw])],
        )

        strict = TargetAstBuilder(LoweringPlanner.for_game("th17")).build(module)
        self.assertEqual(strict.routines[0].body[0].strategy.value, "unsupported")

        opted_in = TargetAstBuilder(
            LoweringPlanner.for_game(
                "th17",
                policy=LoweringPolicy(preserve_raw_same_family=True),
            )
        ).build(module)
        rendered = opted_in.render_decl()
        self.assertIn("[raw.same_family_passthrough]", rendered)
        self.assertIn("ins_569(-1);", rendered)

    def test_append_cursor_is_materialized_for_indexed_target(self) -> None:
        operations = [
            semantic_operation("th14", 600, ["0"], 1, routine="Main"),
            semantic_operation("th14", 611, ["0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"], 2, routine="Main"),
            semantic_operation("th14", 611, ["0", "0", "4", "30", "-999999", "0.1f", "-999999.0f"], 3, routine="Main"),
            semantic_operation("th14", 641, ["0"], 4, routine="Main"),
            semantic_operation("th14", 611, ["0", "0", "8", "60", "-999999", "0.2f", "0.3f"], 5, routine="Main"),
        ]
        module = SemanticModule(
            source="source.decl",
            source_game="th14",
            profile="th14",
            routines=[SemanticRoutine("Main", body=operations)],
        )
        planner = LoweringPlanner.for_game(
            "th12",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        )
        target = TargetAstBuilder(planner).build(module)
        rendered = target.render_decl()
        self.assertIn("ins_509(0, 0, 0, 2", rendered)
        self.assertIn("ins_509(0, 1, 0, 4", rendered)
        self.assertIn("ins_509(0, 1, 0, 8", rendered)
        self.assertIn("folded append cursor decrement", rendered)

    def test_spawn_transform_pair_is_emitted_once_as_two_expanded_records(self) -> None:
        operations = [
            semantic_operation(
                "th12",
                509,
                ["0", "3", "0", "524288", "50923526", "12", "2.0f", "0.5f"],
                1,
                routine="Main",
            ),
            semantic_operation(
                "th12",
                509,
                ["0", "4", "0", "1048576", "1", "0", "0.25f", "0.0f"],
                2,
                routine="Main",
            ),
        ]
        module = SemanticModule(
            source="source.decl",
            source_game="th12",
            profile="th12",
            routines=[SemanticRoutine("Main", body=operations)],
        )
        planner = LoweringPlanner.for_game(
            "th15",
            backend_emitter=CanonicalBackendEmitter(module, "th15"),
        )
        target = TargetAstBuilder(planner).build(module)
        rendered = target.render_decl()
        self.assertIn(
            "ins_610(0, 3, 0, 8192, 6, 3, 12, 1, 0.25f, 0.0f, 2.0f, 0.5f);",
            rendered,
        )
        self.assertIn(
            "ins_610(0, 4, 0, 16384, 9, 9, 0, 0, 0.0f, 0.0f, 0.0f, 0.0f);",
            rendered,
        )
        self.assertIn("folded spawned-bullet payload", rendered)
        self.assertNotIn("backend.transform.unsupported", rendered)

    def test_same_game_spawn_transform_pair_preserves_raw_records(self) -> None:
        args = (
            ["0", "3", "0", "524288", "-1", "12", "2.0f", "0.5f"],
            ["0", "4", "0", "1048576", "1", "0", "0.25f", "0.0f"],
        )
        operations = [
            semantic_operation("th12", 509, record, line, routine="Main")
            for line, record in enumerate(args, 1)
        ]
        module = SemanticModule(
            source="source.decl",
            source_game="th12",
            profile="th12",
            routines=[SemanticRoutine("Main", body=operations)],
        )
        emitter = CanonicalBackendEmitter(module, "th12")
        planner = LoweringPlanner.for_game("th12", backend_emitter=emitter)

        target = TargetAstBuilder(planner).build(module)

        self.assertFalse(emitter.spawn_bundle_follower_by_leader)
        self.assertFalse(emitter.spawn_bundle_leader_by_follower)
        self.assertEqual(
            [statement.lines for statement in target.routines[0].body],
            [(f"ins_509({', '.join(record)});",) for record in args],
        )
        self.assertFalse(target.diagnostics)

    def test_divergent_difficulty_cursors_are_not_guessed(self) -> None:
        operations = [
            semantic_operation("th13", 600, ["0"], 1, routine="Main"),
            semantic_operation("th13", 611, ["0", "0", "2", "1", "-999999", "-999999.0f", "-999999.0f"], 2, "E", routine="Main"),
            semantic_operation("th13", 611, ["0", "0", "4", "30", "-999999", "0.1f", "-999999.0f"], 3, routine="Main"),
        ]
        module = SemanticModule(
            source="source.decl",
            source_game="th13",
            profile="th13",
            routines=[SemanticRoutine("Main", body=operations)],
        )
        planner = LoweringPlanner.for_game(
            "th12",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=CanonicalBackendEmitter(module, "th12"),
        )
        target = TargetAstBuilder(planner).build(module)
        last = target.routines[0].body[-1]
        self.assertEqual(last.strategy.value, "unsupported")
        self.assertEqual(last.diagnostics[-1].code, "backend.transform_append_index_join")

    def test_legacy_timeline_and_rank_syntax_are_target_normalized(self) -> None:
        def syntax(line: int, text: str) -> SyntaxStatement:
            return SyntaxStatement(
                node_id=NodeId(f"<module>:{line}:0"),
                statement_kind="raw",
                text=text,
                attributes={},
                provenance=Provenance(
                    game="th08",
                    routine="",
                    span=SourceSpan("source.decl", line, line),
                    raw=text,
                    confidence=Confidence.DOCUMENTED,
                ),
            )

        ranked = semantic_operation(
            "th08",
            23,
            ["1"],
            5,
            "ENHL57",
            routine="Main",
        )
        module = SemanticModule(
            source="source.decl",
            source_game="th08",
            profile="th08",
            top_level=[
                syntax(1, "timeline Timeline0()"),
                syntax(2, "{"),
                syntax(3, "+1:"),
                syntax(4, "}"),
            ],
            routines=[SemanticRoutine("Main", body=[ranked])],
        )
        target = TargetAstBuilder(LoweringPlanner.with_compat_backend("th15")).build(module)
        self.assertEqual(
            [statement.source_node_id for statement in target.top_level],
            ["<module>:1:0", "<module>:2:0", "<module>:3:0", "<module>:4:0"],
        )
        self.assertTrue(all(statement.strategy.value == "unsupported" for statement in target.top_level))
        rendered = target.render_decl()
        self.assertNotIn("timeline Timeline0()", rendered)
        self.assertIn("syntax.timeline.cross_game_unsupported", rendered)
        self.assertIn("!ENHLO7\n", rendered)
        self.assertNotIn("!ENHL57", rendered)

        first_target = TargetAstBuilder(LoweringPlanner.with_compat_backend("th07")).build(module)
        self.assertTrue(all(statement.strategy.value == "unsupported" for statement in first_target.top_level))

    def test_legacy_timeline_region_is_typed_and_rejected_by_the_planner(self) -> None:
        module = build_semantic_module(parse_decl("th08/ecldata1.decl"))
        header = next(
            node for node in module.top_level if node.provenance.span.start_line == 1854
        )
        instruction = next(
            node for node in module.top_level if node.provenance.span.start_line == 1857
        )
        self.assertEqual(header.dialect_region.name, "Timeline0")
        self.assertEqual(header.dialect_region.member_index, 0)
        self.assertEqual(instruction.dialect_region.name, "Timeline0")
        self.assertGreater(instruction.dialect_region.member_count, 100)

        restored = SemanticModule.from_dict(module.to_dict())
        restored_instruction = next(
            node for node in restored.top_level if node.provenance.span.start_line == 1857
        )
        self.assertEqual(restored_instruction.dialect_region, instruction.dialect_region)

        decision = LoweringPlanner.for_game("th07").plan_node(instruction)
        self.assertEqual(decision.strategy.value, "unsupported")
        self.assertEqual(
            decision.diagnostics[0].code,
            "syntax.timeline.cross_game_unsupported",
        )

    def test_cross_game_legacy_macro_rejections_are_structured(self) -> None:
        base_args = ["0", "3", "4", "2", "2.0f", "1.0f", "0.0f", "0.1f", "0"]

        def lower(source: str, opcode: int, args: list[str], target: str = "th15"):
            operation = semantic_operation(source, opcode, args, 1, routine="Main")
            module = SemanticModule(
                source="source.decl",
                source_game=source,
                profile=source,
                routines=[SemanticRoutine("Main", body=[operation])],
            )
            planner = LoweringPlanner.for_game(
                target,
                policy=LoweringPolicy(allow_lossy=True),
                backend_emitter=CanonicalBackendEmitter(module, target),
            )
            return TargetAstBuilder(planner).build(module).routines[0].body[0]

        cases = (
            ("th06", 67, base_args, "th15", "backend.legacy_macro.opaque_runtime"),
            ("th08", 96, [*base_args[:8], "[10000]"], "th15", "backend.legacy_macro.dynamic_flags"),
            ("th08", 96, [*base_args[:8], "512"], "th15", "backend.legacy_macro.transform_flags"),
            ("th08", 96, ["[10000]", *base_args[1:]], "th15", "backend.legacy_macro.dynamic_shape"),
            ("th08", 96, ["999", *base_args[1:]], "th15", "backend.legacy_macro.shape_catalog"),
            (
                "th08",
                102,
                [*base_args[:6], "[10000.0f]", "1.0f", "0"],
                "th15",
                "backend.legacy_macro.dynamic_random_range",
            ),
            ("th08", 96, base_args, "th15", "backend.legacy_macro.color_catalog"),
            ("th08", 96, base_args, "th07", "backend.legacy_macro.color_catalog"),
        )
        for source, opcode, args, target, code in cases:
            with self.subTest(source=source, opcode=opcode, target=target, code=code):
                statement = lower(source, opcode, args, target)
                self.assertEqual(statement.strategy.value, "unsupported")
                self.assertEqual(statement.diagnostics[-1].code, code)

    def test_legacy_random_macro_endpoints_decode_to_ranges(self) -> None:
        base_args = ["0", "3", "4", "2", "3.0f", "1.0f", "3.0f", "-1.0f", "0"]
        expected = {
            "random_angle": {
                "angle_center": "1.0f",
                "angle_half_span": "2.0f",
            },
            "random_speed": {
                "speed_minimum": "1.0f",
                "speed_span": "2.0f",
            },
            "random_angle_speed": {
                "angle_center": "1.0f",
                "angle_half_span": "2.0f",
                "speed_minimum": "1.0f",
                "speed_span": "2.0f",
            },
        }
        for mode, ranges in expected.items():
            with self.subTest(mode=mode):
                decoded = decode_legacy_macro_random_ranges(mode, base_args)
                self.assertIsNotNone(decoded)
                self.assertEqual(decoded.to_dict(), ranges)

    def test_same_game_legacy_macro_uses_identity_lowering(self) -> None:
        args = [
            "[10000]",
            "[10001]",
            "[10002]",
            "[10003]",
            "[10004.0f]",
            "[10005.0f]",
            "[10006.0f]",
            "[10007.0f]",
            "[10008]",
        ]
        for source, opcode in (("th06", 67), ("th07", 64), ("th08", 96)):
            with self.subTest(source=source):
                operation = semantic_operation(source, opcode, args, 1, routine="Main")
                module = SemanticModule(
                    source="source.decl",
                    source_game=source,
                    profile=source,
                    routines=[SemanticRoutine("Main", body=[operation])],
                )
                planner = LoweringPlanner.for_game(
                    source,
                    backend_emitter=CanonicalBackendEmitter(module, source),
                )
                statement = TargetAstBuilder(planner).build(module).routines[0].body[0]
                self.assertEqual(statement.strategy.value, "direct")
                self.assertEqual(statement.lines, (f"ins_{opcode}({', '.join(args)});",))
                self.assertFalse(statement.diagnostics)


if __name__ == "__main__":
    unittest.main()
