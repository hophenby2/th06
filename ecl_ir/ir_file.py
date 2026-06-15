from __future__ import annotations

import json
from dataclasses import fields
from pathlib import Path
from typing import Any

from .model import (
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
    Function,
    FunctionRewrite,
    HelperRoutine,
    IRObject,
    Instruction,
    LaserEmitter,
    ModeOp,
    MotionModifier,
    MovementOp,
    Program,
    ResourcePlan,
    Statement,
    TimelineOp,
    TimelineRewrite,
    UnitFlagOp,
)
from .object_lifter import lift_all_objects, summarize_by_kind
from .parser import parse_decl

SCHEMA_VERSION = 1

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
    }


def program_from_dict(data: dict[str, Any]) -> Program:
    return Program(
        source=str(data.get("source", "")),
        game=str(data.get("game", "")),
        resources={str(key): [str(item) for item in value] for key, value in (data.get("resources", {}) or {}).items()},
        top_level=[statement_from_dict(stmt) for stmt in data.get("top_level", [])],
        functions=[function_from_dict(func) for func in data.get("functions", [])],
    )


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
    return obj.to_dict() if hasattr(obj, "to_dict") else dict(getattr(obj, "__dict__", {}))


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
        return emitter

    cls = IR_CLASS_BY_KIND.get(kind, IRObject)
    if cls is IRObject:
        obj = IRObject(kind, str(data.get("game", "")), str(data.get("function", "")), int(data.get("source_line", 0)), str(data.get("id", "0")), str(data.get("family", "unknown")))
    else:
        obj = cls(str(data.get("game", "")), str(data.get("function", "")), int(data.get("source_line", 0)), str(data.get("id", "0")), str(data.get("family", "unknown")))
    obj.fields = dict(data.get("fields", {}) or {})
    obj.raw = [instruction_from_dict(item) for item in data.get("raw", [])]
    obj.unsupported = [str(item) for item in data.get("unsupported", [])]
    return obj


def build_eclir(path: str | Path) -> dict[str, Any]:
    program = parse_decl(str(path))
    objects = lift_all_objects(program)
    return {
        "schema": "th062.eclir",
        "schema_version": SCHEMA_VERSION,
        "program": program_to_dict(program),
        "summary": summarize_by_kind(objects),
        "objects": [object_to_dict(obj) for obj in objects],
    }


def load_eclir(path: str | Path) -> tuple[Program, list[object], dict[str, Any]]:
    data = json.loads(Path(path).read_text())
    if data.get("schema") != "th062.eclir":
        raise ValueError(f"not a th062.eclir file: {path}")
    program = program_from_dict(data.get("program", {}) or {})
    objects = [object_from_dict(item) for item in data.get("objects", [])]
    return program, objects, data


def dump_eclir(path: str | Path, data: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def emit_eclir_json(path: str | Path) -> str:
    return json.dumps(build_eclir(path), ensure_ascii=False, indent=2)


def emit_roundtrip_source(program: Program) -> str:
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
