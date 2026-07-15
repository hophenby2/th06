from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Iterable

from ..source.model import RoutineSignature


class ValueType(str, Enum):
    INT32 = "int32"
    FLOAT32 = "float32"
    STRING_REF = "string_ref"
    OPAQUE = "opaque"


class VariableStorageScope(str, Enum):
    EVALUATION_STACK = "evaluation_stack"
    ROUTINE_LOCAL = "routine_local"
    CALL_FRAME = "call_frame"
    ENTITY_LOCAL = "entity_local"
    BOSS_PROXY = "boss_proxy"
    STAGE_GLOBAL = "stage_global"
    ENGINE_GLOBAL = "engine_global"
    UNKNOWN = "unknown"


class VariableAccess(str, Enum):
    READ_ONLY = "read_only"
    WRITE_ONLY = "write_only"
    READ_WRITE = "read_write"
    UNKNOWN = "unknown"

    @property
    def readable(self) -> bool:
        return self in {VariableAccess.READ_ONLY, VariableAccess.READ_WRITE}

    @property
    def writable(self) -> bool:
        return self in {VariableAccess.WRITE_ONLY, VariableAccess.READ_WRITE}


class VariableUseKind(str, Enum):
    READ = "read"
    WRITE = "write"
    READ_WRITE = "read_write"
    UNKNOWN = "unknown"


class VariablePropagation(str, Enum):
    NONE = "none"
    COPY_TO_SPAWNED_CHILD = "copy_to_spawned_child"
    SHARED = "shared"
    UNKNOWN = "unknown"


class VariableEncodingKind(str, Enum):
    NUMERIC_SPECIAL = "numeric_special"
    NAMED_LOCAL = "named_local"
    STACK_RELATIVE = "stack_relative"
    UNKNOWN = "unknown"


class OperandState(str, Enum):
    VALUE = "value"
    UNUSED = "unused"
    KEEP_CURRENT = "keep_current"
    DEFAULT = "default"
    ENGINE_SENTINEL = "engine_sentinel"


class EngineValueKind(str, Enum):
    LIVE_PLAYER_ANGLE = "live_player_angle"
    LIVE_RANDOM_ANGLE = "live_random_angle"


class EvaluationTime(str, Enum):
    IMMEDIATE = "immediate"
    FIRE = "fire"
    PER_FRAME = "per_frame"
    UNKNOWN = "unknown"


class SelectionKind(str, Enum):
    DIFFICULTY = "difficulty"


class Confidence(str, Enum):
    DOCUMENTED = "documented"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class NodeId:
    value: str

    def __str__(self) -> str:
        return self.value

    @classmethod
    def for_statement(cls, routine: str, line: int, ordinal: int = 0) -> NodeId:
        scope = routine or "<module>"
        return cls(f"{scope}:{line}:{ordinal}")


class LoweringOwner(str, Enum):
    SEMANTIC = "semantic"
    RAW = "raw"
    SYNTAX = "syntax"
    PATTERN = "pattern"


@dataclass(frozen=True)
class NodeOwnership:
    owner: LoweringOwner
    covered_by: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {"owner": self.owner.value, "covered_by": list(self.covered_by)}

    @classmethod
    def from_dict(cls, data: dict[str, Any], default: LoweringOwner) -> NodeOwnership:
        raw_owner = str(data.get("owner", default.value))
        if raw_owner not in LoweringOwner._value2member_map_:
            raise ValueError(f"invalid lowering owner: {raw_owner}")
        owner = LoweringOwner(raw_owner)
        return cls(owner=owner, covered_by=tuple(str(item) for item in data.get("covered_by", [])))


@dataclass(frozen=True)
class SourceSpan:
    source: str = ""
    start_line: int = 0
    end_line: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "start_line": self.start_line,
            "end_line": self.end_line or self.start_line,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SourceSpan:
        return cls(
            source=str(data.get("source", "")),
            start_line=int(data.get("start_line", 0)),
            end_line=int(data.get("end_line", data.get("start_line", 0))),
        )


@dataclass(frozen=True)
class Provenance:
    game: str
    routine: str
    span: SourceSpan
    opcode: int | None = None
    mnemonic: str = ""
    signature: str = ""
    raw: str = ""
    confidence: Confidence = Confidence.UNKNOWN

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.game,
            "routine": self.routine,
            "span": self.span.to_dict(),
            "opcode": self.opcode,
            "mnemonic": self.mnemonic,
            "signature": self.signature,
            "raw": self.raw,
            "confidence": self.confidence.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Provenance:
        confidence = str(data.get("confidence", Confidence.UNKNOWN.value))
        return cls(
            game=str(data.get("game", "")),
            routine=str(data.get("routine", "")),
            span=SourceSpan.from_dict(dict(data.get("span", {}) or {})),
            opcode=int(data["opcode"]) if data.get("opcode") is not None else None,
            mnemonic=str(data.get("mnemonic", "")),
            signature=str(data.get("signature", "")),
            raw=str(data.get("raw", "")),
            confidence=Confidence(confidence) if confidence in Confidence._value2member_map_ else Confidence.UNKNOWN,
        )


@dataclass(frozen=True)
class VariableSourceEncoding:
    game: str
    kind: VariableEncodingKind
    raw: str
    view_type: ValueType
    numeric_id: int | None = None
    name: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.game,
            "kind": self.kind.value,
            "raw": self.raw,
            "view_type": self.view_type.value,
            "numeric_id": self.numeric_id,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VariableSourceEncoding:
        raw_kind = str(data.get("kind", VariableEncodingKind.UNKNOWN.value))
        raw_view = str(data.get("view_type", ValueType.OPAQUE.value))
        return cls(
            game=str(data.get("game", "")),
            kind=(
                VariableEncodingKind(raw_kind)
                if raw_kind in VariableEncodingKind._value2member_map_
                else VariableEncodingKind.UNKNOWN
            ),
            raw=str(data.get("raw", "")),
            view_type=(
                ValueType(raw_view)
                if raw_view in ValueType._value2member_map_
                else ValueType.OPAQUE
            ),
            numeric_id=(
                int(data["numeric_id"])
                if data.get("numeric_id") is not None
                else None
            ),
            name=str(data.get("name", "")),
        )


@dataclass(frozen=True)
class VariableRef:
    semantic_id: str
    value_type: ValueType
    storage_type: ValueType
    storage_scope: VariableStorageScope
    access: VariableAccess
    propagation: VariablePropagation
    source_encoding: VariableSourceEncoding
    confidence: Confidence = Confidence.UNKNOWN

    def to_dict(self) -> dict[str, Any]:
        return {
            "semantic_id": self.semantic_id,
            "value_type": self.value_type.value,
            "storage_type": self.storage_type.value,
            "storage_scope": self.storage_scope.value,
            "access": self.access.value,
            "propagation": self.propagation.value,
            "source_encoding": self.source_encoding.to_dict(),
            "confidence": self.confidence.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VariableRef:
        raw_type = str(data.get("value_type", ValueType.OPAQUE.value))
        raw_storage_type = str(data.get("storage_type", raw_type))
        raw_scope = str(data.get("storage_scope", VariableStorageScope.UNKNOWN.value))
        raw_access = str(data.get("access", VariableAccess.UNKNOWN.value))
        raw_propagation = str(data.get("propagation", VariablePropagation.UNKNOWN.value))
        raw_confidence = str(data.get("confidence", Confidence.UNKNOWN.value))
        encoding_data = data.get("source_encoding")
        if not isinstance(encoding_data, dict):
            encoding_data = {
                "raw": str(encoding_data or ""),
                "view_type": raw_type,
                "kind": VariableEncodingKind.UNKNOWN.value,
            }
        return cls(
            semantic_id=str(data.get("semantic_id", "unknown")),
            value_type=ValueType(raw_type) if raw_type in ValueType._value2member_map_ else ValueType.OPAQUE,
            storage_type=(
                ValueType(raw_storage_type)
                if raw_storage_type in ValueType._value2member_map_
                else ValueType.OPAQUE
            ),
            storage_scope=(
                VariableStorageScope(raw_scope)
                if raw_scope in VariableStorageScope._value2member_map_
                else VariableStorageScope.UNKNOWN
            ),
            access=(
                VariableAccess(raw_access)
                if raw_access in VariableAccess._value2member_map_
                else VariableAccess.UNKNOWN
            ),
            propagation=(
                VariablePropagation(raw_propagation)
                if raw_propagation in VariablePropagation._value2member_map_
                else VariablePropagation.UNKNOWN
            ),
            source_encoding=VariableSourceEncoding.from_dict(encoding_data),
            confidence=(
                Confidence(raw_confidence)
                if raw_confidence in Confidence._value2member_map_
                else Confidence.UNKNOWN
            ),
        )


@dataclass(frozen=True)
class VariableUse:
    start: int
    end: int
    reference: VariableRef
    kind: VariableUseKind = VariableUseKind.READ

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "kind": self.kind.value,
            "reference": self.reference.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VariableUse:
        raw_kind = str(data.get("kind", VariableUseKind.READ.value))
        return cls(
            start=int(data.get("start", 0)),
            end=int(data.get("end", 0)),
            kind=(
                VariableUseKind(raw_kind)
                if raw_kind in VariableUseKind._value2member_map_
                else VariableUseKind.UNKNOWN
            ),
            reference=VariableRef.from_dict(dict(data.get("reference", {}) or {})),
        )


@dataclass(frozen=True)
class StackRef:
    offset: int
    value_type: ValueType
    source_game: str
    source_encoding: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "offset": self.offset,
            "value_type": self.value_type.value,
            "source_game": self.source_game,
            "source_encoding": self.source_encoding,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StackRef:
        raw_type = str(data.get("value_type", ValueType.OPAQUE.value))
        return cls(
            offset=int(data.get("offset", 0)),
            value_type=(
                ValueType(raw_type)
                if raw_type in ValueType._value2member_map_
                else ValueType.OPAQUE
            ),
            source_game=str(data.get("source_game", "")),
            source_encoding=str(data.get("source_encoding", "")),
        )


@dataclass(frozen=True)
class StackUse:
    start: int
    end: int
    reference: StackRef
    kind: VariableUseKind = VariableUseKind.READ

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "kind": self.kind.value,
            "reference": self.reference.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StackUse:
        raw_kind = str(data.get("kind", VariableUseKind.READ.value))
        return cls(
            start=int(data.get("start", 0)),
            end=int(data.get("end", 0)),
            kind=(
                VariableUseKind(raw_kind)
                if raw_kind in VariableUseKind._value2member_map_
                else VariableUseKind.UNKNOWN
            ),
            reference=StackRef.from_dict(dict(data.get("reference", {}) or {})),
        )


@dataclass(frozen=True)
class ExpressionIR:
    text: str
    value_type: ValueType = ValueType.OPAQUE
    variable_uses: tuple[VariableUse, ...] = ()
    stack_uses: tuple[StackUse, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "type": self.value_type.value,
            "variable_uses": [use.to_dict() for use in self.variable_uses],
            "stack_uses": [use.to_dict() for use in self.stack_uses],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExpressionIR:
        raw_type = str(data.get("type", ValueType.OPAQUE.value))
        value_type = ValueType(raw_type) if raw_type in ValueType._value2member_map_ else ValueType.OPAQUE
        return cls(
            text=str(data.get("text", "")),
            value_type=value_type,
            variable_uses=tuple(
                VariableUse.from_dict(item) for item in data.get("variable_uses", [])
            ),
            stack_uses=tuple(
                StackUse.from_dict(item) for item in data.get("stack_uses", [])
            ),
        )


# Schema-v1 callers used TypedExpr. Keep the import name while making the IR role explicit.
TypedExpr = ExpressionIR


@dataclass(frozen=True)
class ExpressionBinding:
    role: str
    expression: ExpressionIR
    ordinal: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "ordinal": self.ordinal,
            "expression": self.expression.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExpressionBinding:
        return cls(
            role=str(data.get("role", "expression")),
            ordinal=int(data.get("ordinal", 0)),
            expression=ExpressionIR.from_dict(dict(data.get("expression", {}) or {})),
        )


@dataclass(frozen=True)
class EngineValue:
    kind: EngineValueKind
    source_encoding: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind.value, "source_encoding": self.source_encoding}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EngineValue:
        raw_kind = str(data.get("kind", EngineValueKind.LIVE_PLAYER_ANGLE.value))
        if raw_kind not in EngineValueKind._value2member_map_:
            raise ValueError(f"invalid engine value kind: {raw_kind}")
        return cls(EngineValueKind(raw_kind), str(data.get("source_encoding", "")))


@dataclass(frozen=True)
class OperandValue:
    state: OperandState
    expression: TypedExpr | None = None
    engine_value: EngineValue | None = None
    source_text: str = ""
    evaluation_time: EvaluationTime = EvaluationTime.IMMEDIATE

    @classmethod
    def value(
        cls,
        text: object,
        value_type: ValueType = ValueType.OPAQUE,
        evaluation_time: EvaluationTime = EvaluationTime.IMMEDIATE,
    ) -> OperandValue:
        rendered = str(text)
        return cls(
            state=OperandState.VALUE,
            expression=TypedExpr(rendered, value_type),
            source_text=rendered,
            evaluation_time=evaluation_time,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "expression": self.expression.to_dict() if self.expression else None,
            "engine_value": self.engine_value.to_dict() if self.engine_value else None,
            "source_text": self.source_text,
            "evaluation_time": self.evaluation_time.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OperandValue:
        raw_state = str(data.get("state", OperandState.VALUE.value))
        raw_time = str(data.get("evaluation_time", EvaluationTime.IMMEDIATE.value))
        expr_data = data.get("expression")
        engine_data = data.get("engine_value")
        return cls(
            state=OperandState(raw_state) if raw_state in OperandState._value2member_map_ else OperandState.VALUE,
            expression=TypedExpr.from_dict(expr_data) if isinstance(expr_data, dict) else None,
            engine_value=EngineValue.from_dict(engine_data) if isinstance(engine_data, dict) else None,
            source_text=str(data.get("source_text", data.get("encoded", ""))),
            evaluation_time=EvaluationTime(raw_time) if raw_time in EvaluationTime._value2member_map_ else EvaluationTime.UNKNOWN,
        )


@dataclass(frozen=True)
class SemanticOperand:
    name: str
    value: OperandValue

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value.to_dict()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SemanticOperand:
        return cls(
            name=str(data.get("name", "operand")),
            value=OperandValue.from_dict(dict(data.get("value", {}) or {})),
        )


DIFFICULTY_LANES = ("E", "N", "H", "L", "X", "O", "6", "7")
DIFFICULTY_LANE_ALIASES = {
    "E": "E",
    "0": "E",
    "N": "N",
    "1": "N",
    "H": "H",
    "2": "H",
    "L": "L",
    "3": "L",
    "X": "X",
    "4": "X",
    "O": "O",
    "5": "O",
    "6": "6",
    "7": "7",
}


@dataclass(frozen=True)
class DifficultyGuard:
    """An eight-lane execution mask with the original dialect spelling.

    The engine mask has eight independent lanes.  E/N/H/L/X/O are the
    symbolic spellings for lanes 0..5; numeric dialects spell all lanes as
    0..7, while pre-TH13 dialects use 4/5 in place of X/O.
    """

    mask: tuple[str, ...] = ()
    raw: str = ""

    def __post_init__(self) -> None:
        raw = str(self.raw).upper()
        lanes: list[str] = []
        if raw not in {"", "*", "-"}:
            for token in raw:
                lane = DIFFICULTY_LANE_ALIASES.get(token)
                if lane is not None and lane not in lanes:
                    lanes.append(lane)
        for item in self.mask:
            for token in str(item).upper():
                lane = DIFFICULTY_LANE_ALIASES.get(token)
                if lane is not None and lane not in lanes:
                    lanes.append(lane)
        object.__setattr__(self, "mask", tuple(lanes))
        object.__setattr__(self, "raw", raw)

    @property
    def is_unconditional(self) -> bool:
        return self.raw == "*" or (not self.raw and not self.mask)

    def to_dict(self) -> dict[str, Any]:
        return {"mask": list(self.mask), "raw": self.raw}

    @classmethod
    def from_marker(cls, marker: str | None) -> DifficultyGuard:
        if not marker or marker == "*":
            return cls(raw=str(marker or ""))
        text = str(marker).upper()
        return cls(raw=text)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DifficultyGuard:
        return cls(
            mask=tuple(str(item) for item in data.get("mask", [])),
            raw=str(data.get("raw", "")),
        )


@dataclass(frozen=True)
class SelectionCase:
    guard: DifficultyGuard
    value: TypedExpr

    def to_dict(self) -> dict[str, Any]:
        return {"guard": self.guard.to_dict(), "value": self.value.to_dict()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SelectionCase:
        return cls(
            guard=DifficultyGuard.from_dict(dict(data.get("guard", {}) or {})),
            value=TypedExpr.from_dict(dict(data.get("value", {}) or {})),
        )


@dataclass(frozen=True)
class SelectedValue:
    """A source value chosen before its consuming instruction or syntax node."""

    selector: SelectionKind
    cases: tuple[SelectionCase, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "selector": self.selector.value,
            "cases": [case.to_dict() for case in self.cases],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SelectedValue:
        raw_selector = str(data.get("selector", SelectionKind.DIFFICULTY.value))
        selector = (
            SelectionKind(raw_selector)
            if raw_selector in SelectionKind._value2member_map_
            else SelectionKind.DIFFICULTY
        )
        return cls(
            selector=selector,
            cases=tuple(SelectionCase.from_dict(item) for item in data.get("cases", [])),
        )


@dataclass
class SemanticOperation:
    node_id: NodeId
    operation: str
    domain: str
    operands: list[SemanticOperand]
    provenance: Provenance
    guard: DifficultyGuard = field(default_factory=DifficultyGuard)
    selected_values: list[SelectedValue] = field(default_factory=list)
    annotations: dict[str, Any] = field(default_factory=dict)
    ownership: NodeOwnership = field(default_factory=lambda: NodeOwnership(LoweringOwner.SEMANTIC))

    @property
    def node(self) -> str:
        return "semantic_operation"

    def encoded_args(self) -> list[str]:
        return [
            operand.value.source_text
            or (operand.value.expression.text if operand.value.expression else "")
            for operand in self.operands
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "node": self.node,
            "node_id": str(self.node_id),
            "operation": self.operation,
            "domain": self.domain,
            "operands": [operand.to_dict() for operand in self.operands],
            "guard": self.guard.to_dict(),
            "selected_values": [value.to_dict() for value in self.selected_values],
            "provenance": self.provenance.to_dict(),
            "annotations": self.annotations,
            "ownership": self.ownership.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SemanticOperation:
        return cls(
            node_id=NodeId(str(data.get("node_id", ""))),
            operation=str(data.get("operation", "unknown")),
            domain=str(data.get("domain", "raw")),
            operands=[SemanticOperand.from_dict(item) for item in data.get("operands", [])],
            guard=DifficultyGuard.from_dict(dict(data.get("guard", {}) or {})),
            selected_values=[SelectedValue.from_dict(item) for item in data.get("selected_values", [])],
            provenance=Provenance.from_dict(dict(data.get("provenance", {}) or {})),
            annotations=dict(data.get("annotations", {}) or {}),
            ownership=NodeOwnership.from_dict(dict(data.get("ownership", {}) or {}), LoweringOwner.SEMANTIC),
        )


@dataclass
class RawInstructionOp:
    node_id: NodeId
    opcode: int
    args: list[str]
    provenance: Provenance
    guard: DifficultyGuard = field(default_factory=DifficultyGuard)
    selected_values: list[SelectedValue] = field(default_factory=list)
    reason: str = "unconfirmed_semantics"
    ownership: NodeOwnership = field(default_factory=lambda: NodeOwnership(LoweringOwner.RAW))

    @property
    def node(self) -> str:
        return "raw_instruction"

    def to_dict(self) -> dict[str, Any]:
        return {
            "node": self.node,
            "node_id": str(self.node_id),
            "opcode": self.opcode,
            "args": self.args,
            "guard": self.guard.to_dict(),
            "selected_values": [value.to_dict() for value in self.selected_values],
            "provenance": self.provenance.to_dict(),
            "reason": self.reason,
            "ownership": self.ownership.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RawInstructionOp:
        return cls(
            node_id=NodeId(str(data.get("node_id", ""))),
            opcode=int(data.get("opcode", -1)),
            args=[str(arg) for arg in data.get("args", [])],
            guard=DifficultyGuard.from_dict(dict(data.get("guard", {}) or {})),
            selected_values=[SelectedValue.from_dict(item) for item in data.get("selected_values", [])],
            provenance=Provenance.from_dict(dict(data.get("provenance", {}) or {})),
            reason=str(data.get("reason", "unconfirmed_semantics")),
            ownership=NodeOwnership.from_dict(dict(data.get("ownership", {}) or {}), LoweringOwner.RAW),
        )


class DialectRegionKind(str, Enum):
    TIMELINE = "timeline"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class DialectRegion:
    """Membership of a syntax node in one source-dialect block."""

    kind: DialectRegionKind
    name: str
    member_index: int
    member_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "name": self.name,
            "member_index": self.member_index,
            "member_count": self.member_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DialectRegion:
        raw_kind = str(data.get("kind", DialectRegionKind.UNKNOWN.value))
        return cls(
            kind=(
                DialectRegionKind(raw_kind)
                if raw_kind in DialectRegionKind._value2member_map_
                else DialectRegionKind.UNKNOWN
            ),
            name=str(data.get("name", "")),
            member_index=int(data.get("member_index", 0)),
            member_count=int(data.get("member_count", 0)),
        )


@dataclass
class SyntaxStatement:
    node_id: NodeId
    statement_kind: str
    text: str
    attributes: dict[str, Any]
    provenance: Provenance
    guard: DifficultyGuard = field(default_factory=DifficultyGuard)
    selected_values: list[SelectedValue] = field(default_factory=list)
    expressions: list[ExpressionBinding] = field(default_factory=list)
    dialect_region: DialectRegion | None = None
    ownership: NodeOwnership = field(default_factory=lambda: NodeOwnership(LoweringOwner.SYNTAX))

    @property
    def node(self) -> str:
        return "syntax_statement"

    def to_dict(self) -> dict[str, Any]:
        data = {
            "node": self.node,
            "node_id": str(self.node_id),
            "statement_kind": self.statement_kind,
            "text": self.text,
            "attributes": self.attributes,
            "guard": self.guard.to_dict(),
            "selected_values": [value.to_dict() for value in self.selected_values],
            "expressions": [binding.to_dict() for binding in self.expressions],
            "provenance": self.provenance.to_dict(),
            "ownership": self.ownership.to_dict(),
        }
        if self.dialect_region is not None:
            data["dialect_region"] = self.dialect_region.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SyntaxStatement:
        return cls(
            node_id=NodeId(str(data.get("node_id", ""))),
            statement_kind=str(data.get("statement_kind", "raw")),
            text=str(data.get("text", "")),
            attributes=dict(data.get("attributes", {}) or {}),
            guard=DifficultyGuard.from_dict(dict(data.get("guard", {}) or {})),
            selected_values=[
                SelectedValue.from_dict(item) for item in data.get("selected_values", [])
            ],
            expressions=[
                ExpressionBinding.from_dict(item) for item in data.get("expressions", [])
            ],
            dialect_region=(
                DialectRegion.from_dict(dict(data.get("dialect_region", {}) or {}))
                if data.get("dialect_region") is not None
                else None
            ),
            provenance=Provenance.from_dict(dict(data.get("provenance", {}) or {})),
            ownership=NodeOwnership.from_dict(dict(data.get("ownership", {}) or {}), LoweringOwner.SYNTAX),
        )


SemanticNode = SemanticOperation | RawInstructionOp | SyntaxStatement


@dataclass
class SemanticRoutine:
    name: str
    params: str = ""
    body: list[SemanticNode] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "params": self.params, "body": [node.to_dict() for node in self.body]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SemanticRoutine:
        return cls(
            name=str(data.get("name", "")),
            params=str(data.get("params", "")),
            body=[semantic_node_from_dict(item) for item in data.get("body", [])],
        )


@dataclass
class SemanticModule:
    source: str
    source_game: str
    profile: str
    resources: dict[str, list[str]] = field(default_factory=dict)
    routine_signatures: list[RoutineSignature] = field(default_factory=list)
    top_level: list[SyntaxStatement] = field(default_factory=list)
    routines: list[SemanticRoutine] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "th062.semantic-ir",
            "schema_version": 1,
            "source": self.source,
            "source_game": self.source_game,
            "profile": self.profile,
            "resources": self.resources,
            "routine_signatures": [signature.to_dict() for signature in self.routine_signatures],
            "top_level": [node.to_dict() for node in self.top_level],
            "routines": [routine.to_dict() for routine in self.routines],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SemanticModule:
        return cls(
            source=str(data.get("source", "")),
            source_game=str(data.get("source_game", "")),
            profile=str(data.get("profile", data.get("source_game", "unknown"))),
            resources={str(key): [str(item) for item in value] for key, value in (data.get("resources", {}) or {}).items()},
            routine_signatures=[RoutineSignature.from_dict(item) for item in data.get("routine_signatures", [])],
            top_level=[SyntaxStatement.from_dict(item) for item in data.get("top_level", [])],
            routines=[SemanticRoutine.from_dict(item) for item in data.get("routines", [])],
        )


def semantic_node_from_dict(data: dict[str, Any]) -> SemanticNode:
    node = str(data.get("node", ""))
    if node in {"semantic_op", "semantic_operation"}:
        return SemanticOperation.from_dict(data)
    if node in {"raw_instruction_op", "raw_instruction"}:
        return RawInstructionOp.from_dict(data)
    return SyntaxStatement.from_dict(data)


CANONICAL_OPERATION_ALIASES: dict[str, str] = {
    "bullet.et_new": "bullet.manager.reset",
    "bullet.sprite": "bullet.visual.set",
    "bullet.offset": "bullet.origin.offset.set",
    "bullet.angle": "bullet.formation.angles.set",
    "bullet.speed": "bullet.formation.speeds.set",
    "bullet.count": "bullet.formation.counts.set",
    "bullet.aim": "bullet.formation.set",
    "bullet.sound": "bullet.sounds.set",
    "bullet.transform_set": "bullet.transform.replace",
    "bullet.transform_set2": "bullet.transform.replace",
    "bullet.transform": "bullet.transform.append",
    "bullet.transform2": "bullet.transform.append",
    "bullet.copy": "bullet.manager.copy",
    "bullet.et_ex_subtract": "bullet.transform.append_cursor.decrement",
    "bullet.et_speed_r2": "bullet.formation.speeds.by_rank",
    "bullet.et_speed_r3": "bullet.formation.speeds.by_rank",
    "bullet.et_speed_r5": "bullet.formation.speeds.by_rank",
    "bullet.et_count_r2": "bullet.formation.counts.by_rank",
    "bullet.et_count_r3": "bullet.formation.counts.by_rank",
    "bullet.et_count_r5": "bullet.formation.counts.by_rank",
    "bullet.speed_by_difficulty": "bullet.formation.speeds.by_difficulty",
    "bullet.count_by_difficulty": "bullet.formation.counts.by_difficulty",
    "bullet.et_offset_rad": "bullet.origin.polar_offset.set",
    "bullet.distance": "bullet.origin.distance.set",
    "bullet.et_offset_abs": "bullet.origin.absolute.set",
    "laser.new": "laser.spec.reset",
    "laser.on": "laser.activate",
    "laser.straight_on": "laser.activate_straight",
    "laser.curve_on": "laser.activate_curve",
    "laser.end": "laser.end",
    "boss.set_interrupt": "boss.interrupt.hp_or_time.set",
    "boss.set_timeout": "boss.interrupt.timeout.set",
}


INVARIANT_ARG_LAYOUTS: dict[str, tuple[str, ...]] = {
    "flow.iset": ("target", "value"),
    "flow.fset": ("target", "value"),
    "flow.iadd": ("target", "value"),
    "flow.isub": ("target", "value"),
    "flow.imul": ("target", "value"),
    "flow.idiv": ("target", "value"),
    "flow.imod": ("target", "value"),
    "flow.fadd": ("target", "value"),
    "flow.fsub": ("target", "value"),
    "flow.fmul": ("target", "value"),
    "flow.fdiv": ("target", "value"),
    "flow.fmod": ("target", "value"),
    "flow.iset_add": ("target", "left", "right"),
    "flow.iset_sub": ("target", "left", "right"),
    "flow.iset_mul": ("target", "left", "right"),
    "flow.iset_div": ("target", "left", "right"),
    "flow.iset_mod": ("target", "left", "right"),
    "flow.fset_add": ("target", "left", "right"),
    "flow.fset_sub": ("target", "left", "right"),
    "flow.fset_mul": ("target", "left", "right"),
    "flow.fset_div": ("target", "left", "right"),
    "flow.fset_mod": ("target", "left", "right"),
    "flow.fset_sin": ("target", "value"),
    "flow.fset_cos": ("target", "value"),
    "flow.inc": ("target",),
    "flow.dec": ("target",),
    "flow.norm_rad": ("target",),
    "flow.math_angle": ("target", "x1", "y1", "x2", "y2"),
    "flow.math_circle_pos": ("target_x", "target_y", "angle", "radius"),
    "flow.math_distance": ("target", "x1", "y1", "x2", "y2"),
    "flow.seti": ("target",),
    "flow.setf": ("target",),
    "flow.deci": ("target",),
    "flow.wait": ("frames",),
    "bullet.manager.reset": ("manager",),
    "bullet.fire": ("manager",),
    "bullet.visual.set": ("manager", "bullet_type", "color"),
    "bullet.origin.offset.set": ("manager", "x", "y"),
    "bullet.formation.angles.set": ("manager", "angle_a", "angle_b"),
    "bullet.formation.speeds.set": ("manager", "speed_a", "speed_b"),
    "bullet.formation.counts.set": ("manager", "count_a", "count_b"),
    "bullet.formation.set": ("manager", "formation"),
    "bullet.sounds.set": ("manager", "fire_sound", "transform_sound"),
    "bullet.manager.copy": ("destination", "source"),
    "bullet.transform.append_cursor.decrement": ("manager",),
    "bullet.macro.configure": ("bullet_type", "color", "ways", "layers", "speed_a", "speed_b", "angle_a", "angle_b", "flags"),
    "bullet.auto_fire.schedule": ("interval",),
    "bullet.auto_fire.schedule_random_delay": ("interval",),
    "bullet.formation.speeds.by_difficulty": (
        "manager",
        "speed_a_easy", "speed_a_normal", "speed_a_hard", "speed_a_lunatic",
        "speed_b_easy", "speed_b_normal", "speed_b_hard", "speed_b_lunatic",
    ),
    "bullet.formation.counts.by_difficulty": (
        "manager",
        "count_a_easy", "count_a_normal", "count_a_hard", "count_a_lunatic",
        "count_b_easy", "count_b_normal", "count_b_hard", "count_b_lunatic",
    ),
    "bullet.origin.polar_offset.set": ("manager", "angle", "radius"),
    "bullet.origin.distance.set": ("manager", "distance"),
    "bullet.origin.absolute.set": ("manager", "x", "y"),
    "bullet.cancel_radius": ("radius",),
    "bullet.clear_radius": ("radius",),
    "movement.position.set": ("x", "y"),
    "movement.position.tween": ("duration", "interpolation", "x", "y"),
    "movement.position_rel.set": ("x", "y"),
    "movement.position_rel.tween": ("duration", "interpolation", "x", "y"),
    "movement.velocity.set": ("angle", "speed"),
    "movement.velocity.tween": ("duration", "interpolation", "angle", "speed"),
    "movement.velocity_rel.set": ("angle", "speed"),
    "movement.velocity_rel.tween": ("duration", "interpolation", "angle", "speed"),
    "anm.select": ("resource_bank",),
    "anm.set_sprite": ("slot", "script"),
    "anm.set_main": ("slot", "script"),
    "anm.play": ("resource_bank", "script"),
    "enemy.create": ("routine", "x", "y", "health", "main_drop", "score"),
    "enemy.create_abs": ("routine", "x", "y", "health", "main_drop", "score"),
    "boss.interrupt.hp_or_time.set": ("slot", "health", "duration", "routine"),
    "boss.interrupt.timeout.set": ("slot", "routine"),
    "laser.spec.reset": ("laser", "start_offset", "length", "end_offset", "width"),
    "laser.timing": ("laser", "warning", "expand", "active", "shrink", "flags"),
    "laser.trajectory": ("laser", "x_speed", "y_speed"),
}


_WRITE_FIRST_OPERATIONS = {
    "flow.iset",
    "flow.fset",
    "flow.iset_add",
    "flow.iset_sub",
    "flow.iset_mul",
    "flow.iset_div",
    "flow.iset_mod",
    "flow.fset_add",
    "flow.fset_sub",
    "flow.fset_mul",
    "flow.fset_div",
    "flow.fset_mod",
    "flow.fset_sin",
    "flow.fset_cos",
    "flow.math_angle",
    "flow.math_distance",
    "flow.seti",
    "flow.setf",
}
_READ_WRITE_FIRST_OPERATIONS = {
    "flow.iadd",
    "flow.isub",
    "flow.imul",
    "flow.idiv",
    "flow.imod",
    "flow.fadd",
    "flow.fsub",
    "flow.fmul",
    "flow.fdiv",
    "flow.fmod",
    "flow.inc",
    "flow.dec",
    "flow.norm_rad",
    "flow.deci",
}


def operand_use_kinds(
    operation: str,
    names: list[str],
) -> list[VariableUseKind]:
    if operation == "flow.math_circle_pos" and len(names) == 4:
        return [
            VariableUseKind.WRITE,
            VariableUseKind.WRITE,
            VariableUseKind.READ,
            VariableUseKind.READ,
        ]
    if operation in _WRITE_FIRST_OPERATIONS and names:
        return [VariableUseKind.WRITE, *([VariableUseKind.READ] * (len(names) - 1))]
    if operation in _READ_WRITE_FIRST_OPERATIONS and names:
        return [
            VariableUseKind.READ_WRITE,
            *([VariableUseKind.READ] * (len(names) - 1)),
        ]
    return [
        VariableUseKind.UNKNOWN
        if name.startswith("operand_")
        else VariableUseKind.READ
        for name in names
    ]


@dataclass(frozen=True)
class SourceForm:
    operation: str
    opcode_family: str
    operand_names: tuple[str, ...]


RANK_SAMPLE_LABELS: dict[int, tuple[str, ...]] = {
    2: ("low", "high"),
    3: ("low", "medium", "high"),
    5: ("low", "medium_low", "medium", "medium_high", "high"),
}


def rank_operand_names(value_name: str, sample_count: int) -> tuple[str, ...]:
    labels = RANK_SAMPLE_LABELS[sample_count]
    return (
        "manager",
        *(f"{value_name}_a_{label}" for label in labels),
        *(f"{value_name}_b_{label}" for label in labels),
    )


SOURCE_FORMS: tuple[SourceForm, ...] = (
    SourceForm("bullet.origin.offset.set", "th06", ("x", "y", "z")),
    SourceForm("bullet.origin.offset.set", "th07", ("x", "y", "z")),
    SourceForm("bullet.origin.offset.set", "th08", ("x", "y")),
    SourceForm("bullet.sounds.set", "th06", ("fire_sound",)),
    SourceForm("bullet.sounds.set", "th07", ("fire_sound", "transform_sound")),
    SourceForm("bullet.sounds.set", "th08", ("fire_sound", "transform_sound")),
) + tuple(
    SourceForm(operation, family, rank_operand_names(value_name, sample_count))
    for operation, value_name in (
        ("bullet.formation.speeds.by_rank", "speed"),
        ("bullet.formation.counts.by_rank", "count"),
    )
    for family in ("th10_th11", "th12", "th13_plus")
    for sample_count in (2, 3, 5)
)


class DialectDecoder:
    def __init__(self, source_forms: Iterable[SourceForm] = SOURCE_FORMS) -> None:
        self._layouts = {
            (form.operation, form.opcode_family, len(form.operand_names)): form.operand_names
            for form in source_forms
        }

    def operand_names(self, operation: str, opcode_family: str, count: int) -> list[str]:
        declared = self._layouts.get((operation, opcode_family, count))
        if declared is None and operation in INVARIANT_ARG_LAYOUTS:
            invariant = INVARIANT_ARG_LAYOUTS[operation]
            declared = invariant if len(invariant) == count else None
        if declared is None:
            return [f"operand_{index}" for index in range(count)]
        return list(declared)

    def decode(
        self,
        operation: str,
        opcode_family: str,
        args: Iterable[object],
        signature: str = "",
        operand_names: Iterable[str] | None = None,
        source_game: str = "",
    ) -> list[SemanticOperand]:
        from .variable_ir import parse_expression

        rendered = [str(arg) for arg in args]
        names = (
            [str(name) for name in operand_names]
            if operand_names is not None
            else self.operand_names(operation, opcode_family, len(rendered))
        )
        if len(names) != len(rendered):
            names = [f"operand_{index}" for index in range(len(rendered))]
        use_kinds = operand_use_kinds(operation, names)
        return [
            SemanticOperand(
                name=name,
                value=OperandValue(
                    state=OperandState.VALUE,
                    expression=parse_expression(
                        source_game,
                        value,
                        value_type_for_signature(signature, index, value),
                        use_kind,
                    ),
                    source_text=value,
                ),
            )
            for index, (name, value, use_kind) in enumerate(zip(names, rendered, use_kinds))
        ]


DEFAULT_DIALECT_DECODER = DialectDecoder()


def transform_keep_current_token(
    game: str,
    mode_semantic: str,
    operand_name: str,
) -> str | None:
    semantic = {
        "spawn_bullet_packed_v13": "spawn_bullet_advanced",
        "spawn_bullet_expanded": "spawn_bullet_advanced",
    }.get(mode_semantic, mode_semantic)
    legacy_fields = {
        "accel": {"s"},
        "pause_then_relative_velocity": {"s"},
        "bounce_all": {"r"},
        "bounce_no_bottom": {"r"},
        "velocity_over_time": {"s"},
    }
    if game in {"th10", "th11", "th12", "th125", "th128"} and operand_name in legacy_fields.get(semantic, set()):
        return "-999.0f"
    if game in {"th13", "th14", "th143"} and semantic == "spawn_bullet_advanced" and operand_name in {"r", "m"}:
        return "-999.0f"
    return None


def transform_engine_value_kind(
    game: str,
    mode_semantic: str,
    operand_name: str,
    raw: str,
) -> EngineValueKind | None:
    if mode_semantic != "velocity_over_time" or operand_name != "s":
        return None
    token = str(raw).strip()
    if game in {"th13", "th14", "th143"} and token == "999.0f":
        return EngineValueKind.LIVE_PLAYER_ANGLE
    if game in {"th15", "th16", "th165", "th17"} and token == "999999.0f":
        return EngineValueKind.LIVE_PLAYER_ANGLE
    if game in {"th18", "th185"}:
        if token == "3000000.0f":
            return EngineValueKind.LIVE_PLAYER_ANGLE
        if token == "4000000.0f":
            return EngineValueKind.LIVE_RANDOM_ANGLE
    return None


def transform_engine_value_token(game: str, kind: EngineValueKind) -> str | None:
    if kind is EngineValueKind.LIVE_PLAYER_ANGLE:
        if game in {"th13", "th14", "th143"}:
            return "999.0f"
        if game in {"th15", "th16", "th165", "th17"}:
            return "999999.0f"
        if game in {"th18", "th185"}:
            return "3000000.0f"
    if kind is EngineValueKind.LIVE_RANDOM_ANGLE and game in {"th18", "th185"}:
        return "4000000.0f"
    return None


def contextualize_transform_operands(
    operation: str,
    operands: list[SemanticOperand],
    sentinel_codec: Any,
    mode_semantic: str = "",
    source_game: str = "",
) -> list[SemanticOperand]:
    if operation not in {"bullet.transform.replace", "bullet.transform.append"}:
        return operands
    contextualized: list[SemanticOperand] = []
    for operand in operands:
        if operand.name not in {"a", "b", "c", "d", "r", "s", "m", "n"}:
            contextualized.append(operand)
            continue
        raw = operand.value.source_text
        engine_kind = transform_engine_value_kind(
            source_game,
            mode_semantic,
            operand.name,
            raw,
        )
        if engine_kind is not None:
            contextualized.append(
                SemanticOperand(
                    operand.name,
                    OperandValue(
                        state=OperandState.ENGINE_SENTINEL,
                        expression=operand.value.expression,
                        engine_value=EngineValue(engine_kind, raw),
                        source_text=raw,
                        evaluation_time=EvaluationTime.PER_FRAME,
                    ),
                )
            )
            continue
        is_int = bool(sentinel_codec.is_unused_int(raw))
        is_float = bool(sentinel_codec.is_unused_float(raw))
        special_keep = transform_keep_current_token(source_game, mode_semantic, operand.name)
        is_keep = bool(sentinel_codec.is_keep_current_float(raw)) or (
            special_keep is not None and raw == special_keep
        )
        if not (is_int or is_float or is_keep):
            contextualized.append(operand)
            continue
        keep_fields = {
            "accel": {"s"},
            "pause_then_relative_velocity": {"s"},
            "bounce_all": {"r"},
            "bounce_no_bottom": {"r"},
            "velocity_over_time": {"s"},
            "spawn_bullet_advanced": {"r", "m"},
        }
        keep_current = is_keep and operand.name in keep_fields.get(mode_semantic, set())
        contextualized.append(
            SemanticOperand(
                operand.name,
                OperandValue(
                    state=OperandState.KEEP_CURRENT if keep_current else OperandState.UNUSED,
                    expression=operand.value.expression,
                    source_text=raw,
                    evaluation_time=operand.value.evaluation_time,
                ),
            )
        )
    return contextualized


def literal_int_text(value: object) -> int | None:
    text = str(value).strip()
    if not re.fullmatch(r"[-+]?(?:0[xX][0-9a-fA-F]+|\d+)", text):
        return None
    try:
        return int(text, 0)
    except ValueError:
        return None


def canonical_operation_id(dialect_operation: str, opcode_family: str = "") -> str:
    if dialect_operation in {"bullet.transform", "bullet.transform2"} and opcode_family in {"th10_th11", "th12"}:
        return "bullet.transform.replace"
    return CANONICAL_OPERATION_ALIASES.get(dialect_operation, dialect_operation)


def semantic_domain(operation: str, fallback: str = "raw") -> str:
    """Derive ownership domain from the canonical semantic namespace."""

    namespace, separator, _name = operation.partition(".")
    if not separator or namespace == "raw":
        return fallback
    return namespace


def value_type_for_signature(signature: str, index: int, raw: str) -> ValueType:
    code = signature[index] if index < len(signature) else ""
    if code == "f":
        return ValueType.FLOAT32
    if code == "m":
        return ValueType.STRING_REF
    if code in {"S", "D", "s"}:
        return ValueType.INT32
    text = str(raw).strip()
    if text.startswith('"') and text.endswith('"'):
        return ValueType.STRING_REF
    if re.search(r"\.\d*f\b|\.0f\]", text):
        return ValueType.FLOAT32
    if re.fullmatch(r"[-+]?\d+|\[-?\d+\]", text):
        return ValueType.INT32
    return ValueType.OPAQUE


def semantic_operation_to_backend_event(data: SemanticOperation | dict[str, Any]) -> dict[str, Any]:
    operation = data if isinstance(data, SemanticOperation) else SemanticOperation.from_dict(data)
    dialect_operation = str(operation.annotations.get("dialect_operation") or operation.operation)
    return {
        "op_key": dialect_operation,
        "canonical_operation": operation.operation,
        "domain": operation.domain,
        "source_game": operation.provenance.game,
        "source_opcode": operation.provenance.opcode if operation.provenance.opcode is not None else -1,
        "source_name": operation.provenance.mnemonic,
        "signature": operation.provenance.signature,
        "args": operation.encoded_args(),
        "operand_values": [operand.value.to_dict() for operand in operation.operands],
        "selected_values": [value.to_dict() for value in operation.selected_values],
        "line": operation.provenance.span.start_line,
        "difficulty": operation.guard.raw or None,
    }
