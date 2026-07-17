from __future__ import annotations

import importlib.util
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ecl_ir" / "run_stage01_matrix.py"
SPEC = importlib.util.spec_from_file_location("run_stage01_matrix", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class Stage01MatrixRunnerTests(unittest.TestCase):
    def test_default_matrix_has_all_72_ordered_directions(self) -> None:
        pairs = RUNNER.selected_pairs([])
        self.assertEqual(len(pairs), 72)
        self.assertNotIn(("th10", "th10"), pairs)
        self.assertIn(("th10", "th18"), pairs)
        self.assertIn(("th18", "th10"), pairs)

    def test_explicit_pairs_keep_order_and_remove_duplicates(self) -> None:
        pairs = RUNNER.selected_pairs(
            [("th15", "th12"), ("th10", "th11"), ("th15", "th12")]
        )
        self.assertEqual(pairs, [("th15", "th12"), ("th10", "th11")])

    def test_stage_entries_never_resolve_to_default(self) -> None:
        self.assertEqual(RUNNER.entry_path(ROOT, "th10").name, "stage01.decl")
        self.assertEqual(RUNNER.entry_path(ROOT, "th18").name, "st01.decl")

    def test_thecl_diagnostic_and_argument_warning_are_failures(self) -> None:
        failures = RUNNER.scan_log_failures(
            "thecl.exe:th10_instr_serialize: too few arguments for opcode 408\n"
        )
        self.assertEqual(len(failures), 1)
        self.assertIn("thecl_diagnostic", failures[0]["categories"])
        self.assertIn("too_few_arguments", failures[0]["categories"])

    def test_python_traceback_is_an_execution_failure_signal(self) -> None:
        failures = RUNNER.scan_log_failures(
            "Traceback (most recent call last):\n"
            "  File \"runner.py\", line 1, in <module>\n"
            "RuntimeError: exploded\n"
        )
        categories = {category for item in failures for category in item["categories"].split(",")}
        self.assertIn("python_traceback", categories)
        self.assertIn("python_exception", categories)

    def test_empty_wine_log_is_clean(self) -> None:
        self.assertEqual(RUNNER.scan_log_failures("\n"), [])

    def test_release12_signature_validation_notice_is_not_a_source_failure(self) -> None:
        failures = RUNNER.scan_log_failures(
            "thecl.exe:compat.eclm:7: warning: signature validation is not yet implemented\n"
        )
        self.assertEqual(failures, [])

    def test_th18_wine_command_uses_the_release12_signature_override(self) -> None:
        command = RUNNER.wine_compile_command(
            "wine",
            Path("thecl.exe"),
            "th18",
            Path("input.decl"),
            Path("output.ecl"),
        )
        self.assertIn("-m", command)
        self.assertIn(
            str(RUNNER.TOOLCHAIN_MAPS["th18"]),
            command,
        )

        th17_command = RUNNER.wine_compile_command(
            "wine",
            Path("thecl.exe"),
            "th17",
            Path("input.decl"),
            Path("output.ecl"),
        )
        self.assertNotIn("-m", th17_command)

    def test_checker_code_counts_keep_severity(self) -> None:
        counts = RUNNER.checker_code_counts(
            {
                "diagnostics": [
                    {"severity": "error", "code": "anm.unit_without_setup"},
                    {"severity": "warning", "code": "anm.unit_without_setup"},
                    {"severity": "error", "code": "variable.target_unavailable"},
                ]
            }
        )
        self.assertEqual(
            counts,
            {
                "error:anm.unit_without_setup": 1,
                "error:variable.target_unavailable": 1,
                "warning:anm.unit_without_setup": 1,
            },
        )

    def test_checker_report_validation_rejects_corrupt_diagnostics(self) -> None:
        report = {
            "schema": "th062.ecl-execution-check",
            "schema_version": 1,
            "game": "th12",
            "entry": "main",
            "difficulties": ["E", "N", "H", "L"],
            "diagnostics": [],
            "errors": 0,
            "warnings": 0,
            "states_explored": 12,
            "analysis_complete": True,
            "summary": {
                "diagnostics": 0,
                "errors": 0,
                "warnings": 0,
                "states_explored": 12,
                "analysis_complete": True,
            },
        }
        RUNNER.validate_checker_report(report, "th12")

        report["diagnostics"] = "not-a-list"
        with self.assertRaisesRegex(ValueError, "diagnostics is not a list"):
            RUNNER.validate_checker_report(report, "th12")

    def test_checker_report_allows_zero_states_for_missing_entry(self) -> None:
        diagnostic = {"severity": "error", "code": "execution.entry_not_found"}
        report = {
            "schema": "th062.ecl-execution-check",
            "schema_version": 1,
            "game": "th12",
            "entry": "main",
            "difficulties": ["E", "N", "H", "L"],
            "diagnostics": [diagnostic],
            "errors": 1,
            "warnings": 0,
            "states_explored": 0,
            "analysis_complete": True,
            "summary": {
                "diagnostics": 1,
                "errors": 1,
                "warnings": 0,
                "states_explored": 0,
                "analysis_complete": True,
            },
        }
        RUNNER.validate_checker_report(report, "th12")

    def test_process_registry_terminates_an_active_command(self) -> None:
        registry = RUNNER.ProcessRegistry()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                RUNNER.run_command,
                [sys.executable, "-c", "import time; time.sleep(30)"],
                cwd=ROOT,
                timeout_seconds=60,
                process_registry=registry,
            )
            self.assertTrue(registry.wait_for_active(5.0))
            registry.cancel_all()
            result = future.result(timeout=5.0)

        self.assertTrue(result["cancelled"])
        self.assertEqual(result["return_code"], 130)

    def test_jobs_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "jobs must be greater than zero"):
            RUNNER.validate_positive(0, "jobs")
        with self.assertRaisesRegex(ValueError, "wine jobs must be greater than zero"):
            RUNNER.validate_positive(0, "wine jobs")


if __name__ == "__main__":
    unittest.main()
