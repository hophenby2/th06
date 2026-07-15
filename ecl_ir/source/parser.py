from __future__ import annotations

import codecs
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from ..dialects.game_ids import KNOWN_GAME_IDS, normalize_game_id
from .model import Function, Instruction, Program, RoutineSignature, Statement

FUNC_RE = re.compile(r"^\s*(?:void|sub)\s+(\w+)\s*\(([^)]*)\)\s*(?:\{|$)")
INS_RE = re.compile(r"\bins_(\d+)\s*\((.*)\)\s*;")
DIFF_RE = re.compile(r"^\s*!([ENHLOX0-7*]+)\s*(:)?\s*(.*)$")

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
TIMELINE_DECL_RE = re.compile(r"^\s*timeline\s+(\w+)\s*\(\s*\)")

UTF8_BOM = b"\xef\xbb\xbf"
SOURCE_ENCODINGS = ("utf-8", "cp932", "shift_jis")
# CP932 cannot decode to the supplementary private-use planes, so these codepoints
# can carry individual source bytes through JSON without colliding with valid text.
BYTE_ESCAPE_BASE = 0xF0000
BYTE_ESCAPE_ERROR_HANDLER = "th062_private_use_byte_escape"
BYTE_ESCAPE_SCOPE_DECODE_ERRORS = "decode_errors"
BYTE_ESCAPE_SCOPE_ALL_NON_ASCII = "all_non_ascii_bytes"
SIGNATURE_DISCOVERY_GAMES = {
    "th13", "th14", "th143", "th15", "th16", "th165", "th17", "th18", "th185"
}


class SourceDecodeMode(str, Enum):
    STRICT = "strict"
    PRIVATE_USE_BYTE_ESCAPE = "private_use_byte_escape"


def _escape_invalid_source_bytes(error: UnicodeError) -> tuple[str, int]:
    if not isinstance(error, UnicodeDecodeError):
        raise error
    escaped = "".join(chr(BYTE_ESCAPE_BASE + byte) for byte in error.object[error.start:error.end])
    return escaped, error.end


codecs.register_error(BYTE_ESCAPE_ERROR_HANDLER, _escape_invalid_source_bytes)


def _detect_strict_text_encoding(source_bytes: bytes) -> str | None:
    if source_bytes.startswith(UTF8_BOM):
        try:
            source_bytes.decode("utf-8-sig")
            return "utf-8-sig"
        except UnicodeDecodeError:
            return None

    for encoding in SOURCE_ENCODINGS:
        try:
            source_bytes.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return None


def _escape_all_non_ascii_bytes(source_bytes: bytes, encoding: str) -> str:
    body = (
        source_bytes[len(UTF8_BOM):]
        if encoding == "utf-8-sig" and source_bytes.startswith(UTF8_BOM)
        else source_bytes
    )
    return "".join(chr(byte) if byte < 0x80 else chr(BYTE_ESCAPE_BASE + byte) for byte in body)


def _encode_private_use_byte_escaped_text(text: str, encoding: str) -> bytes:
    codec = "utf-8" if encoding == "utf-8-sig" else encoding
    output = bytearray(UTF8_BOM if encoding == "utf-8-sig" else b"")
    chunk: list[str] = []

    def flush_chunk() -> None:
        if chunk:
            output.extend("".join(chunk).encode(codec))
            chunk.clear()

    for char in text:
        codepoint = ord(char)
        if BYTE_ESCAPE_BASE <= codepoint <= BYTE_ESCAPE_BASE + 0xFF:
            flush_chunk()
            output.append(codepoint - BYTE_ESCAPE_BASE)
        else:
            chunk.append(char)
    flush_chunk()
    return bytes(output)


def split_source_text_lines(text: str, keepends: bool = False) -> list[str]:
    """Split physical source lines without treating in-string controls as newlines."""

    if "\n" not in text:
        parts = text.split("\r")
        if not keepends:
            return parts
        return [
            part + ("\r" if index < len(parts) - 1 else "")
            for index, part in enumerate(parts)
        ]

    parts = text.split("\n")
    lines: list[str] = []
    for index, part in enumerate(parts):
        if index == len(parts) - 1:
            if part:
                lines.append(part)
            continue
        if part.endswith("\r"):
            body = part[:-1]
            ending = "\r\n"
        else:
            body = part
            ending = "\n"
        lines.append(body + ending if keepends else body)
    return lines


@dataclass(frozen=True)
class SourceDocument:
    """Decoded source and the codec metadata required for byte-exact recovery."""

    source_bytes: bytes
    text: str
    encoding: str
    decoding_mode: SourceDecodeMode
    byte_escape_scope: str | None = None

    @classmethod
    def from_bytes(cls, source_bytes: bytes) -> SourceDocument:
        encoding = _detect_strict_text_encoding(source_bytes)
        if encoding is not None:
            text = source_bytes.decode(encoding)
            if text.encode(encoding) == source_bytes:
                return cls(source_bytes, text, encoding, SourceDecodeMode.STRICT)
            return cls(
                source_bytes,
                _escape_all_non_ascii_bytes(source_bytes, encoding),
                encoding,
                SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE,
                BYTE_ESCAPE_SCOPE_ALL_NON_ASCII,
            )

        encoding = "utf-8-sig" if source_bytes.startswith(UTF8_BOM) else "cp932"
        text = source_bytes.decode(encoding, errors=BYTE_ESCAPE_ERROR_HANDLER)
        document = cls(
            source_bytes,
            text,
            encoding,
            SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE,
            BYTE_ESCAPE_SCOPE_DECODE_ERRORS,
        )
        if _encode_private_use_byte_escaped_text(document.text, document.encoding) == source_bytes:
            return document
        return cls(
            source_bytes,
            _escape_all_non_ascii_bytes(source_bytes, encoding),
            encoding,
            SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE,
            BYTE_ESCAPE_SCOPE_ALL_NON_ASCII,
        )

    def metadata(self) -> dict[str, str]:
        metadata = {"encoding": self.encoding, "decoding_mode": self.decoding_mode.value}
        if self.decoding_mode is SourceDecodeMode.PRIVATE_USE_BYTE_ESCAPE:
            metadata["byte_escape_base"] = f"U+{BYTE_ESCAPE_BASE:05X}"
            metadata["byte_escape_scope"] = str(self.byte_escape_scope or BYTE_ESCAPE_SCOPE_DECODE_ERRORS)
        return metadata


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


def annotate_top_level_dialect_regions(statements: list[Statement]) -> None:
    """Attach structural membership to legacy top-level dialect blocks."""

    index = 0
    while index < len(statements):
        match = TIMELINE_DECL_RE.match(statements[index].text)
        if match is None:
            index += 1
            continue
        start = index
        depth = 0
        saw_open = False
        index += 1
        while index < len(statements):
            text = statements[index].text
            depth += text.count("{") - text.count("}")
            saw_open = saw_open or "{" in text
            index += 1
            if saw_open and depth <= 0:
                break
        members = statements[start:index]
        for member_index, statement in enumerate(members):
            statement.attrs["dialect_region"] = {
                "kind": "timeline",
                "name": match.group(1),
                "member_index": member_index,
                "member_count": len(members),
            }


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


@dataclass(frozen=True)
class DifficultySelectionCandidate:
    """A closed rank-value prefix assigned to the next source statement."""

    literal_lines: tuple[int, ...]
    consumer_line: int


def _next_significant_line(lines: list[str], start: int) -> int | None:
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if stripped and not stripped.startswith("//"):
            return index
    return None


def find_difficulty_selection_candidates(source_text: str) -> tuple[DifficultySelectionCandidate, ...]:
    """Find complete, uninterrupted thecl rank-switch tables and their consumer."""

    lines = split_source_text_lines(source_text)
    candidates: list[DifficultySelectionCandidate] = []
    index = 0
    while index < len(lines):
        first = DIFF_RE.match(lines[index])
        if first is None or first.group(1) == "*" or first.group(2) is not None:
            index += 1
            continue

        cursor = index
        literal_lines: list[int] = []
        reset_index: int | None = None
        consumer_index: int | None = None
        consumer_text = ""
        while True:
            marker = DIFF_RE.match(lines[cursor])
            if marker is None or marker.group(1) == "*" or marker.group(2) is not None:
                break
            inline_expression = marker.group(3).strip()
            if inline_expression:
                expression_index = cursor
                expression_text = inline_expression
                next_index = cursor + 1
            else:
                expression_index = _next_significant_line(lines, cursor + 1)
                if expression_index is None:
                    break
                expression_text = lines[expression_index].strip()
                next_index = expression_index + 1
            if not is_difficulty_literal_statement(expression_text, expression_index + 1):
                break
            literal_lines.append(expression_index + 1)

            next_marker_index = _next_significant_line(lines, next_index)
            if next_marker_index is None:
                break
            next_marker = DIFF_RE.match(lines[next_marker_index])
            if next_marker is None or next_marker.group(2) is not None:
                break
            if next_marker.group(1) != "*":
                cursor = next_marker_index
                continue

            reset_index = next_marker_index
            inline_consumer = next_marker.group(3).strip()
            if inline_consumer:
                consumer_index = reset_index
                consumer_text = inline_consumer
            else:
                consumer_index = _next_significant_line(lines, reset_index + 1)
                if consumer_index is not None:
                    consumer_text = lines[consumer_index].strip()
            break

        if (
            literal_lines
            and reset_index is not None
            and consumer_index is not None
            and bool(consumer_text)
        ):
            candidates.append(
                DifficultySelectionCandidate(tuple(literal_lines), consumer_index + 1)
            )
            index = reset_index + 1
        else:
            index += 1
    return tuple(candidates)


def infer_game(path: str | Path) -> str:
    for part in Path(path).parts:
        normalized = normalize_game_id(part)
        if normalized in KNOWN_GAME_IDS:
            return normalized
    return "unknown"


def detect_text_encoding(source_bytes: bytes) -> str:
    return SourceDocument.from_bytes(source_bytes).encoding


def decode_source_bytes(source_bytes: bytes) -> tuple[str, str]:
    document = SourceDocument.from_bytes(source_bytes)
    return document.text, document.encoding


def encode_source_text(
    text: str,
    encoding: str,
    decoding_mode: SourceDecodeMode | str = SourceDecodeMode.STRICT,
) -> bytes:
    mode = SourceDecodeMode(decoding_mode)
    if mode is SourceDecodeMode.STRICT:
        return text.encode(encoding)
    return _encode_private_use_byte_escaped_text(text, encoding)


def parse_decl(path: str | Path) -> Program:
    path = Path(path)
    program = parse_decl_bytes(path.read_bytes(), str(path))
    program.routine_signatures = discover_sibling_routine_signatures(program, path)
    return program


def parse_decl_bytes(source_bytes: bytes, source_name: str | Path) -> Program:
    return parse_decl_text(SourceDocument.from_bytes(source_bytes).text, source_name)


def discover_sibling_routine_signatures(program: Program, source_path: str | Path) -> list[RoutineSignature]:
    source_path = Path(source_path)
    signatures = {signature.name: signature for signature in program.routine_signatures}
    unresolved = {function.name for function in program.functions if not function.params}
    if program.game not in SIGNATURE_DISCOVERY_GAMES or source_path.name != "default.decl" or not unresolved:
        return list(signatures.values())

    try:
        sibling_paths = sorted(source_path.parent.glob("*.decl"))
    except OSError:
        return list(signatures.values())
    for sibling_path in sibling_paths:
        if sibling_path == source_path:
            continue
        try:
            source_document = SourceDocument.from_bytes(sibling_path.read_bytes())
        except OSError:
            continue
        for line_no, raw_line in enumerate(split_source_text_lines(source_document.text), 1):
            match = PROTOTYPE_RE.match(raw_line)
            if not match:
                continue
            name = match.group(1)
            params = match.group(2).strip()
            if name not in unresolved or not params or name in signatures:
                continue
            signatures[name] = RoutineSignature(
                name=name,
                params=params,
                declaration_source=str(sibling_path),
                declaration_line=line_no,
            )
    return list(signatures.values())


def parse_decl_text(source_text: str, source_name: str | Path) -> Program:
    program = Program(source=str(source_name), game=infer_game(source_name))
    difficulty_literal_lines = {
        line
        for candidate in find_difficulty_selection_candidates(source_text)
        for line in candidate.literal_lines
    }
    current: Function | None = None
    pending_diff: str | None = None
    pending_scoped_diff = False
    active_diff: str | None = None
    pending_literal_groups: list[dict[str, str]] = []
    current_literals: dict[str, str] = {}
    resource_name: str | None = None
    resource_lines: list[str] = []

    for line_no, raw_line in enumerate(split_source_text_lines(source_text), 1):
        line = raw_line.strip()
        scoped_diff = pending_scoped_diff

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

        if current is None and TIMELINE_DECL_RE.match(raw_line):
            pending_diff = None
            pending_scoped_diff = False
            active_diff = None
            pending_literal_groups = []
            current_literals = {}

        diff_match = DIFF_RE.match(raw_line)
        statement_line = raw_line
        if diff_match:
            pending_diff = diff_match.group(1)
            scoped_diff = diff_match.group(2) is not None
            pending_scoped_diff = scoped_diff
            line = diff_match.group(3).strip()
            statement_line = line
            if pending_diff == "*":
                if current_literals:
                    pending_literal_groups.append(current_literals)
                    current_literals = {}
                active_diff = None
                if not line:
                    pending_diff = None
                    pending_scoped_diff = False
                    continue
            if not line:
                if not scoped_diff:
                    active_diff = pending_diff
                continue
            active_diff = (
                None
                if scoped_diff or pending_diff == "*"
                else pending_diff
            )
            if line_no in difficulty_literal_lines and is_difficulty_literal_statement(line, line_no):
                if pending_diff in current_literals and current_literals:
                    pending_literal_groups.append(current_literals)
                    current_literals = {}
                current_literals[pending_diff] = line[:-1].strip()
                pending_diff = None
                pending_scoped_diff = False
                continue
        elif (
            pending_diff
            and line_no in difficulty_literal_lines
            and is_difficulty_literal_statement(line, line_no)
        ):
            if pending_diff in current_literals and current_literals:
                pending_literal_groups.append(current_literals)
                current_literals = {}
            current_literals[pending_diff] = line[:-1].strip()
            pending_diff = None
            pending_scoped_diff = False
            continue

        func_match = FUNC_RE.match(raw_line)
        if func_match:
            current = Function(func_match.group(1), func_match.group(2).strip())
            program.functions.append(current)
            pending_diff = None
            pending_scoped_diff = False
            active_diff = None
            pending_literal_groups = []
            current_literals = {}
            continue

        if line == "{" and current is not None:
            continue

        if line == "}" and current is not None:
            current = None
            pending_diff = None
            pending_scoped_diff = False
            active_diff = None
            pending_literal_groups = []
            current_literals = {}
            continue

        if line == "}" and current is None:
            pending_diff = None
            pending_scoped_diff = False
            active_diff = None
            pending_literal_groups = []
            current_literals = {}

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
            pending_scoped_diff = False
            pending_literal_groups = []
            current_literals = {}
        elif stmt.kind != "comment" and line and not line.startswith("!"):
            pending_diff = None
            pending_scoped_diff = False
            pending_literal_groups = []
            current_literals = {}
        if scoped_diff and stmt.kind != "comment":
            active_diff = None

    if resource_name is not None:
        program.resources.setdefault(resource_name, []).extend(parse_resource_entries("\n".join(resource_lines)))
    annotate_top_level_dialect_regions(program.top_level)
    return program
