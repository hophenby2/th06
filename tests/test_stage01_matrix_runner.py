from __future__ import annotations

import importlib.util
import unittest
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

    def test_empty_wine_log_is_clean(self) -> None:
        self.assertEqual(RUNNER.scan_log_failures("\n"), [])


if __name__ == "__main__":
    unittest.main()
