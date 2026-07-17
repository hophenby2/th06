from __future__ import annotations

import unittest

from ecl_ir.canonical.op_ir import semantic_operation
from ecl_ir.canonical.semantic_ir import EngineValueKind, EvaluationTime, OperandState, SemanticOperation
from ecl_ir.analysis.transform_ir import BulletSpawnTransformBundleIR, BulletTransformIR


def transform(game: str, opcode: int, args: list[str]) -> BulletTransformIR:
    operation = semantic_operation(game, opcode, args, 1, routine="Main")
    value = BulletTransformIR.from_semantic_operation(operation)
    if value is None:
        raise AssertionError(f"ins_{opcode} did not decode as a canonical transform")
    return value


class TransformIrTests(unittest.TestCase):
    def test_pause_variants_promote_to_extended_modern_form(self) -> None:
        cases = (
            ("th10", 409, "64", "0"),
            ("th10", 409, "128", "2"),
            ("th10", 409, "256", "4"),
            ("th11", 409, "16", "0"),
            ("th11", 409, "32", "2"),
            ("th11", 409, "64", "4"),
            ("th12", 509, "16", "0"),
            ("th12", 509, "32", "2"),
            ("th12", 509, "64", "4"),
        )
        for game, opcode, mode, subtype in cases:
            with self.subTest(game=game, mode=mode):
                value = transform(
                    game,
                    opcode,
                    ["0", "1", "0", mode, "30", "2", "0.25f", "1.5f"],
                )
                lowered = value.lower_to("th15")
                self.assertIsNotNone(lowered)
                assert lowered is not None
                self.assertEqual(lowered.opcode, 610)
                self.assertEqual(lowered.args[3], "16")
                self.assertEqual(lowered.args[6:8], [subtype, "0"])
                self.assertEqual(lowered.args[8:10], ["0.25f", "1.5f"])

    def test_modern_pause_subtype_projects_only_when_semantics_are_known(self) -> None:
        expected_modes = {"0": ("64", "16"), "2": ("128", "32"), "4": ("256", "64")}
        for subtype, (th10_mode, th12_mode) in expected_modes.items():
            value = transform(
                "th13",
                610,
                [
                    "0", "1", "0", "16", "30", "2", subtype, "0",
                    "0.25f", "1.5f", "-999999.0f", "-999999.0f",
                ],
            )
            with self.subTest(subtype=subtype, target="th10"):
                lowered = value.lower_to("th10")
                self.assertIsNotNone(lowered)
                assert lowered is not None
                self.assertEqual((lowered.opcode, lowered.args[3]), (409, th10_mode))
            with self.subTest(subtype=subtype, target="th12"):
                lowered = value.lower_to("th12")
                self.assertIsNotNone(lowered)
                assert lowered is not None
                self.assertEqual((lowered.opcode, lowered.args[3]), (509, th12_mode))

        for subtype in ("1", "3", "5", "6", "7"):
            value = transform(
                "th13",
                610,
                [
                    "0", "1", "0", "16", "30", "2", subtype, "0",
                    "0.25f", "1.5f", "-999999.0f", "-999999.0f",
                ],
            )
            with self.subTest(subtype=subtype):
                self.assertIsNone(value.lower_to("th12"))
                reason = value.unsupported_reason("th12") or ""
                self.assertTrue("extended" in reason or "changes" in reason)

    def test_modern_pause_requires_extended_parameters(self) -> None:
        value = transform(
            "th13",
            609,
            ["0", "1", "0", "16", "30", "2", "0.25f", "1.5f"],
        )
        self.assertIsNone(value.lower_to("th15"))
        self.assertIn("extended parameter set", value.unsupported_reason("th15") or "")

    def test_modern_write_and_parameter_forms_are_orthogonal(self) -> None:
        cases = (
            (609, ["0", "1", "0", "4", "30", "-999999", "0.1f", "-999999.0f"]),
            (610, ["0", "1", "0", "4", "30", "-999999", "0", "0", "0.1f", "-999999.0f", "-999999.0f", "-999999.0f"]),
            (611, ["0", "0", "4", "30", "-999999", "0.1f", "-999999.0f"]),
            (612, ["0", "0", "4", "30", "-999999", "0", "0", "0.1f", "-999999.0f", "-999999.0f", "-999999.0f"]),
        )
        for opcode, args in cases:
            with self.subTest(opcode=opcode):
                lowered = transform("th15", opcode, args).lower_to("th15")
                self.assertIsNotNone(lowered)
                assert lowered is not None
                self.assertEqual(lowered.opcode, opcode)
                self.assertEqual(lowered.args, args)

    def test_append_materializes_only_with_a_resolved_index(self) -> None:
        value = transform(
            "th15",
            611,
            ["0", "0", "4", "30", "-999999", "0.1f", "-999999.0f"],
        )
        self.assertIsNone(value.lower_to("th12"))
        lowered = value.lower_to("th12", resolved_index=3)
        self.assertIsNotNone(lowered)
        assert lowered is not None
        self.assertEqual(lowered.opcode, 509)
        self.assertEqual(lowered.args[:3], ["0", "3", "0"])

    def test_bounce_masks_are_reencoded_without_truncating_extensions(self) -> None:
        fixed = {"1024": "15", "2048": "13", "134217728": "12"}
        for mode, mask in fixed.items():
            value = transform(
                "th10",
                409,
                ["0", "1", "0", mode, "3", "-999999", "2.0f", "-999999.0f"],
            )
            lowered = value.lower_to("th15")
            self.assertIsNotNone(lowered)
            assert lowered is not None
            self.assertEqual((lowered.args[3], lowered.args[5]), ("64", mask))

        extended_mask = transform(
            "th12",
            509,
            ["0", "1", "0", "256", "3", "29", "2.0f", "-999999.0f"],
        )
        modern = extended_mask.lower_to("th15")
        self.assertIsNotNone(modern)
        assert modern is not None
        self.assertEqual((modern.args[3], modern.args[5]), ("64", "29"))
        self.assertIsNone(extended_mask.lower_to("th10"))

    def test_generation_specific_numeric_modes_do_not_alias(self) -> None:
        th12_jump = transform(
            "th12",
            509,
            ["0", "1", "0", "2097152", "30", "-999999", "-999999.0f", "-999999.0f"],
        )
        self.assertIsNone(th12_jump.lower_to("th15"))

        old_reserved = transform(
            "th10",
            409,
            ["0", "1", "0", "-2147483648", "-999999", "-999999", "-999999.0f", "-999999.0f"],
        )
        self.assertTrue(old_reserved.mode_semantic.startswith("raw:"))
        self.assertIsNone(old_reserved.lower_to("th15"))

    def test_modern_mode_availability_is_game_specific(self) -> None:
        cases = (
            ("th15", "th14", "134217728"),
            ("th16", "th15", "536870912"),
            ("th17", "th16", "1073741824"),
        )
        for source, older_target, mode in cases:
            value = transform(
                source,
                609,
                ["0", "1", "0", mode, "30", "-999999", "0.1f", "0.2f"],
            )
            with self.subTest(source=source, target=older_target, mode=mode):
                self.assertIsNone(value.lower_to(older_target))
                self.assertIn("requires target capability", value.unsupported_reason(older_target) or "")
                self.assertIsNotNone(value.lower_to(source))

        random_speed = transform(
            "th15",
            610,
            [
                "0", "1", "0", "16", "30", "2", "7", "0",
                "0.25f", "1.5f", "-999999.0f", "-999999.0f",
            ],
        )
        self.assertIsNone(random_speed.lower_to("th14"))

        old_subtype = transform(
            "th14",
            610,
            [
                "0", "1", "0", "16", "30", "2", "7", "0",
                "0.25f", "1.5f", "-999.0f", "-999.0f",
            ],
        )
        self.assertIsNone(old_subtype.lower_to("th15"))
        self.assertIn("changes", old_subtype.unsupported_reason("th15") or "")

        jump_loop = transform(
            "th17",
            609,
            ["0", "1", "0", "65536", "30", "$B", "0.1f", "0.2f"],
        )
        self.assertIsNone(jump_loop.lower_to("th15"))

        remove_highlight = transform(
            "th16",
            609,
            ["0", "1", "0", "1048576", "2", "-999999", "-999999.0f", "-999999.0f"],
        )
        self.assertIsNone(remove_highlight.lower_to("th15"))

    def test_spawn_payload_versions_and_contextual_attributes_do_not_alias(self) -> None:
        packed = transform(
            "th13",
            611,
            ["0", "0", "8192", "134743048", "0", "-999.0f", "-999.0f"],
        )
        self.assertEqual(packed.mode_semantic, "spawn_bullet_packed_v13")
        self.assertIsNone(packed.lower_to("th14"))

        attributes = transform(
            "th14",
            612,
            [
                "0", "0", "16384", "1", "2", "3", "4",
                "0.1f", "0.2f", "0.3f", "0.4f",
            ],
        )
        self.assertIsNone(attributes.lower_to("th15"))
        self.assertIn("bundled transform sequence", attributes.unsupported_reason("th15") or "")

    def test_legacy_spawn_pair_decodes_and_expands_as_one_semantic_bundle(self) -> None:
        first = semantic_operation(
            "th12",
            509,
            ["0", "3", "0", "524288", "50923526", "12", "%B", "2.0f"],
            1,
            routine="Main",
        )
        second = semantic_operation(
            "th12",
            509,
            ["0", "4", "0", "1048576", "1", "0", "[-9998.0f]", "0.0f"],
            2,
            routine="Main",
        )
        bundle = BulletSpawnTransformBundleIR.from_operations(first, second)
        self.assertIsNotNone(bundle)
        assert bundle is not None
        self.assertEqual(
            (
                bundle.spread_style,
                bundle.bullet_shape,
                bundle.bullet_color,
                bundle.resume_transform_index,
                bundle.remove_source_bullet,
            ),
            ("6", "8", "9", "3", "0"),
        )
        lowered = bundle.lower_to("th15")
        self.assertIsNotNone(lowered)
        assert lowered is not None
        self.assertEqual([instruction.opcode for instruction in lowered], [610, 610])
        self.assertEqual(
            lowered[0].args,
            [
                "0", "3", "0", "8192", "6", "3", "12", "1",
                "[-9998.0f]", "0.0f", "%B", "2.0f",
            ],
        )
        self.assertEqual(
            lowered[1].args,
            [
                "0", "4", "0", "16384", "9", "9", "0", "0",
                "0.0f", "0.0f", "0.0f", "0.0f",
            ],
        )

    def test_expanded_spawn_pair_repacks_delete_bit_for_th12(self) -> None:
        first = semantic_operation(
            "th14",
            610,
            [
                "0", "3", "0", "8192", "6", "3", "12", "1",
                "0.25f", "0.0f", "2.0f", "0.5f",
            ],
            1,
            routine="Main",
        )
        second = semantic_operation(
            "th14",
            610,
            [
                "0", "4", "0", "16384", "9", "9", "1", "0",
                "0.0f", "0.0f", "0.0f", "0.0f",
            ],
            2,
            routine="Main",
        )
        bundle = BulletSpawnTransformBundleIR.from_operations(first, second)
        self.assertIsNotNone(bundle)
        assert bundle is not None
        lowered = bundle.lower_to("th12")
        self.assertIsNotNone(lowered)
        assert lowered is not None
        payload = int(lowered[0].args[4]) & 0xFFFFFFFF
        self.assertEqual(payload.to_bytes(4, "little"), bytes((6, 8, 9, 0x83)))
        self.assertEqual(lowered[1].args[3:8], ["1048576", "1", "0", "0.25f", "0.0f"])

    def test_spawn_pair_rejects_nonzero_contextual_laser_payload(self) -> None:
        first = semantic_operation(
            "th15",
            612,
            [
                "0", "0", "8192", "6", "3", "12", "1",
                "0.25f", "0.0f", "2.0f", "0.5f",
            ],
            1,
            routine="Main",
        )
        second = semantic_operation(
            "th15",
            612,
            [
                "0", "0", "16384", "9", "9", "0", "0",
                "1.0f", "0.0f", "0.0f", "0.0f",
            ],
            2,
            routine="Main",
        )
        self.assertIsNone(BulletSpawnTransformBundleIR.from_operations(first, second))

    def test_keep_current_tokens_are_mode_field_and_game_specific(self) -> None:
        th12_accel = transform(
            "th12",
            509,
            ["0", "1", "0", "4", "60", "-999999", "0.1f", "-999.0f"],
        )
        self.assertEqual(th12_accel.values["s"].state.value, "keep_current")
        th18_accel = th12_accel.lower_to("th18")
        self.assertIsNotNone(th18_accel)
        assert th18_accel is not None
        self.assertEqual(th18_accel.args[-1], "-9999994.0f")

        th14_spawn = transform(
            "th14",
            612,
            [
                "0", "0", "8192", "1", "2", "3", "4",
                "-999.0f", "0.0f", "-999.0f", "0.0f",
            ],
        )
        self.assertEqual(th14_spawn.values["r"].state.value, "keep_current")
        self.assertEqual(th14_spawn.values["m"].state.value, "keep_current")
        th15_spawn = th14_spawn.lower_to("th15")
        self.assertIsNotNone(th15_spawn)
        assert th15_spawn is not None
        self.assertEqual(th15_spawn.args[7], "-999999.0f")
        self.assertEqual(th15_spawn.args[9], "-999999.0f")

        th18_spawn = transform(
            "th18",
            612,
            [
                "0", "0", "8192", "1", "2", "3", "4",
                "-9999994.0f", "0.0f", "-9999994.0f", "0.0f",
            ],
        )
        th14_lowered = th18_spawn.lower_to("th14")
        self.assertIsNotNone(th14_lowered)
        assert th14_lowered is not None
        self.assertEqual(th14_lowered.args[7], "-999.0f")
        self.assertEqual(th14_lowered.args[9], "-999.0f")

    def test_dynamic_angle_engine_values_are_typed_and_reencoded(self) -> None:
        th14 = semantic_operation(
            "th14",
            609,
            ["0", "1", "0", "2097152", "60", "-999999", "2.0f", "999.0f"],
        )
        value_by_name = {operand.name: operand.value for operand in th14.operands}
        angle = value_by_name["s"]
        self.assertEqual(angle.state, OperandState.ENGINE_SENTINEL)
        self.assertEqual(angle.engine_value.kind, EngineValueKind.LIVE_PLAYER_ANGLE)
        self.assertEqual(angle.evaluation_time, EvaluationTime.PER_FRAME)

        restored = SemanticOperation.from_dict(th14.to_dict())
        self.assertEqual(restored.to_dict(), th14.to_dict())

        canonical = BulletTransformIR.from_semantic_operation(th14)
        self.assertIsNotNone(canonical)
        assert canonical is not None
        th18 = canonical.lower_to("th18")
        self.assertIsNotNone(th18)
        assert th18 is not None
        self.assertEqual(th18.args[-1], "3000000.0f")

        th18_player = transform(
            "th18",
            609,
            ["0", "1", "0", "2097152", "60", "-9999994", "2.0f", "3000000.0f"],
        )
        th14_player = th18_player.lower_to("th14")
        self.assertIsNotNone(th14_player)
        assert th14_player is not None
        self.assertEqual(th14_player.args[-1], "999.0f")

        th18_random = transform(
            "th18",
            609,
            ["0", "1", "0", "2097152", "60", "-9999994", "2.0f", "4000000.0f"],
        )
        self.assertIsNone(th18_random.lower_to("th14"))
        self.assertIn("live_random_angle", th18_random.unsupported_reason("th14") or "")

    def test_legacy_bitmask_transform_is_identity_only(self) -> None:
        value = transform(
            "th08",
            111,
            ["0", "64", "1", "30", "-1", "-1.0f", "-1.0f"],
        )
        identity = value.lower_to("th08")
        self.assertIsNotNone(identity)
        assert identity is not None
        self.assertEqual(identity.opcode, 111)
        self.assertIsNone(value.lower_to("th15"))


if __name__ == "__main__":
    unittest.main()
