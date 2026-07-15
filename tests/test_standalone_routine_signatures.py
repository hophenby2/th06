from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from ecl_ir.cli import main as cli_main
from ecl_ir.artifact.ir_file import build_eclir, dump_eclir, load_eclir
from ecl_ir.source.parser import parse_decl


class StandaloneRoutineSignatureTests(unittest.TestCase):
    def compile_ir(self, ir_path: Path, output_path: Path) -> str:
        result = cli_main([
            "compile-ir",
            str(ir_path),
            "--target",
            "th15",
            "--output",
            str(output_path),
        ])
        self.assertEqual(result, 0)
        return output_path.read_text()

    def test_compile_ir_uses_only_serialized_routine_signatures(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game_dir = Path(temp_dir) / "th14"
            game_dir.mkdir()
            source_path = game_dir / "default.decl"
            sibling_path = game_dir / "stage01.decl"
            source_path.write_text("void Helper()\n{\n    var A, B, C;\n    return;\n}\n")
            sibling_path.write_text("void Helper(var A, var B);\n")

            direct_program = parse_decl(source_path)
            self.assertEqual(
                [(signature.name, signature.params) for signature in direct_program.routine_signatures],
                [("Helper", "var A, var B")],
            )

            data = build_eclir(source_path)
            self.assertEqual(data["program"]["routine_signatures"][0]["params"], "var A, var B")
            self.assertEqual(data["canonical_ir"]["routine_signatures"][0]["params"], "var A, var B")
            ir_path = Path(temp_dir) / "default.eclir.json"
            dump_eclir(ir_path, data)

            baseline = self.compile_ir(ir_path, Path(temp_dir) / "baseline.decl")
            self.assertIn("void Helper(var A, var B)", baseline)
            self.assertIn("var C;", baseline)
            self.assertNotIn("var A, B, C;", baseline)

            sibling_path.write_text("void Helper(var X, var Y, var Z);\n")
            after_sibling_change = self.compile_ir(ir_path, Path(temp_dir) / "changed.decl")
            self.assertEqual(after_sibling_change, baseline)

            source_path.unlink()
            sibling_path.unlink()
            after_source_removal = self.compile_ir(ir_path, Path(temp_dir) / "removed.decl")
            self.assertEqual(after_source_removal, baseline)

            loaded_program, _objects, _loaded_data = load_eclir(ir_path)
            self.assertEqual(loaded_program.routine_signatures[0].params, "var A, var B")

            canonical_only_data = copy.deepcopy(data)
            canonical_only_data["program"].pop("routine_signatures", None)
            canonical_only_ir_path = Path(temp_dir) / "canonical-only.eclir.json"
            dump_eclir(canonical_only_ir_path, canonical_only_data)
            canonical_only_output = self.compile_ir(
                canonical_only_ir_path,
                Path(temp_dir) / "canonical-only.decl",
            )
            self.assertEqual(canonical_only_output, baseline)

            legacy_data = copy.deepcopy(data)
            legacy_data["schema_version"] = 1
            legacy_data["program"].pop("routine_signatures", None)
            legacy_data.pop("canonical_ir", None)
            legacy_data.pop("canonical_summary", None)
            legacy_data.pop("analysis_projections", None)
            legacy_data.pop("analysis_summary", None)
            legacy_ir_path = Path(temp_dir) / "legacy.eclir.json"
            dump_eclir(legacy_ir_path, legacy_data)

            legacy_output = self.compile_ir(legacy_ir_path, Path(temp_dir) / "legacy.decl")
            self.assertIn("void Helper()", legacy_output)


if __name__ == "__main__":
    unittest.main()
