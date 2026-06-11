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
    difficulty_literals: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "opcode": self.opcode,
            "args": self.args,
            "raw": self.raw.strip(),
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
            "raw": self.raw.strip(),
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


@dataclass
class Program:
    source: str
    game: str
    functions: list[Function] = field(default_factory=list)
    resources: dict[str, list[str]] = field(default_factory=dict)
    top_level: list[Statement] = field(default_factory=list)


@dataclass
class IRObject:
    kind: str
    game: str
    function: str
    source_line: int
    id: str = "0"
    family: str = "unknown"
    fields: dict[str, Any] = field(default_factory=dict)
    raw: list[Instruction] = field(default_factory=list)
    unsupported: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "game": self.game,
            "function": self.function,
            "source_line": self.source_line,
            "id": self.id,
            "family": self.family,
            "fields": self.fields,
            "raw": [ins.to_dict() for ins in self.raw],
            "unsupported": self.unsupported,
        }


@dataclass
class BulletTransform:
    index: str = "0"
    channel: str = "0"
    action_type: str = "customRaw"
    raw_opcode: int = 0
    raw_args: list[str] = field(default_factory=list)
    difficulty: Optional[str] = None


@dataclass
class BulletEmitter:
    game: str
    function: str
    source_line: int
    id: str = "0"
    family: str = "unknown"
    origin: dict[str, Any] = field(default_factory=dict)
    appearance: dict[str, Any] = field(default_factory=dict)
    aim: dict[str, Any] = field(default_factory=dict)
    count: dict[str, Any] = field(default_factory=dict)
    speed: dict[str, Any] = field(default_factory=dict)
    sound: dict[str, Any] = field(default_factory=dict)
    flags: dict[str, Any] = field(default_factory=dict)
    transforms: list[BulletTransform] = field(default_factory=list)
    fire_lines: list[int] = field(default_factory=list)
    raw: list[Instruction] = field(default_factory=list)
    unsupported: list[str] = field(default_factory=list)

    @property
    def kind(self) -> str:
        return "BulletEmitter"

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "game": self.game,
            "function": self.function,
            "source_line": self.source_line,
            "id": self.id,
            "family": self.family,
            "origin": self.origin,
            "appearance": self.appearance,
            "aim": self.aim,
            "count": self.count,
            "speed": self.speed,
            "sound": self.sound,
            "flags": self.flags,
            "transforms": [t.__dict__ for t in self.transforms],
            "fire_lines": self.fire_lines,
            "raw": [ins.to_dict() for ins in self.raw],
            "unsupported": self.unsupported,
        }


@dataclass
class LaserEmitter(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "unknown"):
        super().__init__("LaserEmitter", game, function, source_line, id, family)


@dataclass
class MovementOp(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "unknown"):
        super().__init__("Movement", game, function, source_line, id, family)


@dataclass
class AnimationOp(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "unknown"):
        super().__init__("Animation", game, function, source_line, id, family)


@dataclass
class EnemyOp(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "unknown"):
        super().__init__("Enemy", game, function, source_line, id, family)


@dataclass
class BossPattern(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "unknown"):
        super().__init__("BossPattern", game, function, source_line, id, family)


@dataclass
class TimelineOp(IRObject):
    def __init__(self, game: str, function: str, source_line: int, id: str = "0", family: str = "structured"):
        super().__init__("Timeline", game, function, source_line, id, family)
