from __future__ import annotations

import re
from collections import Counter

from .model import Function, Program, Statement, TimelineOp

WAIT_OPS = {23, 24}


def lift_timelines(program: Program) -> list[TimelineOp]:
    objects: list[TimelineOp] = []
    for func in program.functions:
        if not func.statements:
            continue
        timeline = TimelineOp(program.game, func.name, func.statements[0].line_no, func.name)
        timeline.source = program.source
        timeline.fields = {
            "source": program.source,
            "statements": [statement_to_event(stmt) for stmt in func.statements],
            "labels": collect_labels(func),
            "calls": collect_calls(func),
            "variables": collect_variables(func),
            "control_flow": collect_control_flow(func),
            "loops": detect_loops(func),
            "waits": collect_waits(func),
        }
        timeline.unsupported = collect_raw_lines(func)
        objects.append(timeline)
    return objects


def statement_to_event(stmt: Statement) -> dict[str, object]:
    event = {
        "kind": stmt.kind,
        "line": stmt.line_no,
        "text": stmt.text,
        "difficulty": stmt.difficulty,
    }
    event.update(stmt.attrs)
    return event


def collect_labels(func: Function) -> dict[str, int]:
    labels: dict[str, int] = {}
    for stmt in func.statements:
        if stmt.kind == "label":
            labels[stmt.attrs["name"]] = stmt.line_no
    return labels


def collect_calls(func: Function) -> list[dict[str, object]]:
    calls: list[dict[str, object]] = []
    for stmt in func.statements:
        if stmt.kind in {"call", "async_call"}:
            calls.append({
                "kind": stmt.kind,
                "function": stmt.attrs.get("function"),
                "args": stmt.attrs.get("args", []),
                "line": stmt.line_no,
                "async": stmt.kind == "async_call",
            })
    return calls


def collect_variables(func: Function) -> dict[str, object]:
    declared: list[str] = []
    assigned: list[dict[str, str | int]] = []
    for stmt in func.statements:
        if stmt.kind == "var":
            declared.extend(str(var) for var in stmt.attrs.get("vars", []))
        elif stmt.kind == "assign":
            assigned.append({"target": stmt.attrs.get("target", ""), "expr": stmt.attrs.get("expr", ""), "line": stmt.line_no})
    return {"declared": declared, "assignments": assigned}


def collect_control_flow(func: Function) -> list[dict[str, object]]:
    flow: list[dict[str, object]] = []
    for stmt in func.statements:
        if stmt.kind in {"goto", "conditional_goto"}:
            flow.append({
                "kind": stmt.kind,
                "line": stmt.line_no,
                "label": stmt.attrs.get("label"),
                "time": stmt.attrs.get("time"),
                "condition_type": stmt.attrs.get("condition_type"),
                "condition": stmt.attrs.get("condition"),
            })
        elif stmt.kind == "return":
            flow.append({"kind": "return", "line": stmt.line_no})
    return flow


def collect_waits(func: Function) -> list[dict[str, object]]:
    waits: list[dict[str, object]] = []
    for ins in func.body:
        if ins.opcode in WAIT_OPS:
            waits.append({"opcode": ins.opcode, "frames": ins.args[0] if ins.args else "", "line": ins.line_no, "difficulty": ins.difficulty})
    return waits


def collect_raw_lines(func: Function) -> list[str]:
    raw: list[str] = []
    for stmt in func.statements:
        if stmt.kind == "raw":
            raw.append(f"line {stmt.line_no}: {stmt.raw.strip()}")
    return raw


def detect_loops(func: Function) -> list[dict[str, object]]:
    labels = collect_labels(func)
    loops: list[dict[str, object]] = []
    statement_index = {stmt.line_no: index for index, stmt in enumerate(func.statements)}
    for stmt in func.statements:
        if stmt.kind != "conditional_goto":
            continue
        label = str(stmt.attrs.get("label", ""))
        target_line = labels.get(label)
        if target_line is None or target_line >= stmt.line_no:
            continue
        cond = str(stmt.attrs.get("condition", ""))
        counter = extract_counter(cond)
        start_index = statement_index.get(target_line, 0)
        end_index = statement_index.get(stmt.line_no, start_index)
        body = func.statements[start_index + 1:end_index]
        loops.append({
            "kind": "counter_loop" if counter else "backedge_loop",
            "label": label,
            "start_line": target_line,
            "end_line": stmt.line_no,
            "time": stmt.attrs.get("time"),
            "condition_type": stmt.attrs.get("condition_type"),
            "condition": cond,
            "counter": counter,
            "body_statement_count": len(body),
            "body_kinds": dict(Counter(item.kind for item in body)),
        })
    return loops


def extract_counter(condition: str) -> str | None:
    for pattern in (r"([%$][A-Za-z0-9_]+)\s*--", r"--\s*([%$][A-Za-z0-9_]+)", r"([%$][A-Za-z0-9_]+)\s*[<>!=]=?"):
        match = re.search(pattern, condition)
        if match:
            return match.group(1)
    return None
