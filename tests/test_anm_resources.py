from __future__ import annotations

import unittest

from ecl_ir.analysis.anm_resources import (
    AnmActionCandidate,
    build_anm_lowering_plan,
    candidate_pool_for_module,
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

    def test_midboss_role_is_separate_while_shared_banks_stay_common(self) -> None:
        pool = candidate_pool_for_stage("th15", "01")
        midboss_main = next(
            candidate
            for candidate in pool.combinations
            if candidate.bank == 3
            and candidate.actions == (AnmActionCandidate("anm.set_main", 0, 0),)
            and any(item.startswith("st01mbs.decl:MBoss") for item in candidate.evidence)
        )

        self.assertEqual(midboss_main.role, "midboss")
        self.assertTrue(
            all(
                candidate.role == "common"
                for candidate in pool.combinations
                if candidate.bank in {0, 1}
            )
        )

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
        strict_planner = LoweringPlanner.for_game(
            "th15",
            backend_emitter=strict_emitter,
        )
        strict = strict_planner.plan_node(dynamic, "Main")
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
        strict_target = TargetAstBuilder(strict_planner).build(module)
        self.assertEqual(
            [statement.strategy.value for statement in strict_target.routines[0].body],
            ["unsupported", "unsupported"],
        )
        self.assertEqual(permissive.strategy.value, "lossy")
        self.assertEqual(permissive.diagnostics[-1].code, "anm.dynamic_script_candidate")
        rendered = TargetAstBuilder(permissive_planner).build(module).render_decl()
        self.assertEqual(rendered.count("ins_302(2);"), 1)
        self.assertIn("ins_306(0, 0);", permissive.target_text or "")
        self.assertTrue(all(item.startswith("st01.decl:") for item in selection.evidence))

    def test_dynamic_slot_is_lossy_and_dynamic_play_bank_is_unresolved(self) -> None:
        module, nodes = _anm_module(
            "th12",
            "th12/stage01.decl",
            (
                (258, ["1"]),
                (262, ["$A", "50"]),
                (263, ["$A", "101"]),
            ),
        )
        emitter = CanonicalBackendEmitter(module, "th15")
        plan = emitter.anm_plan

        dynamic_slot = plan.selections[str(nodes[1].node_id)]
        self.assertTrue(dynamic_slot.lossy)
        self.assertTrue(dynamic_slot.dynamic_source)
        self.assertNotIn(str(nodes[2].node_id), plan.selections)

        play = LoweringPlanner.for_game(
            "th15",
            backend_emitter=emitter,
        ).plan_node(nodes[2], "Main")
        self.assertEqual(play.strategy.value, "unsupported")
        self.assertEqual(play.diagnostics[-1].code, "anm.resource_context_unresolved")

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

    def test_call_bound_rejects_string_dispatched_callee(self) -> None:
        module = build_semantic_module(parse_decl("th10/stage02.decl"))
        wrapper = next(routine for routine in module.routines if routine.name == "BGirl00")
        dispatch = semantic_operation(
            "th10",
            261,
            ['"Girl00"', "0.0f", "0.0f", "10", "0", "0"],
            9000,
            routine=wrapper.name,
        )
        self.assertEqual(dispatch.operation, "enemy.create_abs_mirror")
        self.assertEqual(dispatch.operands[0].name, "routine")
        wrapper.body.append(dispatch)

        plan = build_anm_lowering_plan(module, "th15")
        callee = next(routine for routine in module.routines if routine.name == "Girl00")
        callee_anm = [
            node
            for node in callee.body
            if getattr(node, "operation", None)
            in {"anm.select", "anm.set_main", "anm.set_sprite"}
        ]

        self.assertFalse(
            any(item.callee == "Girl00" for item in plan.call_materializations.values())
        )
        self.assertTrue(
            all(
                plan.selections[str(node.node_id)].match_kind != "call_bound_folded"
                for node in callee_anm
            )
        )

        linked_module = build_semantic_module(parse_decl("th10/stage02.decl"))
        linked_module.resources.setdefault("ecli", []).append("external.ecl")
        linked_plan = build_anm_lowering_plan(linked_module, "th15")
        self.assertFalse(linked_plan.call_materializations)

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

    def test_play_pos_keeps_source_context_operands(self) -> None:
        module = build_semantic_module(parse_decl("th14/st06bs.decl"))
        emitter = CanonicalBackendEmitter(module, "th18")
        planner = LoweringPlanner.for_game(
            "th18",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=emitter,
        )
        routine = next(item for item in module.routines if item.name == "BossCupEndEff")
        source = next(
            node for node in routine.body if getattr(node, "operation", None) == "anm.play_pos"
        )
        strict = LoweringPlanner.for_game(
            "th18",
            backend_emitter=CanonicalBackendEmitter(module, "th18"),
        ).plan_node(source, routine.name)

        decision = planner.plan_node(source, routine.name)

        self.assertEqual(strict.strategy.value, "unsupported")
        self.assertEqual(strict.diagnostics[-1].code, "backend.lossy_forbidden")
        self.assertEqual(decision.strategy.value, "lossy")
        self.assertEqual(decision.diagnostics[-1].code, "anm.heuristic_package_candidate")
        self.assertIn("evidence=st06bs.decl:BossCard2", decision.target_text or "")
        self.assertIn(
            "ins_338(1, 73, 64.0f, 0.0f, -1.1780972f);",
            decision.target_text or "",
        )

    def test_anm_on_et_is_not_treated_as_a_script_reference(self) -> None:
        node = semantic_operation("th12", 274, ["0", "1"], 1, routine="Boss")
        module = SemanticModule(
            source="th12/stage01.decl",
            source_game="th12",
            profile="th12",
            routines=[SemanticRoutine("Boss", body=[node])],
        )
        planner = LoweringPlanner.for_game(
            "th15",
            backend_emitter=CanonicalBackendEmitter(module, "th15"),
        )

        decision = planner.plan_node(node, "Boss")

        self.assertEqual(node.operation, "anm.on_et")
        self.assertEqual(decision.strategy.value, "direct")
        self.assertEqual(decision.target_text, "ins_274(0, 1);")
        self.assertFalse(decision.diagnostics)

    def test_target_candidates_do_not_cross_control_flow_boundaries(self) -> None:
        cases = (
            ("th10", "04", "stage04.decl:Boss1"),
            ("th11", "01", "stage01.decl:RockS"),
        )
        for game, stage_id, unsafe_evidence in cases:
            with self.subTest(game=game, stage=stage_id):
                pool = candidate_pool_for_stage(game, stage_id)
                self.assertTrue(
                    all(
                        unsafe_evidence not in candidate.evidence
                        or len(candidate.actions) == 1
                        for candidate in pool.combinations
                    )
                )

    def test_guarded_set_actions_are_not_folded_into_another_lane(self) -> None:
        module = build_semantic_module(parse_decl("th11/stage06boss.decl"))
        plan = build_anm_lowering_plan(module, "th15")
        routine = next(item for item in module.routines if item.name == "BossCard2Bomb")
        guarded = [
            node
            for node in routine.body
            if getattr(node, "operation", None) == "anm.set_sprite"
            and node.guard.raw in {"E", "NHL"}
        ]

        self.assertEqual([node.guard.raw for node in guarded], ["E", "NHL"])
        selections = [plan.selections[str(node.node_id)] for node in guarded]
        self.assertTrue(all(selection.actions for selection in selections))
        self.assertTrue(all(selection.folded_into is None for selection in selections))

    def test_play_sequence_uses_same_target_routine_position(self) -> None:
        module = build_semantic_module(parse_decl("th10/stage01.decl"))
        plan = build_anm_lowering_plan(module, "th11")
        routine = next(item for item in module.routines if item.name == "BossDead")
        plays = [
            node for node in routine.body if getattr(node, "operation", None) == "anm.play"
        ]
        selections = [plan.selections[str(node.node_id)] for node in plays]

        self.assertEqual([selection.match_kind for selection in selections], ["routine_sequence"] * 4)
        self.assertEqual(
            [selection.actions[0].script for selection in selections],
            [76, 141, 76, 142],
        )
        self.assertTrue(all(not selection.lossy for selection in selections))

    def test_ambiguous_selected_bank_uses_only_lossy_role_scoped_candidate(self) -> None:
        module = build_semantic_module(parse_decl("th10/stage01.decl"))
        emitter = CanonicalBackendEmitter(module, "th15")
        routine = next(item for item in module.routines if item.name == "Boss1At1")
        source = next(
            node
            for node in routine.body
            if getattr(node, "operation", None) == "anm.selected_play"
        )
        selection = emitter.anm_plan.selections[str(source.node_id)]

        self.assertTrue(selection.lossy)
        self.assertTrue(selection.dynamic_source)
        self.assertEqual(
            [(action.operation, action.bank, action.script) for action in selection.actions],
            [("anm.select", 3, None), ("anm.selected_play", 3, 0)],
        )
        strict = LoweringPlanner.for_game(
            "th15",
            backend_emitter=CanonicalBackendEmitter(module, "th15"),
        ).plan_node(source, routine.name)
        permissive = LoweringPlanner.for_game(
            "th15",
            policy=LoweringPolicy(allow_lossy=True),
            backend_emitter=emitter,
        ).plan_node(source, routine.name)

        self.assertEqual(strict.strategy.value, "unsupported")
        self.assertEqual(strict.diagnostics[-1].code, "backend.lossy_forbidden")
        self.assertEqual(permissive.strategy.value, "lossy")
        self.assertIn("ins_302(3);", permissive.target_text or "")
        self.assertIn("ins_313(0);", permissive.target_text or "")

    def test_stage_routine_with_boss_mapped_source_bank_stays_stage_scoped(self) -> None:
        module = build_semantic_module(parse_decl("th12/stage01.decl"))
        for target_game, target_slot, target_script in (
            ("th10", 1, 45),
            ("th11", 0, 63),
        ):
            with self.subTest(target_game=target_game):
                emitter = CanonicalBackendEmitter(module, target_game)
                routine = next(item for item in module.routines if item.name == "ShipShadow")
                select = next(
                    node
                    for node in routine.body
                    if getattr(node, "operation", None) == "anm.select"
                )
                set_sprite = next(
                    node
                    for node in routine.body
                    if getattr(node, "operation", None) == "anm.set_sprite"
                )

                select_choice = emitter.anm_plan.selections[str(select.node_id)]
                sprite_choice = emitter.anm_plan.selections[str(set_sprite.node_id)]
                self.assertEqual(select_choice.actions[0].bank, 1)
                self.assertEqual(
                    [
                        (action.operation, action.bank, action.slot, action.script)
                        for action in sprite_choice.actions
                    ],
                    [("anm.set_sprite", 1, target_slot, target_script)],
                )
                self.assertTrue(sprite_choice.lossy)
                self.assertTrue(
                    all("Boss" not in evidence for evidence in sprite_choice.evidence)
                )

    def test_set_sprite_uses_only_lossy_same_role_setup_family_fallback(self) -> None:
        module = build_semantic_module(parse_decl("th11/stage01.decl"))
        emitter = CanonicalBackendEmitter(module, "th15")

        for routine_name in ("MBoss", "MBoss2", "MBoss3"):
            with self.subTest(routine=routine_name):
                routine = next(item for item in module.routines if item.name == routine_name)
                source = next(
                    node
                    for node in routine.body
                    if getattr(node, "operation", None) == "anm.set_sprite"
                    and any(
                        operand.name == "script" and operand.value.source_text == "0"
                        for operand in node.operands
                    )
                )
                selection = emitter.anm_plan.selections[str(source.node_id)]

                self.assertEqual(selection.match_kind, "target_corpus_candidate")
                self.assertTrue(selection.lossy)
                self.assertEqual(
                    [
                        (action.operation, action.bank, action.slot, action.script)
                        for action in selection.actions
                    ],
                    [("anm.set_main", 3, 0, 0)],
                )
                self.assertTrue(
                    all(evidence.startswith("st01mbs") for evidence in selection.evidence)
                )

                strict = LoweringPlanner.for_game(
                    "th15",
                    backend_emitter=CanonicalBackendEmitter(module, "th15"),
                ).plan_node(source, routine.name)
                permissive = LoweringPlanner.for_game(
                    "th15",
                    policy=LoweringPolicy(allow_lossy=True),
                    backend_emitter=emitter,
                ).plan_node(source, routine.name)
                self.assertEqual(strict.strategy.value, "unsupported")
                self.assertEqual(strict.diagnostics[-1].code, "backend.lossy_forbidden")
                self.assertEqual(permissive.strategy.value, "lossy")
                self.assertIn("ins_306(0, 0);", permissive.target_text or "")
                self.assertNotIn("ins_313(", permissive.target_text or "")

    def test_unknown_stage_never_falls_back_to_whole_game_pool(self) -> None:
        pool = candidate_pool_for_module("th15", "th11/stage4c01a.decl")

        self.assertIsNone(pool.stage_id)
        self.assertEqual(pool.resources, {})
        self.assertEqual(pool.combinations, ())


if __name__ == "__main__":
    unittest.main()
