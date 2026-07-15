"""Data-driven game profiles for cross-game ECL lowering."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping

from .game_ids import normalize_game_id
from ..canonical.variable_ir import VariableDialect, variable_dialect_for_game


CAP_BULLET_MACRO = "bullet.macro"
CAP_BULLET_MANAGER = "bullet.manager"
CAP_BULLET_TRANSFORM = "bullet.transform"
CAP_TRANSFORM_CHANNELS = "bullet.transform.channels"
CAP_TRANSFORM_INDEXED_REPLACE = "bullet.transform.indexed_replace"
CAP_TRANSFORM_APPEND = "bullet.transform.append"
CAP_TRANSFORM_APPEND_CURSOR = "bullet.transform.append_cursor"
CAP_TRANSFORM_CURSOR_DECREMENT = "bullet.transform.cursor_decrement"
CAP_TRANSFORM_SPAWN_BULLET_PACKED_V13 = "bullet.transform.spawn_bullet.packed_v13"
CAP_TRANSFORM_SPAWN_BULLET_EXPANDED = "bullet.transform.spawn_bullet.expanded"
CAP_TRANSFORM_SPAWN_LASER = "bullet.transform.spawn_laser"
CAP_TRANSFORM_HITBOX_RADIUS = "bullet.transform.hitbox_radius"
CAP_TRANSFORM_HOMING_VELOCITY_BLEND = "bullet.transform.homing_velocity_blend"
CAP_TRANSFORM_RANDOM_SPEED_SUBTYPE = "bullet.transform.pause_random_speed"
CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE = "bullet.transform.pause_preserve_direction"
CAP_TRANSFORM_JUMP_LOOP_COUNT = "bullet.transform.jump_loop_count"
CAP_TRANSFORM_HIGHLIGHT_REMOVE = "bullet.transform.highlight_remove"
CAP_LASER_BASIC = "laser.basic"
CAP_LASER_INFINITE = "laser.infinite"
CAP_LASER_CURVE = "laser.curve"
CAP_RELATIVE_MOTION = "motion.relative"
CAP_ENEMY_INTERACTION = "enemy.interaction"
CAP_RECT_COLLISION = "collision.rectangle"


class RoutineCallEncoding(str, Enum):
    UNKNOWN = "unknown"
    INDEXED_INSTRUCTION = "indexed_instruction"
    NAMED_STACK = "named_stack"


class RoutineLocalEncoding(str, Enum):
    UNKNOWN = "unknown"
    FIXED_REGISTER = "fixed_register"
    NAMED_STACK = "named_stack"


class StackReferenceEncoding(str, Enum):
    NONE = "none"
    RELATIVE_OFFSET = "relative_offset"
    UNKNOWN = "unknown"


class RoutineSyntaxEncoding(str, Enum):
    UNKNOWN = "unknown"
    LEGACY_INSTRUCTIONS = "legacy_instructions"
    STACK_EXPRESSIONS = "stack_expressions"


@dataclass(frozen=True, slots=True)
class RoutineDialect:
    """Calling convention and local-storage ABI for one ECL family."""

    name: str
    call_encoding: RoutineCallEncoding
    local_encoding: RoutineLocalEncoding
    stack_reference_encoding: StackReferenceEncoding
    syntax_encoding: RoutineSyntaxEncoding

    def accepts_call_syntax_from(self, source: RoutineDialect) -> bool:
        return (
            self.call_encoding is RoutineCallEncoding.NAMED_STACK
            and self.call_encoding is source.call_encoding
        )

    def accepts_locals_from(self, source: RoutineDialect) -> bool:
        return (
            self.local_encoding is not RoutineLocalEncoding.UNKNOWN
            and self.local_encoding is source.local_encoding
        )

    def accepts_parameters_from(self, source: RoutineDialect) -> bool:
        return self.accepts_call_syntax_from(source) and self.accepts_locals_from(source)

    @property
    def supports_structured_syntax(self) -> bool:
        return self.syntax_encoding is RoutineSyntaxEncoding.STACK_EXPRESSIONS

    def accepts_stack_references_from(self, source: RoutineDialect) -> bool:
        return (
            self.stack_reference_encoding is StackReferenceEncoding.RELATIVE_OFFSET
            and self.stack_reference_encoding is source.stack_reference_encoding
        )

    @property
    def supports_relative_stack_references(self) -> bool:
        return self.stack_reference_encoding is StackReferenceEncoding.RELATIVE_OFFSET


@dataclass(frozen=True, slots=True)
class SentinelCodec:
    """Source tokens used for unused or keep-current transform operands."""

    unused_int: str | None
    unused_float: str | None
    keep_current_float: str | None = None
    keep_current_float_aliases: tuple[str, ...] = ()

    def is_unused_int(self, value: object) -> bool:
        return self.unused_int is not None and str(value).strip() == self.unused_int

    def is_unused_float(self, value: object) -> bool:
        return self.unused_float is not None and str(value).strip() == self.unused_float

    def is_keep_current_float(self, value: object) -> bool:
        token = str(value).strip()
        return token == self.keep_current_float or token in self.keep_current_float_aliases


@dataclass(frozen=True, slots=True)
class TransformForm:
    """One concrete source/target encoding of a canonical transform write."""

    opcode: int
    write_kind: str
    parameter_set: str
    operand_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TransformDialect:
    """Bullet-manager opcodes and transform-program execution rules."""

    name: str
    mode_encoding: str
    index_model: str
    manager_reset_opcode: int | None = None
    fire_opcode: int | None = None
    forms: tuple[TransformForm, ...] = ()
    copy_opcode: int | None = None
    append_cursor_decrement_opcode: int | None = None
    uses_append_cursor: bool = False
    requires_contiguous_indices: bool = False
    supports_channels: bool = False

    @property
    def transform_replace_opcodes(self) -> tuple[int, ...]:
        return tuple(form.opcode for form in self.forms if form.write_kind == "replace")

    @property
    def transform_append_opcodes(self) -> tuple[int, ...]:
        return tuple(form.opcode for form in self.forms if form.write_kind == "append")

    def form_for_opcode(self, opcode: int) -> TransformForm | None:
        return next((form for form in self.forms if form.opcode == opcode), None)

    def form_for_write(self, write_kind: str, parameter_set: str) -> TransformForm | None:
        return next(
            (
                form
                for form in self.forms
                if form.write_kind == write_kind and form.parameter_set == parameter_set
            ),
            None,
        )

    def is_transform_replace(self, opcode: int) -> bool:
        return opcode in self.transform_replace_opcodes

    def is_transform_append(self, opcode: int) -> bool:
        return opcode in self.transform_append_opcodes


@dataclass(frozen=True, slots=True)
class BulletDialect:
    """Opcode roles for the persistent bullet-manager state machine."""

    name: str
    operations: tuple[tuple[int, str], ...] = ()
    macro_modes: tuple[tuple[int, str], ...] = ()
    signatures: tuple[tuple[int, str], ...] = ()
    implicit_manager: bool = False

    def operation_for(self, opcode: int) -> str | None:
        return next((operation for candidate, operation in self.operations if candidate == opcode), None)

    def macro_mode_for(self, opcode: int) -> str | None:
        return next((mode for candidate, mode in self.macro_modes if candidate == opcode), None)

    def signature_for(self, opcode: int) -> str | None:
        return next((signature for candidate, signature in self.signatures if candidate == opcode), None)

    def is_bullet_opcode(self, opcode: int) -> bool:
        return self.operation_for(opcode) is not None

    def opcodes_for_operation(self, operation: str) -> tuple[int, ...]:
        return tuple(opcode for opcode, candidate in self.operations if candidate == operation)


@dataclass(frozen=True, slots=True)
class GameProfile:
    """Stable profile metadata consumed by lifters and target lowerers."""

    game: str
    generation: str
    opcode_family: str
    capabilities: frozenset[str]
    sentinels: SentinelCodec
    bullet_dialect: BulletDialect
    transform_dialect: TransformDialect
    routine_dialect: RoutineDialect
    variable_dialect: VariableDialect
    extension_namespace: str

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities


UNKNOWN_SENTINELS = SentinelCodec(None, None)
FIRST_GEN_SENTINELS = SentinelCodec("-1", "-1.0f")
MODERN_SENTINELS = SentinelCodec("-999999", "-999999.0f", "-999999.0f")
TH18_SENTINELS = SentinelCodec("-9999994", "-9999994.0f", "-9999994.0f")
TH13_SENTINELS = SentinelCodec(
    "-999999",
    "-999999.0f",
    "-999.0f",
    ("-999999.0f",),
)

UNKNOWN_ROUTINES = RoutineDialect(
    "unknown",
    RoutineCallEncoding.UNKNOWN,
    RoutineLocalEncoding.UNKNOWN,
    StackReferenceEncoding.UNKNOWN,
    RoutineSyntaxEncoding.UNKNOWN,
)
FIRST_GEN_ROUTINES = RoutineDialect(
    "first_gen_indexed",
    RoutineCallEncoding.INDEXED_INSTRUCTION,
    RoutineLocalEncoding.FIXED_REGISTER,
    StackReferenceEncoding.NONE,
    RoutineSyntaxEncoding.LEGACY_INSTRUCTIONS,
)
MODERN_ROUTINES = RoutineDialect(
    "modern_named_stack",
    RoutineCallEncoding.NAMED_STACK,
    RoutineLocalEncoding.NAMED_STACK,
    StackReferenceEncoding.NONE,
    RoutineSyntaxEncoding.STACK_EXPRESSIONS,
)
RELATIVE_STACK_ROUTINES = RoutineDialect(
    "modern_relative_stack",
    RoutineCallEncoding.NAMED_STACK,
    RoutineLocalEncoding.NAMED_STACK,
    StackReferenceEncoding.RELATIVE_OFFSET,
    RoutineSyntaxEncoding.STACK_EXPRESSIONS,
)

UNKNOWN_TRANSFORMS = TransformDialect("unknown", "unknown", "unknown")
TH06_TRANSFORMS = TransformDialect(
    "th06_legacy",
    "opaque",
    "implicit",
    forms=(
        TransformForm(82, "legacy_config", "opaque", ("mode", "a", "b", "c", "r", "s", "m", "n")),
    ),
)
TH07_TRANSFORMS = TransformDialect(
    "th07",
    "th07_bitmask",
    "explicit_contiguous",
    forms=(
        TransformForm(79, "replace", "base", ("index", "mode", "channel", "a", "b", "r", "s")),
    ),
    requires_contiguous_indices=True,
    supports_channels=True,
)
TH08_TRANSFORMS = TransformDialect(
    "th08",
    "th08_bitmask",
    "explicit_contiguous",
    forms=(
        TransformForm(111, "replace", "base", ("index", "mode", "channel", "a", "b", "r", "s")),
    ),
    requires_contiguous_indices=True,
    supports_channels=True,
)
TH10_TRANSFORMS = TransformDialect(
    "th10",
    "th10_bitmask",
    "explicit_contiguous",
    manager_reset_opcode=400,
    fire_opcode=401,
    forms=(
        TransformForm(409, "replace", "base", ("manager", "index", "channel", "mode", "a", "b", "r", "s")),
    ),
    copy_opcode=411,
    requires_contiguous_indices=True,
    supports_channels=True,
)
# TH11 keeps the TH10 manager opcodes but follows TH12 transform modes.
TH11_TRANSFORMS = TransformDialect(
    "th11_th12_compatible",
    "th12_bitmask",
    "explicit_contiguous",
    manager_reset_opcode=400,
    fire_opcode=401,
    forms=(
        TransformForm(409, "replace", "base", ("manager", "index", "channel", "mode", "a", "b", "r", "s")),
    ),
    copy_opcode=411,
    requires_contiguous_indices=True,
    supports_channels=True,
)
TH12_TRANSFORMS = TransformDialect(
    "th12",
    "th12_bitmask",
    "explicit_contiguous",
    manager_reset_opcode=500,
    fire_opcode=501,
    forms=(
        TransformForm(509, "replace", "base", ("manager", "index", "channel", "mode", "a", "b", "r", "s")),
    ),
    copy_opcode=511,
    requires_contiguous_indices=True,
    supports_channels=True,
)
# 609/610 replace explicit indices; 611/612 append through a cursor.
TH13_TRANSFORMS = TransformDialect(
    "th13_plus",
    "th13_plus_bitmask",
    "explicit_replace_and_append_cursor",
    manager_reset_opcode=600,
    fire_opcode=601,
    forms=(
        TransformForm(609, "replace", "base", ("manager", "index", "channel", "mode", "a", "b", "r", "s")),
        TransformForm(610, "replace", "extended", ("manager", "index", "channel", "mode", "a", "b", "c", "d", "r", "s", "m", "n")),
        TransformForm(611, "append", "base", ("manager", "channel", "mode", "a", "b", "r", "s")),
        TransformForm(612, "append", "extended", ("manager", "channel", "mode", "a", "b", "c", "d", "r", "s", "m", "n")),
    ),
    copy_opcode=614,
    uses_append_cursor=True,
    requires_contiguous_indices=True,
    supports_channels=True,
)
TH14_PLUS_TRANSFORMS = TransformDialect(
    "th14_plus",
    "th13_plus_bitmask",
    "explicit_replace_and_append_cursor",
    manager_reset_opcode=600,
    fire_opcode=601,
    forms=TH13_TRANSFORMS.forms,
    copy_opcode=614,
    append_cursor_decrement_opcode=641,
    uses_append_cursor=True,
    requires_contiguous_indices=True,
    supports_channels=True,
)

MACRO_MODES = (
    "aimed_fan",
    "fan",
    "aimed_ring",
    "ring",
    "offset_aimed_ring",
    "offset_ring",
    "random_angle",
    "random_speed",
    "random_angle_speed",
)


def _old_bullet_dialect(
    name: str,
    macro_start: int,
    auto: int,
    auto_random_delay: int,
    defer: int,
    enable: int,
    immediate: int,
    offset: int,
    transform: int,
    clear: int,
    sound: int,
    transform_operation: str,
    macro_signature: str,
    offset_signature: str,
    transform_signature: str,
) -> BulletDialect:
    macros = tuple((macro_start + index, mode) for index, mode in enumerate(MACRO_MODES))
    operations = tuple((opcode, "bullet.macro.configure") for opcode, _mode in macros) + (
        (auto, "bullet.auto_fire.schedule"),
        (auto_random_delay, "bullet.auto_fire.schedule_random_delay"),
        (defer, "bullet.fire.defer"),
        (enable, "bullet.fire.enable"),
        (immediate, "bullet.fire.immediate"),
        (offset, "bullet.origin.offset.set"),
        (transform, transform_operation),
        (clear, "bullet.clear_all"),
        (sound, "bullet.sounds.set"),
    )
    signatures = tuple((opcode, macro_signature) for opcode, _mode in macros) + (
        (auto, "S"),
        (auto_random_delay, "S"),
        (defer, ""),
        (enable, ""),
        (immediate, ""),
        (offset, offset_signature),
        (transform, transform_signature),
        (clear, ""),
        (sound, "SS" if name != "th06" else "S"),
    )
    return BulletDialect(name, operations, macros, signatures, implicit_manager=True)


TH06_BULLETS = _old_bullet_dialect(
    "th06", 67, 76, 77, 78, 79, 80, 81, 82, 83, 84, "bullet.transform.legacy_config", "ssSSffffS", "fff", "SSSSffff"
)
TH07_BULLETS = _old_bullet_dialect(
    "th07", 64, 73, 74, 75, 76, 77, 78, 79, 80, 81, "bullet.transform.replace", "ssSSffffS", "fff", "SSSSSff"
)
TH08_BULLETS = _old_bullet_dialect(
    "th08", 96, 105, 106, 107, 108, 109, 110, 111, 112, 113, "bullet.transform.replace", "SSSSffffS", "ff", "SSSSSff"
)


def _manager_bullet_dialect(
    name: str,
    base: int,
    replace: tuple[int, ...],
    append: tuple[int, ...] = (),
    extra: tuple[tuple[int, str], ...] = (),
) -> BulletDialect:
    common = (
        (base, "bullet.manager.reset"),
        (base + 1, "bullet.fire"),
        (base + 2, "bullet.visual.set"),
        (base + 3, "bullet.origin.offset.set"),
        (base + 4, "bullet.formation.angles.set"),
        (base + 5, "bullet.formation.speeds.set"),
        (base + 6, "bullet.formation.counts.set"),
        (base + 7, "bullet.formation.set"),
        (base + 8, "bullet.sounds.set"),
    )
    transforms = tuple((opcode, "bullet.transform.replace") for opcode in replace) + tuple(
        (opcode, "bullet.transform.append") for opcode in append
    )
    return BulletDialect(name, common + transforms + extra)


TH10_BULLETS = _manager_bullet_dialect(
    "th10_th11",
    400,
    (409,),
    extra=(
        (410, "bullet.clear_all"),
        (411, "bullet.manager.copy"),
        (420, "bullet.cancel_radius"),
        (421, "bullet.clear_radius"),
        (422, "bullet.formation.speeds.by_rank"),
        (423, "bullet.formation.speeds.by_rank"),
        (424, "bullet.formation.speeds.by_rank"),
        (425, "bullet.formation.counts.by_rank"),
        (426, "bullet.formation.counts.by_rank"),
        (427, "bullet.formation.counts.by_rank"),
        (435, "bullet.formation.speeds.by_difficulty"),
        (436, "bullet.formation.counts.by_difficulty"),
        (437, "bullet.origin.polar_offset.set"),
        (438, "bullet.origin.distance.set"),
        (439, "bullet.origin.absolute.set"),
    ),
)
TH12_BULLETS = _manager_bullet_dialect(
    "th12",
    500,
    (509,),
    extra=(
        (510, "bullet.clear_all"),
        (511, "bullet.manager.copy"),
        (512, "bullet.cancel_radius"),
        (513, "bullet.clear_radius"),
        (514, "bullet.formation.speeds.by_rank"),
        (515, "bullet.formation.speeds.by_rank"),
        (516, "bullet.formation.speeds.by_rank"),
        (517, "bullet.formation.counts.by_rank"),
        (518, "bullet.formation.counts.by_rank"),
        (519, "bullet.formation.counts.by_rank"),
        (521, "bullet.formation.speeds.by_difficulty"),
        (522, "bullet.formation.counts.by_difficulty"),
        (523, "bullet.origin.polar_offset.set"),
        (524, "bullet.origin.distance.set"),
        (525, "bullet.origin.absolute.set"),
    ),
)
TH13_BULLETS = _manager_bullet_dialect(
    "th13_plus",
    600,
    (609, 610),
    (611, 612),
    extra=(
        (613, "bullet.clear_all"),
        (614, "bullet.manager.copy"),
        (615, "bullet.cancel_radius"),
        (616, "bullet.clear_radius"),
        (617, "bullet.formation.speeds.by_rank"),
        (618, "bullet.formation.speeds.by_rank"),
        (619, "bullet.formation.speeds.by_rank"),
        (620, "bullet.formation.counts.by_rank"),
        (621, "bullet.formation.counts.by_rank"),
        (622, "bullet.formation.counts.by_rank"),
        (624, "bullet.formation.speeds.by_difficulty"),
        (625, "bullet.formation.counts.by_difficulty"),
        (626, "bullet.origin.polar_offset.set"),
        (627, "bullet.origin.distance.set"),
        (628, "bullet.origin.absolute.set"),
        (640, "bullet.transform.string_operand.patch"),
    ),
)
TH14_PLUS_BULLETS = BulletDialect(
    "th14_plus",
    TH13_BULLETS.operations + ((641, "bullet.transform.append_cursor.decrement"),),
)
UNKNOWN_BULLETS = BulletDialect("unknown")

_EARLY_FIRST_GEN_CAPABILITIES = frozenset(
    {
        CAP_BULLET_MACRO,
        CAP_LASER_BASIC,
    }
)
_TH07_CAPABILITIES = _EARLY_FIRST_GEN_CAPABILITIES | {
    CAP_BULLET_TRANSFORM,
    CAP_TRANSFORM_CHANNELS,
    CAP_TRANSFORM_INDEXED_REPLACE,
}
_TH08_CAPABILITIES = _TH07_CAPABILITIES
_MANAGER_CAPABILITIES = frozenset(
    {
        CAP_BULLET_MANAGER,
        CAP_BULLET_TRANSFORM,
        CAP_TRANSFORM_CHANNELS,
        CAP_TRANSFORM_INDEXED_REPLACE,
        CAP_LASER_BASIC,
        CAP_RELATIVE_MOTION,
    }
)
_TH12_CAPABILITIES = _MANAGER_CAPABILITIES | {
    CAP_LASER_INFINITE,
    CAP_LASER_CURVE,
}
_TH13_CAPABILITIES = _TH12_CAPABILITIES | {
    CAP_TRANSFORM_APPEND,
    CAP_TRANSFORM_APPEND_CURSOR,
    CAP_ENEMY_INTERACTION,
    CAP_TRANSFORM_SPAWN_BULLET_PACKED_V13,
    CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE,
}
_TH14_PLUS_CAPABILITIES = _TH13_CAPABILITIES | {
    CAP_TRANSFORM_CURSOR_DECREMENT,
    CAP_RECT_COLLISION,
}
_TH14_CAPABILITIES = (
    _TH14_PLUS_CAPABILITIES
    - {CAP_TRANSFORM_SPAWN_BULLET_PACKED_V13}
    | {CAP_TRANSFORM_SPAWN_BULLET_EXPANDED}
)
_TH15_CAPABILITIES = (_TH14_CAPABILITIES - {CAP_TRANSFORM_PRESERVE_DIRECTION_SUBTYPE}) | {
    CAP_TRANSFORM_SPAWN_LASER,
    CAP_TRANSFORM_RANDOM_SPEED_SUBTYPE,
}
_TH16_CAPABILITIES = _TH15_CAPABILITIES | {
    CAP_TRANSFORM_HITBOX_RADIUS,
    CAP_TRANSFORM_JUMP_LOOP_COUNT,
    CAP_TRANSFORM_HIGHLIGHT_REMOVE,
}
_TH17_CAPABILITIES = _TH16_CAPABILITIES | {CAP_TRANSFORM_HOMING_VELOCITY_BLEND}


def _profile(
    game: str,
    generation: str,
    opcode_family: str,
    capabilities: frozenset[str],
    sentinels: SentinelCodec,
    bullet_dialect: BulletDialect,
    transform_dialect: TransformDialect,
    routine_dialect: RoutineDialect,
) -> GameProfile:
    return GameProfile(
        game=game,
        generation=generation,
        opcode_family=opcode_family,
        capabilities=capabilities,
        sentinels=sentinels,
        bullet_dialect=bullet_dialect,
        transform_dialect=transform_dialect,
        routine_dialect=routine_dialect,
        variable_dialect=variable_dialect_for_game(game),
        extension_namespace=game,
    )


_PROFILES: dict[str, GameProfile] = {
    # These games share a generation, not an opcode layout.
    "th06": _profile(
        "th06",
        "first",
        "th06",
        _EARLY_FIRST_GEN_CAPABILITIES,
        FIRST_GEN_SENTINELS,
        TH06_BULLETS,
        TH06_TRANSFORMS,
        FIRST_GEN_ROUTINES,
    ),
    "th07": _profile(
        "th07",
        "first",
        "th07",
        _TH07_CAPABILITIES,
        FIRST_GEN_SENTINELS,
        TH07_BULLETS,
        TH07_TRANSFORMS,
        FIRST_GEN_ROUTINES,
    ),
    "th08": _profile(
        "th08",
        "first",
        "th08",
        _TH08_CAPABILITIES,
        FIRST_GEN_SENTINELS,
        TH08_BULLETS,
        TH08_TRANSFORMS,
        FIRST_GEN_ROUTINES,
    ),
}
_PROFILES.update(
    {
        "th10": _profile(
            "th10",
            "second",
            "th10_th11",
            _MANAGER_CAPABILITIES,
            MODERN_SENTINELS,
            TH10_BULLETS,
            TH10_TRANSFORMS,
            MODERN_ROUTINES,
        ),
        "th11": _profile(
            "th11",
            "second",
            "th10_th11",
            _MANAGER_CAPABILITIES,
            MODERN_SENTINELS,
            TH10_BULLETS,
            TH11_TRANSFORMS,
            MODERN_ROUTINES,
        ),
    }
)
_PROFILES.update(
    {
        game: _profile(
            game,
            "third",
            "th12",
            _TH12_CAPABILITIES,
            MODERN_SENTINELS,
            TH12_BULLETS,
            TH12_TRANSFORMS,
            MODERN_ROUTINES,
        )
        for game in ("th12", "th125", "th128")
    }
)
_PROFILES["th13"] = _profile(
    "th13",
    "fourth",
    "th13_plus",
    _TH13_CAPABILITIES,
    TH13_SENTINELS,
    TH13_BULLETS,
    TH13_TRANSFORMS,
    RELATIVE_STACK_ROUTINES,
)
for game in ("th14", "th143"):
    _PROFILES[game] = _profile(
        game,
        "fourth",
        "th13_plus",
        _TH14_CAPABILITIES,
        MODERN_SENTINELS,
        TH14_PLUS_BULLETS,
        TH14_PLUS_TRANSFORMS,
        RELATIVE_STACK_ROUTINES,
    )
_PROFILES["th15"] = _profile(
    "th15", "fourth", "th13_plus", _TH15_CAPABILITIES, MODERN_SENTINELS,
    TH14_PLUS_BULLETS, TH14_PLUS_TRANSFORMS, RELATIVE_STACK_ROUTINES,
)
for game in ("th16", "th165"):
    _PROFILES[game] = _profile(
        game, "fourth", "th13_plus", _TH16_CAPABILITIES, MODERN_SENTINELS,
        TH14_PLUS_BULLETS, TH14_PLUS_TRANSFORMS, RELATIVE_STACK_ROUTINES,
    )
for game in ("th17", "th185"):
    _PROFILES[game] = _profile(
        game, "fourth", "th13_plus", _TH17_CAPABILITIES, MODERN_SENTINELS,
        TH14_PLUS_BULLETS, TH14_PLUS_TRANSFORMS, RELATIVE_STACK_ROUTINES,
    )
_PROFILES["th18"] = _profile(
    "th18",
    "fourth",
    "th13_plus",
    _TH17_CAPABILITIES,
    TH18_SENTINELS,
    TH14_PLUS_BULLETS,
    TH14_PLUS_TRANSFORMS,
    RELATIVE_STACK_ROUTINES,
)

GAME_PROFILES: Mapping[str, GameProfile] = MappingProxyType(_PROFILES)
UNKNOWN_GAME_PROFILE = GameProfile(
    game="unknown",
    generation="unknown",
    opcode_family="unknown",
    capabilities=frozenset(),
    sentinels=UNKNOWN_SENTINELS,
    bullet_dialect=UNKNOWN_BULLETS,
    transform_dialect=UNKNOWN_TRANSFORMS,
    routine_dialect=UNKNOWN_ROUTINES,
    variable_dialect=variable_dialect_for_game("unknown"),
    extension_namespace="unknown",
)

def profile_for_game(game: str) -> GameProfile:
    """Look up a game profile, falling back to a capability-empty profile."""

    return GAME_PROFILES.get(normalize_game_id(game), UNKNOWN_GAME_PROFILE)


def supports_capability(game: str, capability: str) -> bool:
    """Return whether a game's profile advertises a lowering capability."""

    return profile_for_game(game).supports(capability)
