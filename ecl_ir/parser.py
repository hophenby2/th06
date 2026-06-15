from __future__ import annotations

import re
from pathlib import Path

from .model import Function, Instruction, Program, Statement

FUNC_RE = re.compile(r"^\s*(?:void|sub)\s+(\w+)\s*\(([^)]*)\)\s*(?:\{|$)")
INS_RE = re.compile(r"\bins_(\d+)\s*\((.*)\)\s*;")
DIFF_RE = re.compile(r"^\s*!([ENHLOX0-7*]+)\s*(.*)$")

LABEL_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*:\s*(?://.*)?$")
TIME_RE = re.compile(r"^\s*\+(\d+)\s*:\s*(?://(.*))?$")
GOTO_RE = re.compile(r"^\s*goto\s+([A-Za-z_]\w*)\s*@\s*([^;]+)\s*;")
COND_GOTO_RE = re.compile(r"^\s*(if|unless)\s*\((.*)\)\s*goto\s+([A-Za-z_]\w*)\s*@\s*([^;]+)\s*;")
CALL_RE = re.compile(r"^\s*@([A-Za-z_]\w*)\s*\((.*)\)\s*(async(?:\s+[-+]?\d+)?)?\s*;")
RETURN_RE = re.compile(r"^\s*return\s*;")
VAR_RE = re.compile(r"^\s*var\s+(.+?)\s*;")
ASSIGN_RE = re.compile(r"^\s*((?:[%$][A-Za-z0-9_]+)|(?:\[-?\d+(?:\.0f)?\]))\s*=\s*(.+?)\s*;")
RESOURCE_RE = re.compile(r"^\s*(anim|ecli|timeline)\s*\{\s*$")
RESOURCE_INLINE_RE = re.compile(r"^\s*(anim|ecli|timeline)\s*\{(.*)\}\s*$")
PROTOTYPE_RE = re.compile(r"^\s*(?:void|sub)\s+(\w+)\s*\(([^)]*)\)\s*;")



def split_args(arg_text: str) -> list[str]:
    args: list[str] = []
    cur: list[str] = []
    depth = 0
    in_string = False
    escape = False
    for ch in arg_text:
        if in_string:
            cur.append(ch)
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            cur.append(ch)
        elif ch in "([{" :
            depth += 1
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        args.append(tail)
    return args


def parse_resource_entries(text: str) -> list[str]:
    quoted = re.findall(r'"([^"]+)"', text)
    if quoted:
        return quoted
    return [part.strip() for part in text.replace("\n", " ").split(";") if part.strip()]


def classify_statement(raw_line: str, line_no: int, difficulty: str | None = None) -> Statement:
    line = raw_line.strip()
    text = line.split("//", 1)[0].strip()
    if not text:
        return Statement("comment", raw_line.rstrip(), line_no, line, difficulty)
    if m := PROTOTYPE_RE.match(raw_line):
        return Statement("function_decl", raw_line.rstrip(), line_no, text, difficulty, {"function": m.group(1), "params": m.group(2).strip()})
    if m := TIME_RE.match(raw_line):
        return Statement("time", raw_line.rstrip(), line_no, text, difficulty, {"time": m.group(1), "comment": (m.group(2) or "").strip()})
    if m := LABEL_RE.match(raw_line):
        return Statement("label", raw_line.rstrip(), line_no, text, difficulty, {"name": m.group(1)})
    if m := COND_GOTO_RE.match(raw_line):
        return Statement("conditional_goto", raw_line.rstrip(), line_no, text, difficulty, {"condition_type": m.group(1), "condition": m.group(2).strip(), "label": m.group(3), "time": m.group(4).strip()})
    if m := GOTO_RE.match(raw_line):
        return Statement("goto", raw_line.rstrip(), line_no, text, difficulty, {"label": m.group(1), "time": m.group(2).strip()})
    if m := CALL_RE.match(raw_line):
        async_text = (m.group(3) or "").strip()
        attrs = {"function": m.group(1), "args": split_args(m.group(2))}
        if async_text:
            parts = async_text.split()
            if len(parts) > 1:
                attrs["async_slot"] = parts[1]
        return Statement("async_call" if async_text else "call", raw_line.rstrip(), line_no, text, difficulty, attrs)
    if RETURN_RE.match(raw_line):
        return Statement("return", raw_line.rstrip(), line_no, text, difficulty)
    if m := VAR_RE.match(raw_line):
        return Statement("var", raw_line.rstrip(), line_no, text, difficulty, {"vars": split_args(m.group(1))})
    if m := ASSIGN_RE.match(raw_line):
        return Statement("assign", raw_line.rstrip(), line_no, text, difficulty, {"target": m.group(1), "expr": m.group(2).strip()})
    if m := INS_RE.search(raw_line):
        return Statement("instruction", raw_line.rstrip(), line_no, text, difficulty, {"opcode": int(m.group(1)), "args": split_args(m.group(2))})
    return Statement("raw", raw_line.rstrip(), line_no, text, difficulty)


def is_difficulty_literal_statement(line: str, line_no: int = 0) -> bool:
    text = line.strip()
    if not text.endswith(";") or INS_RE.search(text):
        return False
    # Numeric/expression rank tables are raw expression statements like `90;` or `1.5f;`.
    # Real statements such as `@Foo() async;`, `goto`, assignments, returns, etc. must keep the rank marker.
    return classify_statement(text, line_no).kind == "raw"


def infer_game(path: str | Path) -> str:
    for part in Path(path).parts:
        if re.fullmatch(r"th(?:0[6-9]|1[0-8])", part):
            return part
    return "unknown"


def parse_decl(path: str | Path) -> Program:
    path = Path(path)
    program = Program(source=str(path), game=infer_game(path))
    current: Function | None = None
    pending_diff: str | None = None
    active_diff: str | None = None
    pending_literal_groups: list[dict[str, str]] = []
    current_literals: dict[str, str] = {}
    resource_name: str | None = None
    resource_lines: list[str] = []

    for line_no, raw_line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        line = raw_line.strip()

        if resource_name is not None:
            if line == "}":
                program.resources.setdefault(resource_name, []).extend(parse_resource_entries("\n".join(resource_lines)))
                resource_name = None
                resource_lines = []
            else:
                resource_lines.append(raw_line.rstrip())
            continue

        resource_inline_match = RESOURCE_INLINE_RE.match(raw_line)
        if current is None and resource_inline_match:
            program.resources.setdefault(resource_inline_match.group(1), []).extend(parse_resource_entries(resource_inline_match.group(2)))
            continue

        resource_match = RESOURCE_RE.match(raw_line)
        if current is None and resource_match:
            resource_name = resource_match.group(1)
            resource_lines = []
            continue

        diff_match = DIFF_RE.match(raw_line)
        statement_line = raw_line
        if diff_match:
            pending_diff = diff_match.group(1)
            line = diff_match.group(2).strip()
            statement_line = line
            if pending_diff == "*" and not line:
                if current_literals:
                    pending_literal_groups.append(current_literals)
                    current_literals = {}
                active_diff = None
                pending_diff = None
                continue
            if not line:
                active_diff = pending_diff
                continue
            if is_difficulty_literal_statement(line, line_no):
                if pending_diff in current_literals and current_literals:
                    pending_literal_groups.append(current_literals)
                    current_literals = {}
                current_literals[pending_diff] = line[:-1].strip()
                pending_diff = None
                continue
            active_diff = None
        elif pending_diff and is_difficulty_literal_statement(line, line_no):
            if pending_diff in current_literals and current_literals:
                pending_literal_groups.append(current_literals)
                current_literals = {}
            current_literals[pending_diff] = line[:-1].strip()
            active_diff = None
            pending_diff = None
            continue

        func_match = FUNC_RE.match(raw_line)
        if func_match:
            current = Function(func_match.group(1), func_match.group(2).strip())
            program.functions.append(current)
            pending_diff = None
            active_diff = None
            pending_literal_groups = []
            current_literals = {}
            continue

        if line == "{" and current is not None:
            continue

        if line == "}" and current is not None:
            current = None
            pending_diff = None
            active_diff = None
            pending_literal_groups = []
            current_literals = {}
            continue

        if not line:
            continue

        stmt_diff = pending_diff or active_diff
        stmt = classify_statement(statement_line, line_no, stmt_diff)
        if current is not None and pending_literal_groups:
            stmt.attrs["difficulty_literals"] = list(pending_literal_groups)
        if current is not None:
            current.statements.append(stmt)
        elif stmt.kind != "comment":
            program.top_level.append(stmt)

        ins_match = INS_RE.search(statement_line)
        if ins_match and current is not None:
            ins = Instruction(
                opcode=int(ins_match.group(1)),
                args=split_args(ins_match.group(2)),
                raw=raw_line.rstrip(),
                line_no=line_no,
                difficulty=stmt_diff,
                difficulty_literals=[*pending_literal_groups, current_literals] if current_literals else list(pending_literal_groups),
            )
            current.body.append(ins)
            if current.statements and current.statements[-1].kind == "instruction" and current.statements[-1].line_no == line_no:
                current.statements[-1].attrs["difficulty_literals"] = ins.difficulty_literals
            pending_diff = None
            pending_literal_groups = []
            current_literals = {}
        elif line and not line.startswith("!"):
            pending_diff = None
            pending_literal_groups = []
            current_literals = {}

    if resource_name is not None:
        program.resources.setdefault(resource_name, []).extend(parse_resource_entries("\n".join(resource_lines)))
    return program
