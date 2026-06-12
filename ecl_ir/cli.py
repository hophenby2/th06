from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .backend import choose_difficulty, compile_bullet_emitter, compile_ir_op_event, compile_object, first_difficulty_group, normalize_difficulty, th12_aux_emitter_id, wrap_ranked_lines
from .object_lifter import lift_all_objects, summarize_by_kind
from .parser import parse_decl
from .reference import validate_opcode_args
from .semantics import generation_for_game


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
    resources = apply_resource_plans(dict(program.resources), objects, target)
    for resource, entries in resources.items():
        if not should_emit_resource(resource, target):
            continue
        quoted = "; ".join(f'"{entry}"' for entry in entries)
        lines.append(f"{resource} {{ {quoted}; }}")
    top_level_lines = target_top_level_lines(program.top_level, target)
    if top_level_lines:
        lines.append("// top-level declarations")
        lines.extend(top_level_lines)

    by_function: dict[str, list[object]] = {}
    for obj in objects:
        by_function.setdefault(getattr(obj, "function", ""), []).append(obj)

    function_order = [func.name for func in program.functions]
    function_params = inferred_function_params(program)
    alias_lines = emit_entry_aliases(objects, target, set(function_order))
    if alias_lines:
        lines.extend(alias_lines)
        if lines and lines[-1] != "":
            lines.append("")
    for function in function_order:
        function_objects = by_function.get(function, [])
        if not function_objects:
            continue
        params = function_params.get(function, "")
        lines.append("")
        lines.append(target_function_header(function, params, target))
        lines.append("{")
        body_lines = emit_function_body(function_objects, target)
        if params:
            body_lines = drop_redeclared_param_vars(body_lines, params)
        lines.extend(body_lines)
        lines.append("}")
    return "\n".join(lines)






def target_function_header(function: str, params: str, target: str) -> str:
    if generation_for_game(target) == "th06_th08":
        return f"sub {function}()"
    return f"void {function}({params})"


def target_top_level_lines(statements: list[object], target: str) -> list[str]:
    lines: list[str] = []
    skip_timeline_depth = 0
    keep_old_timeline = generation_for_game(target) == "th06_th08"
    for stmt in statements:
        raw = getattr(stmt, "raw", "").strip()
        if not raw:
            continue
        if skip_timeline_depth:
            skip_timeline_depth += raw.count("{")
            skip_timeline_depth -= raw.count("}")
            if skip_timeline_depth <= 0:
                skip_timeline_depth = 0
            continue
        if raw.startswith("timeline "):
            if keep_old_timeline:
                lines.append(raw)
            else:
                skip_timeline_depth = max(1, raw.count("{") - raw.count("}"))
            continue
        if keep_old_timeline:
            continue
        lines.append(raw)
    return lines


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




def should_emit_resource(resource: str, target: str) -> bool:
    target_generation = generation_for_game(target)
    if target_generation == "th06_th08":
        return resource == "timeline"
    if resource == "timeline":
        return False
    return True


def apply_resource_plans(resources: dict[str, list[str]], objects: list[object], target: str) -> dict[str, list[str]]:
    target_generation = generation_for_game(target)
    result = {key: list(value) for key, value in resources.items()}
    for obj in objects:
        if getattr(obj, "kind", None) != "ResourcePlan":
            continue
        for rule in getattr(obj, "fields", {}).get("rules", []):
            if rule.get("when_target_generation") != target_generation:
                continue
            resource = str(rule.get("resource", ""))
            entries = [str(entry) for entry in rule.get("entries", [])]
            mode = str(rule.get("mode", "replace"))
            if mode == "replace":
                result[resource] = entries
            elif mode == "default_if_missing":
                result.setdefault(resource, entries)
            elif mode == "append_missing":
                current = result.setdefault(resource, [])
                for entry in entries:
                    if entry not in current:
                        current.append(entry)
    return result


def emit_entry_aliases(objects: list[object], target: str, function_names: set[str]) -> list[str]:
    target_generation = generation_for_game(target)
    lines: list[str] = []
    for obj in objects:
        if getattr(obj, "kind", None) != "EntryAlias":
            continue
        fields = getattr(obj, "fields", {})
        if fields.get("when_target_generation") != target_generation:
            continue
        aliases = fields.get("aliases", {})
        needed = [(alias, real) for alias, real in aliases.items() if alias not in function_names and real in function_names]
        if not needed:
            continue
        lines.append(f"// entry alias lowering {obj.family} -> {target}: {fields.get('reason', '')}")
        for alias, real in needed:
            lines.extend([f"void {alias}()", "{", f"    @{real}();", "    return;", "}"])
    return lines


def inferred_function_params(program) -> dict[str, str]:
    params = {func.name: getattr(func, "params", "") for func in program.functions}
    if generation_for_game(program.game) != "th13_plus":
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


def is_fire_instruction(ins) -> bool:
    return getattr(ins, "opcode", None) in {401, 501, 601}


def emit_function_body(function_objects: list[object], target: str) -> list[str]:
    timelines = [obj for obj in function_objects if getattr(obj, "kind", None) == "Timeline"]
    helper = next((obj for obj in function_objects if getattr(obj, "kind", None) == "HelperRoutine" and helper_applies(obj, target)), None)
    if helper is not None:
        return emit_helper_routine_body(helper, target)
    rewrites = [obj for obj in function_objects if getattr(obj, "kind", None) == "TimelineRewrite" and rewrite_applies(obj, target)]
    semantic_objects = [obj for obj in function_objects if getattr(obj, "kind", None) not in {"Timeline", "BossPattern", "HelperRoutine", "TimelineRewrite"}]
    if not timelines:
        return emit_semantic_object_block(semantic_objects, target)

    timeline = timelines[0]
    if any(rewrite.fields.get("semantic") == "boss.skip_debug_spell_selector" for rewrite in rewrites):
        return emit_raw_timeline_body(timeline, target, rewrites)
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
    bullet_state = make_bullet_lowering_state(function_objects, source_game, target)
    for event in timeline.fields.get("statements", []):
        stage_rewrite = find_rewrite(rewrites, "stage.skip_debug_spell_selector")
        if stage_rewrite and matches_condition_rewrite(event, stage_rewrite):
            if not skipped_debug_selector:
                lines.append(f"    // timeline rewrite: {stage_rewrite.fields.get('reason', '')}")
                replacement = stage_rewrite.fields.get("replacement_goto", {})
                lines.append(f"    goto {replacement.get('label', 'main_440')} @ {replacement.get('time', '0')};")
                skipped_debug_selector = True
            lines.append(f"    // original debug selector: {event.get('text', '')}")
            continue
        if skipped_debug_selector and stage_rewrite and event.get("kind") in {"call", "goto", "conditional_goto", "label", "instruction"} and int(event.get("line", 0) or 0) < int(stage_rewrite.fields.get("skip_until_line_before", 0) or 0):
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
        lines.extend(emit_timeline_event(event, getattr(timeline, "game", "unknown"), target, bullet_state))
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



def helper_applies(obj, target: str) -> bool:
    return getattr(obj, "fields", {}).get("when_target_generation") == generation_for_game(target)


def rewrite_applies(obj, target: str) -> bool:
    return getattr(obj, "fields", {}).get("when_target_generation") == generation_for_game(target)


def emit_helper_routine_body(helper, target: str) -> list[str]:
    semantic = helper.fields.get("semantic")
    if semantic == "bullet.clear_radial_helper" and generation_for_game(target) == "th12":
        return emit_radial_clear_helper_body(helper)
    return [f"    // unsupported helper routine for {target}: {semantic}"]


def emit_radial_clear_helper_body(helper) -> list[str]:
    name = getattr(helper, "function", "helper")
    clear_opcode = 513 if helper.fields.get("preserve_items") else 512
    interval = str(helper.fields.get("interval", "10"))
    label = f"{name}_120"
    end = f"{name}_216"
    return [
        "    // helper semantic lowering: bullet.clear_radial_helper -> th12 native clear loop.",
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


def find_rewrite(rewrites: list[object], semantic: str):
    return next((rewrite for rewrite in rewrites if getattr(rewrite, "fields", {}).get("semantic") == semantic), None)


def matches_condition_rewrite(event: dict[str, object], rewrite) -> bool:
    needle = str(getattr(rewrite, "fields", {}).get("condition_contains", ""))
    if event.get("kind") != "conditional_goto":
        return False
    return bool(needle) and (needle in str(event.get("text", "")) or needle in str(event.get("condition", "")))


def emit_raw_timeline_body(timeline, target: str, rewrites: list[object] | None = None) -> list[str]:
    rewrites = rewrites or []
    lines: list[str] = []
    lines.append(f"    // Timeline lowering {timeline.family} -> {target}; raw-order boss/bullet-safe path")
    lines.append("    // Boss ECL keeps source instruction order to avoid moving dynamic bullet parameters before initialization.")
    emitted_spelltest_skip = False
    source_game = getattr(timeline, "game", "unknown")
    boss_rewrite = find_rewrite(rewrites, "boss.skip_debug_spell_selector")
    for event in timeline.fields.get("statements", []):
        if boss_rewrite and matches_condition_rewrite(event, boss_rewrite):
            if not emitted_spelltest_skip:
                label = str(event.get("label", ""))
                time = str(event.get("time", "0"))
                if label:
                    lines.append(f"    // timeline rewrite: {boss_rewrite.fields.get('reason', '')}")
                    lines.append(f"    goto {label} @ {time};")
                emitted_spelltest_skip = True
            lines.append(f"    // original spell-test branch: {event.get('text', '')}")
            continue
        lines.extend(emit_timeline_event(event, source_game, target))
    loops = timeline.fields.get("loops", [])
    if loops:
        lines.append("    // detected loops:")
        for loop in loops:
            lines.append(f"    // - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return lines



@dataclass
class BulletLoweringState:
    double_flower_aux: dict[str, str]


def make_bullet_lowering_state(function_objects: list[object], source_game: str, target: str) -> BulletLoweringState | None:
    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    aux: dict[str, str] = {}
    for obj in function_objects:
        if getattr(obj, "kind", None) != "BulletEmitter" or getattr(obj, "family", "") != "th13plus":
            continue
        emitter_id = str(getattr(obj, "id", ""))
        spread = getattr(obj, "semantics", {}).get("bullet", {}).get("spread", {})
        if spread.get("spread_family") == "double_flower":
            aux_id = th12_aux_emitter_id(emitter_id)
            if aux_id:
                aux[emitter_id] = aux_id
    return BulletLoweringState(aux)


def lower_bullet_fire_opcode(opcode: int, args: list[object], source_game: str, target: str, bullet_state: BulletLoweringState | None) -> list[str] | None:
    if opcode != 601 or generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    emitter_id = str(args[0]) if args else "0"
    aux_id = bullet_state.double_flower_aux.get(emitter_id) if bullet_state else None
    if aux_id:
        return [
            f"    // TH15 double flower fire lowered to two TH12 slots: {emitter_id}+{aux_id}",
            f"    ins_501({emitter_id});",
            f"    ins_501({aux_id});",
        ]
    return None


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


def lower_raw_instruction_event(opcode: int, args: list[object], text: str, source_game: str, target: str, difficulty_literals: object = None, ir_op: dict[str, object] | None = None) -> list[str]:
    if ir_op:
        semantic_line = compile_ir_op_event(ir_op, target)
        if semantic_line:
            rendered = [line if line.startswith("    ") else f"    {line}" for line in semantic_line.splitlines()]
            first_instruction = next((line.strip() for line in rendered if line.strip().startswith("ins_")), "")
            match = re.match(r"ins_(\d+)\((.*)\);", first_instruction)
            if match:
                mapped = int(match.group(1))
                mapped_args = [part.strip() for part in match.group(2).split(",")] if match.group(2).strip() else []
                ranked = emit_ranked_raw_instruction(mapped, mapped_args, difficulty_literals)
                if ranked:
                    return [f"    // semantic op_key lowering {source_game}->{target}: {ir_op.get('op_key')} -> ins_{mapped}; ranked args from source difficulty literals", *ranked]
            return [f"    // semantic op_key lowering {source_game}->{target}: {ir_op.get('op_key')}", *rendered]
        return [
            f"    // unsupported semantic op_key for {source_game}->{target}: {ir_op.get('op_key')}",
            f"    // original: {text}",
        ]
    return [
        f"    // no semantic op_key; pairwise opcode fallback disabled for {source_game}->{target}: ins_{opcode}",
        f"    // original: {text}",
    ]


def wrap_event_rank(lines: list[str], event: dict[str, object], target: str) -> list[str]:
    difficulty = event.get("difficulty")
    if not difficulty:
        return lines
    stripped: list[str] = []
    for line in lines:
        stripped.append(line[4:] if line.startswith("    ") else line)
    return [f"    {line}" for line in wrap_ranked_lines(stripped, str(difficulty), target)]



def emit_timeline_event(event: dict[str, object], source_game: str = "unknown", target: str = "", bullet_state: BulletLoweringState | None = None) -> list[str]:
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
                        elif generation_for_game(target) in {"th06_th08", "th10_th11"}:
                            ranked_lines.append(f"    +{literal_time_value(wait_value)}:")
                        else:
                            ranked_lines.append(f"    ins_{opcode}({wait_value});")
                    if len(ranked_lines) > 1:
                        ranked_lines.append("    !*")
                        return ranked_lines
                safe_text = text.replace("ins_", "src_ins_")
                return [f"    // dynamic wait from source opcode {opcode}; TH12 timer labels need a literal", f"    // original source: {safe_text}"]
            if target == "th12":
                return wrap_event_rank([f"    ins_83({wait});"], event, target)
            if target in {"th10", "th11"}:
                collapsed = literal_time_value(wait)
                return wrap_event_rank([f"    +{collapsed}:"], event, target)
            collapsed = literal_time_value(wait)
            if collapsed != wait:
                return wrap_event_rank([f"    // dynamic wait expression collapsed for timer syntax: {wait}", f"    +{collapsed}:"], event, target)
            return wrap_event_rank([f"    +{wait}:"], event, target)
        fire_lowered = lower_bullet_fire_opcode(int(opcode or -1), list(args), source_game, target, bullet_state)
        if fire_lowered:
            return wrap_event_rank(fire_lowered, event, target)
        lowered = lower_raw_instruction_event(int(opcode or -1), list(args), text, source_game, target, event.get("difficulty_literals", []), event.get("ir_op"))
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
    if generation_for_game(target) == "th06_th08" and kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
        if kind == "return":
            return wrap_event_rank(["    ins_1();"], event, target)
        return [f"    // old target drops {kind}: {text}"]
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
