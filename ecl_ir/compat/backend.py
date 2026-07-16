from __future__ import annotations

import re
from ..target.arg_adapter import adapt_args_for_op_key
from copy import deepcopy

from ..analysis.spread_ir import th12_aux_emitter_id
from ..analysis.transform_ir import bullet_transform_instructions, lower_transform_opcode_to_instruction, target_transform_args
from ..canonical.op_ir import op_key_for_opcode, op_lowering_policy, target_opcode_for_op_key
from ..canonical.semantic_ir import SemanticOperation, VariableUseKind, semantic_operation_to_backend_event
from ..canonical.variable_ir import rewrite_argument_variables
from ..dialects.anm_catalog import choose_script, remap_anm_bank, remap_play_script, remap_set_script, target_bank_for_role
from ..dialects.game_ids import normalize_game_id
from ..dialects.game_profile import profile_for_game
from ..dialects.reference import is_opcode_supported, opcode_signature, validate_opcode_args
from ..dialects.semantics import boss_phase_prefix_ops, bullet_shape_semantic, encode_bullet_shape, encode_spread_style, generation_for_game, opcode_map_for, remap_create_item_policy, remap_raw_arg_by_semantic, remap_unit_flag_mask, unsupported_bullet_transform_mode_reason
from ..legacy.model import BulletEmitter, BulletTransform
from ..target.lowering import BackendEmission, LoweringStrategy
from ..target.origin_ir import bullet_origin_instructions

INT_SENTINEL = "-999999"
FLOAT_SENTINEL = "-999999.0f"


TARGET_DIFFICULTY = "N"
DIFFICULTY_FALLBACK_ORDER = ("N", "H", "E", "LO", "L")


def project_backend_args(
    event: dict[str, object],
    target: str,
) -> list[str] | None:
    if event_variables_projected_for_target(event, target):
        return [str(arg) for arg in event.get("args", [])]
    values, _issues = rewrite_argument_variables(
        str(event.get("source_game") or ""),
        target,
        [str(arg) for arg in event.get("args", [])],
        use_kind=VariableUseKind.UNKNOWN,
    )
    return values


def event_variables_projected_for_target(
    event: dict[str, object],
    target: str,
) -> bool:
    annotations = event.get("annotations")
    projected_target = (
        str(annotations.get("variable_projection_target") or "")
        if isinstance(annotations, dict)
        else ""
    )
    return bool(projected_target) and normalize_game_id(projected_target) == normalize_game_id(target)


def choose_difficulty(difficulty: dict[str, str], default: str = "") -> tuple[str, str]:
    normalized = normalize_difficulty(difficulty)
    for key in DIFFICULTY_FALLBACK_ORDER:
        if key in normalized:
            return normalized[key], key
    return default, "placeholder"


def v(value, default):
    if isinstance(value, dict):
        difficulty = value.get("difficulty", {})
        chosen, _ = choose_difficulty(difficulty, value.get("placeholder", default))
        return chosen
    return value if value not in (None, "") else default


def aim_mode_name(raw: str) -> str:
    return {
        "0": "aimed_fan",
        "1": "fan",
        "2": "aimed_ring",
        "3": "ring",
        "4": "offset_aimed_ring",
        "5": "offset_ring",
        "6": "random_angle",
        "7": "random_speed",
        "8": "random_angle_speed",
    }.get(str(raw), "custom")


def difficulty_comment(field: str, value) -> str | None:
    if not isinstance(value, dict) or "difficulty" not in value:
        return None
    parts = ", ".join(f"{key}={val}" for key, val in value["difficulty"].items())
    _, rank = choose_difficulty(value["difficulty"], value.get("placeholder", ""))
    return f"// difficulty {field}: {parts}; lowered using {rank}={v(value, '')}"




def normalize_difficulty(difficulty: object) -> dict[str, str]:
    if not isinstance(difficulty, dict):
        return {}
    normalized: dict[str, str] = {}
    for key, value in difficulty.items():
        if key == "*":
            continue
        for rank in key:
            if rank in {"E", "N", "H", "L"}:
                normalized[rank] = value
            elif rank == "O":
                normalized.setdefault("L", value)
    return normalized


def first_difficulty_group(literals: object) -> dict[str, str]:
    if isinstance(literals, dict):
        return literals
    if isinstance(literals, list):
        for item in literals:
            if isinstance(item, dict) and item:
                return item
    return {}


def difficulty_rank_order(difficulty: dict[str, str]) -> list[str]:
    normalized = normalize_difficulty(difficulty)
    return [rank for rank in ("E", "N", "H", "L") if rank in normalized]


def normalized_rank_marker(marker: str | None, target: str = "") -> str | None:
    if not marker:
        return None
    marker = str(marker).strip()
    if not marker:
        return None
    if marker == "*":
        return "*"
    out: list[str] = []
    for ch in marker:
        mapped = "L" if ch == "O" else ch
        if mapped in "ENHL":
            if mapped not in out:
                out.append(mapped)
        elif mapped in "01234567X":
            if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
                continue
            out.append(mapped)
    return "".join(out) or None


def wrap_ranked_lines(lines: list[str], difficulty: str | None, target: str = "") -> list[str]:
    marker = normalized_rank_marker(difficulty, target)
    if not marker:
        return lines
    if marker == "*":
        return lines if lines and lines[0] == "!*" else ["!*", *lines]
    return [f"!{marker}", *lines, "!*"]



def emit_checked_instruction(target: str, opcode: int, args: list[object]) -> str:
    rendered = [str(arg) for arg in args]
    error = validate_opcode_args(target, opcode, rendered)
    if error:
        return f"// skipped invalid instruction from reference table: {error}; ins_{opcode}({', '.join(rendered)})"
    return f"ins_{opcode}({', '.join(rendered)});"


def as_float_expr(value: object) -> object:
    if isinstance(value, dict):
        result = dict(value)
        if "placeholder" in result:
            result["placeholder"] = as_float_expr(result["placeholder"])
        if isinstance(result.get("difficulty"), dict):
            result["difficulty"] = {rank: as_float_expr(val) for rank, val in result["difficulty"].items()}
        return result
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return f"{text}.0f"
    text = re.sub(r"(?<![\w.])([-+]?\d+)(?![\w.])\s*/", lambda m: f"{m.group(1)}.0f /", text)
    text = re.sub(r"/\s*([-+]?\d+)(?![\w.])", lambda m: f"/ _f({m.group(1)})", text)
    text = re.sub(r"(?<![\w.])([-+]?\d+\.\d+)(?![\w.])", lambda m: m.group(1) + ("" if m.group(1).endswith("f") else "f"), text)
    text = re.sub(r"_f\(_S\(([^()]*)\)\s*/\s*_f\(([-+]?\d+)\)\)", r"_f(_S(\1)) / _f(\2)", text)
    return text


def as_int_expr(value: object):
    if isinstance(value, dict):
        result = dict(value)
        difficulty = result.get("difficulty")
        if isinstance(difficulty, dict):
            result["difficulty"] = {rank: as_int_expr(item) for rank, item in difficulty.items()}
        if "placeholder" in result:
            result["placeholder"] = as_int_expr(result["placeholder"])
        return result
    text = str(value).strip()
    text = re.sub(r"\[(-?\d+)\.0f\]", r"[\1]", text)
    text = re.sub(r"%([A-Za-z][A-Za-z0-9_]*)", r"$\1", text)
    if re.fullmatch(r"[-+]?\d+\.0f?", text):
        return text.split(".")[0]
    return text


def normalize_target_args_for_op_key(op_key: str, target: str, args: list[str]) -> list[str]:
    normalized = [str(arg) for arg in args]
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        float_indices_by_op = {
            "movement.position.set": {0, 1},
            "movement.position.tween": {2, 3},
            "movement.position_rel.set": {0, 1},
            "movement.position_rel.tween": {2, 3},
            "movement.velocity.set": {0, 1},
            "movement.velocity.tween": {2, 3},
            "movement.velocity_rel.set": {0, 1},
            "movement.velocity_rel.tween": {2, 3},
            "movement.circle.set": {0, 1, 2, 3},
            "movement.circle.tween": {2, 3, 4},
            "movement.circle_rel.set": {0, 1, 2, 3},
            "movement.circle_rel.tween": {2, 3, 4},
            "movement.move_rand": {2},
            "movement.move_rand_rel": {2},
            "movement.ellipse.set": {0, 1, 2, 3, 4, 5},
            "movement.ellipse.tween": {2, 3, 4, 5, 6},
            "movement.ellipse_rel.set": {0, 1, 2, 3, 4, 5},
            "movement.ellipse_rel.tween": {2, 3, 4, 5, 6},
            "movement.bezier": {1, 2, 3, 4, 5, 6},
            "movement.bezier_rel": {1, 2, 3, 4, 5, 6},
        }
        for index in float_indices_by_op.get(op_key, set()):
            if index < len(normalized):
                normalized[index] = str(as_float_expr(normalized[index]))
    if target == "th12" and op_key in {
        "movement.position.tween", "movement.position_rel.tween",
        "movement.velocity.tween", "movement.velocity_rel.tween",
        "movement.ellipse.tween", "movement.ellipse_rel.tween",
    }:
        if len(normalized) > 1 and normalized[1] not in {"0", "1", "4", "9"}:
            normalized[1] = "0"
    return normalized



UNSAFE_TARGET_OPCODES: dict[str, set[int]] = {
    # thtk12/thecl.exe -c 8 has no usable format entry for these despite names in th08.eclm.
    "th08": {143, 162},
    # Listed in eclmap, but thtk12's version-12 format table cannot serialize it.
    "th12": {22},
}


def target_opcode_is_safe(target: str, opcode: int) -> bool:
    return int(opcode) not in UNSAFE_TARGET_OPCODES.get(target, set())


def op_lowering_policy_applies(policy: dict[str, object], target: str, source_game: str = "") -> bool:
    target_generations = policy.get("target_generations")
    if isinstance(target_generations, list) and generation_for_game(target) not in {str(item) for item in target_generations}:
        return False
    source_generations = policy.get("source_generations")
    if source_game and isinstance(source_generations, list) and generation_for_game(source_game) not in {str(item) for item in source_generations}:
        return False
    return True


def negated_expr(value: object) -> str:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", text):
        if text.startswith("-"):
            return text[1:]
        if text.startswith("+"):
            return f"-{text[1:]}"
        return f"-{text}"
    if text.startswith("(") and text.endswith(")"):
        return f"-{text}"
    return f"-({text})"


def policy_args(args: list[str], policy: dict[str, object]) -> list[str]:
    arg_policy = policy.get("arg_policy") if isinstance(policy.get("arg_policy"), dict) else {}
    out = list(args)
    take_first = arg_policy.get("take_first")
    if isinstance(take_first, int):
        out = out[:take_first]
    defaults = arg_policy.get("defaults")
    if isinstance(defaults, list):
        while len(out) < len(defaults):
            out.append(str(defaults[len(out)]))
    indices = arg_policy.get("indices")
    if isinstance(indices, list):
        selected: list[str] = []
        for raw_index in indices:
            try:
                index = int(raw_index)
            except (TypeError, ValueError):
                continue
            if 0 <= index < len(out):
                selected.append(out[index])
        out = selected
    negate_indices = arg_policy.get("negate_indices")
    if isinstance(negate_indices, list):
        for raw_index in negate_indices:
            try:
                index = int(raw_index)
            except (TypeError, ValueError):
                continue
            if 0 <= index < len(out):
                out[index] = negated_expr(out[index])
    int_indices = arg_policy.get("int_indices")
    if isinstance(int_indices, list):
        for raw_index in int_indices:
            try:
                index = int(raw_index)
            except (TypeError, ValueError):
                continue
            if 0 <= index < len(out):
                out[index] = as_int_expr(out[index])
    return out


def compile_legacy_laser_on_aimed_policy(event: dict[str, object], target: str, policy: dict[str, object]) -> str | None:
    args = [str(arg) for arg in event.get("args", [])]
    if len(args) < 8:
        return None
    et_id, style, angle, _speed, length, active_time, _flags, width = args[:8]
    active_time_i = as_int_expr(active_time)
    if generation_for_game(target) == "th13_plus":
        lines = [
            f"// legacy laserOnA lowering {event.get('source_game')}->{target}: approximated as target straight laser; reason={policy.get('reason', '')}",
            f"ins_700({et_id}, 0.0f, {length}, 0.0f, {width});",
            f"ins_701({et_id}, 0, 0, {active_time_i}, 0, 0);",
            f"ins_708({et_id}, {angle});",
            f"ins_702({et_id});",
            f"// original laser style={style}; source args: {', '.join(args)}",
        ]
        return "\n".join(lines)
    if target == "th12":
        lines = [
            f"// legacy laserOnA lowering {event.get('source_game')}->{target}: approximated as target straight laser; reason={policy.get('reason', '')}",
            f"ins_600({et_id}, 0.0f, {length}, 0.0f, {width});",
            f"ins_601({et_id}, 0, 0, {active_time_i}, 0, 0);",
            f"ins_608({et_id}, {angle});",
            f"ins_602({et_id});",
            f"// original laser style={style}; source args: {', '.join(args)}",
        ]
        return "\n".join(lines)
    return None


def compile_op_lowering_policy(event: dict[str, object], target: str) -> str | None:
    policy = event.get("lowering_policy") if isinstance(event.get("lowering_policy"), dict) else None
    if not policy or not op_lowering_policy_applies(policy, target, str(event.get("source_game") or "")):
        return None
    op_key = str(event.get("op_key") or "")
    args_list = [str(arg) for arg in event.get("args", [])]
    args = ", ".join(args_list)
    strategy = str(policy.get("strategy", ""))
    reason = str(policy.get("reason", ""))
    if strategy == "drop":
        return f"// dropped by IR op lowering policy for {target}: {op_key}({args}); reason={reason}"
    if strategy == "approximate":
        approximation = str(policy.get("approximation", ""))
        return f"// approximated by IR op lowering policy for {target}: {op_key}({args}); reason={reason}; approximation={approximation}"
    if strategy == "stack_vm_sequence":
        return compile_stack_vm_sequence_policy(event, target, policy)
    if strategy == "emit_raw_ins":
        rendered_args = [policy_template_arg(arg, args_list) for arg in policy.get("args", [])]
        opcode = int(policy.get("opcode", 0))
        line = f"ins_{opcode}({', '.join(rendered_args)});" if rendered_args else f"ins_{opcode}();"
        return f"// emitted raw instruction by IR op lowering policy for {target}: {op_key}; reason={reason}\n{line}"
    if strategy == "legacy_laser_on_aimed":
        return compile_legacy_laser_on_aimed_policy(event, target, policy)
    if strategy == "legacy_conditional_jump":
        legacy_args = project_backend_args(event, target)
        if legacy_args is None:
            return None
        if len(legacy_args) != 4:
            return None
        jump_opcode = target_opcode_for_op_key(str(policy.get("target_op_key", "flow.jmp_neq")), target)
        if jump_opcode is None or not is_opcode_supported(target, jump_opcode):
            return None
        compare_opcode = int(policy.get("compare_opcode", 0))
        return "\n".join([
            f"// legacy conditional jump by IR op lowering policy for {target}: {op_key}; reason={reason}",
            stack_push(legacy_args[0]),
            stack_push(legacy_args[1]),
            f"ins_{compare_opcode}();",
            f"ins_{jump_opcode}({legacy_args[3]}, {legacy_args[2]});",
        ])
    if strategy == "legacy_loop_jump":
        legacy_args = project_backend_args(event, target)
        if legacy_args is None:
            return None
        if len(legacy_args) != 3:
            return None
        jump_opcode = target_opcode_for_op_key(str(policy.get("target_op_key", "flow.jmp_neq")), target)
        if jump_opcode is None or not is_opcode_supported(target, jump_opcode):
            return None
        decrement_opcode = int(policy.get("decrement_opcode", 78))
        return "\n".join([
            f"// legacy loop jump by IR op lowering policy for {target}: {op_key}; reason={reason}",
            f"ins_{decrement_opcode}({legacy_args[2]});",
            f"ins_{jump_opcode}({legacy_args[1]}, {legacy_args[0]});",
        ])
    if strategy == "emit_target_op":
        target_op_key = str(policy.get("target_op_key") or op_key)
        lowered_args = policy_args(args_list, policy)
        lowered = emit_target_op(target, target_op_key, lowered_args)
        if lowered:
            return f"// emitted by IR op lowering policy for {target}: {op_key} -> {target_op_key}; reason={reason}\n{lowered}"
        return None
    if strategy == "emit_target_op_sequence":
        lines = []
        for item in policy.get("sequence", []) if isinstance(policy.get("sequence"), list) else []:
            if not isinstance(item, dict):
                continue
            item_args = [str(arg).replace("$0", args_list[0] if args_list else "0").replace("$1", args_list[1] if len(args_list) > 1 else "0") for arg in item.get("args", [])]
            lowered = emit_target_op(target, str(item.get("target_op_key", "")), item_args)
            if lowered:
                lines.append(lowered)
        if lines:
            return f"// emitted sequence by IR op lowering policy for {target}: {op_key}; reason={reason}\n" + "\n".join(lines)
        return None
    if strategy == "catalog_sprite":
        if not args_list:
            return f"// unsupported catalog_sprite IR lowering for {target}: {op_key}({args}); reason=missing_slot_arg"
        slot_index = int(policy.get("slot_arg_index", 0) or 0)
        slot = args_list[slot_index] if slot_index < len(args_list) else "0"
        chosen = choose_script(target, str(policy.get("catalog_role", "boss")), str(policy.get("catalog_purpose", "familiar")), kind=str(policy.get("catalog_kind", "sprite")))
        if chosen is None:
            return f"// unsupported catalog_sprite IR lowering for {target}: {op_key}({args}); reason=no_target_catalog_sprite"
        metadata = []
        metadata_names = policy.get("metadata_arg_names") if isinstance(policy.get("metadata_arg_names"), dict) else {}
        for index_text, name in metadata_names.items():
            try:
                index = int(index_text)
            except ValueError:
                continue
            if index < len(args_list):
                metadata.append(f"{name}={args_list[index]}")
        lines = [
            f"// catalog_sprite IR lowering for {target}: {op_key}; bank {chosen.bank}, script {chosen.script}; reason={reason}",
            f"ins_{target_opcode_for_op_key('anm.select', target)}({chosen.bank});",
            f"ins_{target_opcode_for_op_key('anm.set_sprite', target)}({slot}, {chosen.script});",
        ]
        if metadata:
            lines.append(f"// IR metadata preserved: {', '.join(metadata)}")
        return "\n".join(lines)
    return None



def compile_preemptive_op_lowering_policy(event: dict[str, object], target: str) -> str | None:
    policy = event.get("lowering_policy") if isinstance(event.get("lowering_policy"), dict) else None
    if not policy or not op_lowering_policy_applies(policy, target, str(event.get("source_game") or "")):
        return None
    strategy = str(policy.get("strategy", ""))
    reason = str(policy.get("reason", ""))
    if strategy in {"emit_target_op", "emit_target_op_sequence", "stack_vm_sequence", "emit_raw_ins", "legacy_laser_on_aimed", "legacy_conditional_jump", "legacy_loop_jump", "catalog_sprite"}:
        return compile_op_lowering_policy(event, target)
    if strategy == "drop":
        return compile_op_lowering_policy(event, target)
    return None

def compile_lossy_semantic_fallback(event: dict[str, object], target: str) -> str | None:
    op_key = str(event.get("op_key") or "")
    args = ", ".join(str(arg) for arg in event.get("args", []))
    if lowered := compile_op_lowering_policy(event, target):
        return lowered
    return f"// unsupported semantic op without IR lowering policy for {target}: {op_key}({args})"


def stack_push(value: str) -> str:
    return f"{value};"


def policy_template_arg(value: object, args_list: list[str]) -> str:
    text = str(value)
    for index, arg in enumerate(args_list):
        text = text.replace(f"${index}", arg)
    return text


def compile_stack_vm_sequence_policy(event: dict[str, object], target: str, policy: dict[str, object]) -> str | None:
    args_list = project_backend_args(event, target)
    if args_list is None:
        return None
    lines: list[str] = []
    for item in policy.get("sequence", []) if isinstance(policy.get("sequence"), list) else []:
        if not isinstance(item, dict):
            continue
        if "push_arg" in item:
            index = int(item.get("push_arg", 0))
            if index < len(args_list):
                lines.append(stack_push(args_list[index]))
            continue
        if "push" in item:
            lines.append(stack_push(policy_template_arg(item.get("push", "0"), args_list)))
            continue
        if "ins" in item:
            opcode = int(item.get("ins", 0))
            item_args = [policy_template_arg(arg, args_list) for arg in item.get("args", [])]
            lines.append(f"ins_{opcode}({', '.join(item_args)});" if item_args else f"ins_{opcode}();")
    if not lines:
        return None
    return f"// stack VM sequence by IR op lowering policy for {target}: {event.get('op_key')}; reason={policy.get('reason', '')}\n" + "\n".join(lines)


def parse_int_literal(value: str) -> int | None:
    if re.fullmatch(r"-?\d+", str(value).strip()):
        return int(str(value).strip())
    return None


def anm_role_hint(event: dict[str, object], context: dict[str, object] | None = None) -> str | None:
    source_game = str(event.get("source_game") or "")
    path = str(context.get("source_path", "") if context else "").replace("\\", "/").lower()
    name = path.rsplit("/", 1)[-1]
    function = str(context.get("function", "") if context else "")
    if any(token in name for token in ("boss", "mbs", "bs")):
        return "boss"
    if source_game and name.startswith(("stage", "st")):
        return "stage"
    if function.startswith(("Boss", "MBoss", "MainBoss", "MainMBoss")) or function in {"HPWait", "MBossCard1LaserHit"}:
        return "boss"
    return None


def remap_anm_args(event: dict[str, object], target: str, args: list[str], context: dict[str, object] | None = None) -> list[str]:
    source_game = str(event.get("source_game") or "")
    if not source_game or source_game == target:
        return args
    op_key = canonical_anm_op_key(str(event.get("op_key") or ""))
    role_hint = anm_role_hint(event, context)
    if op_key == "anm.select" and len(args) == 1:
        source_bank = parse_int_literal(args[0])
        if source_bank is None:
            return args
        return [str(remap_anm_bank(source_game, target, source_bank, role_hint))]
    if op_key in {"anm.play", "anm.play_abs"} and len(args) >= 2:
        source_bank = parse_int_literal(args[0])
        source_script = parse_int_literal(args[1])
        if source_bank is None or source_script is None:
            return args
        purpose = "boss_spawn" if role_hint == "boss" else "stage_spawn" if role_hint == "stage" else "spawn"
        chosen = remap_play_script(source_game, target, source_bank, source_script, role_hint, purpose)
        return [str(chosen.bank), str(chosen.script), *args[2:]]
    if op_key in {"anm.set_sprite", "anm.set_main"} and len(args) == 2:
        if role_hint == "boss" and op_key == "anm.set_sprite" and args[0].strip() == "4" and generation_for_game(target) == "th13_plus":
            return ["3", "-1"]
        script = parse_int_literal(args[1])
        if script is None:
            if role_hint == "boss":
                chosen = choose_script(target, "boss", "familiar")
                if chosen is not None:
                    return [args[0], str(chosen.script)]
            return args
        source_bank = target_bank_for_role(source_game, role_hint) if role_hint else None
        if source_bank is None and role_hint:
            source_bank = target_bank_for_role(source_game, role_hint)
        if source_bank is None:
            return args
        set_kind = "main" if op_key == "anm.set_main" else "sprite"
        purpose = anm_set_purpose(event, role_hint, set_kind, args)
        return [args[0], str(remap_set_script(source_game, target, source_bank, script, role_hint, purpose, set_kind).script)]
    return args


def canonical_anm_op_key(op_key: str) -> str:
    if op_key.startswith("animation."):
        return "anm." + op_key.removeprefix("animation.")
    return op_key


def anm_select_prefix_for_event(event: dict[str, object], target: str, context: dict[str, object] | None = None) -> list[str]:
    source_game = str(event.get("source_game") or "")
    if not source_game or source_game == target:
        return []
    op_key = canonical_anm_op_key(str(event.get("op_key") or ""))
    if op_key not in {"anm.set_main", "anm.set_sprite"}:
        return []
    role_hint = anm_role_hint(event, context)
    if not role_hint:
        return []
    bank = None
    args = [str(arg) for arg in event.get("args", [])]
    if len(args) == 2:
        script = parse_int_literal(args[1])
        source_bank = target_bank_for_role(source_game, role_hint)
        if script is not None and source_bank is not None:
            set_kind = "main" if op_key == "anm.set_main" else "sprite"
            purpose = anm_set_purpose(event, role_hint, set_kind, args)
            bank = remap_set_script(source_game, target, source_bank, script, role_hint, purpose, set_kind).bank
    if bank is None:
        bank = target_bank_for_role(target, role_hint)
    select_opcode = target_opcode_for_op_key("anm.select", target)
    if bank is None or select_opcode is None or not is_opcode_supported(target, select_opcode):
        return []
    return [f"ins_{select_opcode}({bank});"]


def anm_set_purpose(event: dict[str, object], role_hint: str | None, set_kind: str, args: list[str]) -> str:
    if role_hint == "stage":
        return "stage_enemy"
    if role_hint == "boss" and set_kind == "sprite":
        if args:
            slot = str(args[0]).strip()
            if slot == "1":
                return "boss_sprite"
            if slot == "2":
                return "boss_sprite_secondary"
        return "boss_aux"
    return "main"


def normalize_backend_event(event: SemanticOperation | dict[str, object]) -> dict[str, object]:
    """Convert a typed semantic node or schema-v1 event at the backend boundary."""

    if isinstance(event, SemanticOperation):
        source: dict[str, object] = event.to_dict()
        normalized = semantic_operation_to_backend_event(event)
    elif isinstance(event, dict):
        source = event
        if str(event.get("node") or "") in {"semantic_op", "semantic_operation"}:
            normalized = semantic_operation_to_backend_event(event)
        else:
            normalized = dict(event)
    else:
        raise TypeError(f"unsupported backend event: {type(event).__name__}")

    # Keep identity and ownership available to diagnostics without making the
    # compatibility event the canonical representation.
    for key in ("node_id", "ownership", "provenance", "guard", "annotations"):
        if key in source:
            normalized[key] = source[key]

    args = [str(arg) for arg in normalized.get("args", [])]
    normalized["args"] = args
    op_key = str(normalized.get("op_key") or "")
    normalized.pop("lowering_policy", None)
    if op_key:
        canonical = str(normalized.get("canonical_operation") or "")
        policy_key = canonical if canonical.startswith("bullet.transform.") else op_key
        policy = op_lowering_policy(policy_key, args)
        if policy:
            normalized["lowering_policy"] = policy
    return normalized


def target_bullet_encoding(event: dict[str, object], target: str) -> tuple[str, int] | None:
    canonical = str(event.get("canonical_operation") or "")
    if not canonical.startswith("bullet."):
        return None
    profile = profile_for_game(target)
    candidates = profile.bullet_dialect.opcodes_for_operation(canonical)
    if not candidates:
        return None
    if canonical == "bullet.macro.configure":
        annotations = event.get("annotations")
        macro_mode = str(annotations.get("macro_mode") or "") if isinstance(annotations, dict) else ""
        opcode = next(
            (
                candidate
                for candidate, candidate_mode in profile.bullet_dialect.macro_modes
                if candidate in candidates and candidate_mode == macro_mode
            ),
            None,
        )
        if opcode is None:
            return None
    else:
        args = [str(arg) for arg in event.get("args", [])]
        matching = [
            opcode
            for opcode in candidates
            if not (signature := opcode_signature(target, opcode)) or len(signature.replace("*", "")) == len(args)
        ]
        opcode = (matching or list(candidates))[0]
    dialect_operation = op_key_for_opcode(target, opcode)
    if profile.bullet_dialect.implicit_manager:
        dialect_operation = canonical
    return dialect_operation, opcode


def encode_canonical_operand_states(
    event: dict[str, object],
    target: str,
    args: list[str],
) -> list[str]:
    operand_values = event.get("operand_values")
    if not isinstance(operand_values, list) or len(operand_values) != len(args):
        return args
    sentinels = profile_for_game(target).sentinels
    encoded = list(args)
    for index, raw_value in enumerate(operand_values):
        if not isinstance(raw_value, dict):
            continue
        state = str(raw_value.get("state") or "value")
        expression = raw_value.get("expression")
        value_type = str(expression.get("type") or "") if isinstance(expression, dict) else ""
        if state == "unused":
            token = sentinels.unused_float if value_type == "float32" else sentinels.unused_int
            if token is not None:
                encoded[index] = token
        elif state == "keep_current" and value_type == "float32":
            token = sentinels.keep_current_float or sentinels.unused_float
            if token is not None:
                encoded[index] = token
    return encoded


def compile_ir_op_event(event: SemanticOperation | dict[str, object], target: str, comment: str | None = None, context: dict[str, object] | None = None) -> str | None:
    event = normalize_backend_event(event)
    op_key = str(event.get("op_key") or "")
    if not op_key:
        return None
    args = encode_canonical_operand_states(
        event,
        target,
        [str(arg) for arg in event.get("args", [])],
    )
    event = {**event, "args": args}
    raw_source_opcode = event.get("source_opcode")
    source_opcode = int(raw_source_opcode) if raw_source_opcode is not None else -1
    if op_key.startswith("raw.") and source_opcode == 1 and is_opcode_supported(target, 1):
        return "ins_1();"
    source_game = str(event.get("source_game") or "")
    projected_args = project_backend_args(event, target)
    if projected_args is None:
        return None
    args = projected_args
    annotations = dict(event.get("annotations", {}) or {})
    annotations["variable_projection_target"] = normalize_game_id(target)
    event = {**event, "args": args, "annotations": annotations}
    if lowered := compile_preemptive_op_lowering_policy(event, target):
        return lowered
    if target == "th12" and source_game in {"th13", "th14", "th15", "th16", "th17", "th18"} and source_opcode in {611, 612}:
        return compile_lossy_semantic_fallback(event, target)
    if op_key == "flow.call_async" and str(event.get("args", ["", ""])[-1]) == "-1":
        return compile_lossy_semantic_fallback(event, target)
    if op_key == "flow.float_time" and generation_for_game(target) != "th13_plus":
        return compile_lossy_semantic_fallback(event, target)
    if op_key == "flow.nop" and source_game in {"th10", "th11", "th12"} and generation_for_game(target) == "th13_plus":
        return "ins_0();"
    target_bullet = target_bullet_encoding(event, target)
    semantic_op_key = target_bullet[0] if target_bullet else canonical_anm_op_key(op_key)
    semantic_map = opcode_map_for(source_game, target, source_opcode) if source_game and source_opcode >= 0 else None
    semantic_op_key = (
        target_bullet[0]
        if target_bullet
        else (semantic_map.semantic if semantic_map is not None and semantic_map.semantic else op_key)
        if op_key.startswith("raw.")
        else canonical_anm_op_key(op_key)
    )
    if (
        target_bullet
        and str(event.get("canonical_operation") or "") in {"bullet.transform.replace", "bullet.transform.append"}
        and len(args) <= 8
    ):
        semantic_op_key = "bullet.transform"
    opcode = (
        target_bullet[1]
        if target_bullet
        else target_opcode_for_op_key(
            semantic_op_key,
            target,
            operand_count=len(args),
        )
    )
    if opcode is None and op_key.startswith("raw.") and semantic_map is not None:
        opcode = semantic_map.target_opcode
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return compile_lossy_semantic_fallback(event, target)
    if semantic_map is not None and semantic_map.arg_order is not None:
        args = [args[index] for index in semantic_map.arg_order if index < len(args)]
    if source_game and source_opcode >= 0:
        args = remap_raw_arg_by_semantic(source_game, target, source_opcode, opcode, args)
    args = remap_anm_args({**event, "op_key": semantic_op_key}, target, args, context)
    adapted_args = adapt_args_for_op_key(
        semantic_op_key,
        source_game,
        source_opcode,
        target,
        opcode,
        args,
        project_variables=not event_variables_projected_for_target(event, target),
    )
    if adapted_args is None:
        return None
    if semantic_op_key in {
        "enemy.create",
        "enemy.create_abs",
        "enemy.create_mirror",
        "enemy.create_abs_mirror",
        "enemy.create_func",
        "enemy.create_abs_func",
        "enemy.create_mirror_func",
        "enemy.create_abs_mirror_func",
    } and adapted_args:
        adapted_args[-1] = remap_create_item_policy(
            source_game,
            target,
            adapted_args[-1],
        )
    args = normalize_target_args_for_op_key(semantic_op_key, target, adapted_args)
    error = validate_opcode_args(target, opcode, args)
    if error:
        return compile_lossy_semantic_fallback(event, target)
    line = emit_checked_instruction(target, opcode, args)
    prefix = [
        *anm_select_prefix_for_event({**event, "op_key": semantic_op_key}, target, context),
        *boss_phase_prefix_ops(semantic_op_key, target),
    ]
    if prefix:
        line = "\n".join(prefix + [line])
    if comment:
        return f"// {comment}: {semantic_op_key} -> ins_{opcode}\n{line}"
    return line


def compile_ir_op_emission(
    event: SemanticOperation | dict[str, object],
    target: str,
    comment: str | None = None,
    context: dict[str, object] | None = None,
) -> BackendEmission | None:
    """Expose legacy text lowering through a typed planner result."""

    normalized = normalize_backend_event(event)
    text = compile_ir_op_event(normalized, target, comment, context)
    if not text:
        return None
    stripped = text.lstrip()
    if stripped.startswith(("// unsupported ", "// skipped invalid instruction")):
        return BackendEmission(
            text=text,
            strategy=LoweringStrategy.UNSUPPORTED,
            code="backend.unsupported",
            reason="target backend reported that no lowering is implemented",
        )

    policy = normalized.get("lowering_policy")
    policy_strategy = str(policy.get("strategy") or "") if isinstance(policy, dict) else ""
    used_lossy_policy = (
        policy_strategy in {"drop", "approximate", "legacy_laser_on_aimed", "catalog_sprite"}
        and (
            "by IR op lowering policy" in text
            or "legacy laserOnA lowering" in text
            or "catalog_sprite IR lowering" in text
        )
    )
    visibly_lossy = stripped.startswith(("// dropped ", "// approximated ")) or " approximated as " in text
    if used_lossy_policy or visibly_lossy:
        reason = str(policy.get("reason") or "") if isinstance(policy, dict) else ""
        return BackendEmission(
            text=text,
            strategy=LoweringStrategy.LOSSY,
            code="backend.lossy_policy",
            reason=reason or "legacy backend selected an explicit approximation or drop policy",
            details={"backend_policy_strategy": policy_strategy} if policy_strategy else {},
        )
    return BackendEmission(text=text)


def compile_unsupported_ir_op(event: dict[str, object], target: str) -> str:
    op_key = event.get("op_key") or "unknown"
    opcode = event.get("source_opcode")
    args = ", ".join(str(arg) for arg in event.get("args", []))
    return f"// unsupported semantic op for {target}: {op_key}; source ins_{opcode}({args})"



def sound_args(e: BulletEmitter, emitter_id: str, default_mode: str = "-1") -> list[str] | None:
    sound = e.sound.get("id")
    if sound in (None, ""):
        return None
    mode = e.sound.get("mode", default_mode)
    if mode in (None, ""):
        mode = default_mode
    return [emitter_id, str(sound), str(mode)]

def emit_ranked_instruction(opcode: int, args: list[str], difficulty: dict[str, str], replace_index: int) -> list[str]:
    lines: list[str] = []
    normalized = normalize_difficulty(difficulty)
    for rank in difficulty_rank_order(difficulty):
        ranked_args = list(args)
        ranked_args[replace_index] = normalized[rank]
        lines.append(f"!{rank}")
        lines.append(f"ins_{opcode}({', '.join(ranked_args)});")
    if lines:
        lines.append("!*")
    return lines


def maybe_difficulty_table(value) -> dict[str, str] | None:
    if isinstance(value, dict) and isinstance(value.get("difficulty"), dict):
        return value["difficulty"]
    return None


def resolved_arg(value, default: str) -> str:
    if isinstance(value, dict):
        return str(value.get("placeholder", default))
    return v(value, default)


def emit_instruction_with_ranked_args(opcode: int, args: list[object], defaults: list[str]) -> list[str]:
    if not any(maybe_difficulty_table(value) for value in args):
        return [f"ins_{opcode}({', '.join(str(resolved_arg(value, defaults[idx])) for idx, value in enumerate(args))});"]
    default_args = [str(resolved_arg(value, defaults[idx])) for idx, value in enumerate(args)]
    lines: list[str] = [f"ins_{opcode}({', '.join(default_args)});"]
    for rank in ("E", "N", "H", "L"):
        ranked_args: list[str] = []
        has_rank = False
        for idx, value in enumerate(args):
            difficulty = maybe_difficulty_table(value)
            if difficulty:
                normalized = normalize_difficulty(difficulty)
                ranked_args.append(str(normalized.get(rank, resolved_arg(value, defaults[idx]))))
                has_rank = has_rank or rank in normalized
            else:
                ranked_args.append(str(resolved_arg(value, defaults[idx])))
        if has_rank:
            lines.append(f"!{rank}")
            lines.append(f"ins_{opcode}({', '.join(ranked_args)});")
    if lines:
        lines.append("!*")
    return lines


def rank_values(value, fallback: str) -> list[str] | None:
    difficulty = maybe_difficulty_table(value)
    if not difficulty:
        return None
    normalized = normalize_difficulty(difficulty)
    return [normalized.get(rank, fallback) for rank in ("E", "N", "H", "L")]


def th12_difficulty_speed_args(emitter_id: str, speed_value, fallback_speed: str, speed_step_value, fallback_step: str) -> list[str] | None:
    first = rank_values(speed_value, fallback_speed)
    step = rank_values(speed_step_value, fallback_step)
    if not first and not step:
        return None
    first = first or [fallback_speed for _ in range(4)]
    step = step or [fallback_step for _ in range(4)]
    return [emitter_id, *first, *step]


def th12_difficulty_count_args(emitter_id: str, ways_value, fallback_ways: str, layers_value, fallback_layers: str) -> list[str] | None:
    ways = rank_values(ways_value, fallback_ways)
    layer_values = rank_values(layers_value, fallback_layers)
    if not ways and not layer_values:
        return None
    ways = ways or [fallback_ways for _ in range(4)]
    layer_values = layer_values or [fallback_layers for _ in range(4)]
    return [emitter_id, *ways, *layer_values]

def emit_th12_bullet_setup_lines(
    emitter_id: str,
    aim_raw_value,
    style_value,
    color_value,
    ways_value,
    ways: str,
    layers_value,
    layers: str,
    angle_value,
    angle_step_value,
    speed_value,
    speed: str,
    speed_step_value,
    speed_step: str,
) -> list[str]:
    emitter_id = as_int_expr(emitter_id)
    aim_raw_value = as_int_expr(aim_raw_value)
    style_value = as_int_expr(style_value)
    color_value = as_int_expr(color_value)
    ways_value = as_int_expr(ways_value)
    layers_value = as_int_expr(layers_value)
    ways = as_int_expr(ways)
    layers = as_int_expr(layers)
    lines: list[str] = [f"ins_500({emitter_id});"]
    lines.extend(emit_instruction_with_ranked_args(507, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(502, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    count_args = th12_difficulty_count_args(emitter_id, ways_value, ways, layers_value, layers)
    if count_args:
        lines.append(f"ins_522({', '.join(count_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(506, [emitter_id, ways, layers], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(504, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    speed_args = th12_difficulty_speed_args(emitter_id, speed_value, speed, speed_step_value, speed_step)
    if speed_args:
        lines.append(f"ins_521({', '.join(speed_args)});")
    else:
        lines.extend(emit_instruction_with_ranked_args(505, [emitter_id, speed, speed_step], ["0", "1.0f", "0.0f"]))
    return lines


def append_sound_lines(lines: list[str], target: str, e: BulletEmitter, emitter_id: str) -> None:
    opcode = {"th10": 408, "th11": 408, "th12": 508, "th13": 608, "th14": 608, "th15": 608, "th16": 608, "th17": 608, "th18": 608}.get(target)
    if opcode is None:
        return
    args = sound_args(e, emitter_id)
    if args:
        lines.append(emit_checked_instruction(target, opcode, args))


def spread_semantics(e: BulletEmitter) -> dict:
    return getattr(e, "semantics", {}).get("bullet", {}).get("spread", {})


def fire_at_definition(emitter: BulletEmitter) -> bool:
    return bool(getattr(emitter, "semantics", {}).get("bullet", {}).get("fire_at_definition"))


def append_definition_fire(text: str, emitter: BulletEmitter, target: str) -> str:
    if not fire_at_definition(emitter):
        return text
    emitter_id = v(emitter.id, "0")
    fire_opcode = {
        "th10": 401, "th11": 401, "th12": 501,
        "th13": 601, "th14": 601, "th15": 601, "th16": 601, "th17": 601, "th18": 601,
    }.get(target)
    if fire_opcode is None:
        return text
    lines = text.splitlines()
    if any(re.search(rf"\bins_{fire_opcode}\s*\(\s*{re.escape(str(emitter_id))}\s*\)", line) for line in lines):
        return text
    lines.append(f"// LuaSTG direct bullet call lowered to target fire")
    lines.append(f"ins_{fire_opcode}({emitter_id});")
    spread_plan = (getattr(emitter, "semantics", {}).get("lowering_plan", {}) or {}).get("spread", {}) if target == "th12" else {}
    aux_id = spread_plan.get("aux_emitter_id") if isinstance(spread_plan, dict) else None
    if aux_id:
        lines.append(f"ins_{fire_opcode}({aux_id});")
    return "\n".join(lines)


def definition_emitter_state(emitter: BulletEmitter) -> BulletEmitter:
    state = getattr(emitter, "semantics", {}).get("definition_state")
    if not isinstance(state, dict):
        return emitter
    definition = BulletEmitter(
        game=emitter.game,
        function=emitter.function,
        source_line=emitter.source_line,
        id=emitter.id,
        family=emitter.family,
    )
    definition.origin = deepcopy(state.get("origin", emitter.origin))
    definition.appearance = deepcopy(state.get("appearance", emitter.appearance))
    definition.aim = deepcopy(state.get("aim", emitter.aim))
    definition.count = deepcopy(state.get("count", emitter.count))
    definition.speed = deepcopy(state.get("speed", emitter.speed))
    definition.sound = deepcopy(state.get("sound", emitter.sound))
    definition.flags = deepcopy(state.get("flags", emitter.flags))
    definition.semantics = deepcopy(emitter.semantics)
    if isinstance(state.get("semantics"), dict):
        definition.semantics["bullet"] = deepcopy(state["semantics"].get("bullet", definition.semantics.get("bullet", {})))
    definition.transforms = [BulletTransform(**transform) for transform in state.get("transforms", []) if isinstance(transform, dict)]
    definition.fire_lines = emitter.fire_lines[:]
    definition.raw = emitter.raw[:]
    definition.unsupported = emitter.unsupported[:]
    return definition


def compile_bullet_emitter(emitter: BulletEmitter, target: str) -> str:
    definition = definition_emitter_state(emitter)
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        compiled = compile_th13plus(definition)
    elif target == "th12":
        compiled = compile_th12(definition)
    elif target in {"th10", "th11"}:
        compiled = compile_th10_slot(definition, target)
    elif target in {"th06", "th07", "th08"}:
        compiled = compile_th08_macro(definition, target)
    else:
        raise ValueError(f"unsupported target backend: {target}")
    return append_definition_fire(compiled, emitter, target)


def compile_object(obj, target: str) -> str:
    kind = getattr(obj, "kind", None)
    if kind == "BulletEmitter":
        compiled = compile_bullet_emitter(obj, target)
    elif kind == "LaserEmitter":
        compiled = compile_laser(obj, target)
    elif kind == "Movement":
        compiled = compile_movement(obj, target)
    elif kind == "Animation":
        compiled = compile_named_op(obj, target, ANIMATION_OPS)
    elif kind == "EnemyVisual":
        compiled = compile_enemy_visual(obj, target)
    elif kind == "Enemy":
        compiled = compile_named_op(obj, target, ENEMY_OPS)
    elif kind == "BossPattern":
        compiled = compile_boss_pattern(obj, target)
    elif kind == "EffectEmitter":
        compiled = compile_effect_emitter(obj, target)
    elif kind == "FamiliarSpawner":
        compiled = compile_familiar_spawner(obj, target)
    elif kind == "AutoBulletTimer":
        compiled = compile_auto_bullet_timer(obj, target)
    elif kind == "BossTimer":
        compiled = compile_boss_timer(obj, target)
    elif kind == "MotionModifier":
        compiled = compile_motion_modifier(obj, target)
    elif kind == "UnitFlag":
        compiled = compile_unit_flag(obj, target)
    elif kind == "Mode":
        compiled = compile_mode(obj, target)
    elif kind == "Timeline":
        compiled = compile_timeline(obj, target)
    else:
        compiled = compile_raw_comment(obj, target)
    if target in {"th06", "th07", "th08", "th09", "th10", "th11"}:
        compiled = strip_line_comments(compiled)
    difficulty = object_difficulty(obj)
    return "\n".join(wrap_ranked_lines(compiled.splitlines(), difficulty, target))


def strip_line_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue
        lines.append(line)
    return "\n".join(lines)



def compile_enemy_visual(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    source_game = getattr(obj, "game", "")
    if fields.get("semantic") != "stage_enemy_visual":
        return compile_raw_comment(obj, target)
    select_opcode = target_opcode_for_op_key("anm.select", target)
    main_opcode = target_opcode_for_op_key("anm.set_main", target)
    sprite_opcode = target_opcode_for_op_key("anm.set_sprite", target)
    drop_opcode = target_opcode_for_op_key("unit.drop_main", target)
    if not select_opcode or not main_opcode:
        return compile_structured_preserve(obj, target, "stage enemy visual has no verified ANM target ops")
    if not is_opcode_supported(target, select_opcode) or not is_opcode_supported(target, main_opcode):
        return compile_structured_preserve(obj, target, "stage enemy visual target ANM ops unsupported")
    main_script = str(fields.get("main_script", "0"))
    overlay_script = str(fields.get("overlay_script", ""))
    overlay_slot = str(fields.get("overlay_slot", "1"))
    drop_style = str(fields.get("drop_style", ""))
    lines = [
        f"// semantic EnemyVisual stage_enemy_visual {source_game}->{target}: color={fields.get('color', 'unknown')} source_script={fields.get('source_script', '')}",
        f"ins_{select_opcode}(2);",
        f"ins_{main_opcode}(0, {main_script});",
    ]
    if overlay_script and sprite_opcode and is_opcode_supported(target, sprite_opcode):
        lines.append(f"ins_{sprite_opcode}({overlay_slot}, {overlay_script});")
    if drop_style and drop_opcode and is_opcode_supported(target, drop_opcode):
        lines.append(f"ins_{drop_opcode}({drop_style});")
    return "\n".join(lines)

def object_difficulty(obj) -> str | None:
    if getattr(obj, "kind", None) == "BulletEmitter":
        return None
    raw = getattr(obj, "raw", []) or []
    difficulties = [getattr(ins, "difficulty", None) for ins in raw if getattr(ins, "difficulty", None)]
    if difficulties and all(item == difficulties[0] for item in difficulties):
        return difficulties[0]
    fields = getattr(obj, "fields", {}) or {}
    difficulty = fields.get("difficulty")
    return str(difficulty) if difficulty else None


ANIMATION_OPS = {
    "th12": {"anmSelect": 258, "anmSetSprite": 259, "anmSetMain": 262, "anmPlay": 263, "anmPlayAbs": 264},
    "th10_th11": {"anmSelect": 258, "anmSetSprite": 259, "anmSetMain": 262, "anmPlay": 263, "anmPlayAbs": 264},
    "th13plus": {"anmSelect": 302, "anmSetSprite": 303, "anmSetMain": 306, "anmPlay": 307, "anmPlayAbs": 308, "anmSwitch": 317, "anmReset": 318},
}

ENEMY_OPS = {
    "th12": {"enmCreate": 256, "enmCreateA": 257, "enmCreateM": 260, "enmCreateAM": 261, "enmCreateF": 265, "enmCreateAF": 266, "enmCreateMF": 267, "enmCreateAMF": 268},
    "th10_th11": {"enmCreate": 256, "enmCreateA": 257, "enmCreateM": 260, "enmCreateAM": 261, "enmCreateF": 265, "enmCreateAF": 266, "enmCreateMF": 267, "enmCreateAMF": 268},
    "th13plus": {"enmCreate": 300, "enmCreateA": 301, "enmCreateM": 304, "enmCreateAM": 305, "enmCreateF": 309, "enmCreateAF": 310, "enmCreateMF": 311, "enmCreateAMF": 312},
}

BOSS_OPS = {
    "th12": {"lifeSet": 411, "setBoss": 412, "timerReset": 413, "setInterrupt": 414, "setTimeout": 421, "spellEnd": 423, "setChapter": 424, "spell": 437, "spell2": 438, "spell3": 439},
    "th13plus": {"lifeSet": 511, "setBoss": 512, "timerReset": 513, "setInterrupt": 514, "setTimeout": 521, "spellEnd": 523, "setChapter": 524, "spell": 537, "spell2": 538, "spell3": 539},
}


def target_family(target: str) -> str:
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return "th13plus"
    if target in {"th10", "th11"}:
        return "th10_th11"
    if target in {"th06", "th07", "th08"}:
        return "th08_macro"
    return "th12"


def target_policy_applies(policy: dict[str, object], target: str) -> bool:
    targets = policy.get("targets")
    return not isinstance(targets, list) or target in {str(item) for item in targets}


def compile_target_policy(obj, target: str) -> str | None:
    fields = getattr(obj, "fields", {}) or {}
    policies = fields.get("target_policy", {}) or {}
    if drop := policies.get("drop_for_target"):
        if isinstance(drop, dict) and target_policy_applies(drop, target):
            return f"// dropped by IR target policy: {drop.get('reason', 'drop_for_target')}"
    if omit := policies.get("omit_runtime_entity"):
        if isinstance(omit, dict) and target_policy_applies(omit, target):
            return f"// omitted runtime entity by IR target policy: {omit.get('reason', 'omit_runtime_entity')}"
    if legacy := policies.get("legacy_attack_animation"):
        if isinstance(legacy, dict):
            lowered = emit_target_op(target, str(legacy.get("fallback_op_key", "anm.play")), [str(arg) for arg in legacy.get("args", ["0", "0"])])
            if lowered:
                return f"// animation semantic lowering {obj.family} -> {target}: {legacy.get('semantic', 'legacy_attack_animation')}\n{lowered}"
            return compile_structured_preserve(obj, target, "legacy boss attack animation has no verified target slot")
    if wrapper := policies.get("stage_enemy_wrapper_anm"):
        if isinstance(wrapper, dict) and target_policy_applies(wrapper, target):
            combo = (wrapper.get("native_combos", {}) or {}).get(str(wrapper.get("source_script", "")))
            if isinstance(combo, dict):
                select_opcode = target_opcode_for_op_key("anm.select", target)
                main_opcode = target_opcode_for_op_key("anm.set_main", target)
                sprite_opcode = target_opcode_for_op_key("anm.set_sprite", target)
                if select_opcode and main_opcode and sprite_opcode:
                    lines = [
                        f"// IR stage_enemy_wrapper_anm lowering {obj.game}->{target}: source_script={wrapper.get('source_script')}",
                        f"ins_{select_opcode}({combo.get('bank', '2')});",
                        f"ins_{main_opcode}({combo.get('main_slot', '0')}, {combo.get('main_script', '0')});",
                    ]
                    if combo.get("sprite_script") not in {None, ""}:
                        lines.append(f"ins_{sprite_opcode}({combo.get('sprite_slot', '1')}, {combo.get('sprite_script')});")
                    return "\n".join(lines)
    if aux := policies.get("boss_aux_sprite"):
        if isinstance(aux, dict):
            chosen = choose_script(target, str(aux.get("catalog_role", "boss")), str(aux.get("catalog_purpose", "familiar")), kind=str(aux.get("catalog_kind", "sprite")))
            if chosen is None:
                return None
            return "\n".join([
                f"// IR boss_aux_sprite lowering through target ANM catalog: bank {chosen.bank}, script {chosen.script}",
                f"ins_{target_opcode_for_op_key('anm.select', target)}({chosen.bank});",
                f"ins_{target_opcode_for_op_key('anm.set_sprite', target)}({aux.get('source_slot', '0')}, {chosen.script});",
            ])
    if spell := policies.get("spell_ex_common_header"):
        if isinstance(spell, dict) and op_lowering_policy_applies(spell, target, getattr(obj, "game", "")):
            args = [str(arg) for arg in (fields.get("spell", {}) or {}).get("args", fields.get("args", []))]
            lowered = emit_target_op(target, str(spell.get("target_op_key", "boss.spell_ex")), policy_args(args, spell))
            if lowered:
                return f"// IR spell_ex_common_header lowering {obj.game}->{target}: {spell.get('reason', '')}\n{lowered}"
    return None


def compile_named_op(obj, target: str, table_by_family: dict[str, dict[str, int]]) -> str:
    if lowered_by_policy := compile_target_policy(obj, target):
        return lowered_by_policy
    if getattr(obj, "kind", None) == "Enemy" and obj.fields.get("semantic") == "flying_bowl_line_visual" and obj.fields.get("target_behavior") == "omit_visual_helper":
        return "// omitted visual helper object: flying_bowl_line_visual; bullet motion is represented by emitter transforms"
    if getattr(obj, "kind", None) == "Animation" and obj.fields.get("op") == "anmPlayAttack":
        lowered = emit_target_op(target, "anm.play", ["0", "0"])
        if lowered:
            return f"// animation semantic lowering {obj.family} -> {target}: legacy boss attack animation approximated as ANM play\n{lowered}"
        return compile_structured_preserve(obj, target, "legacy boss attack animation has no verified target slot")
    source_events = object_ir_events(obj)
    source_event = source_events[0] if source_events else {}
    event = {
        **source_event,
        "op_key": obj.fields.get("op_key"),
        "source_game": getattr(obj, "game", ""),
        "source_opcode": getattr(obj.raw[0], "opcode", -1) if getattr(obj, "raw", None) else -1,
        "args": semantic_object_args(obj, target),
    }
    if getattr(obj, "kind", None) == "Enemy":
        event = semantic_enemy_create_event(obj, target, event)
    context = {"function": getattr(obj, "function", ""), "source_path": getattr(obj, "source", "") or obj.fields.get("source", "")}
    lowered = compile_ir_op_event(event, target, f"{obj.kind} lowering {obj.family} -> {target}", context)
    if lowered:
        return lowered
    if event.get("op_key"):
        return compile_raw_comment(obj, target) + f"\n// unsupported semantic op_key for {target}: {event.get('op_key')}"
    family = target_family(target)
    semantic = obj.fields.get("op")
    opcode = table_by_family.get(family, {}).get(semantic)
    if opcode is None:
        return compile_raw_comment(obj, target) + f"\n// unsupported legacy semantic op for {target}: {semantic}"
    args = remap_named_args(obj, target, semantic, obj.fields.get("args", []))
    return f"// legacy {obj.kind} lowering without op_key {obj.family} -> {target}: {semantic}\n" + emit_checked_instruction(target, opcode, args)


def semantic_enemy_create_event(obj, target: str, event: dict[str, object]) -> dict[str, object]:
    fields = getattr(obj, "fields", {}) or {}
    create = fields.get("create")
    if not isinstance(create, dict):
        return event
    target_forms = create.get("target_forms") if isinstance(create.get("target_forms"), dict) else {}
    op_key = str(target_forms.get(generation_for_game(target)) or event.get("op_key") or "")
    if not op_key:
        return event
    return {**event, "op_key": op_key, "create": create}


def semantic_object_args(obj, target: str) -> list[str]:
    args = [str(arg) for arg in (getattr(obj, "fields", {}) or {}).get("args", [])]
    return args


def remap_named_args(obj, target: str, semantic: str, args: list[str]) -> list[str]:
    args = list(args)
    source_game = getattr(obj, "game", "")
    if not source_game or source_game == target:
        return args
    context = {"function": getattr(obj, "function", ""), "source_path": getattr(obj, "source", "") or obj.fields.get("source", "")}
    role_hint = anm_role_hint({"source_game": source_game}, context)
    if semantic == "anmSelect" and len(args) == 1:
        source_bank = parse_int_literal(args[0])
        if source_bank is not None:
            return [str(remap_anm_bank(source_game, target, source_bank, role_hint))]
    if semantic in {"anmPlay", "anmPlayAbs"} and len(args) >= 2:
        source_bank = parse_int_literal(args[0])
        source_script = parse_int_literal(args[1])
        if source_bank is not None and source_script is not None:
            purpose = "boss_spawn" if role_hint == "boss" else "stage_spawn" if role_hint == "stage" else "spawn"
            chosen = remap_play_script(source_game, target, source_bank, source_script, role_hint, purpose)
            return [str(chosen.bank), str(chosen.script), *args[2:]]
    if semantic in {"anmSetMain", "anmSetSprite"} and len(args) == 2 and role_hint:
        script = parse_int_literal(args[1])
        source_bank = target_bank_for_role(source_game, role_hint)
        if script is not None and source_bank is not None:
            set_kind = "main" if semantic == "anmSetMain" else "sprite"
            purpose = "boss_aux" if role_hint == "boss" and set_kind == "sprite" else "stage_enemy" if role_hint == "stage" else "main"
            return [args[0], str(remap_set_script(source_game, target, source_bank, script, role_hint, purpose, set_kind).script)]
    return args


def compile_boss_pattern(obj, target: str) -> str:
    lines = [f"// BossPattern lowering {obj.family} -> {target}; semantic op_key backend"]
    for item in obj.fields.get("ops", []):
        event = {
            "op_key": item.get("op_key"),
            "source_game": getattr(obj, "game", ""),
            "source_opcode": item.get("opcode", -1),
            "args": item.get("args", []),
        }
        lowered = compile_ir_op_event(event, target)
        if lowered:
            lines.extend(lowered.splitlines())
        else:
            lines.append(compile_unsupported_ir_op(event, target))
    return "\n".join(lines)


def compile_timeline(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    if getattr(obj, "game", "") == "luastg" and fields.get("op") == "wait":
        frames = str(fields.get("frames", "1"))
        if target in {"th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
            return f"// LuaSTG wait lowering -> {target}\nins_83({frames});"
        return f"// LuaSTG wait lowering -> {target}; old target wait syntax requires manual placement\n// wait {frames} frames"
    lines = [f"// Timeline lowering {obj.family} -> {target}; structure-preserving draft"]
    lines.append("// control-flow, async scheduling, and expression semantics require target-game verification")
    for event in obj.fields.get("statements", []):
        kind = event.get("kind")
        text = event.get("text") or ""
        if kind == "instruction":
            lines.append(f"// body instruction preserved in object-specific lowerings too: {text}")
        elif kind in {"label", "time", "goto", "conditional_goto", "call", "async_call", "return", "var", "assign"}:
            lines.append(text + (";" if kind in {"goto", "conditional_goto", "call", "async_call", "return", "var", "assign"} and not str(text).endswith(";") else ""))
        elif text:
            lines.append(f"// raw: {text}")
    loops = obj.fields.get("loops", [])
    if loops:
        lines.append("// detected loops:")
        for loop in loops:
            lines.append(f"// - {loop.get('kind')} {loop.get('label')} lines {loop.get('start_line')}..{loop.get('end_line')} condition={loop.get('condition')}")
    return "\n".join(lines)


def compile_raw_comment(obj, target: str) -> str:
    lines = [f"// no safe lowering implemented for {obj.kind} family={obj.family} to {target}"]
    for ins in getattr(obj, "raw", []):
        lines.append(f"// {ins.raw.strip()}")
    return "\n".join(lines)


def object_ir_events(obj) -> list[dict[str, object]]:
    fields = getattr(obj, "fields", {}) or {}
    events = list(fields.get("operations") or fields.get("ir_ops") or [])
    if events:
        return [normalize_backend_event(event) for event in events]
    return [
        {"op_key": None, "source_game": getattr(obj, "game", ""), "source_opcode": ins.opcode, "args": ins.args}
        for ins in getattr(obj, "raw", [])
    ]


def compile_structured_preserve(obj, target: str, reason: str = "no native equivalent") -> str:
    fields = getattr(obj, "fields", {}) or {}
    lines = [f"// semantic object preserved for {target}: {obj.kind}.{fields.get('semantic', obj.family)} ({reason})"]
    for key in ("effect", "spawn", "trail", "focus_animation", "timer", "interrupt", "life_bar", "motion"):
        if key in fields:
            lines.append(f"//   {key}: {fields[key]}")
    for ins in getattr(obj, "raw", []):
        lines.append(f"//   source: {ins.raw.strip()}")
    return "\n".join(lines)


def emit_if_supported(target: str, op_key: str, args: list[str], source_game: str = "", source_opcode: int = -1) -> str | None:
    opcode = target_opcode_for_op_key(op_key, target)
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return None
    adapted = adapt_args_for_op_key(op_key, source_game, source_opcode, target, opcode, [str(arg) for arg in args])
    if adapted is None:
        return None
    adapted = normalize_target_args_for_op_key(op_key, target, adapted)
    error = validate_opcode_args(target, opcode, adapted)
    if error:
        return None
    return emit_checked_instruction(target, opcode, adapted)


def emit_target_op(target: str, op_key: str, args: list[str]) -> str | None:
    opcode = target_opcode_for_op_key(op_key, target)
    if opcode is None or not is_opcode_supported(target, opcode) or not target_opcode_is_safe(target, opcode):
        return None
    normalized = normalize_target_args_for_op_key(op_key, target, [str(arg) for arg in args])
    error = validate_opcode_args(target, opcode, normalized)
    if error:
        return None
    return emit_checked_instruction(target, opcode, normalized)


def target_sub_name(value: object) -> str:
    text = str(value).strip()
    if text.startswith('"') and text.endswith('"'):
        return text
    if re.fullmatch(r"-?\d+", text):
        return f'"Sub{text}"'
    return f'"{text}"'


def float_literal(value: object, default: str = "0.0f") -> str:
    text = str(value).strip()
    if re.fullmatch(r"[-+]?\d+", text):
        return f"{text}.0f"
    if re.fullmatch(r"[-+]?\d+\.\d+f?", text):
        return text if text.endswith("f") else f"{text}f"
    if re.fullmatch(r"\[-?\d+\]", text):
        return text[:-1] + ".0f]"
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]", text):
        return text
    return default


def compile_effect_emitter(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    lines = [f"// EffectEmitter lowering {obj.family} -> {target}: {semantic}"]
    visual_policy = (fields.get("target_policy", {}) or {}).get("visual_effect", {})
    if visual_policy:
        effect = fields.get("effect", {}) or {}
        amount = str(effect.get("amount", "1"))
        op_key = str(visual_policy.get("target_op_key", "anm.play"))
        args = [str(arg) for arg in visual_policy.get("args", [])]
        lowered = emit_target_op(target, op_key, args)
        if lowered:
            lines.append(f"// IR visual effect policy count={amount}: {visual_policy.get('strategy', op_key)}")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic in {"effect_burst", "effect_burst_angle"}:
        effect = fields.get("effect", {}) or {}
        script_expr = str(effect.get("script_expr", "0"))
        amount = str(effect.get("amount", "1"))
        angle = str(effect.get("angle") or "0.0f")
        play_rotate = emit_target_op(target, "anm.play_rotate", ["0", script_expr, angle])
        play_plain = emit_target_op(target, "anm.play", ["0", script_expr])
        if play_rotate and semantic == "effect_burst_angle":
            lines.append(f"// approximated old etama effect count={amount} using target ANM play_rotate")
            lines.append(play_rotate)
            return "\n".join(lines)
        if play_plain:
            lines.append(f"// approximated old etama effect count={amount} using target ANM play")
            lines.append(play_plain)
            return "\n".join(lines)
    if semantic == "card_effect":
        lowered = next((candidate for event in object_ir_events(obj) if (candidate := compile_ir_op_event(event, target))), None)
        if lowered:
            lines.extend(lowered.splitlines())
            return "\n".join(lines)
    if semantic in {"spell_effect_state", "spell_start_effect_state"}:
        high = emit_target_op(target, "anm.play_high", ["0", "0"])
        if high:
            lines.append("// approximated legacy spell visual state as target high-priority ANM boundary")
            lines.append(high)
            return "\n".join(lines)
        lines.append("// metadata-only spell visual state boundary; no target runtime opcode required")
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "visual effect has no verified cross-generation equivalent").splitlines())


def compile_familiar_spawner(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    spawn = fields.get("spawn", {}) or {}
    lines = [f"// FamiliarSpawner lowering {obj.family} -> {target}: {semantic}"]
    policies = fields.get("target_policy", {}) or {}
    if spawn:
        sub = target_sub_name(spawn.get("sub", ""))
        x = str(spawn.get("x", "0.0f"))
        y = str(spawn.get("y", "0.0f"))
        life = str(spawn.get("life", "0"))
        item = str(spawn.get("item", "0"))
        score = str(spawn.get("score", "0"))
        rel = spawn.get("position_mode") != "absolute"
        op_key = "enemy.create_func" if rel else "enemy.create_abs_func"
        fallback = [sub, x, y, life, item, score]
        if not emit_target_op(target, op_key, fallback):
            op_key = "enemy.create" if rel else "enemy.create_abs"
            fallback = [sub, x, y, life, item, score]
        lowered = emit_target_op(target, op_key, fallback)
        if lowered:
            policy = (policies.get("familiar_spawn", {}) or {})
            lines.append(f"// IR familiar spawn policy: {policy.get('strategy', 'enemy_child_approximation')}; focus invulnerability is metadata")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "focus_animation":
        focus_policy = (policies.get("focus_animation", {}) or {})
        focus = fields.get("focus_animation", {}) or {}
        lowered = emit_target_op(target, str(focus_policy.get("target_op_key", "anm.play")), [str(arg) for arg in focus_policy.get("args", ["0", str(focus.get("script_expr", "0"))])])
        if lowered:
            lines.append("// approximated familiar focus ANM as ordinary ANM play")
            lines.append(lowered)
            return "\n".join(lines)
    if semantic == "trail_toggle":
        trail_policy = (policies.get("trail_toggle", {}) or {})
        lines.append(f"// IR familiar trail policy: {trail_policy.get('strategy', 'metadata_only')}; target games have no verified equivalent trail runtime")
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "familiar runtime behavior is TH08-specific").splitlines())


def compile_auto_bullet_timer(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    timer = fields.get("timer", {}) or {}
    lines = [f"// AutoBulletTimer lowering {obj.family} -> {target}: {semantic}"]
    plan = fields.get("lowering_plan", {}) or {}
    if semantic == "defer_attribute_fire" or plan.get("strategy") == "metadata_only":
        lines.append(f"// IR auto-fire policy: {plan.get('reason', 'target slot emitters are configured without implicit fire')}")
        return "\n".join(lines)
    interval = str(timer.get("interval", "1"))
    fire = emit_target_op(target, str(plan.get("target_op_key", "bullet.fire")), ["0"])
    if fire:
        lines.append(f"// auto-fire interval={interval} preserved as high-level timer; emitted one fire tick at source position")
        lines.append(fire)
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "target has no verified auto-fire timer primitive").splitlines())


def emit_plan_instruction(target: str, plan: dict[str, object]) -> list[str]:
    if not isinstance(plan, dict):
        return []
    if sequence := plan.get("sequence"):
        lines: list[str] = []
        if isinstance(sequence, list):
            for item in sequence:
                if not isinstance(item, dict):
                    continue
                lowered = emit_target_op(target, str(item.get("target_op_key", "")), [str(arg) for arg in item.get("args", [])])
                if lowered:
                    lines.append(lowered)
        return lines
    target_op_key = str(plan.get("target_op_key", ""))
    if not target_op_key:
        return []
    lowered = emit_target_op(target, target_op_key, [str(arg) for arg in plan.get("args", [])])
    return [lowered] if lowered else []


def plan_for_target_generation(plan: dict[str, object], target: str) -> dict[str, object]:
    if str(plan.get("strategy", "")) != "target_by_generation":
        return plan
    plans = plan.get("plans") if isinstance(plan.get("plans"), dict) else {}
    selected = plans.get(generation_for_game(target)) or plans.get(target)
    if isinstance(selected, dict):
        return selected
    return {}


def compile_boss_timer(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    plan = fields.get("lowering_plan", {}) if isinstance(fields.get("lowering_plan"), dict) else {}
    selected_plan = plan_for_target_generation(plan, target)
    lines = [f"// BossTimer lowering {obj.family} -> {target}: {semantic}; plan={plan.get('strategy', 'direct')}"]
    lowered_lines = emit_plan_instruction(target, selected_plan)
    if lowered_lines:
        reason = selected_plan.get("reason") or plan.get("reason") or selected_plan.get("strategy") or plan.get("strategy")
        lines.append(f"// IR boss timer plan: {reason}")
        lines.extend(lowered_lines)
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "boss HUD/timer semantics differ across generations").splitlines())



def compile_unit_flag(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    flag = fields.get("flag", {}) or {}
    op_key = str(fields.get("op_key") or flag.get("op_key") or "")
    raw = str(flag.get("raw_flag", "0"))
    source_game = getattr(obj, "game", "")
    mapping = (fields.get("targets", {}) or {}).get(target) or remap_unit_flag_mask(source_game, target, raw)
    target_value = mapping.get("target_flag", "drop")
    names = "+".join(str(name) for name in flag.get("names", [])) or raw
    dropped = mapping.get("dropped", []) or []
    suffix = ""
    if dropped:
        suffix = "; dropped=" + "+".join(str(item.get("semantic", "")) for item in dropped)
    if target_value in {None, "", "drop"}:
        return f"// UnitFlag lowering {source_game}->{target}: dropped {op_key}({raw}); semantic={names}{suffix}"
    lowered = emit_target_op(target, op_key, [str(target_value)])
    if lowered:
        return f"// UnitFlag lowering {source_game}->{target}: {op_key}({raw}) {names} -> {target_value}{suffix}\n{lowered}"
    return compile_lossy_semantic_fallback({"op_key": op_key, "source_game": source_game, "source_opcode": getattr(obj.raw[0], "opcode", -1) if getattr(obj, "raw", None) else -1, "args": [raw]}, target)

def compile_mode(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    mode = fields.get("mode", {}) or {}
    semantic = fields.get("semantic", "mode")
    if semantic == "bullet_transform_mode":
        return "// Mode IR metadata: bullet transform mode raw={raw} semantic={name} target_th12={th12} target_th15={th15}".format(
            raw=mode.get("raw", ""), name=mode.get("name", ""), th12=mode.get("target_th12", ""), th15=mode.get("target_th15", "")
        )
    if semantic == "movement_tween_mode":
        return "// Mode IR metadata: movement tween mode raw={raw} semantic={name} target={target}".format(raw=mode.get("raw", ""), name=mode.get("name", ""), target=mode.get("target", ""))
    if semantic == "mirror_mode":
        lowered = emit_target_op(target, "movement.mirror_mode", [str(mode.get("raw", "0"))])
        if lowered:
            return f"// Mode lowering mirror mode -> {target}\n{lowered}"
    return f"// Mode IR metadata: {semantic} {mode}"

def compile_motion_modifier(obj, target: str) -> str:
    fields = getattr(obj, "fields", {}) or {}
    semantic = str(fields.get("semantic", ""))
    plan = fields.get("lowering_plan", {}) if isinstance(fields.get("lowering_plan"), dict) else {}
    lines = [f"// MotionModifier lowering {obj.family} -> {target}: {semantic}; plan={plan.get('strategy', 'direct')}"]
    lowered_lines = emit_plan_instruction(target, plan_for_target_generation(plan, target))
    if lowered_lines:
        lines.append(f"// IR motion modifier plan: {plan.get('reason', plan.get('strategy', 'direct'))}")
        lines.extend(lowered_lines)
        return "\n".join(lines)
    return "\n".join(lines + compile_structured_preserve(obj, target, "motion modifier needs runtime state unavailable in target opcode").splitlines())


def compile_luastg_laser(obj, target: str) -> str | None:
    if getattr(obj, "game", "") != "luastg":
        return None
    params = (getattr(obj, "fields", {}) or {}).get("params", {}) or {}
    laser_id = str(getattr(obj, "id", "0"))
    style = str(params.get("style", laser_id)).strip()
    length = str(params.get("length", "512.0f")).strip()
    width = str(params.get("width", "16.0f")).strip()
    warn = str(params.get("warn_time", "0")).strip()
    fade_in = str(params.get("fade_in", "0")).strip()
    active = str(params.get("active_time", "60")).strip()
    fade_out = str(params.get("fade_out", "15")).strip()
    angle = as_float_expr(params.get("angle", "0.0f"))
    kind = str(params.get("kind", "line")).strip().strip('"\'')
    if target == "th12":
        fire_opcode = 611 if kind == "curve" else 602
        return "\n".join([
            f"// LuaSTG laser semantic lowering -> th12: {kind}",
            f"ins_600({laser_id}, 0.0f, {length}, 0.0f, {width});",
            f"ins_601({laser_id}, {warn}, {fade_in}, {active}, {fade_out}, 0);",
            f"ins_608({laser_id}, {angle});",
            f"ins_{fire_opcode}({laser_id});",
        ])
    if target in {"th13", "th14", "th15", "th16", "th17", "th18"}:
        return "\n".join([
            f"// LuaSTG laser semantic lowering -> {target}: preserved draft, opcode mapping incomplete",
            f"// style={style} id={laser_id} length={length} width={width} angle={angle} timing={warn},{fade_in},{active},{fade_out} kind={kind}",
        ])
    return compile_raw_comment(obj, target) + f"\n// LuaSTG laser lowering to {target} is not implemented"


def compile_laser(obj, target: str) -> str:
    luastg_lowered = compile_luastg_laser(obj, target)
    if luastg_lowered is not None:
        return luastg_lowered
    if target in {"th06", "th07", "th08", "th10", "th11"}:
        return compile_raw_comment(obj, target) + f"\n// laser lowering to {target} is not implemented yet"
    if target not in {"th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported laser target: {target}")
    lines = [f"// laser lowering {obj.family} -> {target}; semantic op_key backend"]
    events = object_ir_events(obj)
    for event in events:
        lowered = compile_ir_op_event(event, target)
        if lowered:
            lines.extend(lowered.splitlines())
        else:
            lines.append(compile_unsupported_ir_op(event, target))
    return "\n".join(lines)


def parenthesize_expr(expr: object) -> str:
    expr = str(expr).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", expr):
        return expr
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]|[%$][A-Za-z_][A-Za-z0-9_]*", expr):
        return expr
    if expr.startswith("(") and expr.endswith(")"):
        return expr
    return f"({expr})"


def add_float_expr(left: object, right: object) -> str:
    left_text = str(left).strip()
    right_text = str(right).strip()
    if right_text.startswith("-") and re.fullmatch(r"-\d+(?:\.\d+)?f?", right_text):
        return f"{parenthesize_expr(left_text)} - {right_text[1:]}"
    return f"{parenthesize_expr(left_text)} + {parenthesize_expr(right_text)}"


def th12_unit_move_mode(mode: object) -> str:
    text = str(mode).strip()
    return text if text in {"0", "1", "4", "9"} else "0"


def normalize_th12_move_args(movement: str, args: list[str]) -> list[str]:
    normalized = [str(arg) for arg in args]
    if movement in {"movePosTime", "movePosRelTime", "moveVelTime", "moveVelRelTime", "moveEllipseTime", "moveEllipseRelTime", "moveBezier", "moveBezierRel"}:
        if len(normalized) > 1 and normalized[1] not in {"0", "1", "4", "9"}:
            normalized[1] = "0"
    return normalized


def compile_split_motion_semantic(obj, target: str) -> str | None:
    if target != "th12":
        return None
    motion = obj.fields.get("semantics", {}).get("motion", {})
    op = motion.get("op")
    rel = op in {"moveDirRel", "moveDirRelTime", "moveSpeedRel", "moveSpeedRelTime"}
    direct_opcode = 306 if rel else 304
    time_opcode = 307 if rel else 305
    if op in {"moveDir", "moveDirRel"}:
        speed = motion.get("speed")
        direction = motion.get("direction")
        if speed is None or direction is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: direction set needs current speed"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered speed\nins_{direct_opcode}({direction}, {speed});"
    if op in {"moveDirTime", "moveDirRelTime"}:
        speed = motion.get("speed")
        base_direction = motion.get("base_direction")
        delta = motion.get("direction_delta")
        if speed is None or base_direction is None or delta is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: direction interpolation needs current direction and speed"
        direction = add_float_expr(base_direction, delta)
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered speed\nins_{time_opcode}({motion.get('time', '0')}, {th12_unit_move_mode(motion.get('mode', '0'))}, {direction}, {speed});"
    if op in {"moveSpeed", "moveSpeedRel"}:
        direction = motion.get("direction")
        speed = motion.get("speed")
        if direction is None or speed is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: speed set needs current direction"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered direction\nins_{direct_opcode}({direction}, {speed});"
    if op in {"moveSpeedTime", "moveSpeedRelTime"}:
        direction = motion.get("direction")
        speed = motion.get("speed")
        if direction is None or speed is None:
            return compile_raw_comment(obj, target) + "\n// unsupported split movement semantic: speed interpolation needs current direction"
        return f"// movement semantic lowering {obj.family} -> {target}: {op} with remembered direction\nins_{time_opcode}({motion.get('time', '0')}, {th12_unit_move_mode(motion.get('mode', '0'))}, {direction}, {speed});"
    return None


def compile_movement(obj, target: str) -> str:
    if target not in {"th06", "th07", "th08", "th10", "th11", "th12", "th13", "th14", "th15", "th16", "th17", "th18"}:
        raise ValueError(f"unsupported movement target: {target}")
    semantic = compile_split_motion_semantic(obj, target)
    if semantic is not None:
        return semantic
    source_events = object_ir_events(obj)
    event = {
        **(source_events[0] if source_events else {}),
        "op_key": obj.fields.get("op_key"),
        "source_game": getattr(obj, "game", ""),
        "source_opcode": getattr(obj.raw[0], "opcode", -1) if getattr(obj, "raw", None) else -1,
        "args": obj.fields.get("args", []),
    }
    lowered = compile_ir_op_event(event, target, f"movement lowering {obj.family} -> {target}")
    if lowered:
        return lowered
    return compile_raw_comment(obj, target) + f"\n// unsupported movement semantic op_key for {target}: {obj.fields.get('op_key') or obj.fields.get('op')}"


def compile_th13plus(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = remap_bullet_spread_style_for_target(e, target="th15")
    if aim_raw_value is None:
        aim_raw_value = mode_raw(e.aim.get("mode"), default="1")
    style_value = remap_bullet_shape_for_target(e, target="th15")
    color_value = e.appearance.get("color")
    curve_plan = (e.semantics.get("lowering_plan", {}) or {}).get("curve_laser", {})
    if curve_plan:
        appearance_override = curve_plan.get("appearance_override", {}) or {}
        style_value = appearance_override.get("style", "0")
        color_value = appearance_override.get("color", "2")
    ways_value = e.count.get("ways")
    layers_value = e.count.get("layers")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    speed_value = e.speed.get("first")
    speed_step_value = e.speed.get("step")
    lines = [emit_checked_instruction("th15", 600, [emitter_id])]
    lines.extend(emit_instruction_with_ranked_args(607, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(602, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    lines.extend(emit_instruction_with_ranked_args(606, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(604, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    lines.extend(emit_instruction_with_ranked_args(605, [emitter_id, speed_value, speed_step_value if speed_step_value is not None else e.speed.get("last_or_step")], ["0", "1.0f", e.speed.get("last_or_step", "0.0f")]))
    lines.extend(th13plus_origin_lines(str(emitter_id), e.origin))
    lines.extend(th13plus_laser_origin_lines(e, str(emitter_id)))
    if args := sound_args(e, emitter_id):
        lines.append(emit_checked_instruction("th15", 608, args))
    for field, value in (("speed.first", e.speed.get("first")), ("count.ways", e.count.get("ways"))):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment)
    curve_plan = (e.semantics.get("lowering_plan", {}) or {}).get("curve_laser", {})
    transforms = curve_laser_th13plus_transforms(e.transforms, curve_plan) if curve_plan else e.transforms
    for transform in transforms:
        lowered = lower_transform_for_th13plus(transform, e.game, "th15", str(emitter_id))
        if lowered:
            lines.extend(lowered)
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    return "\n".join(lines)


def curve_laser_th13plus_transforms(transforms, curve_plan: dict[str, object] | None = None):
    plan = curve_plan or {}
    drop_modes = {str(mode) for mode in plan.get("drop_modes", ["512"])}
    renumber = bool(plan.get("renumber_transform_slots", True))
    normalize_tangent_delay = bool(plan.get("normalize_tangent_delay", True))
    normalized = []
    next_index = 0
    for transform in transforms:
        args = [str(arg) for arg in transform.raw_args]
        if transform.raw_opcode == 509 and len(args) == 8:
            mode = args[3]
            if mode in drop_modes:
                continue
            args = args[:]
            if renumber:
                args[1] = str(next_index)
            if normalize_tangent_delay and mode == "8" and args[5] == "-999999":
                args[5] = "0"
            next_index += 1
            cloned = deepcopy(transform)
            cloned.raw_args = args
            normalized.append(cloned)
            continue
        normalized.append(transform)
    return normalized


def lower_transform_for_th13plus(transform, source_game: str, target: str, emitter_id: str) -> list[str] | None:
    lowered = bullet_transform_instructions(transform, source_game, target)
    if lowered is None and target_transform_args(transform) is None:
        reason = (getattr(transform, "semantics", {}) or {}).get("drop_reason", "unsupported transform")
        return [f"// omitted transform from IR: {reason}; original ins_{transform.raw_opcode}({', '.join(str(arg) for arg in transform.raw_args)})"]
    if not lowered:
        args = target_transform_args(transform) or [str(arg) for arg in transform.raw_args]
        if transform.raw_opcode == 509:
            reason = unsupported_bullet_transform_mode_reason(source_game, target, args[3] if len(args) > 3 else "")
            if reason:
                return [f"// dropped unsupported bullet transform mode from ins_509: {reason}; original args: {', '.join(args)}"]
        return None
    lines: list[str] = []
    for instruction in lowered:
        if instruction.opcode == 624 and len(instruction.args) == 9:
            lines.extend(emit_instruction_with_ranked_args(624, instruction.args, [emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
        elif instruction.opcode == 625 and len(instruction.args) == 9:
            lines.extend(emit_instruction_with_ranked_args(625, instruction.args, [emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
        else:
            lines.append(f"ins_{instruction.opcode}({', '.join(instruction.args)});")
    return lines
    return None


def th13plus_origin_lines(emitter_id: str, origin: dict[str, object]) -> list[str]:
    return [emit_checked_instruction("th15", ins.opcode, ins.args) for ins in bullet_origin_instructions("th15", emitter_id, origin)]


def th12_origin_lines(emitter_id: str, origin: dict[str, object]) -> list[str]:
    return [emit_checked_instruction("th12", ins.opcode, ins.args) for ins in bullet_origin_instructions("th12", emitter_id, origin)]


def emitter_has_curve_laser(e: BulletEmitter) -> bool:
    return any(getattr(ins, "opcode", None) == 611 for ins in getattr(e, "raw", []))


def th13plus_laser_origin_lines(e: BulletEmitter, emitter_id: str) -> list[str]:
    return []


def remap_bullet_spread_style_for_target(e: BulletEmitter, target: str):
    spread = spread_semantics(e)
    if spread:
        return encode_spread_style(spread, target, e.aim.get("mode_raw"))
    return e.aim.get("mode_raw")


def remap_bullet_shape_for_target(e: BulletEmitter, target: str):
    value = e.appearance.get("style")
    if isinstance(value, dict):
        return {rank: encode_bullet_shape(bullet_shape_semantic(e.game, shape), target, shape) for rank, shape in value.items()}
    semantic_shape = getattr(e, "semantics", {}).get("bullet", {}).get("shape")
    if semantic_shape:
        return encode_bullet_shape(semantic_shape, target, value)
    return value


def compile_th12(e: BulletEmitter) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = remap_bullet_spread_style_for_target(e, target="th12")
    if aim_raw_value is None:
        aim_raw_value = mode_raw(e.aim.get("mode"), default="1")
    style_value = remap_bullet_shape_for_target(e, target="th12")
    color_value = e.appearance.get("color")
    ways_value = e.count.get("ways")
    speed_value = e.speed.get("first")
    ways = v(ways_value, "1")
    layers_value = e.count.get("layers")
    layers = v(layers_value, "1")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    angle = v(angle_value, "0.0f")
    angle_step = v(angle_step_value, "0.0f")
    speed = v(speed_value, "1.0f")
    speed_step_value = e.speed.get("step")
    if speed_step_value is None and e.speed.get("last_or_step") is not None:
        speed_step_value = e.speed.get("last_or_step")
    speed_step = v(speed_step_value, e.speed.get("last_or_step", "0.0f"))

    spread_plan = (e.semantics.get("lowering_plan", {}) or {}).get("spread", {})
    aux_emitter_id = str(spread_plan.get("aux_emitter_id")) if spread_plan else None
    if spread_plan and aux_emitter_id:
        lines = [f"// IR spread lowering: double_flower split to two TH12 single-side slots: {emitter_id}+{aux_emitter_id}"]
        lines.extend(emit_th12_bullet_setup_lines(emitter_id, spread_plan.get("primary_style", aim_raw_value), style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step))
        lines.extend(emit_th12_bullet_setup_lines(aux_emitter_id, spread_plan.get("aux_style", aim_raw_value), style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step))
    else:
        lines = emit_th12_bullet_setup_lines(emitter_id, aim_raw_value, style_value, color_value, ways_value, ways, layers_value, layers, angle_value, angle_step_value, speed_value, speed, speed_step_value, speed_step)

    append_sound_lines(lines, "th12", e, str(emitter_id))
    if aux_emitter_id:
        append_sound_lines(lines, "th12", e, str(aux_emitter_id))
    lines.extend(th12_origin_lines(str(emitter_id), e.origin))
    if aux_emitter_id:
        lines.extend(th12_origin_lines(str(aux_emitter_id), e.origin))

    for field, value in (("speed.first", speed_value), ("speed.step", speed_step_value), ("count.ways", ways_value), ("count.layers", layers_value)):
        comment = difficulty_comment(field, value)
        if comment:
            lines.insert(0, comment.replace("lowered using", "preserved as TH12 difficulty table; default preview"))
    next_transform_index = 0
    for transform in e.transforms:
        if transform.raw_opcode == 509 and len(transform.raw_args) == 8:
            lines.append(f"ins_509({', '.join(transform.raw_args)});")
            if str(transform.raw_args[0]) == str(emitter_id) and re.fullmatch(r"-?\d+", str(transform.raw_args[1])):
                next_transform_index = max(next_transform_index, int(str(transform.raw_args[1])) + 1)
        elif transform.raw_opcode == 510 and len(transform.raw_args) == 0:
            lines.append("ins_510();")
        elif transform.raw_opcode == 511 and len(transform.raw_args) == 2:
            lines.append(f"ins_511({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 512 and len(transform.raw_args) == 1:
            lines.append(f"ins_512({', '.join(transform.raw_args)});")
        elif transform.raw_opcode == 624 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(521, transform.raw_args, [emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
            if aux_emitter_id:
                aux_args = [aux_emitter_id, *transform.raw_args[1:]]
                lines.extend(emit_instruction_with_ranked_args(521, aux_args, [aux_emitter_id, "1.0f", "1.0f", "1.0f", "1.0f", "0.0f", "0.0f", "0.0f", "0.0f"]))
        elif transform.raw_opcode == 625 and len(transform.raw_args) == 9:
            lines.extend(emit_instruction_with_ranked_args(522, transform.raw_args, [emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
            if aux_emitter_id:
                aux_args = [aux_emitter_id, *transform.raw_args[1:]]
                lines.extend(emit_instruction_with_ranked_args(522, aux_args, [aux_emitter_id, "1", "1", "1", "1", "1", "1", "1", "1"]))
        elif transform.raw_opcode == 609 and len(transform.raw_args) == 8:
            lowered = lower_transform_opcode_to_instruction(e.game, "th12", transform.raw_opcode, transform.raw_args)
            if not lowered:
                lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
                continue
            lines.append(f"ins_{lowered.opcode}({', '.join(lowered.args)});")
            if str(transform.raw_args[0]) == str(emitter_id) and re.fullmatch(r"-?\d+", str(transform.raw_args[1])):
                next_transform_index = max(next_transform_index, int(str(transform.raw_args[1])) + 1)
        elif transform.raw_opcode == 611 and len(transform.raw_args) == 7:
            lowered = lower_transform_opcode_to_instruction(e.game, "th12", transform.raw_opcode, transform.raw_args, next_transform_index)
            if lowered:
                lines.append(f"ins_{lowered.opcode}({', '.join(lowered.args)});")
                if aux_emitter_id and str(transform.raw_args[0]) == str(emitter_id):
                    aux_args = [aux_emitter_id, *lowered.args[1:]]
                    lines.append(f"ins_{lowered.opcode}({', '.join(aux_args)});")
                next_transform_index += 1
            else:
                lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {610, 612}:
            lines.append(f"// unsupported th13+ transform for th12; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        elif transform.raw_opcode in {510, 511, 512}:
            lines.append(f"// unsupported th12 transform opcode/arity in generated context; preserved source ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
        else:
            lines.append(f"// unsupported transform from ins_{transform.raw_opcode}: {', '.join(transform.raw_args)}")
    return "\n".join(lines)




def old_macro_arg(value: object, default: str, numeric: str = "float") -> str:
    text = str(v(value, default)).strip()
    if isinstance(value, dict):
        text = str(v(value, default)).strip()
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?f?", text):
        return text
    if re.fullmatch(r"\[-?\d+(?:\.0f)?\]", text):
        return text
    if numeric == "int":
        return default
    return default


def old_macro_int(value: object, default: str) -> str:
    return old_macro_arg(value, default, "int")


def old_macro_float(value: object, default: str) -> str:
    return old_macro_arg(value, default, "float")


def clamp_old_shape(shape: object, target: str) -> str:
    value = str(v(shape, "0"))
    if not re.fullmatch(r"-?\d+", value):
        return value
    number = int(value)
    max_shape = 9 if target in {"th06", "th07"} else 20
    return str(min(max(number, 0), max_shape))


def compile_th08_macro(e: BulletEmitter, target: str) -> str:
    mode = e.aim.get("mode") or aim_mode_name(str(v(e.aim.get("mode_raw"), "1")))
    old_macro_plan = (e.semantics.get("lowering_plan", {}) or {}).get("old_macro", {})
    opcode_by_mode = old_macro_plan.get("opcode_by_mode", {}) if isinstance(old_macro_plan, dict) else {}
    opcode = int(opcode_by_mode.get(mode, 97))
    style = clamp_old_shape(old_macro_int(e.appearance.get("style"), "0"), target)
    color = old_macro_int(e.appearance.get("color"), "0")
    ways = old_macro_int(e.count.get("ways"), "1")
    layers = old_macro_int(e.count.get("layers"), "1")
    speed_max = old_macro_float(e.speed.get("first"), "1.0f")
    speed_min = old_macro_float(e.speed.get("step", e.speed.get("last_or_step")), speed_max)
    angle = old_macro_float(e.aim.get("base_angle"), "0.0f")
    angle_step = old_macro_float(e.aim.get("angle_step"), "0.0f")
    flags = old_macro_int(e.flags.get("raw"), "0")
    lines = [f"// bullet lowering {e.family} -> {target}: macro opcode ins_{opcode}; semantic verification required"]
    for transform in e.transforms:
        if transform.raw_opcode == 111 and len(transform.raw_args) == 7:
            lines.append(f"ins_111({', '.join(str(arg) for arg in transform.raw_args)});")
        elif transform.raw_opcode in {409, 509, 609, 610, 611, 612}:
            lines.append(f"// transform not representable in {target} macro backend: ins_{transform.raw_opcode}({', '.join(str(arg) for arg in transform.raw_args)});")
    # TH06-08 macro order is minspeed, maxspeed; TH10+ slot order stores first/max then last/min.
    lines.append(f"ins_{opcode}({style}, {color}, {ways}, {layers}, {speed_min}, {speed_max}, {angle}, {angle_step}, {flags});")
    return "\n".join(lines)


def compile_th10_slot(e: BulletEmitter, target: str) -> str:
    emitter_id = v(e.id, "0")
    aim_raw_value = e.aim.get("mode_raw", mode_raw(e.aim.get("mode"), default="1"))
    style_value = e.appearance.get("style")
    color_value = e.appearance.get("color")
    ways_value = e.count.get("ways")
    layers_value = e.count.get("layers")
    angle_value = e.aim.get("base_angle")
    angle_step_value = e.aim.get("angle_step")
    speed_value = e.speed.get("first")
    speed_step_value = e.speed.get("step", e.speed.get("last_or_step", "0.0f"))
    start_opcode = 401 if e.fire_lines and e.raw and e.raw[0].opcode == 401 else 400
    lines = [f"// bullet lowering {e.family} -> {target}: slot backend; semantic verification required"]
    lines.append(f"ins_{start_opcode}({emitter_id});")
    lines.extend(emit_instruction_with_ranked_args(407, [emitter_id, aim_raw_value], ["0", "1"]))
    lines.extend(emit_instruction_with_ranked_args(402, [emitter_id, style_value, color_value], ["0", "0", "0"]))
    lines.extend(emit_instruction_with_ranked_args(406, [emitter_id, ways_value, layers_value], ["0", "1", "1"]))
    lines.extend(emit_instruction_with_ranked_args(404, [emitter_id, as_float_expr(angle_value if angle_value is not None else "0.0f"), as_float_expr(angle_step_value if angle_step_value is not None else "0.0f")], ["0", "0.0f", "0.0f"]))
    lines.extend(emit_instruction_with_ranked_args(405, [emitter_id, speed_value, speed_step_value], ["0", "1.0f", "0.0f"]))
    append_sound_lines(lines, target, e, str(emitter_id))
    for transform in e.transforms:
        if transform.raw_opcode == 409 and len(transform.raw_args) == 8:
            lines.append(f"ins_409({', '.join(str(arg) for arg in transform.raw_args)});")
        elif transform.raw_opcode in {509, 609, 610, 611, 612}:
            append_slot = "0" if transform.raw_opcode in {611, 612} else None
            lowered = lower_transform_opcode_to_instruction(e.game, target, transform.raw_opcode, transform.raw_args, append_slot)
            if lowered:
                lines.append(f"ins_{lowered.opcode}({', '.join(lowered.args)});")
            else:
                lines.append(f"// transform not representable in {target} slot backend: ins_{transform.raw_opcode}({', '.join(str(arg) for arg in transform.raw_args)});")
    if not e.fire_lines:
        lines.append(f"// source emitter had no explicit fire line; add ins_401({emitter_id}) at call site if needed")
    elif start_opcode != 401:
        lines.append(f"ins_401({emitter_id});")
    return "\n".join(lines)


def mode_raw(mode: str | None, default: str = "1") -> str:
    return {
        "aimed_fan": "0",
        "fan": "1",
        "aimed_ring": "2",
        "ring": "3",
        "offset_aimed_ring": "4",
        "offset_ring": "5",
        "random_angle": "6",
        "random_speed": "7",
        "random_angle_speed": "8",
    }.get(mode or "", default)
