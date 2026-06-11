from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .backend import compile_bullet_emitter, compile_object
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
    for resource, entries in program.resources.items():
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
    function_params = {func.name: getattr(func, "params", "") for func in program.functions}
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
        lines.extend(emit_function_body(function_objects, target))
        lines.append("}")
    return "\n".join(lines)




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
        "Boss": "MainBoss", "Boss1": "MainBoss", "Boss2": "MainBoss",
        "MBoss": "MainMBossDebug", "MBoss1": "MainMBossDebug", "MBoss2": "MainMBossDebug",
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


def emit_function_body(function_objects: list[object], target: str) -> list[str]:
    timelines = [obj for obj in function_objects if getattr(obj, "kind", None) == "Timeline"]
    semantic_objects = [obj for obj in function_objects if getattr(obj, "kind", None) != "Timeline"]
    if not timelines:
        return emit_semantic_object_block(semantic_objects, target)

    timeline = timelines[0]
    object_starts: dict[int, list[object]] = {}
    covered_lines: set[int] = set()
    for obj in semantic_objects:
        raw = getattr(obj, "raw", [])
        if not raw:
            object_starts.setdefault(getattr(obj, "source_line", 0), []).append(obj)
            continue
        object_starts.setdefault(raw[0].line_no, []).append(obj)
        covered_lines.update(ins.line_no for ins in raw)

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


TH13PLUS_TO_TH12_RAW = {
    500: 400, 501: 401, 502: 402, 503: 403, 504: 404, 505: 405, 506: 406, 507: 407,
    508: 408, 509: 409, 510: 410, 511: 411, 512: 412, 513: 413, 514: 414, 515: 415,
    516: 416, 517: 417, 518: 418, 519: 419, 520: 420, 521: 421, 522: 422, 523: 423,
    524: 424, 525: 425, 526: 426, 527: 427, 528: 428, 529: 435, 530: 436, 531: 437,
    532: 438, 533: 439, 534: 440, 535: 435, 536: 436, 537: 437, 538: 438, 539: 439,
    540: 440, 542: 442, 543: 443, 544: 444, 545: 445, 546: 446, 547: 447, 548: 448,
    549: 449, 552: 452, 553: 453, 554: 454, 555: 455, 556: 456,
    612: 512,
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


def literal_time_value(value: str) -> str:
    value = str(value).strip()
    if value.isdigit():
        return value
    match = re.match(r"\d+", value)
    if match:
        return match.group(0)
    return "1"


def lower_raw_instruction_event(opcode: int, args: list[object], text: str, source_game: str, target: str) -> list[str]:
    if source_game in {"th13", "th14", "th15", "th16", "th17", "th18"} and target == "th12":
        if opcode in TH13PLUS_TO_TH12_RAW:
            mapped = TH13PLUS_TO_TH12_RAW[opcode]
            return [
                f"    // raw opcode fallback {source_game}->th12: ins_{opcode} -> ins_{mapped}; verify semantics",
                f"    ins_{mapped}({', '.join(str(arg) for arg in args)});",
            ]
        if opcode in TH13PLUS_TO_TH12_RAW_UNSUPPORTED:
            return [
                f"    // unsupported {source_game}->th12 opcode ins_{opcode}: {TH13PLUS_TO_TH12_RAW_UNSUPPORTED[opcode]}",
                f"    // original: {text}",
            ]
    return []




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
                literals = event.get("difficulty_literals", {})
                if isinstance(literals, dict) and literals:
                    for rank in ("LO", "L", "H", "N", "E"):
                        if rank in literals:
                            wait_value = str(literals[rank])
                            if target == "th12":
                                return [f"    // dynamic wait collapsed from difficulty literals using {rank}", f"    ins_83({wait_value});"]
                            return [f"    // dynamic wait collapsed from difficulty literals using {rank}", f"    +{literal_time_value(wait_value)}:"]
                safe_text = text.replace("ins_", "src_ins_")
                return [f"    // dynamic wait from source opcode {opcode}; TH12 timer labels need a literal", f"    // original source: {safe_text}"]
            if target == "th12":
                return [f"    ins_83({wait});"]
            collapsed = literal_time_value(wait)
            if collapsed != wait:
                return [f"    // dynamic wait expression collapsed for timer syntax: {wait}", f"    +{collapsed}:"]
            return [f"    +{wait}:"]
        lowered = lower_raw_instruction_event(int(opcode or -1), list(args), text, source_game, target)
        if lowered:
            return lowered
        return [f"    // unlifted instruction: {text}"]
    if kind == "time":
        # +N: is a compile-time timestamp accepted by TH10+ thecl, not a wait opcode.
        # It must be preserved for TH12; only TH13+ ins_23/24 waits are lowered to ins_83.
        return [f"    {text}"]
    if kind == "label":
        return [f"    {text}"]
    if kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
        suffix = "" if text.endswith(";") else ";"
        return [f"    {text}{suffix}"]
    if kind == "raw":
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
    compile_cmd.add_argument("--target", required=True, choices=["th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    compile_cmd.add_argument("--kind", default="BulletEmitter", choices=["BulletEmitter", "LaserEmitter", "Movement", "Animation", "Enemy", "BossPattern", "Timeline"])
    compile_cmd.add_argument("--index", type=int, default=0, help="0-based lifted object index within --kind")
    compile_cmd.set_defaults(func=cmd_compile)


    transpile = sub.add_parser("transpile", help="lower a whole .decl file as a structured draft")
    transpile.add_argument("input")
    transpile.add_argument("--target", required=True, choices=["th12", "th13", "th14", "th15", "th16", "th17", "th18"])
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
