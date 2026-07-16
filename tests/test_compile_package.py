from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from ecl_ir.cli import main as cli_main


class CompilePackageTests(unittest.TestCase):
    def write_decl(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_reference(
        self,
        root: Path,
        name: str = "st01.decl",
        game: str = "th15",
    ) -> Path:
        reference = root / "reference" / game / name
        self.write_decl(
            reference,
            """anim { "target_enemy.anm"; "target_stage.anm"; }
void main()
{
    ins_0();
}
""",
        )
        return reference

    def make_source_package(self, root: Path) -> Path:
        package = root / "source" / "th10"
        source_root = package / "stage01.decl"
        self.write_decl(
            source_root,
            """anim { "source_enemy.anm"; "source_stage.anm"; }
ecli { "default.ecl"; "boss/st01bs.ecl"; }
void main()
{
    ins_9999();
}
""",
        )
        self.write_decl(
            package / "default.decl",
            """ecli { "shared.ecl"; }
void DefaultHelper()
{
    ins_0();
}
""",
        )
        self.write_decl(
            package / "boss" / "st01bs.decl",
            """ecli { "../shared.ecl"; }
void BossHelper()
{
    ins_0();
}
""",
        )
        self.write_decl(
            package / "shared.decl",
            """ecli { "default.ecl"; }
void SharedHelper()
{
    ins_0();
}
""",
        )
        return source_root

    def compile_package(
        self,
        source: Path,
        reference: Path,
        output: Path,
        *policy_args: str,
    ) -> int:
        return cli_main(
            [
                "compile-package",
                str(source),
                "--target",
                "th15",
                "--reference-package",
                str(reference),
                "--output-dir",
                str(output),
                *policy_args,
            ]
        )

    def test_recursive_package_compile_renames_root_and_preserves_siblings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = self.make_source_package(root)
            reference = self.make_reference(root)

            strict_output = root / "strict"
            strict_result = self.compile_package(source, reference, strict_output)

            self.assertEqual(strict_result, 1)
            expected = {
                Path("st01.decl"),
                Path("default.decl"),
                Path("shared.decl"),
                Path("boss/st01bs.decl"),
            }
            self.assertEqual(
                {path.relative_to(strict_output) for path in strict_output.rglob("*.decl")},
                expected,
            )
            self.assertFalse((strict_output / "stage01.decl").exists())
            for relative in expected:
                rendered = (strict_output / relative).read_text(encoding="utf-8")
                self.assertIn("// canonical lowering plan:", rendered)
            self.assertIn(
                "unsupported=1",
                (strict_output / "st01.decl").read_text(encoding="utf-8"),
            )

            permissive_output = root / "permissive"
            permissive_result = self.compile_package(
                source,
                reference,
                permissive_output,
                "--allow-lossy",
                "--preserve-raw-same-family",
                "--preserve-raw-cross-family",
            )

            self.assertEqual(permissive_result, 0)
            root_text = (permissive_output / "st01.decl").read_text(encoding="utf-8")
            self.assertIn('anim { "target_enemy.anm"; "target_stage.anm"; }', root_text)
            self.assertIn('ecli { "default.ecl"; "boss/st01bs.ecl"; }', root_text)
            self.assertIn("ins_9999();", root_text)
            self.assertIn("raw=1", root_text)

    def test_missing_recursive_source_dependency_returns_two_without_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source" / "th10" / "stage01.decl"
            self.write_decl(
                source,
                """ecli { "missing/st01bs.ecl"; }
void main()
{
    ins_0();
}
""",
            )
            reference = self.make_reference(root)
            output = root / "output"
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                result = self.compile_package(source, reference, output)

            self.assertEqual(result, 2)
            self.assertIn("does not exist", stderr.getvalue())
            self.assertFalse(output.exists())

    def test_mismatched_reference_stage_is_a_configuration_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source" / "th10" / "stage01.decl"
            self.write_decl(source, "void main()\n{\n    ins_0();\n}\n")
            reference = self.make_reference(root, "st02.decl")
            output = root / "output"

            with contextlib.redirect_stderr(io.StringIO()):
                result = self.compile_package(source, reference, output)

            self.assertEqual(result, 2)
            self.assertFalse(output.exists())

    def test_mismatched_reference_game_is_a_configuration_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source" / "th10" / "stage01.decl"
            self.write_decl(source, "void main()\n{\n    ins_0();\n}\n")
            reference = self.make_reference(root, game="th14")
            output = root / "output"

            with contextlib.redirect_stderr(io.StringIO()):
                result = self.compile_package(source, reference, output)

            self.assertEqual(result, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
