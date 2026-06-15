from __future__ import annotations

from pathlib import Path
import re

from .model import EntryAlias, FunctionRewrite, HelperRoutine, Program, ResourcePlan, TimelineRewrite
from .semantics import generation_for_game

STAGE_ENTRY_ALIASES: dict[str, str] = {
    "BGirl00": "MainSub00", "BGirl02": "MainSub01", "BGirl04": "MainSub02", "BGirl05": "MainSub03", "BGirl07": "MainSub04", "BGirl10": "MainSub05",
    "GGirl00": "MainSub00", "GGirl02": "MainSub01", "GGirl04": "MainSub02", "GGirl05": "MainSub03", "GGirl07": "MainSub04", "GGirl10": "MainSub05",
    "RGirl00": "MainSub00", "RGirl02": "MainSub01", "RGirl04": "MainSub02", "RGirl05": "MainSub03", "RGirl07": "MainSub04", "RGirl10": "MainSub05",
    "YGirl00": "MainSub00", "YGirl02": "MainSub01", "YGirl04": "MainSub02", "YGirl05": "MainSub03", "YGirl07": "MainSub04", "YGirl10": "MainSub05",
    "MainSub02b": "MainSub02", "MainSub07b": "MainSub07", "MainSub08": "MainLatter", "MainSub08b": "MainLatter",
    "MainSub09": "MainLatter", "MainSub10": "MainLatter2", "MainSub10b": "MainLatter2", "MainSub11": "MainLatter2",
    "MainSub12": "MainLatter2", "MainSub13": "MainLatter2",
}

STAGE_ENTRY_ANM_PURPOSE: dict[str, dict[str, int | str | None]] = {
    # Script preferences are semantic colors; emitters clamp them through the
    # target game's actually-used stage enemy sprite catalog.
    "B": {"purpose": "stage_enemy", "preferred_script": 50, "z_index": 2, "z_index_after": 0},
    "G": {"purpose": "stage_enemy", "preferred_script": 52, "z_index": 9, "z_index_after": 0},
    "R": {"purpose": "stage_enemy", "preferred_script": 51, "z_index": 1, "z_index_after": 1},
    "Y": {"purpose": "stage_enemy", "preferred_script": 53, "z_index": None, "z_index_after": 0},
}

BULLET_CLEAR_HELPERS = {"Ecl_EtBreak", "Ecl_EtBreak2", "Ecl_EtBreak2_ni", "Ecl_EtBreak_ni"}
BOSS_SCRIPT_FILES = {"st01bs.decl", "st01mbs.decl", "st01mbs2.decl"}


def lift_program_adapters(program: Program) -> list[object]:
    adapters: list[object] = []
    adapters.extend(lift_resource_plan(program))
    adapters.extend(lift_entry_aliases(program))
    adapters.extend(lift_helper_routines(program))
    adapters.extend(lift_timeline_rewrites(program))
    adapters.extend(lift_function_rewrites(program))
    return adapters


def source_role(program: Program) -> str:
    name = Path(program.source).name
    if name == "default.decl":
        return "global_helpers"
    if name in BOSS_SCRIPT_FILES:
        return "external_boss_script"
    if any(func.name == "main" for func in program.functions):
        return "stage_timeline"
    return "script"


def lift_resource_plan(program: Program) -> list[ResourcePlan]:
    role = source_role(program)
    if generation_for_game(program.game) != "th13_plus":
        return []
    if role not in {"stage_timeline", "external_boss_script"}:
        return []
    obj = ResourcePlan(program.game, "", 0, "resource_plan", "program")
    obj.fields = {
        "role": role,
        "rules": [
            {
                "resource": "anim",
                "when_target_generation": "th12",
                "entries": ["enemy.anm", "stgenm01.anm"],
                "mode": "replace" if role == "stage_timeline" else "default_if_missing",
                "reason": "target ABI provides enemy and stage/boss ANM banks separately",
            }
        ],
    }
    return [obj]


def lift_entry_aliases(program: Program) -> list[EntryAlias]:
    if source_role(program) != "stage_timeline" or generation_for_game(program.game) != "th13_plus":
        return []
    function_names = {func.name for func in program.functions}
    aliases = {alias: target for alias, target in STAGE_ENTRY_ALIASES.items() if alias not in function_names and target in function_names}
    if not aliases:
        return []
    obj = EntryAlias(program.game, "", 0, "stage_entry_aliases", "program")
    obj.fields = {
        "when_target_generation": "th12",
        "aliases": aliases,
        "anm_setup": {
            alias: setup
            for alias in aliases
            if (setup := STAGE_ENTRY_ANM_PURPOSE.get(alias[:1])) is not None
        },
        "reason": "target stage scheduler references named enemy entries that differ from source function names",
    }
    return [obj]


def lift_helper_routines(program: Program) -> list[HelperRoutine]:
    if source_role(program) != "global_helpers" or generation_for_game(program.game) != "th13_plus":
        return []
    objects: list[HelperRoutine] = []
    for func in program.functions:
        if func.name not in BULLET_CLEAR_HELPERS:
            continue
        obj = HelperRoutine(program.game, func.name, func.statements[0].line_no if func.statements else 0, func.name, "program")
        obj.fields = {
            "semantic": "bullet.clear_radial_helper",
            "when_target_generation": "th12",
            "interval": "6" if func.name in {"Ecl_EtBreak2", "Ecl_EtBreak2_ni"} else "10",
            "preserve_items": func.name.endswith("_ni"),
        }
        objects.append(obj)
    return objects


def lift_timeline_rewrites(program: Program) -> list[TimelineRewrite]:
    rewrites: list[TimelineRewrite] = []
    if program.game in {"th10", "th11"} and source_role(program) == "stage_timeline":
        for func in program.functions:
            if not re.fullmatch(r"(?:B|G|R|Y)Girl00[A-Z]*", func.name):
                continue
            obj = TimelineRewrite(program.game, func.name, 0, "stage_enemy_drop_after_anm", "program")
            obj.fields = {
                "semantic": "timeline.order.drop_after_visual_setup",
                "when_target_generation": "th13_plus",
                "move_op_key": "unit.drop_main",
                "insert_before_call_regex": r"@Girl00[A-Z]*\(",
                "reason": "TH13+ target should apply item-drop state after wrapper ANM setup, before shared enemy body",
            }
            rewrites.append(obj)
    if generation_for_game(program.game) != "th13_plus":
        return rewrites
    role = source_role(program)
    if role == "stage_timeline" and any(func.name == "main" for func in program.functions):
        obj = TimelineRewrite(program.game, "main", 0, "skip_debug_selector", "program")
        obj.fields = {
            "semantic": "stage.skip_debug_spell_selector",
            "when_target_generation": "th12",
            "condition_contains": "[-9907]",
            "skip_until_line_before": 1302,
            "replacement_goto": {"label": "main_440", "time": "0"},
            "reason": "normal target stage entry should bypass source spell-test selector",
        }
        rewrites.append(obj)
    if role == "external_boss_script":
        for func in program.functions:
            obj = TimelineRewrite(program.game, func.name, 0, "skip_boss_spelltest", "program")
            obj.fields = {
                "semantic": "boss.skip_debug_spell_selector",
                "when_target_generation": "th12",
                "condition_contains": "[-9907]",
                "reason": "normal target boss flow should bypass source spell-test selector",
            }
            rewrites.append(obj)
    return rewrites


def lift_function_rewrites(program: Program) -> list[FunctionRewrite]:
    rewrites: list[FunctionRewrite] = []
    if program.game == "th10" and source_role(program) == "stage_timeline" and any(func.name == "MapleEnemy" for func in program.functions):
        obj = FunctionRewrite(program.game, "MapleEnemy", 0, "omit_maple_enemy", "program")
        obj.fields = {
            "semantic": "visual_helper_function.omit",
            "when_target_generation": "th13_plus",
            "function": "MapleEnemy",
            "call_names": ["MapleEnemy"],
            "reason": "TH10 MapleEnemy is a visual helper; target runtime entity is unstable and nonessential",
        }
        rewrites.append(obj)
    return rewrites
