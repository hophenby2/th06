from __future__ import annotations

import argparse
import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .anm_catalog import choose_script, remap_set_script
from .backend import choose_difficulty, compile_bullet_emitter, compile_ir_op_event, compile_object, definition_emitter_state, first_difficulty_group, normalize_difficulty, parse_int_literal, wrap_ranked_lines
from .object_lifter import lift_all_objects, summarize_by_kind
from .parser import parse_decl
from .reference import validate_opcode_args
from .semantics import bullet_shape_semantic, encode_bullet_shape, encode_spread_style, generation_for_game, lifted_raw_coverage_policy, opcode_map_for, remap_raw_arg_by_semantic, spread_semantic, unsupported_bullet_transform_mode_reason
from .spread_ir import add_float_expr, double_flower_aux_config_args, double_flower_center_delta, double_flower_lowering_for_th12, halve_double_flower_layer_args, negated_float_expr, th12_aux_emitter_id
from .transform_ir import BulletTransformIR, TransformTimelineState, build_th12_to_th13plus_slot_maps_from_args, lower_transform_opcode_to_instruction
from .luastg_backend import emit_luastg_file
from .luastg_lifter import emit_luastg_ir_json
from .luastg_normalizer import emit_normalized_json, normalize_luastg_file


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
        if generation_for_game(target) == "th06_th08" and params:
            body_lines = old_target_param_initializers(params) + body_lines
        if params:
            body_lines = drop_redeclared_param_vars(body_lines, params)
        lines.extend(body_lines)
        lines.append("}")
    if generation_for_game(target) == "th06_th08":
        lines = normalize_old_target_lines(lines)
    return "\n".join(lines)


def stage06_th12_to_th15_resources(kind: str) -> dict[str, list[str]]:
    if kind == "stage":
        return {"anim": ["enemy.anm", "st06enm.anm"], "ecli": ["default.ecl", "st06bs.ecl"]}
    return {}


def is_stage06_boss_function(name: str) -> bool:
    return name.startswith("Boss") or name in {"HPWait", "MBossCard1LaserHit"}


def emit_th15_stage06_mainboss_wrapper() -> list[str]:
    return [
        "void MainBoss()",
        "{",
        "    // th15 stage-side boss wrapper, mirroring th15 st06.decl",
        "    ins_519();",
        "    ins_301(\"Boss\", 144.0f, -16.0f, 40, 1000, 1);",
        "    ins_519();",
        "+1:",
        "    ins_520();",
        "    ins_524(81);",
        "+60:",
        "    ins_518(2);",
        "    ins_519();",
        "    return;",
        "}",
    ]


def emit_transpile_selected_functions(program, objects, target: str, selected_functions: set[str], resources: dict[str, list[str]], header_note: str, include_stage_wrapper: bool = False) -> str:
    lines: list[str] = []
    lines.append(f"// source: {program.source}")
    lines.append(f"// source game: {program.game}")
    lines.append(f"// target: {target}")
    lines.append(header_note)
    for resource, entries in resources.items():
        if not should_emit_resource(resource, target):
            continue
        quoted = "; ".join(f'"{entry}"' for entry in entries)
        lines.append(f"{resource} {{ {quoted}; }}")
    if include_stage_wrapper:
        lines.append("// top-level declarations")
        lines.append("void MainBossSpell();")
        lines.append("")
        lines.extend(emit_th15_stage06_mainboss_wrapper())
    by_function: dict[str, list[object]] = {}
    for obj in objects:
        function = getattr(obj, "function", "")
        if function in selected_functions:
            by_function.setdefault(function, []).append(obj)

    function_params = inferred_function_params(program)
    for function in [func.name for func in program.functions if func.name in selected_functions]:
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


def emit_th12_stage06_to_th15_pair(program, objects) -> tuple[str, str]:
    function_names = {func.name for func in program.functions}
    boss_functions = {name for name in function_names if is_stage06_boss_function(name)}
    stage_functions = function_names - boss_functions
    stage = emit_transpile_selected_functions(
        program,
        objects,
        "th15",
        stage_functions,
        stage06_th12_to_th15_resources("stage"),
        "// th12 stage06 -> th15 stage-side lowering; resources follow th15 st06.decl",
        include_stage_wrapper=True,
    )
    boss = emit_transpile_selected_functions(
        program,
        objects,
        "th15",
        boss_functions,
        stage06_th12_to_th15_resources("boss"),
        "// th12 stage06 -> th15 boss-side lowering; ANM bank follows th15 st06bs.decl",
    )
    return stage, boss


def normalize_old_target_lines(lines: list[str]) -> list[str]:
    normalized: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        if "//" in line:
            line = line.split("//", 1)[0].rstrip()
            stripped = line.lstrip()
        if not stripped:
            if normalized and normalized[-1] != "":
                normalized.append("")
            continue
        if re.fullmatch(r"\+[-+]?\d+:", stripped) or re.fullmatch(r"\w+:", stripped):
            normalized.append(stripped)
            continue
        if stripped.startswith("!"):
            normalized.append(stripped)
            continue
        normalized.extend(lower_old_target_expression_line(replace_old_param_refs(line)))
    while normalized and normalized[0] == "":
        normalized.pop(0)
    return normalized







def old_target_param_initializers(params: str) -> list[str]:
    initials: list[str] = []
    int_map = {"A": 10000, "B": 10001, "C": 10002, "D": 10003, "E": 10004, "F": 10005}
    float_map = {"A": 10016, "B": 10017, "C": 10018, "D": 10019, "E": 10020, "F": 10021}
    for part in [item.strip() for item in params.split(",") if item.strip()]:
        pieces = part.split()
        name = pieces[-1] if pieces else ""
        if not re.fullmatch(r"[A-F]", name):
            continue
        if part.startswith("float"):
            initials.append(f"    ins_7([{float_map[name]}.0f], %{name});")
        else:
            initials.append(f"    ins_6([{int_map[name]}], ${name});")
    return initials


def replace_old_param_refs(line: str) -> str:
    int_map = {"A": "[10000]", "B": "[10001]", "C": "[10002]", "D": "[10003]", "E": "[10004]", "F": "[10005]"}
    float_map = {"A": "[10016.0f]", "B": "[10017.0f]", "C": "[10018.0f]", "D": "[10019.0f]", "E": "[10020.0f]", "F": "[10021.0f]"}
    line = re.sub(r"\$([A-F])\b", lambda match: int_map.get(match.group(1), match.group(0)), line)
    line = re.sub(r"%([A-F])\b", lambda match: float_map.get(match.group(1), match.group(0)), line)
    return line


def lower_old_target_expression_line(line: str) -> list[str]:
    stripped = line.strip()
    match = re.fullmatch(r"ins_(\d+)\((.*)\);", stripped)
    if not match:
        return [line]
    opcode = int(match.group(1))
    args = [part.strip() for part in split_args_text(match.group(2))]
    prefix = line[:len(line) - len(line.lstrip())]
    if opcode == 2 and len(args) == 1:
        lowered = lower_old_int_expr(args[0], "[10008]")
        if lowered:
            return [prefix + item for item in [*lowered, "ins_2([10008]);"]]
    if opcode == 64 and len(args) == 4:
        setup: list[str] = []
        out_args = list(args)
        for index in (2, 3):
            lowered = lower_old_float_expr(out_args[index], f"[{10030 + index - 2}.0f]")
            if lowered:
                setup.extend(lowered)
                out_args[index] = f"[{10030 + index - 2}.0f]"
        if setup:
            return [prefix + item for item in [*setup, f"ins_64({', '.join(out_args)});"]]
    if opcode == 165 and len(args) == 1:
        lowered = lower_old_float_expr(args[0], "[10030.0f]")
        if lowered:
            return [prefix + item for item in [*lowered, "ins_165([10030.0f]);"]]
    return [line]


def split_args_text(text: str) -> list[str]:
    args: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    escape = False
    for char in text:
        if in_string:
            current.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            current.append(char)
        elif char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current or text.strip():
        args.append("".join(current).strip())
    return args


def lower_old_int_expr(expr: str, temp: str) -> list[str] | None:
    expr = expr.strip()
    match = re.fullmatch(r"(\[[^\]]+\]|[-+]?\d+)\s*%\s*([-+]?\d+)", expr)
    if match:
        return [f"ins_6({temp}, {match.group(1)});", f"ins_14({temp}, {match.group(2)});"]
    match = re.fullmatch(r"\((\[[^\]]+\]|[-+]?\d+)\s*%\s*([-+]?\d+)\)\s*([+-])\s*([-+]?\d+)", expr)
    if match:
        op = "ins_10" if match.group(3) == "+" else "ins_11"
        return [f"ins_6({temp}, {match.group(1)});", f"ins_14({temp}, {match.group(2)});", f"{op}({temp}, {match.group(4)});"]
    return None


def lower_old_float_expr(expr: str, temp: str) -> list[str] | None:
    expr = expr.strip()
    match = re.fullmatch(r"(?:_f\(0\)|0(?:\.0f)?)\s*-\s*(\[[^\]]+\.0f\])", expr)
    if match:
        return [f"ins_7({temp}, 0.0f);", f"ins_16({temp}, {match.group(1)});"]
    match = re.fullmatch(r"(\[[^\]]+\.0f\])\s*([+-])\s*(?:_f\()?([-+]?\d+(?:\.\d+)?)(?:f)?(?:\))?", expr)
    if match:
        op = "ins_15" if match.group(2) == "+" else "ins_16"
        value = match.group(3)
        if "." not in value:
            value = f"{value}.0f"
        elif not value.endswith("f"):
            value = f"{value}f"
        return [f"ins_7({temp}, {match.group(1)});", f"{op}({temp}, {value});"]
    return None


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
    result = align_stage_resources_to_target(result, objects, target)
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


def align_stage_resources_to_target(resources: dict[str, list[str]], objects: list[object], target: str) -> dict[str, list[str]]:
    if generation_for_game(target) != "th13_plus":
        return resources
    source_path = ""
    source_game = ""
    for obj in objects:
        source_path = str(getattr(obj, "source", "") or getattr(obj, "fields", {}).get("source", "") or source_path)
        source_game = str(getattr(obj, "game", "") or source_game)
        if source_path and source_game:
            break
    if generation_for_game(source_game) not in {"th10_th11", "th12"}:
        return resources
    name = Path(source_path).name.lower()
    match = re.fullmatch(r"stage(\d\d)\.decl", name)
    if not match:
        return resources
    stage = match.group(1)
    result = {key: list(value) for key, value in resources.items()}
    anim_entries = result.get("anim", [])
    result["anim"] = ["enemy.anm", f"st{stage}enm.anm"] if anim_entries else [f"st{stage}enm.anm"]
    ecli_entries = result.get("ecli", [])
    if ecli_entries:
        target_stage = Path(f"E:/fork/th062/{target}/st{stage}.decl")
        if target_stage.exists():
            target_program = parse_decl(str(target_stage))
            target_ecli = target_program.resources.get("ecli", [])
            if target_ecli:
                result["ecli"] = target_ecli
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
        anm_setup = fields.get("anm_setup", {})
        lines.append(f"// entry alias lowering {obj.family} -> {target}: {fields.get('reason', '')}")
        for alias, real in needed:
            lines.extend([f"void {alias}()", "{"])
            setup = anm_setup.get(alias) if isinstance(anm_setup, dict) else None
            if isinstance(setup, dict):
                z_index = setup.get("z_index")
                z_index_after = setup.get("z_index_after")
                if z_index is not None and not z_index_after:
                    lines.append(f"    ins_410({z_index});")
                preferred = setup.get("preferred_script")
                preferred_script = preferred if isinstance(preferred, int) else None
                chosen = choose_script(target, "stage", str(setup.get("purpose") or "stage_enemy"), preferred_script, kind="main")
                if chosen is not None:
                    lines.append(f"    ins_258({chosen.bank});")
                    lines.append(f"    ins_262({setup.get('main_slot', 1)}, {chosen.script});")
                if z_index is not None and z_index_after:
                    lines.append(f"    ins_410({z_index});")
            lines.extend([f"    @{real}();", "    return;", "}"])
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


def should_preserve_dynamic_bullet_config(ins) -> bool:
    return getattr(ins, "opcode", None) in {502, 503, 504, 505, 506, 507, 508, 523, 524, 525, 600, 602, 603, 604, 605, 606, 607, 608, 609, 611, 612, 624, 625, 626, 627, 628}


def should_cover_lifted_raw_instruction(ins, obj, source_game: str, target: str) -> bool:
    if is_fire_instruction(ins):
        return False
    policy = lifted_raw_coverage_policy(getattr(obj, "kind", ""), source_game, target, getattr(obj, "family", ""))
    if policy == "contiguous_setup_prefix":
        return True
    return not should_preserve_dynamic_bullet_config(ins)


def covered_lines_for_lifted_object(obj, source_game: str, target: str) -> set[int]:
    raw = getattr(obj, "raw", [])
    if not raw:
        return set()
    if getattr(obj, "kind", None) == "LaserEmitter":
        return set()
    covered: set[int] = set()
    policy = lifted_raw_coverage_policy(getattr(obj, "kind", ""), source_game, target, getattr(obj, "family", ""))
    if policy == "contiguous_setup_prefix":
        previous_line: int | None = None
        for ins in raw:
            line_no = getattr(ins, "line_no", None)
            if previous_line is not None and line_no != previous_line + 1:
                break
            if is_fire_instruction(ins):
                break
            if should_cover_lifted_raw_instruction(ins, obj, source_game, target):
                covered.add(line_no)
            previous_line = line_no
        return covered
    for ins in raw:
        if is_fire_instruction(ins):
            break
        if should_cover_lifted_raw_instruction(ins, obj, source_game, target):
            covered.add(ins.line_no)
    return covered


def should_emit_semantic_object_in_timeline(obj, source_game: str, target: str) -> bool:
    if getattr(obj, "kind", None) == "LaserEmitter":
        return False
    if (
        getattr(obj, "kind", None) == "BulletEmitter"
        and generation_for_game(source_game) == "th13_plus"
        and generation_for_game(target) == "th12"
    ):
        return False
    return True


def object_for_timeline_compile(obj, bullet_state: BulletLoweringState | None):
    if (
        bullet_state
        and getattr(obj, "kind", None) == "BulletEmitter"
        and str(getattr(obj, "id", "")) in bullet_state.curve_laser_emitters
    ):
        cloned = copy.copy(obj)
        cloned.semantics = copy.deepcopy(getattr(obj, "semantics", {}))
        cloned.semantics["curve_laser_fire"] = True
        return cloned
    return obj


def emit_function_body(function_objects: list[object], target: str) -> list[str]:
    timelines = [obj for obj in function_objects if getattr(obj, "kind", None) == "Timeline"]
    if (
        target == "th15"
        and timelines
        and getattr(timelines[0], "game", "") == "th10"
        and getattr(timelines[0], "function", "") == "MapleEnemy"
    ):
        return [
            "    // omitted TH10 MapleEnemy visual helper for TH15 stability",
            "    return;",
        ]
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
    source_game = getattr(timeline, "game", "unknown")
    object_starts: dict[int, list[object]] = {}
    covered_lines: set[int] = set()
    for obj in semantic_objects:
        raw = getattr(obj, "raw", [])
        if not raw:
            object_starts.setdefault(getattr(obj, "source_line", 0), []).append(obj)
            continue
        object_starts.setdefault(raw[0].line_no, []).append(obj)
        covered_lines.update(covered_lines_for_lifted_object(obj, source_game, target))

    lines: list[str] = []
    lines.append(f"    // Timeline lowering {timeline.family} -> {target}; interleaved structured draft")
    lines.append("    // control-flow, async scheduling, and expression semantics require target-game verification")
    skipped_debug_selector = False
    if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        bullet_state = make_bullet_lowering_state_from_events(timeline.fields.get("statements", []), source_game, target)
    else:
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
                if not should_emit_semantic_object_in_timeline(obj, source_game, target):
                    continue
                lines.append(f"    // object {obj.kind} source_line={obj.source_line} family={obj.family}")
                compile_obj = object_for_timeline_compile(obj, bullet_state)
                for line in compile_object(compile_obj, target).splitlines():
                    lines.append(f"    {line}")
                if bullet_state:
                    bullet_state.observe_th12_definition_transforms(compile_obj, source_game, target)
        if line_no in covered_lines:
            continue
        context = {"function": getattr(timeline, "function", ""), "source_path": getattr(timeline, "source", "")}
        lines.extend(emit_timeline_event(event, getattr(timeline, "game", "unknown"), target, bullet_state, context))
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
    if generation_for_game(source_game) == "th13_plus" and generation_for_game(target) == "th12":
        bullet_state = BulletLoweringState({}, {}, TransformTimelineState(), {}, {}, {}, set())
    elif generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        bullet_state = make_bullet_lowering_state_from_events(timeline.fields.get("statements", []), source_game, target)
    else:
        bullet_state = None
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
        context = {"function": getattr(timeline, "function", ""), "source_path": getattr(timeline, "source", "")}
        lines.extend(emit_timeline_event(event, source_game, target, bullet_state, context))
    loops = timeline.fields.get("loops", [])
    if loops:
        lines.append("    // detected loops:")
        for loop in loops:
            lines.append(f"    // - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return lines



@dataclass
class BulletLoweringState:
    double_flower_aux: dict[str, str]
    transform_next_index: dict[str, int]
    transform_timeline: TransformTimelineState
    double_flower_ways: dict[str, str]
    pending_curve_laser_offsets: dict[str, tuple[str, str]]
    pending_origin_distance: dict[str, str]
    curve_laser_emitters: set[str]

    def activate_double_flower(self, emitter_id: str) -> str | None:
        aux_id = th12_aux_emitter_id(emitter_id)
        if aux_id:
            self.double_flower_aux[emitter_id] = aux_id
            self.transform_next_index[aux_id] = self.transform_next_index.get(emitter_id, 0)
        return aux_id

    def deactivate_double_flower(self, emitter_id: str) -> None:
        self.double_flower_aux.pop(emitter_id, None)
        self.double_flower_ways.pop(emitter_id, None)

    def aux_for(self, emitter_id: str) -> str | None:
        return self.double_flower_aux.get(emitter_id)

    def next_transform_index(self, emitter_id: str) -> int:
        index = self.transform_next_index.get(emitter_id, 0)
        self.transform_next_index[emitter_id] = index + 1
        aux_id = self.aux_for(emitter_id)
        if aux_id:
            self.transform_next_index[aux_id] = index + 1
        return index

    def observe_transform_index(self, emitter_id: str, index: object) -> None:
        text = str(index)
        if re.fullmatch(r"-?\d+", text):
            self.transform_next_index[emitter_id] = max(self.transform_next_index.get(emitter_id, 0), int(text) + 1)
            aux_id = self.aux_for(emitter_id)
            if aux_id:
                self.transform_next_index[aux_id] = self.transform_next_index[emitter_id]

    def reset_transform_index(self, emitter_id: str) -> None:
        self.transform_next_index[emitter_id] = 0
        self.transform_timeline.reset_emitter(emitter_id)
        self.deactivate_double_flower(emitter_id)

    def normalize_th12_transform(self, args: list[str], source_game: str, target: str) -> list[str] | None:
        rendered, _semantics = self.transform_timeline.annotate_th12_to_th13plus_args(args, source_game, target)
        return rendered

    def observe_th12_definition_transforms(self, obj: object, source_game: str, target: str) -> None:
        if generation_for_game(source_game) != "th12" or generation_for_game(target) != "th13_plus":
            return
        if getattr(obj, "kind", None) != "BulletEmitter":
            return
        definition = definition_emitter_state(obj)
        for transform in getattr(definition, "transforms", []) or []:
            if getattr(transform, "raw_opcode", None) != 509 or len(getattr(transform, "raw_args", [])) != 8:
                continue
            if (getattr(transform, "semantics", {}) or {}).get("drop"):
                continue
            args = [str(arg) for arg in getattr(transform, "raw_args", [])]
            if args[3] == "8" and (getattr(transform, "semantics", {}) or {}).get("effective_start") is not None:
                self.transform_timeline.next_start_by_emitter_channel[(args[0], args[2])] = str(int(args[5]) + int(args[4])) if re.fullmatch(r"-?\d+", args[5]) and re.fullmatch(r"-?\d+", args[4]) else f"{args[5]} + {args[4]}"

    def observe_count(self, emitter_id: str, ways: object) -> None:
        if self.aux_for(emitter_id):
            self.double_flower_ways[emitter_id] = str(ways)

    def ways_for(self, emitter_id: str) -> str | None:
        return self.double_flower_ways.get(emitter_id)

    def observe_absolute_origin(self, emitter_id: str, x: object, y: object) -> None:
        self.pending_curve_laser_offsets[emitter_id] = (str(x), str(y))

    def pop_curve_laser_offset(self, emitter_id: str) -> tuple[str, str] | None:
        return self.pending_curve_laser_offsets.pop(emitter_id, None)

    def observe_origin_distance(self, emitter_id: str, distance: object) -> None:
        self.pending_origin_distance[emitter_id] = str(distance)

    def pop_origin_distance(self, emitter_id: str) -> str | None:
        return self.pending_origin_distance.pop(emitter_id, None)


def make_bullet_lowering_state(function_objects: list[object], source_game: str, target: str) -> BulletLoweringState | None:
    if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        return BulletLoweringState({}, {}, TransformTimelineState(), {}, {}, {}, set())
    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    aux: dict[str, str] = {}
    for obj in function_objects:
        if getattr(obj, "kind", None) != "BulletEmitter" or getattr(obj, "family", "") != "th13plus":
            continue
        emitter_id = str(getattr(obj, "id", ""))
        spread = getattr(obj, "semantics", {}).get("bullet", {}).get("spread", {})
        lowering = double_flower_lowering_for_th12(emitter_id, spread)
        if lowering:
            aux[emitter_id] = lowering.aux_emitter_id
    return BulletLoweringState(aux, {}, TransformTimelineState(), {}, {}, {}, set())


def make_bullet_lowering_state_from_events(events: list[dict[str, object]], source_game: str, target: str) -> BulletLoweringState | None:
    state = make_bullet_lowering_state([], source_game, target)
    if not state:
        return None
    transform_args: list[list[object]] = []
    for event in events:
        if event.get("kind") != "instruction":
            continue
        opcode = int(event.get("opcode") or -1)
        args = event.get("args", [])
        if opcode == 509:
            transform_args.append(list(args))
        elif opcode == 611:
            emitter_id = str(args[0]) if args else "0"
            state.curve_laser_emitters.add(emitter_id)
    state.transform_timeline.slot_maps = build_th12_to_th13plus_slot_maps_from_args(transform_args, source_game, target)
    return state


def lower_bullet_fire_opcode(opcode: int, args: list[object], source_game: str, target: str, bullet_state: BulletLoweringState | None) -> list[str] | None:
    if opcode == 401 and generation_for_game(source_game) == "th10_th11" and generation_for_game(target) == "th13_plus":
        emitter_id = str(args[0]) if args else "0"
        return [
            f"    // dynamic bullet fire lowering {source_game}->{target}: ins_401 -> ins_601",
            f"    ins_601({emitter_id});",
        ]
    if opcode == 611 and generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        emitter_id = str(args[0]) if args else "0"
        if bullet_state:
            bullet_state.pop_curve_laser_offset(emitter_id)
            bullet_state.pop_origin_distance(emitter_id)
        lines = [f"    // dynamic curve laser fire lowering {source_game}->{target}: ins_611 -> ins_711"]
        lines.append(f"    ins_711({emitter_id});")
        return lines
    if opcode == 501 and generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        emitter_id = str(args[0]) if args else "0"
        lines: list[str] = []
        if bullet_state:
            distance = bullet_state.pop_origin_distance(emitter_id)
            if distance is not None:
                lines.extend([
                    f"    // dynamic bullet distance lowering {source_game}->{target}: pending ins_524 -> ins_627 before fire",
                    f"    ins_627({emitter_id}, {distance});",
                ])
        lines.extend([
            f"    // dynamic bullet fire lowering {source_game}->{target}: ins_501 -> ins_601",
            f"    ins_601({emitter_id});",
        ])
        return lines
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


def emitter_arg_replaced(args: list[str], emitter_id: str) -> list[str]:
    if not args:
        return args
    return [emitter_id, *args[1:]]


def ranked_or_plain_lines(
    opcode: int,
    args: list[str],
    difficulty_literals: object,
    comment: str,
    extra_ranked: list[tuple[int, list[str]]] | None = None,
    extra_plain: list[tuple[int, list[str]]] | None = None,
) -> list[str]:
    ranked = emit_ranked_raw_instruction(opcode, args, difficulty_literals)
    if ranked:
        lines = [comment + "; ranked args from source difficulty literals", *ranked]
        for extra_opcode, extra_args in extra_ranked or []:
            extra = emit_ranked_raw_instruction(extra_opcode, extra_args, difficulty_literals)
            if extra:
                lines.extend(extra)
            else:
                lines.append(f"    ins_{extra_opcode}({', '.join(extra_args)});")
        return lines
    lines = [comment, f"    ins_{opcode}({', '.join(args)});"]
    for extra_opcode, extra_args in extra_plain or []:
        lines.append(f"    ins_{extra_opcode}({', '.join(extra_args)});")
    return lines


def lower_bullet_create_opcode(opcode: int, args: list[object], source_game: str, target: str, bullet_state: BulletLoweringState | None) -> list[str] | None:
    if opcode != 600 or generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    emitter_id = str(args[0]) if args else "0"
    if bullet_state:
        bullet_state.reset_transform_index(emitter_id)
    return [
        f"    // dynamic bullet create lowering {source_game}->{target}: ins_600 -> ins_500",
        f"    ins_500({emitter_id});",
    ]


def lower_bullet_config_opcode(opcode: int, args: list[object], source_game: str, target: str, difficulty_literals: object = None, bullet_state: BulletLoweringState | None = None) -> list[str] | None:
    if generation_for_game(source_game) == "th10_th11" and generation_for_game(target) == "th13_plus":
        mapping = {
            400: 600,
            402: 602,
            404: 604,
            405: 605,
            406: 606,
            407: 607,
        }
        mapped = mapping.get(opcode)
        if mapped is None:
            return None
        rendered_args = [str(arg) for arg in args]
        if opcode == 402 and len(rendered_args) >= 3:
            rendered_args[1] = encode_bullet_shape(bullet_shape_semantic(source_game, rendered_args[1]), target, rendered_args[1])
        elif opcode == 407 and len(rendered_args) >= 2:
            rendered_args[1] = encode_spread_style(spread_semantic(source_game, rendered_args[1]), target, rendered_args[1])
        return ranked_or_plain_lines(
            mapped,
            rendered_args,
            difficulty_literals,
            f"    // dynamic bullet config lowering {source_game}->{target}: ins_{opcode} -> ins_{mapped}",
        )
    if opcode == 502 and generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus" and len(args) >= 3:
        emitter_id = str(args[0])
        if bullet_state and emitter_id in bullet_state.curve_laser_emitters:
            rendered_args = [emitter_id, "0", "2"]
            return [
                f"    // curve laser material lowering {source_game}->{target}: TH13+ curve laser uses visible sprite/color",
                f"    ins_602({', '.join(rendered_args)});",
            ]
    if opcode == 524 and generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus" and len(args) >= 2:
        emitter_id = str(args[0])
        if bullet_state:
            bullet_state.observe_origin_distance(emitter_id, args[1])
            return [
                f"    // dynamic bullet distance lowering {source_game}->{target}: defer ins_524 until base origin is known",
            ]
        rendered_args = [str(arg) for arg in args]
        return [
            f"    // dynamic bullet distance lowering {source_game}->{target}: ins_524 -> ins_627",
            f"    ins_627({', '.join(rendered_args)});",
        ]
    if opcode == 525 and generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus" and len(args) >= 3:
        emitter_id = str(args[0])
        if bullet_state and emitter_id in bullet_state.curve_laser_emitters:
            rendered_args = [str(arg) for arg in args]
            return [
                f"    // test TH12 absolute curve-laser origin lowering {source_game}->{target}: ins_525 -> ins_628",
                f"    ins_628({', '.join(rendered_args)});",
            ]
        distance = bullet_state.pop_origin_distance(emitter_id) if bullet_state else None
        if bullet_state:
            bullet_state.observe_absolute_origin(emitter_id, args[1], args[2])
        rendered_args = [str(arg) for arg in args]
        lines = [
            f"    // dynamic absolute bullet origin lowering {source_game}->{target}: ins_525 -> ins_628",
            f"    ins_628({', '.join(rendered_args)});",
        ]
        if distance is not None:
            lines.extend([
                f"    // dynamic bullet distance lowering {source_game}->{target}: preserved preceding ins_524 after absolute base",
                f"    ins_627({emitter_id}, {distance});",
            ])
        return lines
    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    mapping = {
        602: 502,
        603: 503,
        604: 504,
        605: 505,
        606: 506,
        607: 507,
        608: 508,
        624: 521,
        625: 522,
    }
    mapped = mapping.get(opcode)
    if mapped is None:
        return None
    rendered_args = [str(arg) for arg in args]
    if opcode == 607 and len(rendered_args) >= 2:
        spread = spread_semantic(source_game, rendered_args[1])
        flower_lowering = double_flower_lowering_for_th12(rendered_args[0], spread)
        if flower_lowering and bullet_state:
            emitter_id = rendered_args[0]
            aux_id = bullet_state.activate_double_flower(emitter_id)
            if aux_id:
                primary_args = [emitter_id, flower_lowering.primary_style]
                aux_args = [aux_id, flower_lowering.aux_style]
                return [
                    f"    // TH15 double flower spread lowered to two TH12 single-side flower slots: {emitter_id}+{aux_id}",
                    f"    ins_507({', '.join(primary_args)});",
                    f"    ins_500({aux_id});",
                    f"    ins_507({', '.join(aux_args)});",
                ]
        if bullet_state and rendered_args:
            bullet_state.deactivate_double_flower(rendered_args[0])
    rendered_args = remap_raw_arg_by_semantic(source_game, target, opcode, mapped, rendered_args)
    aux_id = bullet_state.aux_for(str(args[0])) if bullet_state and args else None
    if bullet_state and opcode == 606 and len(rendered_args) >= 2 and args:
        bullet_state.observe_count(str(args[0]), rendered_args[1])
    aux_args = double_flower_aux_config_args(rendered_args, aux_id) if aux_id else None
    if aux_id and opcode == 606:
        rendered_args, difficulty_literals = halve_double_flower_layer_args(rendered_args, difficulty_literals)
        aux_args = double_flower_aux_config_args(rendered_args, aux_id)
    if aux_id and opcode == 604 and len(rendered_args) >= 3:
        # The primary double-flower slot is the TH12 left-bias flower, and the
        # auxiliary slot is right-bias.  Reverse the source angular step on the
        # left side, and offset both sides by pi/(2*way) so their shared center
        # stays aligned with TH15's native double-flower center.
        delta = double_flower_center_delta(bullet_state.ways_for(str(args[0])) if bullet_state else None)
        rendered_args = rendered_args[:]
        if delta:
            rendered_args[1] = add_float_expr(rendered_args[1], f"-{delta}")
        rendered_args[2] = negated_float_expr(rendered_args[2])
        if aux_args and delta:
            aux_args = aux_args[:]
            aux_args[1] = add_float_expr(aux_args[1], delta)
    comment = f"    // dynamic bullet config lowering {source_game}->{target}: ins_{opcode} -> ins_{mapped}"
    if aux_args:
        comment = f"    // dynamic bullet config lowering {source_game}->{target}: ins_{opcode} -> ins_{mapped}; mirrored to double-flower slot {aux_id}"
    return ranked_or_plain_lines(
        mapped,
        rendered_args,
        difficulty_literals,
        comment,
        extra_ranked=[(mapped, aux_args)] if aux_args else None,
        extra_plain=[(mapped, aux_args)] if aux_args else None,
    )


def lower_bullet_transform_opcode(opcode: int, args: list[object], source_game: str, target: str, difficulty_literals: object = None, bullet_state: BulletLoweringState | None = None) -> list[str] | None:
    if generation_for_game(source_game) == "th10_th11" and generation_for_game(target) == "th13_plus":
        if opcode != 409 or len(args) != 8:
            return None
        transform_ir = BulletTransformIR.from_opcode(source_game, opcode, [str(arg) for arg in args])
        if not transform_ir or transform_ir.unsupported_reason(target):
            reason = unsupported_bullet_transform_mode_reason(source_game, target, str(args[3]) if len(args) > 3 else "")
            return [
                f"    // dropped unsupported bullet transform mode from ins_409: {reason}",
                f"    // original args: {', '.join(str(arg) for arg in args)}",
            ]
        target_instruction = transform_ir.lower_to(target)
        if not target_instruction:
            return None
        return ranked_or_plain_lines(
            target_instruction.opcode,
            target_instruction.args,
            difficulty_literals,
            f"    // dynamic bullet transform lowering {source_game}->{target}: ins_409 -> ins_{target_instruction.opcode}",
        )

    if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus":
        if opcode != 509 or len(args) != 8:
            return None
        rendered = [str(arg) for arg in args]
        curve_laser = bool(bullet_state and rendered[0] in bullet_state.curve_laser_emitters)
        if curve_laser and rendered[3] == "512":
            return [
                "    // dropped TH12 curve-laser uncancelable-time transform before TH15 lowering",
                f"    // original args: {', '.join(rendered)}",
            ]
        if curve_laser and bullet_state:
            rendered = rendered[:]
            rendered[1] = str(bullet_state.next_transform_index(rendered[0]))
        elif bullet_state:
            normalized = bullet_state.normalize_th12_transform(rendered, source_game, target)
            if normalized is None:
                return [
                    f"    // dropped unsupported bullet transform mode from ins_509: {unsupported_bullet_transform_mode_reason(source_game, target, rendered[3])}",
                    f"    // original args: {', '.join(rendered)}",
                ]
            rendered = normalized
        reason = unsupported_bullet_transform_mode_reason(source_game, target, rendered[3])
        if reason:
            return [
                f"    // dropped unsupported bullet transform mode from ins_509: {reason}",
                f"    // original args: {', '.join(rendered)}",
            ]
        transform_ir = BulletTransformIR.from_opcode(source_game, opcode, rendered)
        if not transform_ir:
            return None
        target_instruction = transform_ir.lower_to(target)
        if not target_instruction:
            return None
        target_opcode = target_instruction.opcode
        converted = target_instruction.args
        if curve_laser and rendered[3] == "8" and len(converted) >= 6 and converted[5] == "-999999":
            converted[5] = "0"
        return ranked_or_plain_lines(
            target_opcode,
            converted,
            difficulty_literals,
            f"    // dynamic bullet transform lowering {source_game}->{target}: ins_509 -> ins_{target_opcode}",
        )

    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    lowered = None
    if opcode == 609 and len(args) == 8:
        lowered = lower_transform_opcode_to_instruction(source_game, target, opcode, args)
        if lowered and bullet_state:
            bullet_state.observe_transform_index(str(args[0]), args[1])
    elif opcode == 611 and len(args) == 7:
        if bullet_state:
            index = bullet_state.next_transform_index(str(args[0]))
        else:
            index = 0
        lowered = lower_transform_opcode_to_instruction(source_game, target, opcode, args, index)
    elif opcode == 612 and len(args) == 11:
        if bullet_state:
            index = bullet_state.next_transform_index(str(args[0]))
        else:
            index = 0
        lowered = lower_transform_opcode_to_instruction(source_game, target, opcode, args, index)
    if not lowered:
        return None
    aux_id = bullet_state.aux_for(str(args[0])) if bullet_state and args else None
    converted = lowered.args
    aux_converted = emitter_arg_replaced(converted, aux_id) if aux_id else None
    comment = f"    // dynamic bullet transform lowering {source_game}->{target}: ins_{opcode} -> ins_{lowered.opcode}"
    if aux_converted:
        comment = f"    // dynamic bullet transform lowering {source_game}->{target}: ins_{opcode} -> ins_{lowered.opcode}; mirrored to double-flower slot {aux_id}"
    return ranked_or_plain_lines(
        lowered.opcode,
        converted,
        difficulty_literals,
        comment,
        extra_ranked=[(lowered.opcode, aux_converted)] if aux_converted else None,
        extra_plain=[(lowered.opcode, aux_converted)] if aux_converted else None,
    )


def lower_th13_misc_bullet_opcode(opcode: int, args: list[object], source_game: str, target: str, difficulty_literals: object = None, bullet_state: BulletLoweringState | None = None) -> list[str] | None:
    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    if opcode == 627 and len(args) == 2:
        rendered = [str(arg) for arg in args]
        aux_id = bullet_state.aux_for(rendered[0]) if bullet_state else None
        aux_rendered = emitter_arg_replaced(rendered, aux_id) if aux_id else None
        comment = f"    // dynamic bullet distance lowering {source_game}->{target}: ins_627 -> ins_524"
        if aux_rendered:
            comment = f"    // dynamic bullet distance lowering {source_game}->{target}: ins_627 -> ins_524; mirrored to double-flower slot {aux_id}"
        return ranked_or_plain_lines(
            524,
            rendered,
            difficulty_literals,
            comment,
            extra_ranked=[(524, aux_rendered)] if aux_rendered else None,
            extra_plain=[(524, aux_rendered)] if aux_rendered else None,
        )
    return None


def lower_th13_diff_float_opcode(opcode: int, args: list[object], source_game: str, target: str, difficulty_literals: object = None) -> list[str] | None:
    if generation_for_game(source_game) != "th13_plus" or generation_for_game(target) != "th12":
        return None
    if opcode != 536 or len(args) != 5:
        return None
    rendered = [str(arg) for arg in args]
    ranked = emit_ranked_raw_instruction(436, rendered, difficulty_literals)
    if ranked:
        return [f"    // dynamic difficulty float lowering {source_game}->{target}: ins_536 -> ins_436; ranked args from source difficulty literals", *ranked]
    return [
        f"    // dynamic difficulty float lowering {source_game}->{target}: ins_536 -> ins_436",
        f"    ins_436({', '.join(rendered)});",
    ]


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


def is_th12_stage06_to_th15_context(source_game: str, target: str, context: dict[str, object] | None) -> bool:
    if source_game != "th12" or target != "th15" or not context:
        return False
    return str(context.get("source_path", "")).replace("\\", "/").endswith("/th12/stage06.decl")


def th12_stage06_to_th15_mainfront_boundary(event: dict[str, object], source_game: str, target: str, context: dict[str, object] | None) -> list[str] | None:
    if not is_th12_stage06_to_th15_context(source_game, target, context):
        return None
    if str(context.get("function", "")) != "main" or event.get("kind") != "call":
        return None
    if str(event.get("function", "")) != "MainSub02":
        return None
    return [
        "    // th15 st06 MainFront boundary before third wave: clear old enemies/bullets and advance chapter",
        "    ins_525();",
        "    ins_616(640.0f);",
        "    ins_524(1);",
        "    ins_23(10);",
    ]


def lower_raw_instruction_event(opcode: int, args: list[object], text: str, source_game: str, target: str, difficulty_literals: object = None, ir_op: dict[str, object] | None = None, context: dict[str, object] | None = None) -> list[str]:
    if ir_op:
        semantic_map = opcode_map_for(source_game, target, opcode)
        if semantic_map is not None and str(ir_op.get("op_key") or "").startswith("raw."):
            ir_op = {
                **ir_op,
                "op_key": semantic_map.semantic,
                "source_game": source_game,
                "source_opcode": opcode,
            }
        semantic_line = compile_ir_op_event(ir_op, target, context=context)
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



def emit_timeline_event(event: dict[str, object], source_game: str = "unknown", target: str = "", bullet_state: BulletLoweringState | None = None, context: dict[str, object] | None = None) -> list[str]:
    kind = event.get("kind")
    text = str(event.get("text") or "")
    if not text:
        return []
    if kind == "instruction":
        opcode = event.get("opcode")
        opcode_int = int(opcode) if opcode is not None else -1
        args = event.get("args", [])
        if (
            is_th12_stage06_to_th15_context(source_game, target, context)
            and opcode_int in {256, 257}
            and args
            and str(args[0]).strip('"') == "Boss"
            and str(context.get("function", "")) == "main"
        ):
            return wrap_event_rank([
                "    // th12 inline Boss spawn redirected through th15 stage-side MainBoss wrapper",
                "    @MainBoss();",
            ], event, target)
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
        create_lowered = lower_bullet_create_opcode(opcode_int, list(args), source_game, target, bullet_state)
        if create_lowered:
            return wrap_event_rank(create_lowered, event, target)
        if generation_for_game(source_game) == "th12" and generation_for_game(target) == "th13_plus" and opcode_int == 509 and len(args) >= 4:
            reason = unsupported_bullet_transform_mode_reason(source_game, target, args[3])
            if reason:
                return wrap_event_rank([
                    f"    // dropped unsupported bullet transform mode from ins_509: {reason}",
                    f"    // original: {text}",
                ], event, target)
        fire_lowered = lower_bullet_fire_opcode(opcode_int, list(args), source_game, target, bullet_state)
        if fire_lowered:
            return wrap_event_rank(fire_lowered, event, target)
        config_lowered = lower_bullet_config_opcode(opcode_int, list(args), source_game, target, event.get("difficulty_literals", []), bullet_state)
        if config_lowered:
            if any(line.strip().startswith("!") for line in config_lowered):
                return config_lowered
            return wrap_event_rank(config_lowered, event, target)
        transform_lowered = lower_bullet_transform_opcode(opcode_int, list(args), source_game, target, event.get("difficulty_literals", []), bullet_state)
        if transform_lowered:
            if any(line.strip().startswith("!") for line in transform_lowered):
                return transform_lowered
            return wrap_event_rank(transform_lowered, event, target)
        misc_bullet_lowered = lower_th13_misc_bullet_opcode(opcode_int, list(args), source_game, target, event.get("difficulty_literals", []), bullet_state)
        if misc_bullet_lowered:
            if any(line.strip().startswith("!") for line in misc_bullet_lowered):
                return misc_bullet_lowered
            return wrap_event_rank(misc_bullet_lowered, event, target)
        diff_float_lowered = lower_th13_diff_float_opcode(opcode_int, list(args), source_game, target, event.get("difficulty_literals", []))
        if diff_float_lowered:
            if any(line.strip().startswith("!") for line in diff_float_lowered):
                return diff_float_lowered
            return wrap_event_rank(diff_float_lowered, event, target)
        lowered = lower_raw_instruction_event(opcode_int, list(args), text, source_game, target, event.get("difficulty_literals", []), event.get("ir_op"), context)
        if lowered:
            if any(line.strip().startswith("!") for line in lowered):
                return lowered
            return wrap_event_rank(lowered, event, target)
        return wrap_event_rank([f"    // unlifted instruction: {text}"], event, target)
    if kind == "time":
        wait = str(event.get("time") or "").strip()
        if generation_for_game(source_game) in {"th10_th11", "th12"} and generation_for_game(target) == "th13_plus" and wait:
            return wrap_event_rank([f"    ins_23({literal_time_value(wait)});"], event, target)
        return wrap_event_rank([f"    {text}"], event, target)
    if kind == "label":
        return [f"    {text}"]
    if generation_for_game(target) == "th06_th08" and kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
        if kind == "return":
            return wrap_event_rank(["    ins_1();"], event, target)
        return [f"    // old target drops {kind}: {text}"]
    if (
        target == "th12"
        and generation_for_game(source_game) == "th13_plus"
        and kind in {"call", "async_call"}
        and str(event.get("function", "")).startswith("EffChargePoint")
    ):
        return wrap_event_rank([f"    // dropped TH13+ charge-point effect call for TH12 stability: {text}"], event, target)
    if (
        target == "th15"
        and source_game == "th10"
        and kind in {"call", "async_call"}
        and str(event.get("function", "")) == "MapleEnemy"
    ):
        return wrap_event_rank(["    // omitted TH10 MapleEnemy visual helper create for TH15 stability"], event, target)
    if kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
        suffix = "" if text.endswith(";") else ";"
        statement_text = remap_call_statement_text(event, source_game, target, context) if kind in {"call", "async_call"} else f"{text}{suffix}"
        ranked = emit_ranked_text_from_literals(statement_text, event.get("difficulty_literals", []))
        if ranked:
            return ranked
        boundary = th12_stage06_to_th15_mainfront_boundary(event, source_game, target, context)
        if boundary:
            return wrap_event_rank([*boundary, f"    {statement_text}"], event, target)
        return wrap_event_rank([f"    {statement_text}"], event, target)
    if kind == "raw":
        raw_expr = text.strip()
        if raw_expr.endswith(";"):
            raw_expr = raw_expr[:-1].strip()
        if re.fullmatch(r"[%$]?[A-Za-z_][A-Za-z0-9_]*|[-+]?\d+(?:\.\d+)?f?", raw_expr):
            return wrap_event_rank([f"    {raw_expr};"], event, target)
        return [f"    // raw: {text}"]
    return []

def remap_call_statement_text(event: dict[str, object], source_game: str, target: str, context: dict[str, object] | None = None) -> str:
    text = str(event.get("text") or "")
    suffix = "" if text.endswith(";") else ";"
    if source_game != target and source_game in {"th10", "th11"} and generation_for_game(target) == "th13_plus":
        source_path = str(context.get("source_path", "") if context else "").replace("\\", "/")
        function = str(event.get("function", ""))
        args = [str(arg) for arg in event.get("args", [])]
        if is_stage_decl_path(source_path) and function_uses_stage_enemy_anm_args(function) and args:
            remapped = remap_th10_stage_enemy_call_anm_args(args, target)
            if remapped != args:
                async_suffix = " async" if event.get("kind") == "async_call" else ""
                return f"@{function}({', '.join(remapped)}){async_suffix};"
    if source_game != target and source_game == "th12" and target == "th15":
        source_path = str(context.get("source_path", "") if context else "").replace("\\", "/")
        function = str(event.get("function", ""))
        args = [str(arg) for arg in event.get("args", [])]
        if source_path.endswith("/th12/stage06.decl") and function in {"Girl01", "Girl02"} and args:
            remapped = remap_th12_stage_enemy_main_arg_to_target(args[0], target)
            if remapped is not None:
                args = [remapped, *args[1:]]
                async_suffix = " async" if event.get("kind") == "async_call" else ""
                return f"@{function}({', '.join(args)}){async_suffix};"
    return f"{text}{suffix}"


def is_stage_decl_path(path: str) -> bool:
    name = path.rsplit("/", 1)[-1].lower()
    return name.startswith("stage") or name.startswith("st")


def function_uses_stage_enemy_anm_args(function: str) -> bool:
    return bool(re.fullmatch(r"(?:[BGRY])?(?:Girl|SpCir|Cir)[A-Za-z0-9_]*|Ecl_Girl[A-Za-z0-9_]*", function))


TH10_STAGE_MAIN_ARG_TO_TH13PLUS = {
    "0": "0",
    "5": "5",
    "10": "35",
    "15": "40",
    "20": "20",
    "25": "25",
    "30": "35",
    "35": "40",
    "49": "147",
    "50": "152",
    "51": "157",
    "52": "162",
}

def remap_th10_stage_enemy_call_anm_args(args: list[str], target: str) -> list[str]:
    if generation_for_game(target) != "th13_plus":
        return args
    remapped = list(args)
    first = str(remapped[0]).strip()
    if first in TH10_STAGE_MAIN_ARG_TO_TH13PLUS:
        remapped[0] = TH10_STAGE_MAIN_ARG_TO_TH13PLUS[first]
    if len(remapped) >= 2:
        second = str(remapped[1]).strip()
        parsed = parse_int_literal(second)
        if parsed is not None:
            remapped[1] = str(remap_set_script("th10", target, 1, parsed, "stage", "stage_enemy", "sprite").script)
    return remapped


def remap_th12_stage_enemy_main_arg_to_target(value: str, target: str) -> str | None:
    semantic_by_source = {
        "21": "stage_blue",
        "31": "stage_green",
        "26": "stage_red",
        "36": "stage_yellow",
    }
    purpose = semantic_by_source.get(str(value).strip())
    if purpose is None:
        return None
    chosen = choose_script(target, "stage", purpose, kind="main")
    return str(chosen.script) if chosen is not None else None


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


def cmd_transpile_stage06_th15(args: argparse.Namespace) -> int:
    program, objects = load_objects(args.input)
    if program.game != "th12" or Path(program.source).name != "stage06.decl":
        raise SystemExit("transpile-stage06-th15 expects th12/stage06.decl as input")
    stage, boss = emit_th12_stage06_to_th15_pair(program, objects)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "st06.decl").write_text(stage)
    (out_dir / "st06bs.decl").write_text(boss)
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


def cmd_luastg_lift(args: argparse.Namespace) -> int:
    output = emit_luastg_ir_json(args.input)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
    return 0


def cmd_luastg_normalize(args: argparse.Namespace) -> int:
    output = emit_normalized_json(args.input)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
    return 0


def cmd_luastg_compile(args: argparse.Namespace) -> int:
    objects = normalize_luastg_file(args.input)
    kinds = [item.strip() for item in args.kind.split(",") if item.strip()]
    if "all" in kinds:
        kinds = ["Timeline", "Movement", "BulletEmitter", "LaserEmitter", "BossPattern"]
    selected = [obj for obj in objects if getattr(obj, "kind", None) in kinds]
    if args.limit is not None:
        selected = selected[:args.limit]
    lines = [f"// source LuaSTG: {args.input}", f"// target: {args.target}", f"// selected kinds {','.join(kinds)}: {len(selected)}"]
    for obj in selected:
        lines.append(f"// object {obj.kind} {obj.function}:{obj.source_line} family={obj.family}")
        lines.extend(compile_object(obj, args.target).splitlines())
    output = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
    return 0


DEFAULT_LUASTG_EXPORT_KINDS = ["Timeline", "Movement", "BulletEmitter", "LaserEmitter", "BossPattern"]
LUASTG_EXPORT_HELPER_FUNCTIONS = {
    "ecl_new_bullet", "ecl_shot", "ecl_laser", "ecl_move_rand",
    "ecl_pick_rank", "ecl_rad", "ecl_sync_self",
}


def parse_kind_list(raw: str) -> list[str]:
    kinds = [item.strip() for item in raw.split(",") if item.strip()]
    if "all" in kinds:
        return list(DEFAULT_LUASTG_EXPORT_KINDS)
    return kinds


def safe_ecl_function_name(name: str) -> str:
    cleaned = re.sub(r"\W+", "_", name.strip())
    cleaned = cleaned.strip("_") or "luastg_main"
    if re.match(r"^\d", cleaned):
        cleaned = f"luastg_{cleaned}"
    return cleaned


def lua_param_to_ecl_var(param: str) -> str | None:
    param = param.strip()
    match = re.fullmatch(r"[vi]_([A-Za-z][A-Za-z0-9_]*)", param)
    if match:
        return match.group(1)
    return None


def collect_luastg_function_params(path: str) -> dict[str, list[str]]:
    params: dict[str, list[str]] = {}
    pattern = re.compile(r"^\s*function\s+([A-Za-z_][\w\.]*)\s*\(([^)]*)\)")
    try:
        lines = Path(path).read_text(errors="replace").splitlines()
    except OSError:
        return params
    for raw in lines:
        match = pattern.match(raw)
        if not match:
            continue
        function = match.group(1).replace(".", "_")
        names: list[str] = []
        for raw_param in match.group(2).split(","):
            raw_param = raw_param.strip()
            if raw_param == "self" or not raw_param:
                continue
            ecl_var = lua_param_to_ecl_var(raw_param)
            if ecl_var and ecl_var not in names:
                names.append(ecl_var)
        params[function] = names
    return params


def used_ecl_vars(lines: list[str]) -> list[str]:
    found: list[str] = []
    for line in lines:
        for name in re.findall(r"[%$]([A-Za-z][A-Za-z0-9_]*)", line):
            if name not in found:
                found.append(name)
    return found


def compile_luastg_function_body(objects: list[object], target: str, params: list[str] | None = None) -> list[str]:
    body_lines: list[str] = []
    for obj in sorted(objects, key=lambda item: (getattr(item, "source_line", 0), getattr(item, "kind", ""))):
        body_lines.append(f"    // object {obj.kind} source_line={obj.source_line} family={obj.family}")
        compiled = compile_object(obj, target)
        for line in compiled.splitlines():
            body_lines.append(f"    {line}" if line else "")
    if not body_lines:
        body_lines.append("    // no liftable LuaSTG semantic operations in this function")
        return body_lines
    declared_params = set(params or [])
    locals_needed = [name for name in used_ecl_vars(body_lines) if name not in declared_params]
    if locals_needed and generation_for_game(target) != "th06_th08":
        return [f"    var {', '.join(locals_needed)};"] + body_lines
    return body_lines


def emit_luastg_export(input_path: str, target: str, kinds: list[str], functions: list[str] | None = None, limit: int | None = None) -> str:
    objects = normalize_luastg_file(input_path)
    function_params = collect_luastg_function_params(input_path)
    allowed_functions = set(functions or [])
    by_function: dict[str, list[object]] = {}
    for obj in objects:
        function = str(getattr(obj, "function", "") or "luastg_main")
        if function in LUASTG_EXPORT_HELPER_FUNCTIONS:
            continue
        if allowed_functions and function not in allowed_functions:
            continue
        if getattr(obj, "kind", None) not in kinds:
            continue
        by_function.setdefault(function, []).append(obj)

    function_names = sorted(by_function, key=lambda name: min(getattr(obj, "source_line", 0) for obj in by_function[name]))
    if limit is not None:
        remaining = max(limit, 0)
        limited: dict[str, list[object]] = {}
        for name in function_names:
            if remaining <= 0:
                break
            items = by_function[name][:remaining]
            limited[name] = items
            remaining -= len(items)
        by_function = limited
        function_names = [name for name in function_names if name in by_function]

    lines = [
        f"// source LuaSTG: {input_path}",
        f"// target: {target}",
        "// grouped semantic export: LuaSTG -> shared IR -> ECL draft",
        f"// selected kinds {','.join(kinds)}; functions={len(function_names)}",
    ]
    used_names: dict[str, int] = {}
    for function in function_names:
        safe_name = safe_ecl_function_name(function)
        count = used_names.get(safe_name, 0)
        used_names[safe_name] = count + 1
        if count:
            safe_name = f"{safe_name}_{count + 1}"
        lines.append("")
        params = function_params.get(function, [])
        param_text = ", ".join(f"var {name}" for name in params)
        lines.append(f"// LuaSTG function: {function}")
        lines.append(target_function_header(safe_name, param_text, target))
        lines.append("{")
        lines.extend(compile_luastg_function_body(by_function[function], target, params))
        lines.append("}")
    return "\n".join(lines) + "\n"


def cmd_luastg_export(args: argparse.Namespace) -> int:
    functions = [item.strip() for item in args.functions.split(",") if item.strip()] if args.functions else None
    output = emit_luastg_export(args.input, args.target, parse_kind_list(args.kind), functions, args.limit)
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output, end="")
    return 0


def cmd_luastg(args: argparse.Namespace) -> int:
    names = args.functions.split(",") if args.functions else None
    emit_luastg_file(args.input, args.output, args.module_name, names, args.runtime)
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
    compile_cmd.add_argument("--kind", default="BulletEmitter", choices=["BulletEmitter", "LaserEmitter", "Movement", "Animation", "Enemy", "BossPattern", "Timeline", "EffectEmitter", "FamiliarSpawner", "AutoBulletTimer", "BossTimer", "MotionModifier"])
    compile_cmd.add_argument("--index", type=int, default=0, help="0-based lifted object index within --kind")
    compile_cmd.set_defaults(func=cmd_compile)


    transpile = sub.add_parser("transpile", help="lower a whole .decl file as a structured draft")
    transpile.add_argument("input")
    transpile.add_argument("--target", required=True, choices=["th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    transpile.add_argument("--output", help="write output to file instead of stdout")
    transpile.set_defaults(func=cmd_transpile)

    transpile_stage06 = sub.add_parser("transpile-stage06-th15", help="lower th12 stage06 into th15 st06/st06bs package")
    transpile_stage06.add_argument("input")
    transpile_stage06.add_argument("--output-dir", required=True)
    transpile_stage06.set_defaults(func=cmd_transpile_stage06_th15)

    scan = sub.add_parser("scan", help="scan a directory for liftable objects")
    scan.add_argument("root")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=cmd_scan)

    luastg = sub.add_parser("luastg", help="lower ECL boss IR to an approximate LuaSTG module")
    luastg.add_argument("input")
    luastg.add_argument("--output", required=True)
    luastg.add_argument("--module-name", default="ecl_stage06_boss")
    luastg.add_argument("--functions", help="comma-separated ECL function names to emit; default emits Boss* functions")
    luastg.add_argument("--runtime", choices=["thlib", "liu_10_mc"], default="liu_10_mc", help="LuaSTG runtime helper backend")
    luastg.set_defaults(func=cmd_luastg)

    luastg_lift = sub.add_parser("luastg-lift", help="lift LuaSTG/THlib script patterns to semantic JSON IR")
    luastg_lift.add_argument("input")
    luastg_lift.add_argument("--output", help="write JSON output to file instead of stdout")
    luastg_lift.set_defaults(func=cmd_luastg_lift)

    luastg_norm = sub.add_parser("luastg-normalize", help="lift LuaSTG/THlib script and normalize to shared semantic IR JSON")
    luastg_norm.add_argument("input")
    luastg_norm.add_argument("--output", help="write JSON output to file instead of stdout")
    luastg_norm.set_defaults(func=cmd_luastg_normalize)

    luastg_compile = sub.add_parser("luastg-compile", help="compile normalized LuaSTG semantic objects to an ECL target draft")
    luastg_compile.add_argument("input")
    luastg_compile.add_argument("--target", required=True, choices=["th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    luastg_compile.add_argument("--kind", default="BulletEmitter", help="object kind, comma-separated kinds, or all")
    luastg_compile.add_argument("--limit", type=int, help="compile only first N objects of the selected kind")
    luastg_compile.add_argument("--output", help="write output to file instead of stdout")
    luastg_compile.set_defaults(func=cmd_luastg_compile)

    luastg_export = sub.add_parser("luastg-export", help="compile LuaSTG semantic IR to function-grouped ECL target draft")
    luastg_export.add_argument("input")
    luastg_export.add_argument("--target", required=True, choices=["th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"])
    luastg_export.add_argument("--kind", default="all", help="object kind, comma-separated kinds, or all")
    luastg_export.add_argument("--functions", help="comma-separated LuaSTG function names to export")
    luastg_export.add_argument("--limit", type=int, help="compile only first N selected objects across exported functions")
    luastg_export.add_argument("--output", help="write grouped ECL draft to file instead of stdout")
    luastg_export.set_defaults(func=cmd_luastg_export)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
