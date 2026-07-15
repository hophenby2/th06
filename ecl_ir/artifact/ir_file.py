from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..analysis.bullet_ir import analyze_bullet_module, bullet_analysis_summary
from ..canonical.semantic_ir import SemanticModule
from ..canonical.semantic_lifter import build_semantic_module, semantic_module_summary
from ..legacy.model import (
    AnimationOp,
    AutoBulletTimer,
    BossPattern,
    BossTimer,
    BulletEmitter,
    BulletTransform,
    EffectEmitter,
    EnemyOp,
    EnemyVisualOp,
    EntryAlias,
    FamiliarSpawner,
    FunctionRewrite,
    HelperRoutine,
    IRObject,
    LaserEmitter,
    ModeOp,
    MotionModifier,
    MovementOp,
    ResourcePlan,
    TimelineOp,
    TimelineRewrite,
    UnitFlagOp,
)
from ..legacy.object_lifter import lift_all_objects, summarize_by_kind
from ..source.model import Function, Instruction, Program, RoutineSignature, Statement
from ..source.parser import (
    SourceDecodeMode,
    SourceDocument,
    decode_source_bytes,
    detect_text_encoding,
    discover_sibling_routine_signatures,
    encode_source_text,
    parse_decl,
    parse_decl_bytes as parse_source_bytes,
    parse_decl_text as parse_source_text,
    split_source_text_lines,
)

SCHEMA_VERSION = 2


@dataclass(frozen=True)
class DeclTextCodec:
    """Serialization contract for generated thecl source, outside semantic IR."""

    encoding: str = "utf-8"
    decoding_mode: SourceDecodeMode = SourceDecodeMode.STRICT

    @classmethod
    def from_eclir(cls, data: dict[str, Any] | None) -> DeclTextCodec:
        data = data or {}
        source_decoding = (
            data.get("source_decoding")
            if isinstance(data.get("source_decoding"), dict)
            else {}
        )
        return cls(
            encoding=str(
                source_decoding.get("encoding")
                or data.get("source_encoding")
                or "utf-8"
            ),
            decoding_mode=SourceDecodeMode(
                str(
                    source_decoding.get("decoding_mode")
                    or SourceDecodeMode.STRICT.value
                )
            ),
        )

    @classmethod
    def from_source_bytes(cls, source_bytes: bytes) -> DeclTextCodec:
        document = SourceDocument.from_bytes(source_bytes)
        return cls(document.encoding, document.decoding_mode)

    def encode(self, text: str) -> bytes:
        return encode_source_text(text, self.encoding, self.decoding_mode)

IR_CLASS_BY_KIND = {
    "Animation": AnimationOp,
    "AutoBulletTimer": AutoBulletTimer,
    "BossPattern": BossPattern,
    "BossTimer": BossTimer,
    "BulletEmitter": BulletEmitter,
    "EffectEmitter": EffectEmitter,
    "Enemy": EnemyOp,
    "EnemyVisual": EnemyVisualOp,
    "EntryAlias": EntryAlias,
    "FamiliarSpawner": FamiliarSpawner,
    "FunctionRewrite": FunctionRewrite,
    "HelperRoutine": HelperRoutine,
    "IRObject": IRObject,
    "LaserEmitter": LaserEmitter,
    "Mode": ModeOp,
    "MotionModifier": MotionModifier,
    "Movement": MovementOp,
    "ResourcePlan": ResourcePlan,
    "Timeline": TimelineOp,
    "TimelineRewrite": TimelineRewrite,
    "UnitFlag": UnitFlagOp,
}


def instruction_to_dict(ins: Instruction) -> dict[str, Any]:
    return ins.to_dict()


def instruction_from_dict(data: dict[str, Any]) -> Instruction:
    return Instruction(
        opcode=int(data.get("opcode", 0)),
        args=[str(arg) for arg in data.get("args", [])],
        raw=str(data.get("raw", "")),
        line_no=int(data.get("line_no", 0)),
        difficulty=data.get("difficulty"),
        difficulty_literals=data.get("difficulty_literals", {}),
    )


def statement_to_dict(stmt: Statement) -> dict[str, Any]:
    return stmt.to_dict()


def statement_from_dict(data: dict[str, Any]) -> Statement:
    return Statement(
        kind=str(data.get("kind", "raw")),
        raw=str(data.get("raw", "")),
        line_no=int(data.get("line_no", 0)),
        text=str(data.get("text", "")),
        difficulty=data.get("difficulty"),
        attrs=dict(data.get("attrs", {}) or {}),
    )


def function_to_dict(func: Function) -> dict[str, Any]:
    return {
        "name": func.name,
        "params": func.params,
        "statements": [statement_to_dict(stmt) for stmt in func.statements],
        "body": [instruction_to_dict(ins) for ins in func.body],
    }


def function_from_dict(data: dict[str, Any]) -> Function:
    return Function(
        name=str(data.get("name", "")),
        params=str(data.get("params", "")),
        statements=[statement_from_dict(stmt) for stmt in data.get("statements", [])],
        body=[instruction_from_dict(ins) for ins in data.get("body", [])],
    )


def program_to_dict(program: Program) -> dict[str, Any]:
    return {
        "source": program.source,
        "game": program.game,
        "resources": program.resources,
        "top_level": [statement_to_dict(stmt) for stmt in program.top_level],
        "functions": [function_to_dict(func) for func in program.functions],
        "routine_signatures": [signature.to_dict() for signature in program.routine_signatures],
    }


def program_from_dict(data: dict[str, Any]) -> Program:
    return Program(
        source=str(data.get("source", "")),
        game=str(data.get("game", "")),
        resources={str(key): [str(item) for item in value] for key, value in (data.get("resources", {}) or {}).items()},
        top_level=[statement_from_dict(stmt) for stmt in data.get("top_level", [])],
        functions=[function_from_dict(func) for func in data.get("functions", [])],
        routine_signatures=[RoutineSignature.from_dict(item) for item in data.get("routine_signatures", [])],
    )


def program_source_structure(program: Program) -> dict[str, Any]:
    """Program fields that must agree with reparsing the stored source bytes."""

    data = program_to_dict(program)
    data.pop("routine_signatures", None)
    return data


def bullet_transform_from_dict(data: dict[str, Any]) -> BulletTransform:
    return BulletTransform(
        index=str(data.get("index", "0")),
        channel=str(data.get("channel", "0")),
        action_type=str(data.get("action_type", "customRaw")),
        raw_opcode=int(data.get("raw_opcode", 0)),
        raw_args=list(data.get("raw_args", []) or []),
        difficulty=data.get("difficulty"),
        semantics=dict(data.get("semantics", {}) or {}),
    )


def object_to_dict(obj: object) -> dict[str, Any]:
    data = obj.to_dict() if hasattr(obj, "to_dict") else dict(getattr(obj, "__dict__", {}))
    if hasattr(obj, "source"):
        data["source"] = str(getattr(obj, "source"))
    return data


def object_from_dict(data: dict[str, Any]) -> object:
    kind = str(data.get("kind", "IRObject"))
    if kind == "BulletEmitter":
        emitter = BulletEmitter(
            str(data.get("game", "")),
            str(data.get("function", "")),
            int(data.get("source_line", 0)),
            str(data.get("id", "0")),
            str(data.get("family", "unknown")),
        )
        for name in ("origin", "appearance", "aim", "count", "speed", "sound", "flags", "semantics"):
            setattr(emitter, name, dict(data.get(name, {}) or {}))
        emitter.transforms = [bullet_transform_from_dict(item) for item in data.get("transforms", [])]
        emitter.fire_lines = [int(item) for item in data.get("fire_lines", [])]
        emitter.raw = [instruction_from_dict(item) for item in data.get("raw", [])]
        emitter.unsupported = [str(item) for item in data.get("unsupported", [])]
        if "source" in data:
            emitter.source = str(data.get("source", ""))
        return emitter

    cls = IR_CLASS_BY_KIND.get(kind, IRObject)
    if cls is IRObject:
        obj = IRObject(kind, str(data.get("game", "")), str(data.get("function", "")), int(data.get("source_line", 0)), str(data.get("id", "0")), str(data.get("family", "unknown")))
    else:
        obj = cls(str(data.get("game", "")), str(data.get("function", "")), int(data.get("source_line", 0)), str(data.get("id", "0")), str(data.get("family", "unknown")))
    obj.fields = dict(data.get("fields", {}) or {})
    obj.raw = [instruction_from_dict(item) for item in data.get("raw", [])]
    obj.unsupported = [str(item) for item in data.get("unsupported", [])]
    if "source" in data:
        obj.source = str(data.get("source", ""))
    return obj


FUNC_HEADER_RE = re.compile(r"^\s*(?:void|sub)\s+(\w+)\s*\(([^)]*)\)\s*(\{)?\s*(?://.*)?$")
RESOURCE_START_RE = re.compile(r"^\s*(anim|ecli|timeline)\s*\{")


def split_source_lines(source_bytes: bytes) -> list[str]:
    source_text, _encoding = decode_source_bytes(source_bytes)
    return split_source_text_lines(source_text, keepends=True)


def line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\\r\\n"
    if line.endswith("\n"):
        return "\\n"
    if line.endswith("\r"):
        return "\\r"
    return ""


def line_without_ending(line: str) -> str:
    return line[:-2] if line.endswith("\r\n") else line[:-1] if line.endswith(("\n", "\r")) else line


def build_source_layout(source_bytes: bytes) -> dict[str, Any]:
    source_document = SourceDocument.from_bytes(source_bytes)
    lines = split_source_text_lines(source_document.text, keepends=True)
    items: list[dict[str, Any]] = []
    resource_stack: dict[str, Any] | None = None
    current_function: dict[str, Any] | None = None
    pending_function: dict[str, Any] | None = None
    brace_depth = 0
    for index, physical_line in enumerate(lines, 1):
        body = line_without_ending(physical_line)
        stripped = body.strip()
        item: dict[str, Any] = {"line_no": index, "raw": body, "ending": line_ending(physical_line)}

        if resource_stack is not None:
            item["kind"] = "resource_line"
            item["resource"] = resource_stack["name"]
            if stripped == "}":
                item["kind"] = "resource_end"
                resource_stack = None
            items.append(item)
            continue

        if current_function is not None:
            item["function"] = current_function["name"]
            if stripped == "{" and brace_depth == 0:
                item["kind"] = "function_open"
                brace_depth = 1
                items.append(item)
                continue
            if stripped == "}" and brace_depth <= 1:
                item["kind"] = "function_end"
                current_function["end_line"] = index
                current_function = None
                brace_depth = 0
                items.append(item)
                continue
            if "{" in stripped:
                brace_depth += stripped.count("{")
            if "}" in stripped:
                brace_depth = max(1, brace_depth - stripped.count("}"))
            item["kind"] = classify_layout_line(stripped)
            items.append(item)
            continue

        match = FUNC_HEADER_RE.match(body)
        if match:
            item["kind"] = "function_header"
            item["function"] = match.group(1)
            item["params"] = match.group(2).strip()
            item["header_has_open_brace"] = bool(match.group(3))
            current_function = {"name": match.group(1), "start_line": index, "params": match.group(2).strip()}
            brace_depth = 1 if match.group(3) else 0
            pending_function = None if match.group(3) else current_function
            items.append(item)
            continue

        if pending_function is not None and stripped == "{":
            item["kind"] = "function_open"
            item["function"] = pending_function["name"]
            current_function = pending_function
            pending_function = None
            brace_depth = 1
            items.append(item)
            continue

        resource_match = RESOURCE_START_RE.match(body)
        if resource_match:
            item["kind"] = "resource_inline" if "}" in stripped else "resource_start"
            item["resource"] = resource_match.group(1)
            if item["kind"] == "resource_start":
                resource_stack = {"name": resource_match.group(1)}
            items.append(item)
            continue

        item["kind"] = classify_layout_line(stripped)
        items.append(item)
    return {**source_document.metadata(), "line_count": len(lines), "items": items}


def classify_layout_line(stripped: str) -> str:
    if not stripped:
        return "blank"
    if stripped.startswith("//"):
        return "comment"
    if stripped.startswith("!"):
        return "difficulty"
    if stripped.startswith("+") and stripped.endswith(":"):
        return "time_label"
    if stripped.endswith(":"):
        return "label"
    if stripped.startswith("var "):
        return "var"
    if stripped.startswith("@"): 
        return "call"
    if stripped.startswith(("goto ", "if ", "unless ")):
        return "branch"
    if stripped.startswith("return"):
        return "return"
    if "ins_" in stripped:
        return "instruction"
    if "=" in stripped and stripped.endswith(";"):
        return "assign"
    return "raw"


def emit_layout_source(data: dict[str, Any]) -> str | None:
    layout = data.get("source_layout")
    if not isinstance(layout, dict):
        return None
    items = layout.get("items")
    if not isinstance(items, list):
        return None
    return "".join(str(item.get("raw", "")) + decode_line_ending(str(item.get("ending", ""))) for item in items)


def decode_line_ending(value: str) -> str:
    return {"\\r\\n": "\r\n", "\\n": "\n", "\\r": "\r"}.get(value, value)


def build_eclir(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    source_bytes = path.read_bytes()
    source_document = SourceDocument.from_bytes(source_bytes)
    program = parse_source_text(source_document.text, str(path))
    program.routine_signatures = discover_sibling_routine_signatures(program, path)
    canonical_ir = build_semantic_module(program)
    bullet_analysis = analyze_bullet_module(canonical_ir)
    objects = lift_all_objects(program)
    return {
        "schema": "th062.eclir",
        "schema_version": SCHEMA_VERSION,
        "source_bytes_base64": base64.b64encode(source_bytes).decode("ascii"),
        "source_text": source_document.text,
        "source_encoding": source_document.encoding,
        "source_decoding": source_document.metadata(),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_layout": build_source_layout(source_bytes),
        "program": program_to_dict(program),
        "canonical_ir": canonical_ir.to_dict(),
        "canonical_summary": semantic_module_summary(canonical_ir),
        "analysis_projections": {"bullet_manager": bullet_analysis.to_dict()},
        "analysis_summary": {"bullet_manager": bullet_analysis_summary(bullet_analysis)},
        "summary": summarize_by_kind(objects),
        "objects": [object_to_dict(obj) for obj in objects],
    }


def load_eclir(path: str | Path) -> tuple[Program, list[object], dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "th062.eclir":
        raise ValueError(f"not a th062.eclir file: {path}")
    program = program_from_dict(data.get("program", {}) or {})
    canonical_data = data.get("canonical_ir")
    if not program.routine_signatures and isinstance(canonical_data, dict):
        program.routine_signatures = list(SemanticModule.from_dict(canonical_data).routine_signatures)
    objects = [object_from_dict(item) for item in data.get("objects", [])]
    return program, objects, data


def dump_eclir(path: str | Path, data: dict[str, Any]) -> None:
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def emit_eclir_json(path: str | Path) -> str:
    return json.dumps(build_eclir(path), ensure_ascii=False, indent=2)


def emit_layout_roundtrip_source(data: dict[str, Any]) -> str | None:
    return emit_layout_source(data)


def emit_layout_roundtrip_bytes(data: dict[str, Any]) -> bytes | None:
    text = emit_layout_source(data)
    if text is None:
        return None
    layout = data.get("source_layout") if isinstance(data.get("source_layout"), dict) else {}
    source_decoding = data.get("source_decoding") if isinstance(data.get("source_decoding"), dict) else {}
    encoding = str(
        layout.get("encoding") or source_decoding.get("encoding") or data.get("source_encoding") or "utf-8"
    )
    decoding_mode = str(
        layout.get("decoding_mode")
        or source_decoding.get("decoding_mode")
        or SourceDecodeMode.STRICT.value
    )
    return encode_source_text(text, encoding, decoding_mode)


def emit_roundtrip_bytes(program: Program, data: dict[str, Any] | None = None, canonical: bool = False) -> bytes:
    if data and not canonical and isinstance(data.get("source_bytes_base64"), str):
        return base64.b64decode(data["source_bytes_base64"])
    output = emit_roundtrip_source(program, data if canonical else None, canonical=True)
    return DeclTextCodec.from_eclir(data).encode(output)


def emit_roundtrip_source(program: Program, data: dict[str, Any] | None = None, canonical: bool = False) -> str:
    if data and not canonical and isinstance(data.get("source_text"), str):
        text = data["source_text"]
        return text if text.endswith("\n") else text + "\n"
    lines: list[str] = []
    for resource, entries in program.resources.items():
        quoted = "; ".join(f'"{entry}"' for entry in entries)
        lines.append(f"{resource} {{ {quoted}; }}")
    for stmt in program.top_level:
        raw = stmt.raw.strip()
        if raw and not raw.startswith(("anim", "ecli", "timeline")):
            lines.append(raw)
    for func in program.functions:
        if lines and lines[-1] != "":
            lines.append("")
        header = f"void {func.name}({func.params})" if func.params else f"void {func.name}()"
        lines.extend([header, "{"])
        if func.statements:
            for stmt in func.statements:
                raw = stmt.raw.rstrip()
                if not raw:
                    continue
                lines.append(raw if raw.startswith(("!", "+", "-")) or raw.endswith(":") else f"    {raw.strip()}")
        else:
            for ins in func.body:
                raw = ins.raw.rstrip()
                lines.append(raw if raw.startswith("!") else f"    {raw.strip()}")
        lines.append("}")
    return "\n".join(lines) + "\n"


def validate_eclir_data(data: dict[str, Any]) -> dict[str, Any]:
    program = program_from_dict(data.get("program", {}) or {})
    source_text = data.get("source_text")
    source_bytes_base64 = data.get("source_bytes_base64")
    result: dict[str, Any] = {
        "schema": data.get("schema"),
        "schema_version": data.get("schema_version"),
        "game": program.game,
        "functions": len(program.functions),
        "instructions": sum(len(func.body) for func in program.functions),
        "routine_signatures": len(program.routine_signatures),
        "resources": {key: len(value) for key, value in program.resources.items()},
        "objects": len(data.get("objects", []) or []),
        "ok": True,
        "warnings": [],
    }
    canonical_data = data.get("canonical_ir")
    invalid_owners = invalid_canonical_owners(canonical_data) if isinstance(canonical_data, dict) else []
    if invalid_owners:
        result["ok"] = False
        result["warnings"].append(
            "canonical IR contains invalid lowering owner values: "
            + ", ".join(sorted(set(invalid_owners)))
        )
    if isinstance(canonical_data, dict) and not invalid_owners:
        canonical_ir = SemanticModule.from_dict(canonical_data)
        canonical_summary = semantic_module_summary(canonical_ir)
        result["canonical_ir"] = canonical_summary
        expected_canonical_ir = build_semantic_module(program)
        if canonical_ir.to_dict() != expected_canonical_ir.to_dict():
            result["ok"] = False
            result["warnings"].append("canonical IR content differs from Program-derived canonical IR")
        stored_canonical_summary = data.get("canonical_summary")
        if isinstance(stored_canonical_summary, dict) and stored_canonical_summary != canonical_summary:
            result["ok"] = False
            result["warnings"].append("canonical summary differs from canonical IR")
        canonical_instruction_count = canonical_summary["semantic_ops"] + canonical_summary["raw_instruction_ops"]
        if len(canonical_ir.routines) != len(program.functions):
            result["ok"] = False
            result["warnings"].append("canonical IR routine count differs from Program IR")
        if canonical_instruction_count != result["instructions"]:
            result["ok"] = False
            result["warnings"].append("canonical IR instruction effect count differs from Program IR")
        if canonical_ir.routine_signatures != program.routine_signatures:
            result["ok"] = False
            result["warnings"].append("canonical IR routine signatures differ from Program IR")
        canonical_node_ids = {
            str(node.node_id)
            for routine in canonical_ir.routines
            for node in routine.body
        }
        all_canonical_nodes = [
            *canonical_ir.top_level,
            *(node for routine in canonical_ir.routines for node in routine.body),
        ]
        canonical_node_id_list = [str(node.node_id) for node in all_canonical_nodes]
        if any(not node_id for node_id in canonical_node_id_list):
            result["ok"] = False
            result["warnings"].append("canonical IR contains an empty NodeId")
        if len(canonical_node_id_list) != len(set(canonical_node_id_list)):
            result["ok"] = False
            result["warnings"].append("canonical IR contains duplicate NodeIds")
        expected_owners = {
            "semantic_operation": "semantic",
            "raw_instruction": "raw",
            "syntax_statement": "syntax",
        }
        wrong_owners = [
            str(node.node_id)
            for node in all_canonical_nodes
            if node.ownership.owner.value != expected_owners.get(node.node, node.ownership.owner.value)
        ]
        if wrong_owners:
            result["ok"] = False
            result["warnings"].append(
                f"canonical IR contains {len(wrong_owners)} nodes with invalid lowering ownership"
            )
        projections = data.get("analysis_projections")
        bullet_projection = projections.get("bullet_manager") if isinstance(projections, dict) else None
        if isinstance(bullet_projection, dict):
            action_node_ids = {
                str(action.get("source_node_id", ""))
                for routine in bullet_projection.get("routines", [])
                if isinstance(routine, dict)
                for action in routine.get("actions", [])
                if isinstance(action, dict)
            }
            unknown_node_ids = sorted(action_node_ids - canonical_node_ids)
            result["bullet_analysis_actions"] = sum(
                len(routine.get("actions", []))
                for routine in bullet_projection.get("routines", [])
                if isinstance(routine, dict)
            )
            if unknown_node_ids:
                result["ok"] = False
                result["warnings"].append(
                    f"bullet analysis references {len(unknown_node_ids)} unknown canonical node ids"
                )
    elif int(data.get("schema_version", 1) or 1) >= 2 and not invalid_owners:
        result["ok"] = False
        result["warnings"].append("schema v2 IR is missing canonical_ir")
    else:
        result["warnings"].append("schema v1 IR has no canonical effect layer")
    reparsed: Program | None = None
    if isinstance(source_bytes_base64, str):
        source_bytes = base64.b64decode(source_bytes_base64)
        digest = hashlib.sha256(source_bytes).hexdigest()
        result["source_sha256_actual"] = digest
        result["source_sha256_expected"] = data.get("source_sha256")
        if data.get("source_sha256") and digest != data.get("source_sha256"):
            result["ok"] = False
            result["warnings"].append("source_bytes sha256 mismatch")
        layout_bytes = emit_layout_roundtrip_bytes(data)
        if layout_bytes is not None:
            layout_digest = hashlib.sha256(layout_bytes).hexdigest()
            result["source_layout_sha256_actual"] = layout_digest
            if layout_digest != digest:
                result["ok"] = False
                result["warnings"].append("source_layout reconstruction differs from source bytes")
        reparsed = parse_decl_bytes(source_bytes, str(data.get("program", {}).get("source", "<eclir>")))
    elif isinstance(source_text, str):
        digest = hashlib.sha256(DeclTextCodec.from_eclir(data).encode(source_text)).hexdigest()
        result["source_sha256_actual"] = digest
        result["source_sha256_expected"] = data.get("source_sha256")
        if data.get("source_sha256") and digest != data.get("source_sha256"):
            result["ok"] = False
            result["warnings"].append("source_text sha256 mismatch")
        reparsed = parse_decl_text(source_text, str(data.get("program", {}).get("source", "<eclir>")))
        result["warnings"].append("source_bytes_base64 missing; exact byte roundtrip is unavailable")
    else:
        result["warnings"].append("source_text/source_bytes missing; roundtrip will be canonical only")
    if reparsed is not None:
        if program_source_structure(reparsed) != program_source_structure(program):
            result["ok"] = False
            result["warnings"].append("Program IR content differs from reparsed source")
        if len(reparsed.functions) != len(program.functions):
            result["ok"] = False
            result["warnings"].append(f"function count mismatch source={len(reparsed.functions)} program={len(program.functions)}")
        if sum(len(func.body) for func in reparsed.functions) != result["instructions"]:
            result["ok"] = False
            result["warnings"].append("instruction count mismatch between source and program")
    return result


def invalid_canonical_owners(canonical_data: dict[str, Any]) -> list[str]:
    valid = {"semantic", "raw", "syntax", "pattern"}
    nodes = [
        *canonical_data.get("top_level", []),
        *(
            node
            for routine in canonical_data.get("routines", [])
            if isinstance(routine, dict)
            for node in routine.get("body", [])
        ),
    ]
    return [
        str(owner)
        for node in nodes
        if isinstance(node, dict)
        and isinstance(node.get("ownership"), dict)
        and "owner" in node["ownership"]
        and (owner := node["ownership"].get("owner")) not in valid
    ]


def parse_decl_text(source_text: str, source_name: str) -> Program:
    return parse_source_text(source_text, source_name)


def parse_decl_bytes(source_bytes: bytes, source_name: str) -> Program:
    return parse_source_bytes(source_bytes, source_name)
