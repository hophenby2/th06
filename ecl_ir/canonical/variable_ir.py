"""Typed variable references and per-game numeric variable dialects.

Numeric IDs are an encoding detail, not a cross-game identity.  This module
decodes them to stable semantic IDs and refuses a target encoding unless type,
storage, propagation, and use-site access are compatible.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import re
from typing import Iterable

from ..dialects.game_ids import normalize_game_id
from .semantic_ir import (
    Confidence,
    ExpressionBinding,
    ExpressionIR,
    OperandValue,
    SemanticOperand,
    SemanticOperation,
    StackRef,
    StackUse,
    SyntaxStatement,
    ValueType,
    VariableAccess,
    VariableEncodingKind,
    VariablePropagation,
    VariableRef,
    VariableSourceEncoding,
    VariableStorageScope,
    VariableUse,
    VariableUseKind,
    operand_use_kinds,
)


@dataclass(frozen=True, slots=True)
class VariableSpec:
    numeric_id: int
    semantic_id: str
    storage_type: ValueType
    storage_scope: VariableStorageScope
    access: VariableAccess
    propagation: VariablePropagation
    confidence: Confidence = Confidence.DOCUMENTED
    priority: int = 0


@dataclass(frozen=True, slots=True)
class VariableProjectionIssue:
    code: str
    message: str
    semantic_id: str
    source_encoding: str
    source_game: str
    target_game: str

    def details(self) -> dict[str, object]:
        return {
            "semantic_id": self.semantic_id,
            "source_encoding": self.source_encoding,
            "source_game": self.source_game,
            "target_game": self.target_game,
        }


@dataclass(frozen=True, slots=True)
class ExpressionProjection:
    expression: ExpressionIR | None
    issues: tuple[VariableProjectionIssue, ...] = ()


I = ValueType.INT32
F = ValueType.FLOAT32
L = VariableStorageScope.ENTITY_LOCAL
B = VariableStorageScope.BOSS_PROXY
G = VariableStorageScope.STAGE_GLOBAL
E = VariableStorageScope.ENGINE_GLOBAL
C = VariableStorageScope.CALL_FRAME
RO = VariableAccess.READ_ONLY
RW = VariableAccess.READ_WRITE
NONE = VariablePropagation.NONE
COPY = VariablePropagation.COPY_TO_SPAWNED_CHILD
SHARED = VariablePropagation.SHARED


def _spec(
    numeric_id: int,
    semantic_id: str,
    storage_type: ValueType,
    scope: VariableStorageScope,
    access: VariableAccess,
    propagation: VariablePropagation,
    *,
    confidence: Confidence = Confidence.DOCUMENTED,
    priority: int = 0,
) -> VariableSpec:
    return VariableSpec(
        numeric_id,
        semantic_id,
        storage_type,
        scope,
        access,
        propagation,
        confidence,
        priority,
    )


def _modern_base() -> dict[int, VariableSpec]:
    specs = {
        -10000: _spec(-10000, "rng.integer.full_range", I, E, RO, SHARED),
        -9999: _spec(-9999, "rng.float.unit", F, E, RO, SHARED),
        -9998: _spec(-9998, "rng.angle.signed_pi", F, E, RO, SHARED),
        -9991: _spec(-9991, "player.position.x", F, E, RO, SHARED),
        -9990: _spec(-9990, "player.position.y", F, E, RO, SHARED),
        -9989: _spec(-9989, "entity.angle_to_player", F, L, RO, NONE),
        -9988: _spec(-9988, "entity.age.frames", I, L, RO, NONE),
        -9987: _spec(-9987, "rng.float.signed_unit", F, E, RO, SHARED),
        -9986: _spec(-9986, "phase.timeout_flag", I, G, RO, SHARED),
        -9963: _spec(-9963, "boss.position.final.x", F, E, RO, SHARED),
        -9962: _spec(-9962, "boss.position.final.y", F, E, RO, SHARED),
        -9961: _spec(-9961, "entity.anm.slot0.script_id", I, L, RO, NONE),
        -9960: _spec(-9960, "game.rank.value", I, E, RO, SHARED),
        -9959: _spec(-9959, "game.difficulty.index", I, E, RO, SHARED),
        -9958: _spec(-9958, "entity.motion.final_angle", F, L, RO, NONE),
        -9957: _spec(-9957, "constant.true", I, E, RO, SHARED),
        -9956: _spec(-9956, "entity.angle_to_player.absolute", F, L, RO, NONE),
        -9955: _spec(-9955, "entity.angle_to_player.relative", F, L, RO, NONE),
        -9954: _spec(-9954, "entity.health", I, L, RO, NONE),
    }
    for offset, axis in enumerate(("x", "y")):
        specs[-9997 + offset] = _spec(
            -9997 + offset, f"entity.position.final.{axis}", F, L, RO, NONE
        )
        specs[-9995 + offset] = _spec(
            -9995 + offset, f"entity.position.absolute.{axis}", F, L, RO, NONE
        )
        specs[-9993 + offset] = _spec(
            -9993 + offset, f"entity.position.relative.{axis}", F, L, RO, NONE
        )
        specs[-9977 + offset] = _spec(
            -9977 + offset,
            f"entity.position.final.{axis}",
            F,
            L,
            RO,
            NONE,
            priority=10,
        )
        specs[-9975 + offset] = _spec(
            -9975 + offset,
            f"entity.position.absolute.{axis}",
            F,
            L,
            RO,
            NONE,
            priority=10,
        )
        specs[-9973 + offset] = _spec(
            -9973 + offset,
            f"entity.position.relative.{axis}",
            F,
            L,
            RO,
            NONE,
            priority=10,
        )
        specs[-9965 + offset] = _spec(
            -9965 + offset,
            f"player.position.{axis}",
            F,
            E,
            RO,
            SHARED,
            priority=10,
        )
    for index in range(4):
        specs[-9985 + index] = _spec(
            -9985 + index, f"entity.local.int.{index}", I, L, RW, COPY
        )
        specs[-9981 + index] = _spec(
            -9981 + index, f"entity.local.float.{index}", F, L, RW, COPY
        )
    for numeric_id, semantic_id in (
        (-9971, "entity.motion.angle.absolute"),
        (-9970, "entity.motion.angle.relative"),
        (-9969, "entity.motion.speed.absolute"),
        (-9968, "entity.motion.speed.relative"),
        (-9967, "entity.motion.circle_radius.absolute"),
        (-9966, "entity.motion.circle_radius.relative"),
    ):
        specs[numeric_id] = _spec(numeric_id, semantic_id, F, L, RO, NONE)
    for offset, lane in enumerate(("easy", "normal", "hard", "lunatic")):
        numeric_id = -9953 + offset
        specs[numeric_id] = _spec(
            numeric_id, f"game.difficulty.is_{lane}", I, E, RO, SHARED
        )
    return specs


def _modern_11() -> dict[int, VariableSpec]:
    specs = {
        -9949: _spec(-9949, "player.miss_count.chapter", I, G, RW, SHARED),
        -9948: _spec(-9948, "player.bomb_count.chapter", I, G, RW, SHARED),
        -9947: _spec(-9947, "spell.capture_state", I, G, RW, SHARED),
        -9946: _spec(-9946, "enemy.count.all", I, E, RO, SHARED),
        -9945: _spec(-9945, "player.shot_type", I, E, RO, SHARED),
        -9944: _spec(-9944, "entity.distance_to_player", F, L, RO, NONE),
    }
    for index in range(4):
        specs[-9943 + index] = _spec(
            -9943 + index, f"boss.primary.local.int.{index}", I, B, RW, SHARED
        )
        specs[-9939 + index] = _spec(
            -9939 + index, f"boss.primary.local.float.{index}", F, B, RW, SHARED
        )
        specs[-9935 + index] = _spec(
            -9935 + index, f"entity.local.float.{index + 4}", F, L, RW, COPY
        )
    return specs


MODERN_12 = {
    -9931: _spec(-9931, "enemy.last_spawned_id", I, E, RO, SHARED),
    -9930: _spec(-9930, "player.power.scaled_100", I, E, RO, SHARED),
}


def _modern_125_stable() -> dict[int, VariableSpec]:
    specs = {
        -9914: _spec(-9914, "entity.id", I, L, RO, NONE),
        -9911: _spec(-9911, "boss.motion.angle", F, E, RO, SHARED),
        -9910: _spec(-9910, "boss.motion.speed", F, E, RO, SHARED),
    }
    for index in range(4):
        specs[-9926 + index] = _spec(
            -9926 + index, f"stage.global.int.{index}", I, G, RW, SHARED
        )
    for index in range(8):
        specs[-9922 + index] = _spec(
            -9922 + index, f"stage.global.float.{index}", F, G, RW, SHARED
        )
    return specs


MODERN_125_DS = {
    -9929: _spec(-9929, "th125.double_spoiler.unknown.1", I, G, RO, SHARED, confidence=Confidence.UNKNOWN),
    -9928: _spec(-9928, "th125.double_spoiler.unknown.2", I, G, RO, SHARED, confidence=Confidence.UNKNOWN),
    -9927: _spec(-9927, "th125.double_spoiler.unknown.3", I, G, RO, SHARED, confidence=Confidence.UNKNOWN),
    -9913: _spec(-9913, "th125.double_spoiler.photo_count", I, G, RO, SHARED),
    -9912: _spec(-9912, "th125.double_spoiler.unknown.4", I, G, RO, SHARED, confidence=Confidence.UNKNOWN),
}

MODERN_128 = {
    -9909: _spec(-9909, "entity.parent_id", I, L, RO, NONE),
}
MODERN_13 = {
    -9908: _spec(-9908, "enemy.count.killable", I, E, RO, SHARED),
    -9907: _spec(-9907, "game.spell.practice.selection_id", I, E, RO, SHARED),
}
MODERN_14 = {
    # Real TH14 scripts use this slot, but the reference catalog still marks
    # its mirror interpretation unverified. Keep identity support, not cross-game direct.
    -9906: _spec(
        -9906,
        "entity.mirror_state",
        I,
        L,
        RO,
        NONE,
        confidence=Confidence.INFERRED,
    ),
}
MODERN_15 = {
    -9905: _spec(-9905, "stage.chapter.index", I, E, RO, SHARED),
    -9904: _spec(-9904, "player.miss_count.run_total", I, E, RO, SHARED),
}
MODERN_16 = {
    -9903: _spec(-9903, "th16.subseason.selected", I, E, RO, SHARED),
}
MODERN_17 = {
    -9903: _spec(-9903, "th17.hyper.active", I, E, RO, SHARED),
    -9902: _spec(-9902, "th17.graze.recent", I, E, RO, SHARED),
    -9901: _spec(-9901, "th17.animal_tokens.active", I, E, RO, SHARED),
    -9900: _spec(-9900, "th17.hyper.dying", I, E, RO, SHARED),
    -9899: _spec(-9899, "achievement_mode", I, E, RO, SHARED),
}
MODERN_18 = {
    -9899: _spec(-9899, "achievement_mode", I, E, RO, SHARED),
    -9898: _spec(-9898, "bullet.active_count", I, E, RO, SHARED),
}


def _th08_specs() -> dict[int, VariableSpec]:
    specs: dict[int, VariableSpec] = {}
    for index in range(4):
        specs[10000 + index] = _spec(
            10000 + index, f"entity.local.int.{index}", I, L, RW, COPY
        )
    for numeric_id, index in zip(range(10004, 10008), range(8, 12)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.entity.local.int.{index}", I, L, RW, COPY
        )
    for index in range(8):
        specs[10008 + index] = _spec(
            10008 + index, f"th08.entity.private.int.{index}", I, L, RW, NONE
        )
        specs[10016 + index] = _spec(
            10016 + index, f"entity.local.float.{index}", F, L, RW, COPY
        )
    # The source order is LF2..LF7, LF0, LF1.
    for numeric_id, index in zip(range(10024, 10032), (2, 3, 4, 5, 6, 7, 0, 1)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.entity.private.float.{index}", F, L, RW, NONE
        )
    specs.update(
        {
            10032: _spec(10032, "rng.integer.full_range", I, E, RO, SHARED),
            10033: _spec(10033, "rng.float.unit", F, E, RO, SHARED),
            10035: _spec(10035, "rng.float.signed_unit", F, E, RO, SHARED),
            10040: _spec(10040, "game.difficulty.index", I, E, RW, SHARED),
            10041: _spec(10041, "game.rank.value", I, E, RW, SHARED),
            10042: _spec(10042, "entity.position.absolute.x", F, L, RW, NONE),
            10043: _spec(10043, "entity.position.absolute.y", F, L, RW, NONE),
            10044: _spec(10044, "th08.entity.position.absolute.z", F, L, RW, NONE),
            10045: _spec(10045, "player.position.x", F, L, RW, NONE),
            10046: _spec(10046, "player.position.y", F, L, RW, NONE),
            10047: _spec(10047, "th08.player.position.z", F, L, RW, NONE),
            10048: _spec(10048, "entity.angle_to_player", F, L, RW, NONE),
            10049: _spec(10049, "entity.age.frames", I, L, RW, NONE),
            10050: _spec(10050, "entity.distance_to_player", F, L, RW, NONE),
            10051: _spec(10051, "entity.health", I, L, RW, NONE),
            10052: _spec(10052, "th08.player.shot_type", I, E, RO, SHARED),
            10082: _spec(10082, "rng.angle.signed_pi", F, E, RO, SHARED),
            10083: _spec(10083, "th08.entity.damage.previous_frame", F, L, RO, NONE),
            10084: _spec(10084, "th08.boss.id", I, L, RO, NONE),
            10088: _spec(10088, "th08.entity.life_threshold", I, L, RW, NONE),
            10092: _spec(10092, "th08.entity.drop_main", I, L, RW, NONE),
            10093: _spec(10093, "th08.entity.score_reward", I, L, RW, NONE),
            10094: _spec(10094, "th08.entity.local.float.8", F, L, RW, COPY),
            10095: _spec(10095, "th08.entity.local.float.9", F, L, RW, COPY),
            10096: _spec(10096, "th08.entity.familiar_count", I, L, RO, NONE),
            10097: _spec(10097, "th08.player.is_youkai", I, E, RO, SHARED),
            10098: _spec(10098, "th08.stage.time_threshold_met", I, E, RO, SHARED),
            10099: _spec(10099, "th08.spell.capture_state", I, E, RO, SHARED),
            10100: _spec(10100, "th08.spell.timer", I, E, RO, SHARED),
        }
    )
    for index in range(4, 8):
        specs[10032 + index] = _spec(
            10032 + index, f"th08.entity.local.int.{index}", I, L, RW, COPY
        )
    for index, numeric_id in enumerate(range(10053, 10057)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.call.in.int.{index}", I, C, RW, NONE
        )
    for index, numeric_id in enumerate(range(10057, 10061)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.call.in.float.{index}", F, C, RW, NONE
        )
    for index, numeric_id in enumerate(range(10061, 10065)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.call.out.int.{index}", I, C, RW, NONE
        )
    for index, numeric_id in enumerate(range(10065, 10069)):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.call.out.float.{index}", F, C, RW, NONE
        )
    movement_names = (
        "angle",
        "angular_velocity",
        "speed",
        "acceleration",
        "circle_radius",
        "origin.x",
        "origin.y",
        "origin.z",
        "circle_angle",
        "circle_speed",
        "target.x",
        "target.y",
        "target.z",
    )
    for numeric_id, name in zip(range(10069, 10082), movement_names):
        specs[numeric_id] = _spec(
            numeric_id, f"th08.entity.motion.{name}", F, L, RW, NONE
        )
    return specs


def _opaque_overlay(game: str, numeric_ids: Iterable[int]) -> dict[int, VariableSpec]:
    return {
        numeric_id: _spec(
            numeric_id,
            f"opaque.{game}.numeric_special.{numeric_id}",
            I,
            VariableStorageScope.UNKNOWN,
            VariableAccess.UNKNOWN,
            VariablePropagation.UNKNOWN,
            confidence=Confidence.UNKNOWN,
        )
        for numeric_id in numeric_ids
    }


def _build_game_specs() -> dict[str, dict[int, VariableSpec]]:
    base = _modern_base()
    add11 = _modern_11()
    stable125 = _modern_125_stable()

    def merged(*layers: dict[int, VariableSpec]) -> dict[int, VariableSpec]:
        result: dict[int, VariableSpec] = {}
        for layer in layers:
            result.update(layer)
        return result

    games: dict[str, dict[int, VariableSpec]] = {
        "th06": {},
        "th07": {},
        "th08": _th08_specs(),
        "th10": merged(base),
        "th11": merged(base, add11),
        "th12": merged(base, add11, MODERN_12),
        "th125": merged(base, add11, MODERN_12, stable125, MODERN_125_DS),
        "th128": merged(
            base,
            add11,
            MODERN_12,
            stable125,
            _opaque_overlay("th128", MODERN_125_DS),
            MODERN_128,
        ),
    }
    stable_modern = merged(base, add11, MODERN_12, stable125, MODERN_128)
    for game in ("th13", "th14", "th143", "th15", "th16", "th165", "th17", "th18", "th185"):
        games[game] = merged(
            stable_modern,
            _opaque_overlay(game, MODERN_125_DS),
            {
                -9907: _spec(
                    -9907,
                    "game.spell.practice.selection_id",
                    I,
                    E,
                    RO,
                    SHARED,
                    confidence=Confidence.INFERRED,
                )
            },
            {-9908: MODERN_13[-9908]},
        )
    games["th13"].update(MODERN_13)
    for game in ("th14", "th143", "th15", "th16", "th165", "th17", "th18", "th185"):
        games[game].update(MODERN_14)
    for game in ("th15", "th16", "th165", "th17", "th18", "th185"):
        games[game].update(MODERN_15)
    for game in ("th16", "th165"):
        games[game].update(MODERN_16)
    games["th17"].update(MODERN_17)
    games["th18"].update(_opaque_overlay("th18", (-9903, -9902, -9901, -9900)))
    games["th18"].update(MODERN_18)
    games["th185"].update(_opaque_overlay("th185", range(-9903, -9889)))
    return games


GAME_VARIABLE_SPECS = _build_game_specs()
GAME_VARIABLE_RANGES: dict[str, tuple[int, int]] = {
    "th06": (10000, 10100),
    "th07": (10000, 10100),
    "th08": (10000, 10100),
    "th10": (-10000, -9950),
    "th11": (-10000, -9932),
    "th12": (-10000, -9930),
    "th125": (-10000, -9910),
    "th128": (-10000, -9909),
    "th13": (-10000, -9907),
    "th14": (-10000, -9906),
    "th143": (-10000, -9906),
    "th15": (-10000, -9904),
    "th16": (-10000, -9903),
    "th165": (-10000, -9903),
    "th17": (-10000, -9899),
    "th18": (-10000, -9898),
    "th185": (-10000, -9890),
}


class VariableDialect:
    def __init__(self, game: str, specs: dict[int, VariableSpec], numeric_range: tuple[int, int] | None) -> None:
        self.game = normalize_game_id(game)
        self.specs = dict(specs)
        self.numeric_range = numeric_range
        by_semantic: dict[str, list[VariableSpec]] = {}
        for spec in specs.values():
            by_semantic.setdefault(spec.semantic_id, []).append(spec)
        self.by_semantic = {
            semantic_id: tuple(sorted(candidates, key=lambda item: item.priority))
            for semantic_id, candidates in by_semantic.items()
        }

    def contains_numeric_id(self, numeric_id: int) -> bool:
        if self.numeric_range is None:
            return False
        low, high = self.numeric_range
        return low <= numeric_id <= high

    def decode_numeric(self, raw: str, numeric_id: int, view_type: ValueType) -> VariableRef | None:
        if not self.contains_numeric_id(numeric_id):
            return None
        spec = self.specs.get(numeric_id)
        if spec is None:
            spec = _spec(
                numeric_id,
                f"opaque.{self.game}.numeric_special.{numeric_id}",
                view_type,
                VariableStorageScope.UNKNOWN,
                VariableAccess.UNKNOWN,
                VariablePropagation.UNKNOWN,
                confidence=Confidence.UNKNOWN,
            )
        return VariableRef(
            semantic_id=spec.semantic_id,
            value_type=view_type,
            storage_type=spec.storage_type,
            storage_scope=spec.storage_scope,
            access=spec.access,
            propagation=spec.propagation,
            source_encoding=VariableSourceEncoding(
                game=self.game,
                kind=VariableEncodingKind.NUMERIC_SPECIAL,
                raw=raw,
                view_type=view_type,
                numeric_id=numeric_id,
            ),
            confidence=spec.confidence,
        )

    def encode(
        self,
        reference: VariableRef,
        use_kind: VariableUseKind,
    ) -> tuple[str | None, VariableProjectionIssue | None]:
        source = reference.source_encoding
        if source.kind is VariableEncodingKind.NAMED_LOCAL:
            source_routines = _routine_dialect_for_game(source.game)
            target_routines = _routine_dialect_for_game(self.game)
            if (
                source.game != self.game
                and not target_routines.accepts_locals_from(source_routines)
            ):
                return None, self._issue(
                    "variable.local_stack_abi_unsupported",
                    (
                        "named stack locals cannot cross the TH06-08 boundary without "
                        "explicit local register allocation"
                    ),
                    reference,
                )
            return source.raw, None
        if source.game == self.game:
            return source.raw, None
        if reference.confidence is not Confidence.DOCUMENTED:
            return None, self._issue(
                "variable.unconfirmed_semantics",
                "source variable semantics are not documented well enough for cross-game encoding",
                reference,
            )
        candidates = self.by_semantic.get(reference.semantic_id, ())
        compatible = [
            candidate
            for candidate in candidates
            if candidate.confidence is Confidence.DOCUMENTED
            and candidate.storage_type is reference.storage_type
            and candidate.storage_scope is reference.storage_scope
            and candidate.propagation is reference.propagation
            and _access_compatible(reference.access, candidate.access, use_kind)
        ]
        if not compatible:
            same_id = (
                self.specs.get(source.numeric_id)
                if source.numeric_id is not None
                else None
            )
            if same_id is not None and same_id.semantic_id != reference.semantic_id:
                return None, self._issue(
                    "variable.semantic_collision",
                    (
                        f"numeric variable {source.numeric_id} means {reference.semantic_id} in "
                        f"{source.game} but {same_id.semantic_id} in {self.game}"
                    ),
                    reference,
                )
            if candidates:
                if not any(candidate.confidence is Confidence.DOCUMENTED for candidate in candidates):
                    return None, self._issue(
                        "variable.unconfirmed_semantics",
                        "target variable semantics are not documented well enough for cross-game encoding",
                        reference,
                    )
                return None, self._issue(
                    "variable.storage_or_access_mismatch",
                    "target has the semantic variable but not with compatible storage or access",
                    reference,
                )
            return None, self._issue(
                "variable.target_unavailable",
                f"target game has no verified encoding for {reference.semantic_id}",
                reference,
            )
        target = compatible[0]
        suffix = ".0f" if reference.value_type is ValueType.FLOAT32 else ""
        return f"[{target.numeric_id}{suffix}]", None

    def _issue(self, code: str, message: str, reference: VariableRef) -> VariableProjectionIssue:
        return VariableProjectionIssue(
            code=code,
            message=message,
            semantic_id=reference.semantic_id,
            source_encoding=reference.source_encoding.raw,
            source_game=reference.source_encoding.game,
            target_game=self.game,
        )


VARIABLE_DIALECTS = {
    game: VariableDialect(game, specs, GAME_VARIABLE_RANGES.get(game))
    for game, specs in GAME_VARIABLE_SPECS.items()
}
UNKNOWN_VARIABLE_DIALECT = VariableDialect("unknown", {}, None)


def variable_dialect_for_game(game: str) -> VariableDialect:
    return VARIABLE_DIALECTS.get(normalize_game_id(game), UNKNOWN_VARIABLE_DIALECT)


def _routine_dialect_for_game(game: str):
    # Imported lazily because GameProfile owns VariableDialect as well.
    from ..dialects.game_profile import profile_for_game

    return profile_for_game(game).routine_dialect


def _access_compatible(
    source: VariableAccess,
    target: VariableAccess,
    use_kind: VariableUseKind,
) -> bool:
    if use_kind is VariableUseKind.READ:
        return source.readable and target.readable
    if use_kind is VariableUseKind.WRITE:
        return source.writable and target.writable
    if use_kind is VariableUseKind.READ_WRITE:
        return source.readable and source.writable and target.readable and target.writable
    return source is target and source is not VariableAccess.UNKNOWN


NUMERIC_VARIABLE_RE = re.compile(r"\[(-?\d+)(\.0f)?\]")
NAMED_VARIABLE_RE = re.compile(r"([%$])([A-Za-z_][A-Za-z0-9_]*)")


def _infer_mutating_use(
    text: str,
    use: VariableUse | StackUse,
) -> VariableUse | StackUse:
    before = text[:use.start].rstrip()
    after = text[use.end:].lstrip()
    if before.endswith(("++", "--")) or after.startswith(("++", "--")):
        return replace(use, kind=VariableUseKind.READ_WRITE)
    if after.startswith(("+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=")):
        return replace(use, kind=VariableUseKind.READ_WRITE)
    if after.startswith("=") and not after.startswith("=="):
        return replace(use, kind=VariableUseKind.WRITE)
    return use


def parse_expression(
    game: str,
    text: object,
    value_type: ValueType = ValueType.OPAQUE,
    use_kind: VariableUseKind = VariableUseKind.READ,
) -> ExpressionIR:
    rendered = str(text)
    dialect = variable_dialect_for_game(game)
    uses: list[VariableUse] = []
    stack_uses: list[StackUse] = []
    normalized_game = normalize_game_id(game)
    routine_dialect = _routine_dialect_for_game(normalized_game)
    index = 0
    quote = ""
    escape = False
    while index < len(rendered):
        char = rendered[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = ""
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
            index += 1
            continue
        if rendered.startswith("//", index):
            break
        numeric_match = NUMERIC_VARIABLE_RE.match(rendered, index)
        if numeric_match:
            raw = numeric_match.group(0)
            view = F if numeric_match.group(2) else I
            reference = dialect.decode_numeric(raw, int(numeric_match.group(1)), view)
            if reference is not None:
                uses.append(VariableUse(index, numeric_match.end(), reference, use_kind))
            else:
                offset = int(numeric_match.group(1))
                if routine_dialect.supports_relative_stack_references and -4096 <= offset < 0:
                    stack_uses.append(
                        StackUse(
                            index,
                            numeric_match.end(),
                            StackRef(offset, view, normalized_game, raw),
                            use_kind,
                        )
                    )
                else:
                    uses.append(
                        VariableUse(
                            index,
                            numeric_match.end(),
                            VariableRef(
                                semantic_id=(
                                    f"opaque.{normalized_game}.bracket_numeric.{offset}."
                                    f"{view.value}"
                                ),
                                value_type=view,
                                storage_type=view,
                                storage_scope=VariableStorageScope.UNKNOWN,
                                access=VariableAccess.UNKNOWN,
                                propagation=VariablePropagation.UNKNOWN,
                                source_encoding=VariableSourceEncoding(
                                    game=normalized_game,
                                    kind=VariableEncodingKind.UNKNOWN,
                                    raw=raw,
                                    view_type=view,
                                    numeric_id=offset,
                                ),
                                confidence=Confidence.UNKNOWN,
                            ),
                            use_kind,
                        )
                    )
            index = numeric_match.end()
            continue
        named_match = NAMED_VARIABLE_RE.match(rendered, index)
        if named_match:
            raw = named_match.group(0)
            view = F if named_match.group(1) == "%" else I
            name = named_match.group(2)
            reference = VariableRef(
                semantic_id=f"routine.local.{name}",
                value_type=view,
                storage_type=view,
                storage_scope=VariableStorageScope.ROUTINE_LOCAL,
                access=RW,
                propagation=NONE,
                source_encoding=VariableSourceEncoding(
                    game=normalize_game_id(game),
                    kind=VariableEncodingKind.NAMED_LOCAL,
                    raw=raw,
                    view_type=view,
                    name=name,
                ),
                confidence=Confidence.DOCUMENTED,
            )
            uses.append(VariableUse(index, named_match.end(), reference, use_kind))
            index = named_match.end()
            continue
        index += 1
    return ExpressionIR(
        rendered,
        value_type,
        tuple(_infer_mutating_use(rendered, use) for use in uses),
        tuple(_infer_mutating_use(rendered, use) for use in stack_uses),
    )


def parse_syntax_expression(statement: SyntaxStatement) -> ExpressionIR:
    expression = parse_expression(
        statement.provenance.game,
        statement.text,
        ValueType.OPAQUE,
        VariableUseKind.READ,
    )
    if statement.statement_kind != "assign":
        return expression
    assignment = statement.text.find("=")
    if assignment < 0:
        return expression
    return replace(
        expression,
        variable_uses=tuple(
            replace(use, kind=VariableUseKind.WRITE)
            if use.end <= assignment
            else use
            for use in expression.variable_uses
        ),
    )


def syntax_expression_bindings(
    game: str,
    statement_kind: str,
    attributes: dict[str, object],
    text: str,
) -> list[ExpressionBinding]:
    bindings: list[ExpressionBinding] = []

    def add(role: str, value: object, kind: VariableUseKind, ordinal: int = 0) -> None:
        bindings.append(
            ExpressionBinding(role, parse_expression(game, value, ValueType.OPAQUE, kind), ordinal)
        )

    if statement_kind == "assign":
        add("target", attributes.get("target", ""), VariableUseKind.WRITE)
        add("value", attributes.get("expr", ""), VariableUseKind.READ)
    elif statement_kind == "conditional_goto":
        add("condition", attributes.get("condition", ""), VariableUseKind.READ)
        add("time", attributes.get("time", ""), VariableUseKind.READ)
    elif statement_kind == "goto":
        add("time", attributes.get("time", ""), VariableUseKind.READ)
    elif statement_kind in {"call", "async_call"}:
        args = attributes.get("args", [])
        if isinstance(args, list):
            for ordinal, value in enumerate(args):
                add("argument", value, VariableUseKind.READ, ordinal)
        if "async_slot" in attributes:
            add("async_slot", attributes["async_slot"], VariableUseKind.READ)
    elif statement_kind == "var":
        values = attributes.get("vars", [])
        if isinstance(values, list):
            for ordinal, value in enumerate(values):
                add("declaration", value, VariableUseKind.UNKNOWN, ordinal)
    elif statement_kind == "raw" and text.rstrip().endswith(";"):
        add("value", text.rstrip()[:-1], VariableUseKind.READ)
    return bindings


def project_expression(expression: ExpressionIR, target_game: str) -> ExpressionProjection:
    target = variable_dialect_for_game(target_game)
    replacements: list[tuple[int, int, str, VariableUse | StackUse]] = []
    issues: list[VariableProjectionIssue] = []
    for use in expression.variable_uses:
        encoded, issue = target.encode(use.reference, use.kind)
        if issue is not None:
            issues.append(issue)
        elif encoded is not None:
            replacements.append((use.start, use.end, encoded, use))
    target_game = normalize_game_id(target_game)
    target_routines = _routine_dialect_for_game(target_game)
    for use in expression.stack_uses:
        source_game = normalize_game_id(use.reference.source_game)
        source_routines = _routine_dialect_for_game(source_game)
        if source_game == target_game or (
            target_routines.accepts_stack_references_from(source_routines)
        ):
            replacements.append(
                (use.start, use.end, use.reference.source_encoding, use)
            )
            continue
        issues.append(
            VariableProjectionIssue(
                code="stack.relative_abi_unsupported",
                message=(
                    "TH13+ stack-relative expression parameters cannot be encoded for "
                    "the target routine ABI"
                ),
                semantic_id=f"stack.relative.{use.reference.offset}",
                source_encoding=use.reference.source_encoding,
                source_game=source_game,
                target_game=target_game,
            )
        )
    if issues:
        return ExpressionProjection(None, tuple(issues))
    pieces: list[str] = []
    projected_uses: list[VariableUse] = []
    projected_stack_uses: list[StackUse] = []
    cursor = 0
    output_length = 0
    for use_start, use_end, encoded, use in sorted(replacements, key=lambda item: item[0]):
        prefix = expression.text[cursor:use_start]
        pieces.append(prefix)
        output_length += len(prefix)
        start = output_length
        pieces.append(encoded)
        output_length += len(encoded)
        if isinstance(use, VariableUse):
            decoded = parse_expression(
                target.game,
                encoded,
                expression.value_type,
                use.kind,
            )
            if decoded.variable_uses:
                projected_uses.append(
                    VariableUse(start, output_length, decoded.variable_uses[0].reference, use.kind)
                )
        else:
            projected_stack_uses.append(
                StackUse(
                    start,
                    output_length,
                    StackRef(
                        use.reference.offset,
                        use.reference.value_type,
                        target_game,
                        encoded,
                    ),
                    use.kind,
                )
            )
        cursor = use_end
    suffix = expression.text[cursor:]
    pieces.append(suffix)
    return ExpressionProjection(
        ExpressionIR(
            "".join(pieces),
            expression.value_type,
            tuple(projected_uses),
            tuple(projected_stack_uses),
        ),
    )


def rewrite_expression_variables(
    source_game: str,
    target_game: str,
    text: object,
    *,
    value_type: ValueType = ValueType.OPAQUE,
    use_kind: VariableUseKind = VariableUseKind.READ,
) -> tuple[str | None, tuple[VariableProjectionIssue, ...]]:
    projected = project_expression(
        parse_expression(source_game, text, value_type, use_kind),
        target_game,
    )
    return (
        projected.expression.text if projected.expression is not None else None,
        projected.issues,
    )


def rewrite_argument_variables(
    source_game: str,
    target_game: str,
    values: Iterable[object],
    *,
    use_kind: VariableUseKind = VariableUseKind.UNKNOWN,
) -> tuple[list[str] | None, tuple[VariableProjectionIssue, ...]]:
    rendered: list[str] = []
    issues: list[VariableProjectionIssue] = []
    for value in values:
        projected, value_issues = rewrite_expression_variables(
            source_game,
            target_game,
            value,
            use_kind=use_kind,
        )
        issues.extend(value_issues)
        if projected is not None:
            rendered.append(projected)
    return (rendered if not issues else None, tuple(issues))


def project_semantic_operation(
    operation: SemanticOperation,
    target_game: str,
) -> tuple[SemanticOperation | None, tuple[VariableProjectionIssue, ...]]:
    operands: list[SemanticOperand] = []
    issues: list[VariableProjectionIssue] = []
    use_kinds = operand_use_kinds(
        operation.operation,
        [operand.name for operand in operation.operands],
    )
    expression_game = normalize_game_id(
        str(
            operation.annotations.get("variable_projection_target")
            or operation.provenance.game
        )
    )
    for operand, use_kind in zip(operation.operands, use_kinds):
        value = operand.value
        if value.expression is None:
            operands.append(operand)
            continue
        expression = parse_expression(
            expression_game,
            value.expression.text,
            value.expression.value_type,
            use_kind,
        )
        projected = project_expression(expression, target_game)
        issues.extend(projected.issues)
        if projected.expression is None:
            operands.append(operand)
            continue
        operands.append(
            replace(
                operand,
                value=replace(
                    value,
                    expression=projected.expression,
                    source_text=projected.expression.text,
                ),
            )
        )
    if issues:
        return None, tuple(issues)
    return replace(
        operation,
        operands=operands,
        annotations={
            **operation.annotations,
            "variable_projection_target": normalize_game_id(target_game),
        },
    ), ()


def project_syntax_statement(
    statement: SyntaxStatement,
    target_game: str,
) -> tuple[str | None, tuple[VariableProjectionIssue, ...]]:
    source_game = normalize_game_id(statement.provenance.game)
    target_game = normalize_game_id(target_game)
    source_routines = _routine_dialect_for_game(source_game)
    target_routines = _routine_dialect_for_game(target_game)
    if (
        statement.statement_kind == "var"
        and source_game != target_game
        and not target_routines.accepts_locals_from(source_routines)
    ):
        issue = VariableProjectionIssue(
            code="variable.local_stack_abi_unsupported",
            message=(
                "stack variable declarations are unavailable in the TH06-08 target ABI; "
                "explicit local register allocation is required"
            ),
            semantic_id="routine.local.declaration",
            source_encoding=statement.text,
            source_game=source_game,
            target_game=target_game,
        )
        return None, (issue,)
    return_expression = project_expression(parse_syntax_expression(statement), target_game)
    return (
        return_expression.expression.text if return_expression.expression is not None else None,
        return_expression.issues,
    )


__all__ = [
    "ExpressionProjection",
    "GAME_VARIABLE_RANGES",
    "GAME_VARIABLE_SPECS",
    "VariableDialect",
    "VariableProjectionIssue",
    "VariableSpec",
    "parse_expression",
    "parse_syntax_expression",
    "project_expression",
    "project_semantic_operation",
    "project_syntax_statement",
    "rewrite_argument_variables",
    "rewrite_expression_variables",
    "syntax_expression_bindings",
    "variable_dialect_for_game",
]
