from __future__ import annotations

from dataclasses import dataclass

from .semantics import generation_for_game


ANM_RESOURCE_OPERATIONS = frozenset(
    {
        "anm.select",
        "anm.play",
        "anm.play_abs",
        "anm.play_attack",
        "anm.play_high",
        "anm.play_pos",
        "anm.play_rotate",
        "anm.familiar",
        "anm.selected_play",
        "anm.set",
        "anm.set_boss",
        "anm.set_boss_ex",
        "anm.set_boss_ex2",
        "anm.set_boss_slot",
        "anm.set_ex",
        "anm.set_ex2",
        "anm.set_main",
        "anm.set_slot",
        "anm.set_sprite",
        "anm.on_et",
    }
)


def operation_uses_anm_resource(operation: str) -> bool:
    return operation in ANM_RESOURCE_OPERATIONS


@dataclass(frozen=True)
class AnmScriptRef:
    bank: int
    script: int


@dataclass(frozen=True)
class AnmRoleCatalog:
    select_banks: tuple[int, ...]
    set_scripts: dict[int, tuple[int, ...]]
    play_scripts: dict[int, tuple[int, ...]]
    main_scripts: dict[int, tuple[int, ...]] | None = None
    sprite_scripts: dict[int, tuple[int, ...]] | None = None

    def has_bank(self, bank: int) -> bool:
        return bank in self.select_banks or bank in self.set_scripts or bank in self.play_scripts

    def has_set_script(self, bank: int, script: int, kind: str = "set") -> bool:
        return script in self.scripts_for_bank(bank, kind)

    def scripts_for_bank(self, bank: int, kind: str = "set") -> tuple[int, ...]:
        if kind == "main" and self.main_scripts is not None:
            return self.main_scripts.get(bank, ())
        if kind == "sprite" and self.sprite_scripts is not None:
            return self.sprite_scripts.get(bank, ())
        return self.set_scripts.get(bank, ())


def _r(*values: int) -> tuple[int, ...]:
    return tuple(values)


ANM_CATALOG: dict[str, dict[str, AnmRoleCatalog]] = {
    "th08": {
        "stage": AnmRoleCatalog((), {}, {}),
        "boss": AnmRoleCatalog((), {}, {}),
    },
    "th10": {
        "stage": AnmRoleCatalog(
            _r(0, 1, 2),
            {
                0: _r(370),
                1: _r(5, 40, 45, 46, 47, 48, 370),
                2: _r(0, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 26, 39),
            },
            {
                0: _r(354, 409, 410, 411, 412, 413, 414, 419, 420, 428, 429, 431, 432, 433, 442, 444),
                2: _r(12, 13),
            },
        ),
        "boss": AnmRoleCatalog((), {}, {}),
    },
    "th11": {
        "stage": AnmRoleCatalog(
            _r(0, 1, 2),
            {
                0: _r(92, 170, 175),
                1: _r(40, 45, 46, 47, 48, 63, 64, 65, 66, 67, 68, 102, 103, 108),
                2: _r(0, 1, 6, 7, 12, 17),
            },
            {0: _r(76, 78, 81, 87, 131, 132, 141, 142, 171, 172, 173, 179, 190), 2: _r(19)},
        ),
        "boss": AnmRoleCatalog(
            _r(0, 1, 2),
            {
                0: _r(92, 170, 178, 181, 183, 185, 187, 192, 195),
                1: _r(20, 45, 46, 47, 48, 109, 113, 119),
                2: _r(0, 5, 7, 8, 11, 14, 23, 27, 35),
            },
            {0: _r(76, 78, 131, 141, 142, 176, 197), 2: _r(24)},
        ),
    },
    "th12": {
        "stage": AnmRoleCatalog(
            _r(0, 1, 2, 3),
            {
                0: _r(95, 158),
                1: _r(40, 45, 50, 51, 52, 53, 98, 99),
                2: _r(0, 7, 8, 9, 11, 12, 19, 22, 25, 26, 28, 29, 30, 35, 39, 41, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 82),
                3: _r(0),
            },
            {0: _r(79, 101, 102, 119, 129, 130, 212, 213, 214), 1: _r(103, 105, 141), 2: _r(7, 8)},
        ),
        "boss": AnmRoleCatalog(
            _r(0, 1, 2),
            {0: _r(95, 158), 1: _r(0, 142, 143, 144, 145), 2: _r(0, 7, 21, 22, 53)},
            {0: _r(79, 119, 129, 130), 2: _r(23, 24)},
        ),
    },
    "th13": {
        "stage": AnmRoleCatalog(
            _r(2, 3),
            {2: _r(0, 5, 20, 25, 30, 35, 40, 53, 56, 65, 71, 78, 80, 82, 85, 88, 91), 3: _r(0)},
            {0: _r(25), 1: _r(63, 91, 92, 93, 94, 95, 98), 3: _r(0)},
        ),
        "boss": AnmRoleCatalog(
            _r(0, 1, 2, 3, 4, 5),
            {0: _r(235), 1: _r(53, 67, 105, 109, 113, 117, 129), 2: _r(82), 3: _r(0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15), 4: _r(0, 9, 10), 5: _r(0, 6, 7)},
            {0: _r(0, 25), 1: _r(25, 61, 63, 65, 67, 71, 76, 78, 82, 86, 96, 97, 98), 3: _r(0), 4: _r(0), 5: _r(0)},
        ),
    },
    "th14": {
        "stage": AnmRoleCatalog(
            _r(2),
            {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40, 53, 56, 59, 79, 80, 83, 87, 88, 93, 96, 99)},
            {1: _r(101, 102, 103, 105)},
        ),
        "boss": AnmRoleCatalog(
            _r(1, 2, 3, 4, 5),
            {1: _r(70, 106, 111, 115, 119, 123, 131), 2: _r(79, 87, 91), 3: _r(0, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16), 4: _r(0), 5: _r(0)},
            {0: _r(27), 1: _r(39, 62, 63, 64, 70, 72, 74, 80, 85), 3: _r(0, 19), 4: _r(0)},
        ),
    },
    "th15": {
        "stage": AnmRoleCatalog(
            _r(2),
            {2: _r(0, 5, 20, 25, 35, 40, 53, 56, 59, 62, 79, 87, 93, 96, 99, 147, 152, 157, 162, 167)},
            {1: _r(102, 103, 106)},
        ),
        "boss": AnmRoleCatalog(
            _r(1, 2, 3, 4, 5),
            {1: _r(107, 112, 116, 120, 124, 132), 2: _r(53, 59, 93, 99, 105), 3: _r(0, 6, 7, 14, 20, 21, 22, 23, 24), 4: _r(0), 5: _r(0, 6)},
            {0: _r(28), 1: _r(32, 63, 64, 65, 73, 75, 79, 86, 88, 90), 3: _r(0), 5: _r(0)},
        ),
    },
    "th16": {
        "stage": AnmRoleCatalog(
            _r(2),
            {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40, 53, 56, 79, 87, 93, 96, 99, 152, 157, 162, 167)},
            {1: _r(75, 102, 103, 104, 106, 107), 3: _r(18, 19, 20, 21, 22)},
        ),
        "boss": AnmRoleCatalog(
            _r(1, 2, 3, 4, 5),
            {1: _r(79, 83, 86, 88, 90, 94, 107, 108, 113, 117, 120, 121, 125), 2: _r(53, 56), 3: _r(0, 6, 7), 4: _r(0), 5: _r(0)},
            {0: _r(28), 1: _r(32, 63, 64, 65, 71, 73, 75, 79, 86, 88, 96, 98), 3: _r(0, 6)},
        ),
    },
    "th17": {
        "stage": AnmRoleCatalog(
            _r(2),
            {2: _r(0, 5, 10, 15, 20, 30, 35, 40, 53, 56, 59, 62, 79, 87, 91, 93, 99, 172, 177, 202, 212)},
            {1: _r(102, 103, 104)},
        ),
        "boss": AnmRoleCatalog(
            _r(1, 2, 3, 4),
            {1: _r(103, 105, 110, 114), 2: _r(79, 91, 99), 3: _r(0, 6, 7, 8), 4: _r(0)},
            {0: _r(28), 1: _r(32, 64, 65, 71, 73, 75, 79, 86, 88, 96), 3: _r(0), 4: _r(0)},
        ),
    },
    "th18": {
        "stage": AnmRoleCatalog(
            _r(2),
            {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40, 53, 56, 59, 62, 65, 68, 77, 80, 91, 99, 103, 105, 111, 114, 184, 189, 214, 224)},
            {1: _r(102, 103, 104), 7: _r(3, 4)},
        ),
        "boss": AnmRoleCatalog(
            _r(1, 2, 3, 4, 5),
            {1: _r(105, 110, 114), 2: _r(91, 251), 3: _r(0, 6, 22), 4: _r(0), 5: _r(0)},
            {0: _r(28), 1: _r(32, 64, 65, 73, 75, 77, 79, 81, 86, 88, 94, 96), 3: _r(0)},
        ),
    },
}

ANM_SET_KIND_CATALOG: dict[str, dict[str, dict[str, dict[int, tuple[int, ...]]]]] = {
    "th10": {
        "stage": {
            "main": {1: _r(5, 40, 45, 46, 47, 48), 2: _r(0, 5, 6, 7, 9, 13, 19, 20)},
            "sprite": {0: _r(370), 1: _r(45, 46, 47, 48, 370), 2: _r(0, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 26, 39)},
        },
        "boss": {"main": {}, "sprite": {}},
    },
    "th11": {
        "stage": {
            "main": {1: _r(40, 45, 46, 47, 48), 2: _r(0, 1, 7, 12)},
            "sprite": {0: _r(92, 170, 175), 1: _r(45, 46, 47, 48, 63, 64, 65, 66, 67, 68, 102, 103, 108), 2: _r(0, 6, 12, 17)},
        },
        "boss": {
            "main": {1: _r(20), 2: _r(0, 7, 11, 14, 27)},
            "sprite": {0: _r(92, 170, 178, 181, 183, 185, 187, 192, 195), 1: _r(45, 46, 47, 48, 109, 113, 119), 2: _r(5, 8, 14, 23, 35)},
        },
    },
    "th12": {
        "stage": {
            "main": {1: _r(40, 45, 50, 51, 52, 53, 98, 99), 2: _r(0, 8, 26, 30, 39, 41), 3: _r(0)},
            "sprite": {0: _r(95, 158), 1: _r(50, 51, 52, 53, 98, 99), 2: _r(0, 7, 8, 9, 11, 12, 19, 22, 25, 26, 28, 29, 35, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 82)},
        },
        "boss": {
            "main": {1: _r(0), 2: _r(0)},
            "sprite": {0: _r(95, 158), 1: _r(142, 143, 144, 145), 2: _r(7, 21, 22, 53)},
        },
    },
    "th13": {
        "stage": {
            "main": {2: _r(0, 5, 20, 25, 30, 35, 40), 3: _r(0)},
            "sprite": {2: _r(53, 56, 65, 71, 78, 80, 82, 85, 88, 91)},
        },
        "boss": {
            "main": {3: _r(0, 15), 4: _r(0), 5: _r(0)},
            "sprite": {0: _r(235), 1: _r(53, 67, 105, 109, 113, 117, 129), 2: _r(82), 3: _r(0, 5, 6, 7, 8, 9, 10, 11, 12, 13), 4: _r(9, 10), 5: _r(6, 7)},
        },
    },
    "th14": {
        "stage": {
            "main": {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40)},
            "sprite": {2: _r(53, 56, 59, 79, 80, 83, 87, 88, 93, 96, 99)},
        },
        "boss": {
            "main": {3: _r(0, 8, 14), 4: _r(0), 5: _r(0)},
            "sprite": {1: _r(70, 106, 111, 115, 119, 123, 131), 2: _r(79, 87, 91), 3: _r(0, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16)},
        },
    },
    "th15": {
        "stage": {
            "main": {2: _r(0, 5, 20, 25, 35, 40, 147, 152, 157, 162, 167)},
            "sprite": {2: _r(53, 56, 59, 62, 79, 87, 93, 96, 99)},
        },
        "boss": {
            "main": {3: _r(0, 7, 14), 4: _r(0), 5: _r(0)},
            "sprite": {1: _r(107, 112, 116, 120, 124, 132), 2: _r(53, 59, 93, 99, 105), 3: _r(0, 6, 20, 21, 22, 23, 24), 5: _r(6)},
        },
    },
    "th16": {
        "stage": {
            "main": {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40, 152, 157, 162, 167)},
            "sprite": {2: _r(53, 56, 79, 87, 93, 96, 99)},
        },
        "boss": {
            "main": {3: _r(0), 4: _r(0), 5: _r(0)},
            "sprite": {1: _r(79, 83, 86, 88, 90, 94, 107, 108, 113, 117, 120, 121, 125), 2: _r(53, 56), 3: _r(0, 6, 7), 4: _r(0)},
        },
    },
    "th17": {
        "stage": {
            "main": {2: _r(0, 5, 10, 15, 20, 30, 35, 40, 172, 177, 202, 212)},
            "sprite": {2: _r(53, 56, 59, 62, 79, 87, 91, 93, 99)},
        },
        "boss": {
            "main": {3: _r(0), 4: _r(0)},
            "sprite": {1: _r(103, 105, 110, 114), 2: _r(79, 91, 99), 3: _r(0, 6, 7, 8)},
        },
    },
    "th18": {
        "stage": {
            "main": {2: _r(0, 5, 10, 15, 20, 25, 30, 35, 40, 184, 189, 214, 224)},
            "sprite": {2: _r(53, 56, 59, 62, 65, 68, 77, 80, 91, 99, 103, 105, 111, 114)},
        },
        "boss": {
            "main": {3: _r(0), 4: _r(0), 5: _r(0)},
            "sprite": {1: _r(105, 110, 114), 2: _r(91, 251), 3: _r(0, 6, 22)},
        },
    },
}


SOURCE_BANK_ROLE_MAP: dict[str, dict[int, str]] = {
    "th10": {1: "stage", 2: "boss"},
    "th11": {1: "stage", 2: "boss"},
    "th12": {1: "stage", 2: "boss", 3: "boss"},
    "th13": {2: "stage", 3: "boss"},
    "th14": {2: "stage", 3: "boss"},
    "th15": {2: "stage", 3: "boss"},
    "th16": {2: "stage", 3: "boss"},
    "th17": {2: "stage", 3: "boss"},
    "th18": {2: "stage", 3: "boss"},
}

TARGET_ROLE_BANK: dict[str, dict[str, int]] = {
    "th10": {"stage": 1, "boss": 2},
    "th11": {"stage": 1, "boss": 2},
    "th12": {"stage": 1, "boss": 2},
    "th13": {"stage": 2, "boss": 3},
    "th14": {"stage": 2, "boss": 3},
    "th15": {"stage": 2, "boss": 3},
    "th16": {"stage": 2, "boss": 3},
    "th17": {"stage": 2, "boss": 3},
    "th18": {"stage": 2, "boss": 3},
}

PURPOSE_FALLBACKS: dict[str, tuple[int, ...]] = {
    "main": (0, 5, 6, 7, 20, 25, 30, 35, 40, 50, 53),
    "stage_enemy": (0, 5, 25, 35, 40, 20, 30, 10, 15, 50, 51, 52, 53),
    "stage_blue": (0, 5, 25, 35, 40, 20, 30, 10, 15, 93, 96, 99),
    "stage_green": (35, 40, 25, 5, 0, 20, 30, 10, 15, 93, 96, 99),
    "stage_red": (5, 25, 0, 35, 40, 20, 30, 10, 15, 93, 96, 99),
    "stage_yellow": (40, 35, 25, 5, 0, 20, 30, 10, 15, 93, 96, 99),
    "boss_aux": (6, 7, 0, 5, 14, 20, 21, 22, 23, 24),
    "boss_sprite": (107, 105, 99, 93, 132, 124, 120, 116, 112),
    "boss_sprite_secondary": (116, 120, 112, 132, 124, 107, 105, 99, 93),
    "familiar": (6, 7, 0, 5, 14, 20, 21, 22, 23, 24),
}

SOURCE_SET_PURPOSES: dict[tuple[str, str, str, int, int], str] = {
    ("th10", "stage", "main", 1, 45): "stage_blue",
    ("th10", "stage", "main", 1, 46): "stage_red",
    ("th10", "stage", "main", 1, 47): "stage_green",
    ("th10", "stage", "main", 1, 48): "stage_yellow",
    ("th10", "stage", "sprite", 1, 45): "stage_blue",
    ("th10", "stage", "sprite", 1, 46): "stage_red",
    ("th10", "stage", "sprite", 1, 47): "stage_green",
    ("th10", "stage", "sprite", 1, 48): "stage_yellow",
    ("th10", "boss", "sprite", 2, 370): "boss_sprite",
    ("th11", "stage", "main", 1, 45): "stage_blue",
    ("th11", "stage", "main", 1, 46): "stage_red",
    ("th11", "stage", "main", 1, 47): "stage_green",
    ("th11", "stage", "main", 1, 48): "stage_yellow",
    ("th11", "stage", "sprite", 1, 45): "stage_blue",
    ("th11", "stage", "sprite", 1, 46): "stage_red",
    ("th11", "stage", "sprite", 1, 47): "stage_green",
    ("th11", "stage", "sprite", 1, 48): "stage_yellow",
    ("th11", "boss", "sprite", 2, 370): "boss_sprite",
    ("th12", "stage", "main", 1, 50): "stage_blue",
    ("th12", "stage", "main", 1, 51): "stage_red",
    ("th12", "stage", "main", 1, 52): "stage_green",
    ("th12", "stage", "main", 1, 53): "stage_yellow",
    ("th12", "stage", "sprite", 1, 50): "stage_blue",
    ("th12", "stage", "sprite", 1, 51): "stage_red",
    ("th12", "stage", "sprite", 1, 52): "stage_green",
    ("th12", "stage", "sprite", 1, 53): "stage_yellow",
}

PLAY_PURPOSE_FALLBACKS: dict[str, tuple[int, ...]] = {
    "spawn": (102, 103, 104, 105, 106, 107, 119, 101),
    "stage_spawn": (102, 103, 104, 105, 106, 107, 119, 101),
    "boss_spawn": (28, 32, 63, 64, 65, 73, 75, 79, 86, 88, 90, 119),
    "effect": (102, 103, 104, 105, 106, 107, 79, 119, 129, 130),
}


def role_catalog(game: str, role: str) -> AnmRoleCatalog | None:
    return ANM_CATALOG.get(game, {}).get(role)


def scripts_for_set_kind(game: str, role: str, bank: int, kind: str) -> tuple[int, ...]:
    by_kind = ANM_SET_KIND_CATALOG.get(game, {}).get(role, {}).get(kind, {})
    if bank in by_kind:
        return by_kind[bank]
    catalog = role_catalog(game, role)
    if catalog is None:
        return ()
    return catalog.scripts_for_bank(bank, kind)


def source_bank_role(game: str, bank: int) -> str | None:
    return SOURCE_BANK_ROLE_MAP.get(game, {}).get(bank)


def target_bank_for_role(game: str, role: str) -> int | None:
    bank = TARGET_ROLE_BANK.get(game, {}).get(role)
    catalog = role_catalog(game, role)
    if bank is not None and catalog and catalog.has_bank(bank):
        return bank
    if catalog and catalog.select_banks:
        return catalog.select_banks[0]
    return bank


def remap_anm_bank(source_game: str, target_game: str, source_bank: int, role_hint: str | None = None) -> int:
    role = role_hint or source_bank_role(source_game, source_bank)
    if role:
        target_bank = target_bank_for_role(target_game, role)
        if target_bank is not None:
            return target_bank
    return source_bank


def choose_script(game: str, role: str, purpose: str = "main", preferred: int | None = None, kind: str = "set") -> AnmScriptRef | None:
    catalog = role_catalog(game, role)
    if catalog is None:
        return None
    candidate_banks = list(catalog.select_banks)
    default_bank = target_bank_for_role(game, role)
    if default_bank is not None:
        candidate_banks = [default_bank, *[bank for bank in candidate_banks if bank != default_bank]]
    if preferred is not None:
        for bank in candidate_banks:
            if preferred in scripts_for_set_kind(game, role, bank, kind):
                return AnmScriptRef(bank, preferred)
    for candidate in PURPOSE_FALLBACKS.get(purpose, ()):
        for bank in candidate_banks:
            if candidate in scripts_for_set_kind(game, role, bank, kind):
                return AnmScriptRef(bank, candidate)
    for bank in candidate_banks:
        scripts = scripts_for_set_kind(game, role, bank, kind)
        if scripts:
            return AnmScriptRef(bank, scripts[0])
    return None


def choose_play_script(game: str, role: str, purpose: str = "spawn", preferred: int | None = None) -> AnmScriptRef | None:
    catalog = role_catalog(game, role)
    if catalog is None:
        return None
    candidates: list[tuple[int, int]] = []
    for bank in sorted(catalog.play_scripts):
        for script in catalog.play_scripts[bank]:
            candidates.append((bank, script))
    if not candidates:
        return None
    if preferred is not None:
        for bank, script in candidates:
            if script == preferred:
                return AnmScriptRef(bank, script)
    for script_preference in PLAY_PURPOSE_FALLBACKS.get(purpose, ()):
        for bank, script in candidates:
            if script == script_preference:
                return AnmScriptRef(bank, script)
    bank, script = candidates[0]
    return AnmScriptRef(bank, script)


def remap_play_script(source_game: str, target_game: str, source_bank: int, source_script: int, role_hint: str | None = None, purpose: str = "spawn") -> AnmScriptRef:
    role = role_hint or source_bank_role(source_game, source_bank)
    target_bank = remap_anm_bank(source_game, target_game, source_bank, role)
    catalog = role_catalog(target_game, role or "")
    if catalog and source_script in catalog.play_scripts.get(target_bank, ()):
        return AnmScriptRef(target_bank, source_script)
    chosen = choose_play_script(target_game, role or "", purpose, source_script)
    if chosen is not None:
        return chosen
    return AnmScriptRef(target_bank, source_script)


def remap_set_script(source_game: str, target_game: str, source_bank: int, source_script: int, role_hint: str | None = None, purpose: str = "main", kind: str = "set") -> AnmScriptRef:
    role = role_hint or source_bank_role(source_game, source_bank)
    target_bank = remap_anm_bank(source_game, target_game, source_bank, role)
    scripts = scripts_for_set_kind(target_game, role or "", target_bank, kind)
    if source_script in scripts:
        return AnmScriptRef(target_bank, source_script)
    purpose = SOURCE_SET_PURPOSES.get((source_game, role or "", kind, source_bank, source_script), purpose)
    chosen = choose_script(target_game, role or "", purpose, source_script, kind)
    if chosen is not None:
        return chosen
    return AnmScriptRef(target_bank, source_script)


def format_catalog_scripts(game: str, role: str) -> str:
    catalog = role_catalog(game, role)
    if not catalog:
        return "-"
    parts = []
    for bank in sorted(catalog.set_scripts):
        parts.append(f"{bank}:{_format_ranges(catalog.set_scripts[bank])}")
    return "; ".join(parts) if parts else "-"


def _format_ranges(values: tuple[int, ...]) -> str:
    vals = sorted(set(values))
    ranges: list[str] = []
    i = 0
    while i < len(vals):
        start = prev = vals[i]
        i += 1
        while i < len(vals) and vals[i] == prev + 1:
            prev = vals[i]
            i += 1
        ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return ",".join(ranges)


def target_generation_role_bank(target: str, role: str) -> int | None:
    if generation_for_game(target) == "th06_th08":
        return None
    return target_bank_for_role(target, role)
