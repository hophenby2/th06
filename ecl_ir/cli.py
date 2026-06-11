from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .backend import choose_difficulty, compile_bullet_emitter, compile_object, first_difficulty_group, normalize_difficulty, wrap_ranked_lines
from .object_lifter import lift_all_objects, summarize_by_kind
from .parser import parse_decl


def load_objects(path: str):
    program = parse_decl(path)
    return program, lift_all_objects(program)


def cmd_lift(args: argparse.Namespace) -> int:
    program, objects = load_objects(args.input)
    data = {
        "source": program.source,
        "game": program.game,
        "functions": len(program.functions),
        "resources": program.resources,
        "resource_counts": {key: len(value) for key, value in program.resources.items()},
        "top_level": [stmt.to_dict() for stmt in program.top_level],
        "summary": summarize_by_kind(objects),
        "objects": [obj.to_dict() for obj in objects],
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_compile(args: argparse.Namespace) -> int:
    _, objects = load_objects(args.input)
    selected = [obj for obj in objects if getattr(obj, "kind", None) == args.kind]
    if not selected:
        raise SystemExit(f"no liftable {args.kind} found in {args.input}")
    if args.index < 0 or args.index >= len(selected):
        raise SystemExit(f"{args.kind} index {args.index} out of range; found {len(selected)} objects")
    obj = selected[args.index]
    print(f"// source: {args.input}")
    print(f"// lifted: {obj.game}.{obj.function}:{obj.source_line} kind={obj.kind} family={obj.family}")
    print(f"// target: {args.target}")
    print(compile_object(obj, args.target))
    return 0


def emit_transpile(program, objects, target: str) -> str:
    lines: list[str] = []
    lines.append(f"// source: {program.source}")
    lines.append(f"// source game: {program.game}")
    lines.append(f"// target: {target}")
    lines.append("// whole-file lowering is a structured draft; verify target-game scheduling and resources")
    resources = dict(program.resources)
    for resource, entries in synthetic_resource_entries(program, target).items():
        resources.setdefault(resource, entries)
    for resource, entries in resources.items():
        entries = target_resource_entries(program, target, resource, entries)
        quoted = "; ".join(f'"{entry}"' for entry in entries)
        lines.append(f"{resource} {{ {quoted}; }}")
    if program.top_level:
        lines.append("// top-level declarations")
        for stmt in program.top_level:
            lines.append(stmt.raw.strip())

    by_function: dict[str, list[object]] = {}
    for obj in objects:
        by_function.setdefault(getattr(obj, "function", ""), []).append(obj)

    function_order = [func.name for func in program.functions]
    function_params = inferred_function_params(program)
    if program.game == "th15" and target == "th12" and Path(program.source).name == "st01.decl":
        lines.extend(th12_stage01_compat_wrappers(set(function_order)))
        if lines and lines[-1] != "":
            lines.append("")
    for function in function_order:
        function_objects = by_function.get(function, [])
        if not function_objects:
            continue
        params = function_params.get(function, "")
        lines.append("")
        lines.append(f"void {function}({params})")
        lines.append("{")
        body_lines = emit_function_body(function_objects, target)
        if params:
            body_lines = drop_redeclared_param_vars(body_lines, params)
        lines.extend(body_lines)
        lines.append("}")
    return "\n".join(lines)




def drop_redeclared_param_vars(lines: list[str], params: str) -> list[str]:
    param_names = {part.strip().split()[-1] for part in params.split(",") if part.strip()}
    if not param_names:
        return lines
    out: list[str] = []
    var_re = re.compile(r"^(\s*)var\s+(.+?)\s*;\s*$")
    for line in lines:
        match = var_re.match(line)
        if not match:
            out.append(line)
            continue
        indent, raw_vars = match.group(1), match.group(2)
        kept = [var.strip() for var in raw_vars.split(",") if var.strip() and var.strip().split()[-1] not in param_names]
        if kept:
            out.append(f"{indent}var {', '.join(kept)};")
    return out


def synthetic_resource_entries(program, target: str) -> dict[str, list[str]]:
    name = Path(program.source).name
    if program.game == "th15" and target == "th12" and name in {"st01bs.decl", "st01mbs.decl", "st01mbs2.decl"}:
        return {"anim": ["enemy.anm", "stgenm01.anm"]}
    return {}


def inferred_function_params(program) -> dict[str, str]:
    params = {func.name: getattr(func, "params", "") for func in program.functions}
    if program.game not in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return params
    if Path(program.source).name != "default.decl":
        return params
    sibling_prototypes = collect_sibling_prototype_params(Path(program.source))
    for func in program.functions:
        if params.get(func.name):
            continue
        proto_params = sibling_prototypes.get(func.name)
        if proto_params:
            params[func.name] = proto_params
    return params


def collect_sibling_prototype_params(source: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    prototype_re = re.compile(r"^\s*(?:void|sub)\s+(\w+)\s*\(([^)]*)\)\s*;")
    for path in sorted(source.parent.glob("*.decl")):
        if path == source:
            continue
        try:
            lines = path.read_text(errors="replace").splitlines()
        except OSError:
            continue
        for raw in lines:
            match = prototype_re.match(raw)
            if not match:
                continue
            name, raw_params = match.group(1), match.group(2).strip()
            if raw_params:
                result.setdefault(name, raw_params)
    return result


def target_resource_entries(program, target: str, resource: str, entries: list[str]) -> list[str]:
    if program.game == "th15" and target == "th12" and resource == "anim" and Path(program.source).name == "st01.decl":
        return ["enemy.anm", "stgenm01.anm"]
    return list(entries)

def th12_stage01_compat_wrappers(function_names: set[str]) -> list[str]:
    mapping = {
        "BGirl00": "MainSub00", "BGirl02": "MainSub01", "BGirl04": "MainSub02", "BGirl05": "MainSub03", "BGirl07": "MainSub04", "BGirl10": "MainSub05",
        "GGirl00": "MainSub00", "GGirl02": "MainSub01", "GGirl04": "MainSub02", "GGirl05": "MainSub03", "GGirl07": "MainSub04", "GGirl10": "MainSub05",
        "RGirl00": "MainSub00", "RGirl02": "MainSub01", "RGirl04": "MainSub02", "RGirl05": "MainSub03", "RGirl07": "MainSub04", "RGirl10": "MainSub05",
        "YGirl00": "MainSub00", "YGirl02": "MainSub01", "YGirl04": "MainSub02", "YGirl05": "MainSub03", "YGirl07": "MainSub04", "YGirl10": "MainSub05",
        # Do not wrap Boss/MBoss names: TH15 stage01 loads them from external ECLI files.
        # A local wrapper with the same name shadows the external entry and can recurse/crash.
        "MainSub02b": "MainSub02", "MainSub07b": "MainSub07", "MainSub08": "MainLatter", "MainSub08b": "MainLatter",
        "MainSub09": "MainLatter", "MainSub10": "MainLatter2", "MainSub10b": "MainLatter2", "MainSub11": "MainLatter2",
        "MainSub12": "MainLatter2", "MainSub13": "MainLatter2",
    }
    lines: list[str] = []
    needed = [(wrapper, target) for wrapper, target in mapping.items() if wrapper not in function_names and target in function_names]
    if not needed:
        return lines
    lines.append("// TH12 stage01 compatibility entry wrappers.")
    lines.append("// These names are used by the original TH12 stage scheduling / enemy entries.")
    for wrapper, target in needed:
        lines.extend([f"void {wrapper}()", "{", f"    @{target}();", "    return;", "}"])
    return lines


def is_fire_instruction(ins) -> bool:
    return getattr(ins, "opcode", None) in {401, 501, 601}


def should_preserve_raw_timeline(program_source: str, source_game: str, target: str, function_name: str) -> bool:
    if source_game not in {"th13", "th14", "th15", "th16", "th17", "th18"} or target != "th12":
        return False
    return Path(program_source or "").name in {"st01bs.decl", "st01mbs.decl", "st01mbs2.decl"}


def emit_function_body(function_objects: list[object], target: str) -> list[str]:
    timelines = [obj for obj in function_objects if getattr(obj, "kind", None) == "Timeline"]
    semantic_objects = [obj for obj in function_objects if getattr(obj, "kind", None) not in {"Timeline", "BossPattern"}]
    if not timelines:
        return emit_semantic_object_block(semantic_objects, target)

    timeline = timelines[0]
    special_default = emit_th15_default_special_body(timeline, target)
    if special_default is not None:
        return special_default
    if should_preserve_raw_timeline(getattr(timeline, "source", ""), getattr(timeline, "game", "unknown"), target, getattr(timeline, "function", "")):
        return emit_raw_timeline_body(timeline, target)
    object_starts: dict[int, list[object]] = {}
    covered_lines: set[int] = set()
    for obj in semantic_objects:
        raw = getattr(obj, "raw", [])
        if not raw:
            object_starts.setdefault(getattr(obj, "source_line", 0), []).append(obj)
            continue
        object_starts.setdefault(raw[0].line_no, []).append(obj)
        covered_lines.update(ins.line_no for ins in raw if not is_fire_instruction(ins))

    lines: list[str] = []
    lines.append(f"    // Timeline lowering {timeline.family} -> {target}; interleaved structured draft")
    lines.append("    // control-flow, async scheduling, and expression semantics require target-game verification")
    skipped_debug_selector = False
    source_game = getattr(timeline, "game", "unknown")
    for event in timeline.fields.get("statements", []):
        if is_th15_stage1_debug_selector_event(event, source_game, target, getattr(timeline, "function", "")):
            if not skipped_debug_selector:
                lines.append("    // TH15 debug/spell selector removed for TH12 normal stage entry.")
                lines.append("    // Original [-9907] branch can trap TH12 in a pre-stage spell-test loop.")
                lines.append("    goto main_440 @ 0;")
                skipped_debug_selector = True
            lines.append(f"    // original debug selector: {event.get('text', '')}")
            continue
        if skipped_debug_selector and event.get("kind") in {"call", "goto", "conditional_goto", "label", "instruction"} and int(event.get("line", 0) or 0) < 1302:
            lines.append(f"    // original debug selector body: {event.get('text', '')}")
            continue
        line_no = int(event.get("line", 0) or 0)
        if line_no in object_starts:
            for obj in sorted(object_starts[line_no], key=lambda item: getattr(item, "kind", "")):
                lines.append(f"    // object {obj.kind} source_line={obj.source_line} family={obj.family}")
                for line in compile_object(obj, target).splitlines():
                    lines.append(f"    {line}")
        if line_no in covered_lines:
            continue
        lines.extend(emit_timeline_event(event, getattr(timeline, "game", "unknown"), target))
    emitted_starts = set(object_starts)
    late_objects = [obj for obj in semantic_objects if getattr(obj, "source_line", 0) not in emitted_starts and not getattr(obj, "raw", [])]
    if late_objects:
        lines.append("    // lifted semantic objects without timeline positions")
        lines.extend(emit_semantic_object_block(late_objects, target))
    loops = timeline.fields.get("loops", [])
    if loops:
        lines.append("    // detected loops:")
        for loop in loops:
            lines.append(f"    // - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return lines


def emit_th15_default_special_body(timeline, target: str) -> list[str] | None:
    if getattr(timeline, "game", "") != "th15" or target != "th12":
        return None
    if Path(str(getattr(timeline, "source", ""))).name != "default.decl":
        return None
    name = getattr(timeline, "function", "")
    if name not in {"Ecl_EtBreak", "Ecl_EtBreak2", "Ecl_EtBreak2_ni", "Ecl_EtBreak_ni"}:
        return None
    interval = "6" if name in {"Ecl_EtBreak2", "Ecl_EtBreak2_ni"} else "10"
    clear_opcode = 513 if name.endswith("_ni") else 512
    label = f"{name}_120"
    end = f"{name}_216"
    return [
        "    // TH15 default bullet-clear helper lowered to TH12 native equivalent.",
        "    var A, B;",
        "    %B = 16.0f;",
        "    ins_402(32);",
        f"    goto {end} @ 1;",
        f"    {label}:",
        f"    ins_{clear_opcode}(%B);",
        "    %B;",
        "    +1:",
        f"    {interval};",
        "    ins_51();",
        "    ins_45(%B);",
        f"    {end}:",
        f"    if (%B < 640.0f) goto {label} @ 0;",
        "    ins_1();",
    ]


def emit_raw_timeline_body(timeline, target: str) -> list[str]:
    lines: list[str] = []
    lines.append(f"    // Timeline lowering {timeline.family} -> {target}; raw-order boss/bullet-safe path")
    lines.append("    // Boss ECL keeps source instruction order to avoid moving dynamic bullet parameters before initialization.")
    emitted_spelltest_skip = False
    for event in timeline.fields.get("statements", []):
        if should_skip_boss_spelltest_event(event, timeline, target):
            if not emitted_spelltest_skip:
                label = str(event.get("label", ""))
                time = str(event.get("time", "0"))
                if label:
                    lines.append("    // TH15 boss spell-test branch removed for TH12 normal stage flow.")
                    lines.append(f"    goto {label} @ {time};")
                emitted_spelltest_skip = True
            lines.append(f"    // original spell-test branch: {event.get('text', '')}")
            continue
        lines.extend(emit_timeline_event(event, getattr(timeline, "game", "unknown"), target))
    loops = timeline.fields.get("loops", [])
    if loops:
        lines.append("    // detected loops:")
        for loop in loops:
            lines.append(f"    // - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return lines



def should_skip_boss_spelltest_event(event: dict[str, object], timeline, target: str) -> bool:
    if target != "th12" or getattr(timeline, "game", "") != "th15":
        return False
    if Path(str(getattr(timeline, "source", ""))).name not in {"st01bs.decl", "st01mbs.decl", "st01mbs2.decl"}:
        return False
    if "[-9907]" not in str(event.get("text", "")) and "[-9907]" not in str(event.get("condition", "")):
        return False
    return event.get("kind") == "conditional_goto"


TH13PLUS_TO_TH12_RAW_REORDER = {
    # enemy / animation
    300: (256, [0, 1, 2, 3, 4, 5]),
    301: (257, [0, 1, 2, 3, 4, 5]),
    302: (258, [0]),
    303: (259, [0, 1]),
    306: (262, [0, 1]),
    307: (263, [0, 1]),
    308: (264, [0, 1]),
    # movement
    400: (300, [0, 1]),
    401: (301, [0, 1, 2, 3]),
    402: (302, [0, 1]),
    403: (303, [0, 1, 2, 3]),
    404: (304, [0, 1]),
    405: (305, [0, 1, 2, 3]),
    406: (306, [0, 1]),
    407: (307, [0, 1, 2, 3]),
    420: (320, [0, 1, 2, 3, 4, 5]),
    421: (321, [0, 1, 2, 3, 4, 5, 6]),
    425: (325, [0, 1, 2, 3, 4, 5, 6]),
    426: (326, [0, 1, 2, 3, 4, 5, 6]),
    427: (327, []),
}

TH13PLUS_TO_TH12_RAW = {
    500: 400, 501: 401, 502: 402, 503: 403, 504: 404, 505: 405, 506: 406, 507: 407,
    508: 408, 509: 409, 510: 410, 511: 411, 512: 412, 513: 413, 514: 414, 515: 415,
    516: 416, 517: 417, 518: 418, 519: 419, 520: 420, 521: 421, 522: 422, 523: 423,
    524: 424, 525: 425, 526: 426, 527: 427, 528: 428, 529: 435, 530: 436, 531: 437,
    532: 438, 533: 439, 534: 440, 535: 435, 536: 436, 537: 437, 538: 438, 539: 439,
    540: 440, 542: 442, 543: 443, 544: 444, 545: 445, 546: 446, 547: 447, 548: 448,
    549: 449, 552: 452, 553: 453, 554: 454, 555: 455, 556: 456,
    # TH13+ bullet slot setup/fire -> TH12 bullet slot setup/fire.
    # Keep these raw-order in boss ECLs so dynamic parameters such as ins_606($F, ...) are not moved.
    600: 500, 601: 501, 602: 502, 603: 503, 604: 504, 605: 505, 606: 506, 607: 507,
    608: 508, 609: 509,
}

TH13PLUS_TO_TH12_RAW_UNSUPPORTED = {
    441: "movement-direction acceleration opcode has no confirmed TH12 one-to-one raw fallback here",
    422: "TH13+ movement opcode not represented in current TH12 movement subset",
    423: "TH13+ movement opcode not represented in current TH12 movement subset",
    445: "speed interpolation opcode may correspond to TH12 345/347 family, not safely mapped yet",
    569: "TH15 pointdevice/LoLK-specific unit flag, no TH12 equivalent",
    610: "TH15 bullet clear/transform opcode is not TH12 opcode 510; parameter formats differ",
    613: "TH15 bullet/effect opcode is not TH12 opcode 513; parameter formats differ",
    614: "TH15 bullet difficulty/rank extension is not TH12 opcode 514; parameter formats differ",
    616: "TH15 bullet/effect opcode is not TH12 opcode 516; parameter formats differ",
    526: "TH15 spell/boss effect opcode is not TH12 opcode 426; parameter formats differ",
    630: "TH15 bullet extension opcode, not mapped to TH12",
    1001: "TH15 game-specific opcode, no TH12 equivalent",
    1002: "TH15 game-specific opcode, no TH12 equivalent",
}


def remap_raw_named_args(source_opcode: int, target_opcode: int, args: list[str], source_game: str, target: str) -> list[str]:
    if source_game == "th15" and target == "th12" and source_opcode == 302 and target_opcode == 258 and len(args) == 1:
        if args[0] == "2":
            return ["1"]
        if args[0] == "3":
            return ["2"]
    if source_game == "th15" and target == "th12" and source_opcode == 602 and target_opcode == 502 and len(args) >= 3:
        mapped = args[:]
        mapped[1] = remap_th15_bullet_shape_to_th12(mapped[1])
        return mapped
    if source_game == "th15" and target == "th12" and source_opcode == 607 and target_opcode == 507 and len(args) >= 2:
        mapped = args[:]
        mapped[1] = remap_th15_bullet_spread_style_to_th12(mapped[1])
        return mapped
    return args


def remap_th15_bullet_spread_style_to_th12(style: str) -> str:
    table = {
        "2": "4",
        "3": "5",
    }
    return table.get(str(style).strip(), style)


def remap_th15_bullet_shape_to_th12(shape: str) -> str:
    table = {
        "0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "4", "6": "5", "7": "6",
        "8": "7", "9": "8", "10": "9", "11": "10", "12": "11", "13": "12", "14": "13", "15": "14",
        "16": "15", "17": "16", "18": "18", "19": "18", "20": "19", "21": "20", "22": "21",
        "23": "22", "24": "22", "25": "24", "26": "29", "27": "29", "28": "24", "29": "25",
        "30": "18", "31": "9", "32": "26", "33": "23", "34": "28", "35": "7", "36": "9",
        "37": "15", "38": "30",
    }
    return table.get(str(shape).strip(), shape)


def literal_time_value(value: str) -> str:
    value = str(value).strip()
    if value.isdigit():
        return value
    match = re.match(r"\d+", value)
    if match:
        return match.group(0)
    return "1"


RANK_PLACEHOLDER_RE = re.compile(r"\[-([12])(?:\.0f)?\]")


def replace_rank_placeholders(arg: str, groups: list[dict[str, str]], rank: str) -> tuple[str, bool]:
    replaced = False

    def repl(match: re.Match[str]) -> str:
        nonlocal replaced
        index = int(match.group(1)) - 1
        if index >= len(groups):
            return match.group(0)
        normalized = normalize_difficulty(groups[index])
        if rank in normalized:
            replaced = True
            return normalized[rank]
        fallback, _ = choose_difficulty(groups[index], match.group(0))
        if fallback != match.group(0):
            replaced = True
        return fallback

    return RANK_PLACEHOLDER_RE.sub(repl, arg), replaced


def difficulty_literal_groups(difficulty_literals: object) -> list[dict[str, str]]:
    if isinstance(difficulty_literals, list):
        return [item for item in difficulty_literals if isinstance(item, dict) and item]
    if isinstance(difficulty_literals, dict) and difficulty_literals:
        return [difficulty_literals]
    return []


def emit_ranked_raw_instruction(opcode: int, args: list[str], difficulty_literals: object, source_opcode: int | None = None, source_game: str = "", target: str = "") -> list[str] | None:
    groups = difficulty_literal_groups(difficulty_literals)
    if not groups or not any(RANK_PLACEHOLDER_RE.search(arg) for arg in args):
        return None

    lines: list[str] = []
    for rank in ("E", "N", "H", "L"):
        ranked_args: list[str] = []
        any_replaced = False
        for arg in args:
            ranked_arg, replaced = replace_rank_placeholders(str(arg), groups, rank)
            ranked_args.append(ranked_arg)
            any_replaced = any_replaced or replaced
        if any_replaced:
            if source_opcode is not None:
                ranked_args = remap_raw_named_args(source_opcode, opcode, ranked_args, source_game, target)
            lines.append(f"    !{rank}")
            lines.append(f"    ins_{opcode}({', '.join(ranked_args)});")
    if not lines:
        return None
    lines.append("    !*")
    return lines


def emit_ranked_text_from_literals(text: str, difficulty_literals: object) -> list[str] | None:
    groups = difficulty_literal_groups(difficulty_literals)
    if not groups or not RANK_PLACEHOLDER_RE.search(text):
        return None
    lines: list[str] = []
    for rank in ("E", "N", "H", "L"):
        ranked_text, replaced = replace_rank_placeholders(text, groups, rank)
        if replaced:
            lines.append(f"    !{rank}")
            lines.append(f"    {ranked_text}")
    if not lines:
        return None
    lines.append("    !*")
    return lines


def lower_raw_instruction_event(opcode: int, args: list[object], text: str, source_game: str, target: str, difficulty_literals: object = None) -> list[str]:
    if source_game in {"th13", "th14", "th15", "th16", "th17", "th18"} and target == "th12":
        if opcode in TH13PLUS_TO_TH12_RAW_REORDER:
            mapped, order = TH13PLUS_TO_TH12_RAW_REORDER[opcode]
            mapped_args = [str(args[index]) for index in order if index < len(args)]
            mapped_args = remap_raw_named_args(opcode, mapped, mapped_args, source_game, target)
            ranked = emit_ranked_raw_instruction(mapped, mapped_args, difficulty_literals, opcode, source_game, target)
            if ranked:
                return [f"    // raw-order opcode map {source_game}->th12: ins_{opcode} -> ins_{mapped}; ranked args from source difficulty literals", *ranked]
            return [
                f"    // raw-order opcode map {source_game}->th12: ins_{opcode} -> ins_{mapped}; verify semantics",
                f"    ins_{mapped}({', '.join(mapped_args)});",
            ]
        if opcode in TH13PLUS_TO_TH12_RAW:
            mapped = TH13PLUS_TO_TH12_RAW[opcode]
            mapped_args = remap_raw_named_args(opcode, mapped, [str(arg) for arg in args], source_game, target)
            ranked = emit_ranked_raw_instruction(mapped, mapped_args, difficulty_literals, opcode, source_game, target)
            if ranked:
                return [f"    // raw opcode fallback {source_game}->th12: ins_{opcode} -> ins_{mapped}; ranked args from source difficulty literals", *ranked]
            return [
                f"    // raw opcode fallback {source_game}->th12: ins_{opcode} -> ins_{mapped}; verify semantics",
                f"    ins_{mapped}({', '.join(mapped_args)});",
            ]
        if opcode in TH13PLUS_TO_TH12_RAW_UNSUPPORTED:
            return [
                f"    // unsupported {source_game}->th12 opcode ins_{opcode}: {TH13PLUS_TO_TH12_RAW_UNSUPPORTED[opcode]}",
                f"    // original: {text}",
            ]
    return []




def wrap_event_rank(lines: list[str], event: dict[str, object], target: str) -> list[str]:
    difficulty = event.get("difficulty")
    if not difficulty:
        return lines
    stripped: list[str] = []
    for line in lines:
        stripped.append(line[4:] if line.startswith("    ") else line)
    return [f"    {line}" for line in wrap_ranked_lines(stripped, str(difficulty), target)]


def is_th15_stage1_debug_selector_event(event: dict[str, object], source_game: str, target: str, function_name: str) -> bool:
    if source_game != "th15" or target != "th12" or function_name != "main":
        return False
    return event.get("kind") == "conditional_goto" and "[-9907]" in str(event.get("condition", ""))

def emit_timeline_event(event: dict[str, object], source_game: str = "unknown", target: str = "") -> list[str]:
    kind = event.get("kind")
    text = str(event.get("text") or "")
    if not text:
        return []
    if kind == "instruction":
        opcode = event.get("opcode")
        args = event.get("args", [])
        if opcode in {23, 24}:
            wait = str(event.get("args", [""])[0]) if event.get("args") else ""
            if wait.startswith("["):
                literals = first_difficulty_group(event.get("difficulty_literals", {}))
                if literals:
                    normalized = normalize_difficulty(literals)
                    ranked_lines = ["    // dynamic wait preserved from difficulty literals"]
                    for rank in ("E", "N", "H", "L"):
                        if rank not in normalized:
                            continue
                        wait_value = str(normalized[rank])
                        ranked_lines.append(f"    !{rank}")
                        if target == "th12":
                            ranked_lines.append(f"    ins_83({wait_value});")
                        else:
                            ranked_lines.append(f"    ins_{opcode}({wait_value});")
                    if len(ranked_lines) > 1:
                        ranked_lines.append("    !*")
                        return ranked_lines
                safe_text = text.replace("ins_", "src_ins_")
                return [f"    // dynamic wait from source opcode {opcode}; TH12 timer labels need a literal", f"    // original source: {safe_text}"]
            if target == "th12":
                return wrap_event_rank([f"    ins_83({wait});"], event, target)
            collapsed = literal_time_value(wait)
            if collapsed != wait:
                return wrap_event_rank([f"    // dynamic wait expression collapsed for timer syntax: {wait}", f"    +{collapsed}:"], event, target)
            return wrap_event_rank([f"    +{wait}:"], event, target)
        lowered = lower_raw_instruction_event(int(opcode or -1), list(args), text, source_game, target, event.get("difficulty_literals", []))
        if lowered:
            if any(line.strip().startswith("!") for line in lowered):
                return lowered
            return wrap_event_rank(lowered, event, target)
        return wrap_event_rank([f"    // unlifted instruction: {text}"], event, target)
    if kind == "time":
        # +N: is a compile-time timestamp accepted by TH10+ thecl, not a wait opcode.
        # It must be preserved for TH12; only TH13+ ins_23/24 waits are lowered to ins_83.
        return wrap_event_rank([f"    {text}"], event, target)
    if kind == "label":
        return [f"    {text}"]
    if kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
        suffix = "" if text.endswith(";") else ";"
        statement_text = f"{text}{suffix}"
        ranked = emit_ranked_text_from_literals(statement_text, event.get("difficulty_literals", []))
        if ranked:
            return ranked
        return wrap_event_rank([f"    {statement_text}"], event, target)
    if kind == "raw":
        if re.fullmatch(r"[%$]?[A-Za-z_][A-Za-z0-9_]*|[-+]?\d+(?:\.\d+)?f?", text):
            return wrap_event_rank([f"    {text};"], event, target)
        return [f"    // raw: {text}"]
    return []


def emit_semantic_object_block(objects: list[object], target: str) -> list[str]:
    lines: list[str] = []
    for obj in sorted(objects, key=lambda item: (getattr(item, "source_line", 0), getattr(item, "kind", ""))):
        lines.append(f"    // object {obj.kind} source_line={obj.source_line} family={obj.family}")
        for line in compile_object(obj, target).splitlines():
            lines.append(f"    {line}")
    return lines


def cmd_transpile(args: argparse.Namespace) -> int:
    program, objects = load_objects(args.input)
    output = emit_transpile(program, objects, args.target)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    root = Path(args.root)
    rows = []
    for path in sorted(root.glob("**/*.decl")):
        program, objects = load_objects(str(path))
        summary = summarize_by_kind(objects)
        if objects:
            rows.append({"path": str(path), "game": program.game, "functions": len(program.functions), "summary": summary, "objects": len(objects)})
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print("path\tgame\tfunctions\tobjects\tsummary")
        for row in rows:
            print(f"{row['path']}\t{row['game']}\t{row['functions']}\t{row['objects']}\t{row['summary']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Experimental cross-game Touhou ECL IR tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    lift = sub.add_parser("lift", help="lift .decl to JSON IR")
    lift.add_argument("input")
    lift.set_defaults(func=cmd_lift)

    compile_cmd = sub.add_parser("compile", help="lift one object and lower to target backend")
    compile_cmd.add_argument("input")
    compile_cmd.add_argument("--target", required=True, choices=["th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    compile_cmd.add_argument("--kind", default="BulletEmitter", choices=["BulletEmitter", "LaserEmitter", "Movement", "Animation", "Enemy", "BossPattern", "Timeline"])
    compile_cmd.add_argument("--index", type=int, default=0, help="0-based lifted object index within --kind")
    compile_cmd.set_defaults(func=cmd_compile)


    transpile = sub.add_parser("transpile", help="lower a whole .decl file as a structured draft")
    transpile.add_argument("input")
    transpile.add_argument("--target", required=True, choices=["th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    transpile.add_argument("--output", help="write output to file instead of stdout")
    transpile.set_defaults(func=cmd_transpile)

    scan = sub.add_parser("scan", help="scan a directory for liftable objects")
    scan.add_argument("root")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=cmd_scan)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
