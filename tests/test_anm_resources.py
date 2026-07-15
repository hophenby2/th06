from __future__ import annotations

import unittest

from ecl_ir.analysis.anm_resources import (
    AnmActionCandidate,
    build_anm_lowering_plan,
    candidate_pool_for_stage,
)
from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.canonical.semantic_ir import SemanticModule, SemanticRoutine
from ecl_ir.canonical.semantic_lifter import build_semantic_module
from ecl_ir.source.parser import parse_decl
from ecl_ir.target.lowering import LoweringPlanner, LoweringPolicy
from ecl_ir.target.target_ir import CanonicalBackendEmitter, TargetAstBuilder


def _anm_module(
    game: str,
    source: str,
    instructions: tuple[tuple[int, list[str]], ...],
    anim: tuple[str, ...] = ("enemy.anm", "source-stage.anm"),
) -> tuple[SemanticModule, list]:
    nodes = [
        semantic_operation(game, opcode, args, line, routine="Main")
        for line, (opcode, args) in enumerate(instructions, 1)
    ]
    return (
        SemanticModule(
            source=source,
            source_game=game,
            profile=game,
            resources={"anim": list(anim)},
            routines=[SemanticRoutine("Main", body=nodes)],
        ),
        nodes,
    )


def _has_action(pool, operation: str, script: int, *, role: str | None = None) -> bool:
    return any(
        (role is None or candidate.role == role)
        and any(
            action.operation == operation and action.script == script
            for action in candidate.actions
        )
        for candidate in pool.combinations
    )


class AnmResourceCandidateTests(unittest.TestCase):
    def test_candidate_pool_is_scoped_to_target_stage_package(self) -> None:
        stage01 = candidate_pool_for_stage("th15", "01")
        stage05 = candidate_pool_for_stage("th15", "05")
        stage06 = candidate_pool_for_stage("th15", "06")

        self.assertEqual(stage06.resources["anim"], ("enemy.anm", "st06enm.anm"))
        self.assertTrue(_has_action(stage05, "anm.set_main", 162, role="stage"))
        self.assertFalse(_has_action(stage06, "anm.set_main", 162, role="stage"))

        self.assertTrue(_has_action(stage05, "anm.set_sprite", 6, role="boss"))
        self.assertFalse(_has_action(stage01, "anm.set_sprite", 6, role="boss"))
        self.assertTrue(
            all(
                evidence.startswith("st06")
                for candidate in stage06.combinations
                for evidence in candidate.evidence
            )
        )

    def test_equal_numeric_combinations_keep_their_manifest_identity(self) -> None:
        stage01 = candidate_pool_for_stage("th14", "01")
        stage02 = candidate_pool_for_stage("th14", "02")
        actions = (
            AnmActionCandidate("anm.set_main", 0, 20),
            AnmActionCandidate("anm.set_sprite", 1, 93),
        )

        first = next(
            candidate
            for candidate in stage01.combinations
            if candidate.bank == 2 and candidate.actions == actions
        )
        second = next(
            candidate
            for candidate in stage02.combinations
            if candidate.bank == 2 and candidate.actions == actions
        )

        self.assertEqual(
            stage01.resources["anim"],
            ("enemy.anm", "st01enm.anm", "st01menm.anm"),
        )
        self.assertEqual(stage02.resources["anim"], ("enemy.anm", "st02enm.anm"))
        self.assertTrue(all(item.startswith("st01") for item in first.evidence))
        self.assertTrue(all(item.startswith("st02") for item in second.evidence))

    def test_select_and_following_set_actions_lower_as_one_candidate(self) -> None:
        module, nodes = _anm_module(
            "th14",
            "th14/st01.decl",
            (
                (302, ["2"]),
                (306, ["0", "40"]),
                (303, ["1", "93"]),
            ),
        )

        plan = build_anm_lowering_plan(module, "th15")
        select = plan.selections[str(nodes[0].node_id)]
        primary = plan.selections[str(nodes[1].node_id)]
        folded = plan.selections[str(nodes[2].node_id)]

        self.assertEqual(
            [(action.operation, action.bank, action.slot, action.script) for action in select.actions],
            [("anm.select", 2, None, None)],
        )
        self.assertEqual(
            [(action.operation, action.bank, action.slot, action.script) for action in primary.actions],
            [
                ("anm.set_main", 2, 0, 40),
                ("anm.set_sprite", 2, 1, 93),
            ],
        )
        self.assertTrue(all(item.startswith("st01.decl:") for item in primary.evidence))
        self.assertEqual(folded.actions, ())
        self.assertEqual(folded.folded_into, str(nodes[1].node_id))

    def test_same_game_anm_lowering_is_exact_identity(self) -> None:
        module, _nodes = _anm_module(
            "th15",
            "th15/st01.decl",
            (
                (302, ["2"]),
                (306, ["0", "40"]),
                (303, ["1", "93"]),
            ),
            anim=("enemy.anm", "st01enm.anm"),
        )
        emitter = CanonicalBackendEmitter(module, "th15")
        planner = LoweringPlanner.for_game("th15", backend_emitter=emitter)

        target = TargetAstBuilder(planner).build(module)

        self.assertFalse(emitter.anm_plan.selections)
        self.assertEqual(target.resources["anim"], ["enemy.anm", "st01enm.anm"])
        self.assertEqual(
            [statement.lines for statement in target.routines[0].body],
            [
                ("ins_302(2);",),
                ("ins_306(0, 40);",),
                ("ins_303(1, 93);",),
            ],
        )
        self.assertTrue(
            all(statement.strategy.value == "direct" for statement in target.routines[0].body)
        )
        self.assertTrue(all(not statement.diagnostics for statement in target.routines[0].body))

    def test_dynamic_script_requires_lossy_opt_in(self) -> None:
        module, nodes = _anm_module(
            "th12",
            "th12/stage01.decl",
            (
                (258, ["1"]),
                (262, ["0", "$A"]),
            ),
        )
        dynamic = nodes[1]

        strict_emitter = CanonicalBackendEmitter(module, "th15")
        strict = LoweringPlanner.for_game(
            "th15",
            backend_emitter=strict_emitter,
        ).plan_node(dynamic, "Main")
        permissive_emitter = CanonicalBackendEmitter(module, "th15")
        permissive_planner = LoweringPlanner.for_game(
            "th15",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=permissive_emitter,
        )
        permissive = permissive_planner.plan_node(dynamic, "Main")

        selection = permissive_emitter.anm_plan.selections[str(dynamic.node_id)]
        self.assertTrue(selection.lossy)
        self.assertEqual(strict.strategy.value, "unsupported")
        self.assertEqual(strict.diagnostics[-1].code, "backend.lossy_forbidden")
        self.assertEqual(permissive.strategy.value, "lossy")
        self.assertEqual(permissive.diagnostics[-1].code, "anm.dynamic_script_candidate")
        rendered = TargetAstBuilder(permissive_planner).build(module).render_decl()
        self.assertEqual(rendered.count("ins_302(2);"), 1)
        self.assertIn("ins_306(0, 0);", permissive.target_text or "")
        self.assertTrue(all(item.startswith("st01.decl:") for item in selection.evidence))

    def test_call_bound_anm_is_materialized_once_before_each_call(self) -> None:
        module = build_semantic_module(parse_decl("th10/stage02.decl"))
        emitter = CanonicalBackendEmitter(module, "th15")
        planner = LoweringPlanner.for_game("th15", backend_emitter=emitter)
        plan = emitter.anm_plan
        expected = {
            "BGirl00": {
                "call": "@Girl00(49, 45);",
                "actions": [
                    ("anm.select", 2, None, None),
                    ("anm.set_main", 2, 0, 0),
                ],
                "evidence": "st02.decl:GirlBlueA01",
                "instructions": ["ins_302(2);", "ins_306(0, 0);"],
            },
            "RGirl00": {
                "call": "@Girl00(50, 46);",
                "actions": [
                    ("anm.select", 2, None, None),
                    ("anm.set_main", 2, 0, 5),
                ],
                "evidence": "st02.decl:GirlRedA01",
                "instructions": ["ins_302(2);", "ins_306(0, 5);"],
            },
            "GGirl00": {
                "call": "@Girl00(51, 47);",
                "actions": [
                    ("anm.select", 2, None, None),
                    ("anm.set_main", 2, 0, 35),
                    ("anm.set_sprite", 2, 1, 93),
                ],
                "evidence": "st02.decl:GirlC01",
                "instructions": ["ins_302(2);", "ins_306(0, 35);", "ins_303(1, 93);"],
            },
            "YGirl00": {
                "call": "@Girl00(52, 48);",
                "actions": [
                    ("anm.select", 2, None, None),
                    ("anm.set_main", 2, 0, 40),
                    ("anm.set_sprite", 2, 1, 93),
                ],
                "evidence": "st02.decl:GirlD01",
                "instructions": ["ins_302(2);", "ins_306(0, 40);", "ins_303(1, 93);"],
            },
        }
        calls = {
            routine.name: node
            for routine in module.routines
            for node in routine.body
            if getattr(node, "statement_kind", None) == "call"
            and node.attributes.get("function") == "Girl00"
        }

        self.assertEqual(set(calls), set(expected))
        for caller, case in expected.items():
            with self.subTest(caller=caller):
                call = calls[caller]
                materialization = plan.call_materializations[str(call.node_id)]
                selection = materialization.selection
                self.assertEqual(materialization.callee, "Girl00")
                self.assertEqual(selection.match_kind, "call_bound_semantic_purpose")
                self.assertEqual(selection.target_stage_id, "02")
                self.assertEqual(
                    [
                        (action.operation, action.bank, action.slot, action.script)
                        for action in selection.actions
                    ],
                    case["actions"],
                )
                self.assertIn(case["evidence"], selection.evidence)
                self.assertTrue(all(item.startswith("st02.decl:") for item in selection.evidence))

        callee = next(routine for routine in module.routines if routine.name == "Girl00")
        callee_anm = [
            node
            for node in callee.body
            if getattr(node, "operation", None)
            in {"anm.select", "anm.set_main", "anm.set_sprite"}
        ]
        self.assertEqual(
            [node.operation for node in callee_anm],
            ["anm.select", "anm.set_sprite", "anm.set_sprite"],
        )
        for node in callee_anm:
            selection = plan.selections[str(node.node_id)]
            self.assertEqual(selection.match_kind, "call_bound_folded")
            self.assertEqual(selection.actions, ())
            self.assertTrue(selection.folded_into.startswith("call-sites:"))

        target = TargetAstBuilder(planner).build(module)
        rendered = target.render_decl()
        for caller, case in expected.items():
            with self.subTest(rendered_caller=caller):
                target_routine = next(routine for routine in target.routines if routine.name == caller)
                call_statement = next(
                    statement
                    for statement in target_routine.body
                    if statement.source_node_id == str(calls[caller].node_id)
                )
                self.assertEqual(call_statement.lines.count("ins_302(2);"), 1)
                self.assertLess(
                    call_statement.lines.index("ins_302(2);"),
                    call_statement.lines.index(case["call"]),
                )
                rendered_sequence = "\n".join(
                    f"    {line}" for line in (*case["instructions"], case["call"])
                )
                self.assertEqual(rendered.count(rendered_sequence), 1)

        target_callee = next(routine for routine in target.routines if routine.name == "Girl00")
        folded_statements = {
            statement.source_node_id: statement
            for statement in target_callee.body
            if statement.source_node_id in {str(node.node_id) for node in callee_anm}
        }
        self.assertEqual(set(folded_statements), {str(node.node_id) for node in callee_anm})
        self.assertTrue(
            all(
                not any(line.lstrip().startswith("ins_") for line in statement.lines)
                for statement in folded_statements.values()
            )
        )

    def test_stage06_blue_candidate_prefers_girl_a01_main_five(self) -> None:
        module = build_semantic_module(parse_decl("th12/stage06.decl"))
        plan = build_anm_lowering_plan(module, "th15")
        wrapper = next(routine for routine in module.routines if routine.name == "BGirl01")
        source_main = next(
            node for node in wrapper.body if getattr(node, "operation", None) == "anm.set_main"
        )

        selection = plan.selections[str(source_main.node_id)]

        self.assertEqual(selection.match_kind, "semantic_purpose")
        self.assertEqual(selection.target_stage_id, "06")
        self.assertEqual(selection.evidence, ("st06.decl:GirlA01",))
        self.assertEqual(
            [(action.operation, action.slot, action.script) for action in selection.actions],
            [("anm.set_main", 0, 5)],
        )
        self.assertNotIn("st06.decl:GirlA01b", selection.evidence)

    def test_play_candidate_does_not_insert_anm_select(self) -> None:
        module = build_semantic_module(parse_decl("th12/stage06.decl"))
        emitter = CanonicalBackendEmitter(module, "th15")
        planner = LoweringPlanner.for_game("th15", backend_emitter=emitter)
        boss = next(routine for routine in module.routines if routine.name == "Boss1")
        source_play = next(
            node for node in boss.body if getattr(node, "operation", None) == "anm.play"
        )
        selection = emitter.anm_plan.selections[str(source_play.node_id)]

        self.assertEqual(
            [(action.operation, action.bank, action.script) for action in selection.actions],
            [("anm.play", 1, 75)],
        )
        self.assertNotIn("anm.select", {action.operation for action in selection.actions})

        target = TargetAstBuilder(planner).build(module)
        target_boss = next(routine for routine in target.routines if routine.name == "Boss1")
        statement = next(
            item for item in target_boss.body if item.source_node_id == str(source_play.node_id)
        )
        self.assertEqual(statement.lines.count("ins_307(1, 75);"), 1)
        self.assertFalse(any(line.startswith("ins_302(") for line in statement.lines))


if __name__ == "__main__":
    unittest.main()
