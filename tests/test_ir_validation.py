from __future__ import annotations

import copy
import unittest

from ecl_ir.artifact.ir_file import build_eclir, validate_eclir_data


class IrValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = build_eclir("th12/stage01.decl")

    def test_duplicate_canonical_node_ids_are_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        routine = next(item for item in data["canonical_ir"]["routines"] if len(item["body"]) >= 2)
        routine["body"][1]["node_id"] = routine["body"][0]["node_id"]
        result = validate_eclir_data(data)
        self.assertFalse(result["ok"])
        self.assertIn("canonical IR contains duplicate NodeIds", result["warnings"])

    def test_wrong_canonical_owner_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        node = next(
            node
            for routine in data["canonical_ir"]["routines"]
            for node in routine["body"]
            if node["node"] == "semantic_operation"
        )
        node["ownership"]["owner"] = "pattern"
        result = validate_eclir_data(data)
        self.assertFalse(result["ok"])
        self.assertTrue(any("invalid lowering ownership" in warning for warning in result["warnings"]))

    def test_unknown_lowering_owner_is_not_silently_defaulted(self) -> None:
        data = copy.deepcopy(self.data)
        node = next(
            node
            for routine in data["canonical_ir"]["routines"]
            for node in routine["body"]
            if node["node"] == "semantic_operation"
        )
        node["ownership"]["owner"] = "patternn"

        result = validate_eclir_data(data)

        self.assertFalse(result["ok"])
        self.assertTrue(any("patternn" in warning for warning in result["warnings"]))

    def test_canonical_content_drift_is_rejected(self) -> None:
        for field in ("operation", "operand"):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                node = next(
                    node
                    for routine in data["canonical_ir"]["routines"]
                    for node in routine["body"]
                    if node["node"] == "semantic_operation" and node["operands"]
                )
                if field == "operation":
                    node["operation"] = "invalid.replacement"
                else:
                    node["operands"][0]["value"]["source_text"] = "999999"

                result = validate_eclir_data(data)

                self.assertFalse(result["ok"])
                self.assertIn(
                    "canonical IR content differs from Program-derived canonical IR",
                    result["warnings"],
                )

    def test_program_content_drift_from_source_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        function = next(function for function in data["program"]["functions"] if function["body"])
        function["body"][0]["opcode"] = 999999

        result = validate_eclir_data(data)

        self.assertFalse(result["ok"])
        self.assertIn("Program IR content differs from reparsed source", result["warnings"])

    def test_stale_canonical_summary_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["canonical_summary"]["semantic_ops"] = -1

        result = validate_eclir_data(data)

        self.assertFalse(result["ok"])
        self.assertIn("canonical summary differs from canonical IR", result["warnings"])


if __name__ == "__main__":
    unittest.main()
