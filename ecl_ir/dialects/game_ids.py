"""Canonical game identifiers shared by parsers and dialect registries."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping


GAME_ID_ALIASES: Mapping[str, str] = MappingProxyType(
    {
        "th6": "th06",
        "th7": "th07",
        "th8": "th08",
        "th12.5": "th125",
        "th12_5": "th125",
        "th12.8": "th128",
        "th12_8": "th128",
        "th14.3": "th143",
        "th14_3": "th143",
        "th16.5": "th165",
        "th16_5": "th165",
        "th18.5": "th185",
        "th18_5": "th185",
    }
)

KNOWN_GAME_IDS = frozenset(
    {
        "th06",
        "th07",
        "th08",
        "th09",
        "th10",
        "th11",
        "th12",
        "th125",
        "th128",
        "th13",
        "th14",
        "th143",
        "th15",
        "th16",
        "th165",
        "th17",
        "th18",
        "th185",
    }
)


def normalize_game_id(game: str) -> str:
    normalized = str(game).strip().lower()
    return GAME_ID_ALIASES.get(normalized, normalized)


__all__ = ["GAME_ID_ALIASES", "KNOWN_GAME_IDS", "normalize_game_id"]
