from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Instruction:
    opcode: int
    args: list[str]
    raw: str
    line_no: int
    difficulty: Optional[str] = None
    difficulty_literals: Any = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "opcode": self.opcode,
            "args": self.args,
            "raw": self.raw,
            "line_no": self.line_no,
            "difficulty": self.difficulty,
            "difficulty_literals": self.difficulty_literals,
        }


@dataclass
class Statement:
    kind: str
    raw: str
    line_no: int
    text: str = ""
    difficulty: Optional[str] = None
    attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "raw": self.raw,
            "line_no": self.line_no,
            "text": self.text,
            "difficulty": self.difficulty,
            "attrs": self.attrs,
        }


@dataclass
class Function:
    name: str
    params: str = ""
    body: list[Instruction] = field(default_factory=list)
    statements: list[Statement] = field(default_factory=list)


@dataclass(frozen=True)
class RoutineSignature:
    name: str
    params: str
    declaration_source: str = ""
    declaration_line: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "params": self.params,
            "declaration_source": self.declaration_source,
            "declaration_line": self.declaration_line,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RoutineSignature:
        return cls(
            name=str(data.get("name", "")),
            params=str(data.get("params", "")),
            declaration_source=str(data.get("declaration_source", "")),
            declaration_line=int(data.get("declaration_line", 0)),
        )


@dataclass
class Program:
    source: str
    game: str
    functions: list[Function] = field(default_factory=list)
    resources: dict[str, list[str]] = field(default_factory=dict)
    top_level: list[Statement] = field(default_factory=list)
    routine_signatures: list[RoutineSignature] = field(default_factory=list)
