from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ecl_ir.analysis.anm_resources import (
    AnmActionCandidate,
    AnmCandidatePool,
    AnmCombinationCandidate,
    AnmRoutinePlayCandidate,
    candidate_pool_for_stage,
)
from ecl_ir.analysis.execution_check import (
    _resolve_generated_source,
    check_ecl_file,
    check_ecl_text,
)


GAME = "th15"
EXPECTED_ANIM = ("enemy.anm", "st01enm.anm")
REPO_ROOT = Path(__file__).resolve().parents[1]


def combination(
    bank: int,
    *actions: AnmActionCandidate,
    role: str = "stage",
) -> AnmCombinationCandidate:
    return AnmCombinationCandidate(
        bank=bank,
        role=role,
        actions=tuple(actions),
        occurrences=1,
        evidence=("st01.decl:Reference",),
    )


def pool_with(*combinations: AnmCombinationCandidate) -> AnmCandidatePool:
    return AnmCandidatePool(
        game=GAME,
        stage_id="01",
        resources={"anim": EXPECTED_ANIM},
        combinations=tuple(combinations),
    )


def action(operation: str, slot: int | None, script: int) -> AnmActionCandidate:
    return AnmActionCandidate(operation, slot, script)


class ExecutionCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        package = self.root / GAME
        package.mkdir()
        self.reference = package / "st01.decl"
        self.reference.write_text(
            'anim { "enemy.anm"; "st01enm.anm"; }\n\nvoid main()\n{\n    return;\n}\n',
            encoding="utf-8",
        )

    def check(
        self,
        body: str,
        *,
        pool: AnmCandidatePool | None = None,
        difficulties: tuple[str, ...] = ("E",),
        source_name: str = "th15/st01.decl",
        reference: bool = True,
        state_budget: int = 50_000,
    ):
        text = (
            'anim { "enemy.anm"; "st01enm.anm"; }\n\n'
            + body.strip()
            + "\n"
        )
        candidate_pool = pool if pool is not None else pool_with()
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidate_pool,
        ):
            return check_ecl_text(
                text,
                source_name=source_name,
                game=GAME,
                reference_package=self.reference if reference else None,
                difficulties=difficulties,
                state_budget=state_budget,
            )

    @staticmethod
    def with_code(report, code: str):
        return [diagnostic for diagnostic in report.diagnostics if diagnostic.code == code]

    def test_guard_is_checked_only_in_its_active_enhl_lane(self) -> None:
        report = self.check(
            """
void main()
{
!H
    ins_319(0, 0.0f);
!*
    return;
}
""",
            difficulties=("E", "N", "H", "L"),
        )

        diagnostics = self.with_code(report, "anm.slot_unbound")
        self.assertEqual([item.difficulty for item in diagnostics], ["H"])
        self.assertTrue(report.has_errors)
        self.assertEqual(report.to_dict()["errors"], len(report.errors))

    def test_undeclared_use_before_declaration_and_parameter_scope(self) -> None:
        report = self.check(
            """
void main()
{
    @Good(1);
    @Bad();
    return;
}

void Good(var P)
{
    ins_23($P);
    return;
}

void Bad()
{
    ins_23($Missing);
    ins_23($Later);
    var Later;
    return;
}
"""
        )

        undeclared = self.with_code(report, "symbol.undeclared_local")
        use_before = self.with_code(report, "symbol.use_before_declaration")
        self.assertEqual({item.details.get("name") for item in undeclared}, {"Missing"})
        self.assertEqual({item.details.get("name") for item in use_before}, {"Later"})
        self.assertFalse(
            any(item.details.get("name") == "P" for item in report.diagnostics)
        )

    def test_unsupported_opcode_arity_and_type_are_distinguished(self) -> None:
        report = self.check(
            """
void main()
{
    ins_9999();
    ins_302();
    ins_302(1.0f);
    return;
}
"""
        )

        invalid = self.with_code(report, "instruction.invalid_arguments")
        self.assertEqual(len(invalid), 3)
        self.assertEqual(
            [item.details.get("kind") for item in invalid],
            ["unsupported_opcode", "arity_or_type", "arity_or_type"],
        )
        self.assertTrue(report.has_errors)

    def test_inactive_guarded_goto_falls_through(self) -> None:
        report = self.check(
            """
void main()
{
!E
    goto Done @ 0;
!*
    ins_319(0, 0.0f);
Done:
    return;
}
""",
            difficulties=("E", "N"),
        )

        diagnostics = self.with_code(report, "anm.slot_unbound")
        self.assertEqual([item.difficulty for item in diagnostics], ["N"])

    def test_loop_reaches_a_fixed_point_within_budget(self) -> None:
        report = self.check(
            """
void main()
{
    var A;
    $A = 2;
Loop:
    if ($A--) goto Loop @ 0;
    return;
}
""",
            state_budget=100,
        )

        self.assertTrue(report.analysis_complete)
        self.assertFalse(self.with_code(report, "execution.state_budget_exceeded"))
        self.assertFalse(report.has_errors)

    def test_budget_exhaustion_does_not_skip_later_difficulty_lanes(self) -> None:
        report = self.check(
            """
void main()
{
    ins_23(1);
    ins_23(1);
    ins_23(1);
    return;
}
""",
            difficulties=("E", "N"),
            state_budget=3,
        )

        diagnostics = self.with_code(report, "execution.state_budget_exceeded")
        self.assertEqual([item.difficulty for item in diagnostics], ["E", "N"])
        self.assertFalse(report.analysis_complete)

    def test_budget_equal_to_unique_state_count_is_complete(self) -> None:
        report = self.check(
            """
void main()
{
Loop:
    goto Loop @ 0;
}
""",
            state_budget=2,
        )

        self.assertEqual(report.states_explored, 2)
        self.assertTrue(report.analysis_complete)
        self.assertFalse(self.with_code(report, "execution.state_budget_exceeded"))

    def test_synchronous_call_inherits_selected_bank_and_slot_state(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    @Child();
    return;
}

void Child()
{
    ins_306(0, 40);
    ins_319(0, 0.0f);
    return;
}
""",
            pool=candidates,
        )

        self.assertFalse(report.has_errors, report.to_dict())
        self.assertFalse(self.with_code(report, "anm.bank_unselected"))
        self.assertFalse(self.with_code(report, "anm.slot_unbound"))

    def test_sibling_prototype_parameters_flow_into_a_parameterless_body(self) -> None:
        package = self.root / "prototype-package"
        package.mkdir()
        root = package / "st01.decl"
        root.write_text(
            """anim { "enemy.anm"; "st01enm.anm"; }
ecli { "helper.ecl"; }
void Helper(var A);

void main()
{
    @Helper(1);
    return;
}
""",
            encoding="utf-8",
        )
        helper = package / "helper.decl"
        helper.write_text(
            """void Helper()
{
    var A;
    if ($A) goto Bound @ 0;
    ins_319(0, 0.0f);
Bound:
    return;
}
""",
            encoding="utf-8",
        )

        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_file(
                root,
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "anm.slot_unbound"))
        self.assertFalse(report.has_errors, report.to_dict())

    def test_spawn_starts_with_fresh_slot_state(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    ins_306(0, 40);
    ins_300("Child", 0.0f, 0.0f, 10, 0, 0);
    return;
}

void Child()
{
    ins_319(0, 0.0f);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.slot_unbound")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].routine, "Child")

    def test_set_without_selected_or_default_bank_is_an_error(self) -> None:
        report = self.check(
            """
void main()
{
    ins_306(0, 40);
    return;
}
""",
            source_name="th15/default.decl",
            reference=False,
        )

        self.assertTrue(self.with_code(report, "anm.bank_unselected"))
        self.assertTrue(report.has_errors)

    def test_slot_consumer_before_set_is_an_error(self) -> None:
        report = self.check(
            """
void main()
{
    ins_319(3, 0.5f);
    return;
}
"""
        )

        diagnostics = self.with_code(report, "anm.slot_unbound")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("slot"), 3)

    def test_individually_valid_actions_do_not_authorize_a_new_combination(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
            combination(2, action("anm.set_sprite", 1, 93)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    ins_306(0, 40);
    ins_303(1, 93);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.combination_not_in_target_package")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(len(diagnostics[0].details.get("actions", [])), 2)

    def test_explicit_play_does_not_change_selected_bank(self) -> None:
        candidates = pool_with(
            combination(1, action("anm.play", None, 10), role="common"),
            combination(2, action("anm.selected_play", None, 20)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    ins_307(1, 10);
    ins_313(20);
    return;
}
""",
            pool=candidates,
        )

        self.assertFalse(report.has_errors, report.to_dict())
        self.assertFalse(self.with_code(report, "anm.selected_play_without_bank"))
        self.assertFalse(self.with_code(report, "anm.play_not_in_target_package"))

    def test_routine_play_evidence_does_not_bypass_unit_role(self) -> None:
        candidate = combination(
            3,
            action("anm.play", None, 10),
            role="boss",
        )
        candidates = AnmCandidatePool(
            game=GAME,
            stage_id="01",
            resources={"anim": EXPECTED_ANIM},
            combinations=(candidate,),
            routine_plays=(
                AnmRoutinePlayCandidate("anm.play", 3, 10, "Boss", 0, "st01bs.decl:Boss"),
            ),
        )
        report = self.check(
            """
void main()
{
    ins_307(3, 10);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.play_wrong_unit_role")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("candidate_roles"), ["boss"])

    def test_unknown_death_anm_bank_and_script_are_reported(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        report = self.check(
            """
void main()
{
    ins_323(999, 999);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.death_resource_unproven")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("bank"), 999)
        self.assertEqual(diagnostics[0].details.get("script"), 999)

    def test_dynamic_anm_operands_are_warnings_not_errors(self) -> None:
        report = self.check(
            """
void main()
{
    var A;
    ins_302($A);
    ins_306(0, $A);
    return;
}
"""
        )

        diagnostics = self.with_code(report, "anm.dynamic_operand_unproven")
        self.assertTrue(diagnostics)
        self.assertTrue(all(item.severity == "warning" for item in diagnostics))
        self.assertFalse(report.has_errors, report.to_dict())

    def test_async_anm_mutation_reports_state_race_warning(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    @Worker() async;
    return;
}

void Worker()
{
    ins_306(0, 40);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.async_state_race")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, "warning")
        self.assertFalse(report.has_errors, report.to_dict())

    def test_anim_manifest_must_match_reference_package(self) -> None:
        target = """
anim { "wrong.anm"; }

void main()
{
    return;
}
"""
        candidates = pool_with()
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "resource.anim_manifest_mismatch")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(tuple(diagnostics[0].details.get("expected", ())), EXPECTED_ANIM)
        self.assertEqual(diagnostics[0].details.get("actual"), ["wrong.anm"])
        serialized = report.to_dict()
        self.assertEqual(serialized["errors"], len(report.errors))
        self.assertEqual(serialized["warnings"], len(report.warnings))
        self.assertIsInstance(serialized["diagnostics"], list)

    def test_embedded_unsupported_lowering_comment_is_an_error(self) -> None:
        target = """
// source: th14/st01.decl
// source game: th14
// target: th15
// [backend.lossy_forbidden] node=main:12:0 strategy=unsupported: lossy lowering was rejected
anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    return;
}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "backend.lossy_forbidden")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, "error")
        self.assertEqual(diagnostics[0].details.get("origin"), "lowering_comment")
        self.assertEqual(diagnostics[0].details.get("strategy"), "unsupported")
        self.assertTrue(report.has_errors)

    def test_generated_legacy_lowering_comments_are_errors(self) -> None:
        target = """
// source: th14/st01.decl
// source game: th14
// target: th15
anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    // unlifted instruction: ins_1();
    // no safe lowering implemented for Movement family=th10 to th15
    // unsupported transform from ins_509: 0, 1
    // old target drops call: @Child();
    // raw: opaque source statement
    return;
}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        codes = {
            "legacy.unlifted_instruction",
            "legacy.no_safe_lowering",
            "legacy.unsupported_transform",
            "legacy.dropped_syntax",
            "legacy.raw_omission",
        }
        diagnostics = [item for item in report.diagnostics if item.code in codes]
        self.assertEqual({item.code for item in diagnostics}, codes)
        self.assertTrue(all(item.severity == "error" for item in diagnostics))
        self.assertTrue(
            all(
                item.details.get("origin") == "legacy_lowering_comment"
                for item in diagnostics
            )
        )

    def test_plain_source_comments_are_not_legacy_lowering_diagnostics(self) -> None:
        report = self.check(
            """
void main()
{
    // raw: documentation for a hand-written source statement
    // unsupported transformation is discussed here
    return;
}
"""
        )

        self.assertFalse(
            any(item.code.startswith("legacy.") for item in report.diagnostics)
        )

    def test_anm_color_and_alpha_literals_stay_in_byte_range(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    ins_306(0, 40);
    ins_325(0, 256, 0, -1);
    ins_326(0, 60, 0, 256, 0, 0);
    ins_327(0, 300);
    ins_328(0, 60, 0, -1);
    ins_332(0, 60, 0, 300);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(
            report,
            "instruction.parameter_value_out_of_range",
        )
        self.assertEqual(len(diagnostics), 6)
        self.assertEqual(
            {(item.details.get("operation"), item.details.get("value")) for item in diagnostics},
            {
                ("anm.color", 256),
                ("anm.color", -1),
                ("anm.color_time", 256),
                ("anm.alpha", 300),
                ("anm.alpha_time", -1),
                ("anm.alpha2_time", 300),
            },
        )
        self.assertTrue(all(item.details.get("min") == 0 for item in diagnostics))
        self.assertTrue(all(item.details.get("max") == 255 for item in diagnostics))

    def test_generated_target_errors_when_source_and_target_anm_traces_differ(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source = source_directory / "st01.decl"
        source.write_text(
            """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    ins_302(2);
    ins_306(0, 40);
    return;
}
""",
            encoding="utf-8",
        )
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
            combination(2, action("anm.set_main", 0, 35)),
        )
        target = f"""
// source: {source}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}

void main()
{{
    ins_302(2);
    ins_306(0, 35);
    return;
}}
"""
        with (
            patch(
                "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
                return_value=candidates,
            ),
            patch(
                "ecl_ir.analysis.anm_resources.candidate_pool_for_stage",
                return_value=candidates,
            ),
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "anm.source_target_trace_mismatch")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, "error")
        self.assertEqual(diagnostics[0].details.get("source_game"), "th14")
        self.assertEqual(diagnostics[0].details.get("target_game"), "th15")
        self.assertNotEqual(
            diagnostics[0].details.get("expected"),
            diagnostics[0].details.get("actual"),
        )

    def test_spawned_boss_uses_the_routine_role_default_bank(self) -> None:
        candidates = AnmCandidatePool(
            game="th10",
            stage_id="01",
            resources={"anim": EXPECTED_ANIM},
            combinations=(
                combination(
                    2,
                    action("anm.selected_play", None, 0),
                    role="boss",
                ),
            ),
        )
        target = """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    ins_256("Boss", 0.0f, 0.0f, 10, 0, 0);
    return;
}

void Boss()
{
    ins_269(0);
    return;
}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th10/stage01.decl",
                game="th10",
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "anm.play_not_in_target_package"))
        self.assertFalse(self.with_code(report, "anm.play_wrong_unit_role"))

    def test_spawned_unit_without_setup_is_reported_as_unproven(self) -> None:
        report = self.check(
            """
void main()
{
    ins_300("Child", 0.0f, 0.0f, 10, 0, 0);
    return;
}

void Child()
{
    ins_23(1);
    return;
}
"""
        )

        diagnostics = self.with_code(report, "anm.unit_without_setup")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, "warning")
        self.assertIsNone(diagnostics[0].details.get("source_expected_setup"))

    def test_flow_ret_checks_spawned_unit_anm_setup(self) -> None:
        report = self.check(
            """
void main()
{
    ins_300("Child", 0.0f, 0.0f, 10, 0, 0);
    return;
}

void Child()
{
    ins_10();
}
"""
        )

        diagnostics = self.with_code(report, "anm.unit_without_setup")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].routine, "Child")

    def test_unreachable_source_setup_does_not_make_missing_target_setup_an_error(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source = source_directory / "st01.decl"
        source.write_text(
            """void main()
{
    ins_300("Child", 0.0f, 0.0f, 10, 0, 0);
    return;
}

void Child()
{
    goto Done @ 0;
    ins_302(2);
    ins_306(0, 40);
Done:
    return;
}
""",
            encoding="utf-8",
        )
        target = f"""// source: {source}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}

void main()
{{
    ins_300("Child", 0.0f, 0.0f, 10, 0, 0);
    return;
}}

void Child()
{{
    ins_23(1);
    return;
}}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "anm.unit_without_setup"))

    def test_unknown_numeric_variable_and_read_only_write_are_errors(self) -> None:
        report = self.check(
            """
void main()
{
    ins_23([-10001]);
    [-9991.0f] = 1.0f;
    return;
}
"""
        )

        unsupported = self.with_code(report, "variable.numeric_reference_unsupported")
        access = self.with_code(report, "variable.access_violation")
        self.assertEqual(len(unsupported), 1)
        self.assertEqual(unsupported[0].details.get("numeric_id"), -10001)
        self.assertEqual(len(access), 1)
        self.assertEqual(access[0].details.get("semantic_id"), "player.position.x")
        self.assertEqual(access[0].details.get("use_kind"), "write")

    def test_relative_stack_reference_requires_a_materialized_value(self) -> None:
        invalid = self.check(
            """
void main()
{
    ins_23([-1]);
    return;
}
"""
        )
        valid = self.check(
            """
void main()
{
!E
    10;
!N
    20;
!H
    30;
!L
    40;
!*
    ins_23([-1]);
    return;
}
""",
            difficulties=("E", "N", "H", "L"),
        )

        diagnostics = self.with_code(invalid, "stack.relative_reference_unbound")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("offset"), -1)
        self.assertFalse(self.with_code(valid, "stack.relative_reference_unbound"))

    def test_th12_selected_evaluation_slots_are_node_local_read_consumers(self) -> None:
        def check_th12(body: str, difficulties: tuple[str, ...] = ("E",)):
            with patch(
                "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
                return_value=pool_with(),
            ):
                return check_ecl_text(
                    body,
                    source_name="th12/stage01.decl",
                    game="th12",
                    difficulties=difficulties,
                )

        valid = check_th12(
            """void main()
{
!E
    10;
!N
    20;
!H
    30;
!L
    40;
!E
    1.0f;
!N
    2.0f;
!H
    3.0f;
!L
    4.0f;
!*
    ins_504(0, [-1.0f], [-2.0f]);
    return;
}
""",
            ("E", "N", "H", "L"),
        )
        self.assertFalse(
            self.with_code(valid, "variable.numeric_reference_unsupported")
        )
        self.assertFalse(self.with_code(valid, "stack.relative_reference_unbound"))

        no_selection = check_th12(
            """void main()
{
    ins_83([-1]);
    return;
}
"""
        )
        unsupported = self.with_code(
            no_selection,
            "variable.numeric_reference_unsupported",
        )
        self.assertEqual(len(unsupported), 1)
        self.assertEqual(unsupported[0].details.get("numeric_id"), -1)

        write_consumer = check_th12(
            """void main()
{
!E
    1;
!*
    [-1] = 5;
    return;
}
"""
        )
        unsupported = self.with_code(
            write_consumer,
            "variable.numeric_reference_unsupported",
        )
        self.assertEqual(len(unsupported), 1)
        self.assertEqual(unsupported[0].details.get("use_kind"), "write")

        selected_case_variable = check_th12(
            """void main()
{
!E
    [-10001];
!*
    ins_83([-1]);
    return;
}
"""
        )
        unsupported = self.with_code(
            selected_case_variable,
            "variable.numeric_reference_unsupported",
        )
        self.assertEqual(len(unsupported), 1)
        self.assertEqual(unsupported[0].details.get("numeric_id"), -10001)

        partial_lanes = check_th12(
            """void main()
{
!E
    10;
!N
    20;
!*
    ins_83([-1]);
    return;
}
""",
            ("E", "N", "H", "L"),
        )
        unbound = self.with_code(partial_lanes, "stack.relative_reference_unbound")
        self.assertEqual([item.difficulty for item in unbound], ["H", "L"])
        self.assertFalse(
            self.with_code(partial_lanes, "variable.numeric_reference_unsupported")
        )

    def test_candidate_combination_must_match_the_unit_role(self) -> None:
        candidates = pool_with(
            combination(
                2,
                action("anm.set_main", 0, 40),
                role="boss",
            ),
        )
        report = self.check(
            """
void main()
{
    ins_302(2);
    ins_306(0, 40);
    return;
}
""",
            pool=candidates,
        )

        diagnostics = self.with_code(report, "anm.combination_wrong_unit_role")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("unit_role"), "stage")
        self.assertEqual(diagnostics[0].details.get("candidate_roles"), ["boss"])

    def test_all_routines_starts_non_entry_routines_with_unknown_anm_state(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        target = """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    return;
}

void Helper()
{
    ins_306(0, 40);
    return;
}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
                all_routines=True,
            )

        self.assertFalse(self.with_code(report, "anm.bank_unselected"))
        self.assertTrue(self.with_code(report, "anm.dynamic_operand_unproven"))

    def test_all_routines_does_not_reaudit_routines_reached_from_entry(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        target = """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    ins_302(2);
    @Helper();
    return;
}

void Helper()
{
    ins_306(0, 40);
    return;
}
"""

        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
                all_routines=True,
            )

        self.assertFalse(self.with_code(report, "anm.dynamic_operand_unproven"))
        self.assertFalse(report.has_errors, report.to_dict())

    def test_reference_package_does_not_supply_a_missing_target_sibling(self) -> None:
        reference_sibling = self.reference.with_name("st01bs.decl")
        reference_sibling.write_text(
            "void Boss()\n{\n    return;\n}\n",
            encoding="utf-8",
        )
        target_directory = self.root / "generated-missing-sibling"
        target_directory.mkdir()
        target = target_directory / "st01.decl"
        target.write_text(
            'anim { "enemy.anm"; "st01enm.anm"; }\n'
            'ecli { "st01bs.ecl"; }\n'
            "void main()\n{\n    return;\n}\n",
            encoding="utf-8",
        )

        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_file(
                target,
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "package.ecli_unresolved")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].details.get("entry"), "st01bs.ecl")
        self.assertNotIn(str(reference_sibling), report.modules)

    def test_explicit_reference_file_builds_the_candidate_pool(self) -> None:
        reference = self.root / "reference" / "st99.decl"
        reference.parent.mkdir()
        boss = reference.parent / "boss" / "st99bs.decl"
        boss.parent.mkdir()
        boss.write_text(
            """void Boss()
{
    ins_302(3);
    ins_306(0, 778);
    return;
}
""",
            encoding="utf-8",
        )
        reference.write_text(
            """anim { "custom-enemy.anm"; "custom-stage.anm"; }
ecli { "boss/st99bs.ecl"; }

void main()
{
    ins_302(2);
    ins_306(0, 777);
    return;
}
""",
            encoding="utf-8",
        )

        pool = candidate_pool_for_stage(GAME, "99", reference)

        self.assertEqual(
            pool.resources.get("anim"),
            ("custom-enemy.anm", "custom-stage.anm"),
        )
        self.assertTrue(
            any(
                candidate.bank == 2
                and candidate.actions == (action("anm.set_main", 0, 777),)
                for candidate in pool.combinations
            )
        )
        self.assertTrue(
            any(
                candidate.bank == 3
                and candidate.actions == (action("anm.set_main", 0, 778),)
                for candidate in pool.combinations
            )
        )

    def test_target_ecli_keeps_its_relative_subdirectory(self) -> None:
        target_directory = self.root / "generated-subdirectory"
        boss = target_directory / "boss" / "st01bs.decl"
        boss.parent.mkdir(parents=True)
        boss.write_text("void Boss()\n{\n    return;\n}\n", encoding="utf-8")
        target = target_directory / "st01.decl"
        target.write_text(
            'anim { "enemy.anm"; "st01enm.anm"; }\n'
            'ecli { "boss/st01bs.ecl"; }\n'
            "void main()\n{\n    return;\n}\n",
            encoding="utf-8",
        )

        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_file(
                target,
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "package.ecli_unresolved"))
        self.assertIn(str(boss), report.modules)

    def test_generated_source_header_sets_game_when_path_has_no_game_id(self) -> None:
        source = self.root / "original.decl"
        source.write_text(
            """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    ins_302(2);
    ins_306(0, 40);
    return;
}
""",
            encoding="utf-8",
        )
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        target = f"""// source: {source}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}

void main()
{{
    ins_302(2);
    ins_306(0, 40);
    return;
}}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "anm.source_action_unresolved"))
        self.assertFalse(self.with_code(report, "anm.source_target_trace_mismatch"))

    def test_default_and_shared_units_do_not_inherit_the_stage_anm_pool(self) -> None:
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        for module_stem in ("default", "shared"):
            with self.subTest(module=module_stem):
                case_root = self.root / f"trace-{module_stem}"
                source_directory = case_root / "th14"
                target_directory = case_root / "generated"
                source_directory.mkdir(parents=True)
                target_directory.mkdir()

                source_member = source_directory / f"{module_stem}.decl"
                source_member.write_text(
                    """void Effect()
{
    ins_302(2);
    ins_306(0, 40);
    return;
}
""",
                    encoding="utf-8",
                )
                source_root = source_directory / "st01.decl"
                source_root.write_text(
                    f"""ecli {{ "{module_stem}.ecl"; }}
void main()
{{
    return;
}}
""",
                    encoding="utf-8",
                )

                target_member = target_directory / f"{module_stem}.decl"
                target_member.write_text(
                    f"""// source: {source_member}
// source game: th14
// target: th15
void Effect()
{{
    return;
}}
""",
                    encoding="utf-8",
                )
                target_root = target_directory / "st01.decl"
                target_root.write_text(
                    f"""// source: {source_root}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}
ecli {{ "{module_stem}.ecl"; }}
void main()
{{
    return;
}}
""",
                    encoding="utf-8",
                )

                with patch(
                    "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
                    return_value=candidates,
                ):
                    report = check_ecl_file(
                        target_root,
                        game=GAME,
                        reference_package=self.reference,
                        difficulties=("E",),
                    )

                unresolved = self.with_code(report, "anm.source_action_unresolved")
                self.assertTrue(unresolved)
                self.assertTrue(
                    all(Path(item.module) == target_member for item in unresolved)
                )
                self.assertFalse(
                    self.with_code(report, "anm.source_target_trace_mismatch")
                )

    def test_source_target_trace_ignores_unreachable_anm_actions(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source = source_directory / "st01.decl"
        source.write_text(
            """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    goto Done @ 0;
    ins_302(2);
    ins_306(0, 40);
Done:
    return;
}
""",
            encoding="utf-8",
        )
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
        )
        target = f"""// source: {source}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}

void main()
{{
    return;
}}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        self.assertFalse(self.with_code(report, "anm.source_action_unresolved"))
        self.assertFalse(self.with_code(report, "anm.source_target_trace_mismatch"))

    def test_source_target_trace_keeps_mutually_exclusive_paths_separate(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source = source_directory / "st01.decl"
        source.write_text(
            """anim { "enemy.anm"; "st01enm.anm"; }

void main()
{
    if ([-9959] == 0) goto BranchB @ 0;
    ins_302(2);
    ins_306(0, 40);
    goto End @ 0;
BranchB:
    ins_302(2);
    ins_306(0, 50);
End:
    return;
}
""",
            encoding="utf-8",
        )
        candidates = pool_with(
            combination(2, action("anm.set_main", 0, 40)),
            combination(2, action("anm.set_main", 0, 50)),
        )
        target = f"""// source: {source}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}

void main()
{{
    if ([-9959] == 0) goto BranchB @ 0;
    ins_302(2);
    ins_306(0, 40);
BranchB:
    ins_302(2);
    ins_306(0, 50);
End:
    return;
}}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=candidates,
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "anm.source_target_trace_mismatch")
        self.assertEqual(len(diagnostics), 1)
        self.assertNotEqual(
            diagnostics[0].details.get("expected"),
            diagnostics[0].details.get("actual"),
        )

    def test_source_target_check_detects_a_removed_call_edge(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source = source_directory / "st01.decl"
        source.write_text(
            """void main()
{
    @Child();
    return;
}

void Child()
{
    return;
}
""",
            encoding="utf-8",
        )
        target = f"""// source: {source}
// source game: th14
// target: th15

void main()
{{
    return;
}}

void Child()
{{
    return;
}}
"""
        with patch(
            "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
            return_value=pool_with(),
        ):
            report = check_ecl_text(
                target,
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(
            report,
            "control_flow.source_target_edge_mismatch",
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].routine, "main")

    def test_generated_source_resolver_handles_workspace_and_windows_prefixes(self) -> None:
        expected = REPO_ROOT / "th14" / "st01.decl"
        self.assertEqual(
            _resolve_generated_source("th062/th14/st01.decl", None).resolve(),
            expected.resolve(),
        )
        self.assertEqual(
            _resolve_generated_source(r"E:\fork\th062\th14\st01.decl", None).resolve(),
            expected.resolve(),
        )

    def test_missing_reference_package_is_a_configuration_error(self) -> None:
        with self.assertRaises(ValueError):
            check_ecl_text(
                "void main()\n{\n    return;\n}\n",
                source_name="th15/st01.decl",
                game=GAME,
                reference_package=self.root / "missing.decl",
                difficulties=("E",),
            )

    def test_each_generated_ecli_member_gets_its_own_source_trace_check(self) -> None:
        source_directory = self.root / "th14"
        source_directory.mkdir()
        source_root = source_directory / "st01.decl"
        source_root.write_text(
            'anim { "enemy.anm"; "st01enm.anm"; }\nvoid main()\n{\n    return;\n}\n',
            encoding="utf-8",
        )
        source_boss = source_directory / "st01bs.decl"
        source_boss.write_text(
            """void Boss()
{
    ins_302(3);
    ins_306(0, 40);
    return;
}
""",
            encoding="utf-8",
        )

        target_directory = self.root / "generated"
        target_directory.mkdir()
        target_root = target_directory / "st01.decl"
        target_root.write_text(
            f"""// source: {source_root}
// source game: th14
// target: th15
anim {{ "enemy.anm"; "st01enm.anm"; }}
ecli {{ "st01bs.ecl"; }}
void main()
{{
    return;
}}
""",
            encoding="utf-8",
        )
        target_boss = target_directory / "st01bs.decl"
        target_boss.write_text(
            f"""// source: {source_boss}
// source game: th14
// target: th15
void Boss()
{{
    ins_302(3);
    ins_306(0, 35);
    return;
}}
""",
            encoding="utf-8",
        )
        candidates = pool_with(
            combination(3, action("anm.set_main", 0, 40), role="boss"),
            combination(3, action("anm.set_main", 0, 35), role="boss"),
        )
        with (
            patch(
                "ecl_ir.analysis.execution_check.candidate_pool_for_stage",
                return_value=candidates,
            ),
            patch(
                "ecl_ir.analysis.anm_resources.candidate_pool_for_stage",
                return_value=candidates,
            ),
        ):
            report = check_ecl_file(
                target_root,
                game=GAME,
                reference_package=self.reference,
                difficulties=("E",),
            )

        diagnostics = self.with_code(report, "anm.source_target_trace_mismatch")
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(Path(diagnostics[0].module), target_boss)
        self.assertEqual(diagnostics[0].routine, "Boss")


if __name__ == "__main__":
    unittest.main()
