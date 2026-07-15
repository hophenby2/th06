from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ecl_ir.cli import main as cli_main
from ecl_ir.artifact.ir_file import (
    build_eclir,
    build_source_layout,
    dump_eclir,
    emit_layout_roundtrip_bytes,
    parse_decl_bytes as reparse_decl_bytes,
    parse_decl_text as reparse_decl_text,
    program_to_dict,
    validate_eclir_data,
)
from ecl_ir.source.parser import (
    BYTE_ESCAPE_BASE,
    BYTE_ESCAPE_SCOPE_ALL_NON_ASCII,
    SourceDecodeMode,
    SourceDocument,
    detect_text_encoding,
    encode_source_text,
    parse_decl,
    parse_decl_bytes,
    split_source_text_lines,
)


ROOT = Path(__file__).resolve().parents[1]
TH18_CP932_SOURCE = ROOT / "th18" / "st01bs.decl"
TH08_INVALID_CP932_SOURCE = ROOT / "th08" / "ecldata1sp.decl"
EXPECTED_SPELL_NAME = '"招符「弾幕万来」"'


def spell_name_args(program) -> list[str]:
    return [
        instruction.args[3]
        for function in program.functions
        for instruction in function.body
        if instruction.opcode == 537 and len(instruction.args) >= 4
    ]


class ParserEncodingTests(unittest.TestCase):
    def test_physical_line_split_preserves_in_string_control_bytes(self) -> None:
        text = 'ins_999("a\x1cb\x0cc\x0bd\re");\nnext();\r\n'
        self.assertEqual(
            split_source_text_lines(text),
            ['ins_999("a\x1cb\x0cc\x0bd\re");', "next();"],
        )
        self.assertEqual(
            split_source_text_lines(text, keepends=True),
            ['ins_999("a\x1cb\x0cc\x0bd\re");\n', "next();\r\n"],
        )

    def test_compile_ir_preserves_in_string_control_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            game_dir = Path(temp_dir) / "th08"
            game_dir.mkdir()
            source_path = game_dir / "control.decl"
            ir_path = Path(temp_dir) / "control.eclir.json"
            output_path = Path(temp_dir) / "control.out.decl"
            operand = b'"a\x1cb\x0cc\x0bd\re"'
            source_path.write_bytes(
                b"void Main()\n{\n    ins_999(" + operand + b");\n}\n"
            )
            dump_eclir(ir_path, build_eclir(source_path))

            result = cli_main([
                "compile-ir",
                str(ir_path),
                "--target",
                "th08",
                "--output",
                str(output_path),
            ])

            self.assertEqual(result, 0)
            self.assertIn(operand, output_path.read_bytes())

    def test_cp932_path_bytes_and_text_share_the_same_structure(self) -> None:
        source_bytes = TH18_CP932_SOURCE.read_bytes()
        source_name = str(TH18_CP932_SOURCE)

        self.assertEqual(detect_text_encoding(source_bytes), "cp932")
        from_path = parse_decl(TH18_CP932_SOURCE)
        from_bytes = reparse_decl_bytes(source_bytes, source_name)
        from_text = reparse_decl_text(source_bytes.decode("cp932"), source_name)

        expected_structure = program_to_dict(from_path)
        self.assertEqual(program_to_dict(from_bytes), expected_structure)
        self.assertEqual(program_to_dict(from_text), expected_structure)
        self.assertEqual(from_path.game, "th18")
        self.assertIn(EXPECTED_SPELL_NAME, spell_name_args(from_path))
        self.assertFalse(any("\ufffd" in name for name in spell_name_args(from_path)))

    def test_cp932_eclir_layout_and_program_roundtrip(self) -> None:
        source_bytes = TH18_CP932_SOURCE.read_bytes()
        data = build_eclir(TH18_CP932_SOURCE)

        self.assertEqual(data["source_encoding"], "cp932")
        self.assertEqual(data["source_decoding"]["decoding_mode"], SourceDecodeMode.STRICT.value)
        roundtrip_bytes = emit_layout_roundtrip_bytes(data)
        self.assertEqual(roundtrip_bytes, source_bytes)

        reparsed = parse_decl_bytes(roundtrip_bytes, TH18_CP932_SOURCE)
        self.assertEqual(program_to_dict(reparsed), data["program"])
        self.assertIn(EXPECTED_SPELL_NAME, spell_name_args(reparsed))

        canonical_spell_names = [
            operand["value"]["source_text"]
            for routine in data["canonical_ir"]["routines"]
            for node in routine["body"]
            if node.get("provenance", {}).get("opcode") == 537
            for operand in node.get("operands", [])
            if operand["value"]["source_text"].startswith('"')
        ]
        self.assertIn(EXPECTED_SPELL_NAME, canonical_spell_names)
        self.assertTrue(validate_eclir_data(data)["ok"])

        text_only_data = dict(data)
        text_only_data.pop("source_bytes_base64")
        text_only_result = validate_eclir_data(text_only_data)
        self.assertTrue(text_only_result["ok"])
        self.assertEqual(text_only_result["source_sha256_actual"], data["source_sha256"])

    def test_compile_ir_preserves_standalone_source_encoding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ir_path = Path(temp_dir) / "source.eclir.json"
            output_path = Path(temp_dir) / "source.decl"
            data = build_eclir(TH18_CP932_SOURCE)
            dump_eclir(ir_path, data)

            result = cli_main([
                "compile-ir",
                str(ir_path),
                "--target",
                "th18",
                "--output",
                str(output_path),
            ])

            self.assertEqual(result, 0)
            output_bytes = output_path.read_bytes()
            self.assertIn(EXPECTED_SPELL_NAME, output_bytes.decode("cp932"))
            self.assertNotIn(EXPECTED_SPELL_NAME.encode("utf-8"), output_bytes)

    def test_transpile_preserves_input_source_encoding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "source.decl"

            result = cli_main([
                "transpile",
                str(TH18_CP932_SOURCE),
                "--target",
                "th18",
                "--output",
                str(output_path),
            ])

            self.assertEqual(result, 0)
            output_bytes = output_path.read_bytes()
            self.assertIn(EXPECTED_SPELL_NAME, output_bytes.decode("cp932"))
            self.assertNotIn(EXPECTED_SPELL_NAME.encode("utf-8"), output_bytes)

    def test_invalid_cp932_bytes_use_reversible_private_use_escapes(self) -> None:
        source = b'void Main()\n{\n    ins_537(0, 0, 0, "bad:\x81\x00");\n}\n'
        document = SourceDocument.from_bytes(source)

        self.assertEqual(document.encoding, "cp932")
        self.assertEqual(document.decoding_mode, SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE)
        self.assertIn(chr(BYTE_ESCAPE_BASE + 0x81), document.text)
        self.assertNotIn("\ufffd", document.text)
        self.assertEqual(encode_source_text(document.text, document.encoding, document.decoding_mode), source)

        program = parse_decl_bytes(source, "th08/invalid.decl")
        self.assertEqual(program.functions[0].body[0].args[3], f'"bad:{chr(BYTE_ESCAPE_BASE + 0x81)}\x00"')

        layout = build_source_layout(source)
        self.assertEqual(layout["decoding_mode"], SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE.value)
        self.assertEqual(emit_layout_roundtrip_bytes({"source_layout": layout}), source)

        arbitrary_bytes = bytes(range(256))
        arbitrary_document = SourceDocument.from_bytes(arbitrary_bytes)
        self.assertEqual(arbitrary_document.byte_escape_scope, BYTE_ESCAPE_SCOPE_ALL_NON_ASCII)
        self.assertEqual(
            encode_source_text(arbitrary_document.text, arbitrary_document.encoding, arbitrary_document.decoding_mode),
            arbitrary_bytes,
        )
        parse_decl_bytes(arbitrary_bytes, "arbitrary-bytes.decl")
        arbitrary_layout = build_source_layout(arbitrary_bytes)
        self.assertEqual(emit_layout_roundtrip_bytes({"source_layout": arbitrary_layout}), arbitrary_bytes)

    def test_real_th08_invalid_cp932_source_parses_and_roundtrips(self) -> None:
        source = TH08_INVALID_CP932_SOURCE.read_bytes()
        document = SourceDocument.from_bytes(source)

        self.assertEqual(document.encoding, "cp932")
        self.assertEqual(document.decoding_mode, SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE)
        self.assertNotIn("\ufffd", document.text)
        self.assertEqual(encode_source_text(document.text, document.encoding, document.decoding_mode), source)

        program = parse_decl(TH08_INVALID_CP932_SOURCE)
        self.assertGreater(len(program.functions), 0)
        layout = build_source_layout(source)
        self.assertEqual(emit_layout_roundtrip_bytes({"source_layout": layout}), source)
        reparsed = parse_decl_bytes(source, TH08_INVALID_CP932_SOURCE)
        self.assertEqual(program_to_dict(reparsed), program_to_dict(program))

        data = build_eclir(TH08_INVALID_CP932_SOURCE)
        self.assertEqual(
            data["source_decoding"]["decoding_mode"],
            SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE.value,
        )
        self.assertEqual(data["source_decoding"]["byte_escape_base"], "U+F0000")
        self.assertEqual(emit_layout_roundtrip_bytes(data), source)
        self.assertTrue(validate_eclir_data(data)["ok"])

    def test_utf8_bom_detection(self) -> None:
        source = b"void Main()\n{\n    ins_1();\n}\n"
        self.assertEqual(detect_text_encoding(source), "utf-8")
        self.assertEqual(detect_text_encoding(b"\xef\xbb\xbf" + source), "utf-8-sig")


if __name__ == "__main__":
    unittest.main()
