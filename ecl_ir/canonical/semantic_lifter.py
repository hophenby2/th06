from __future__ import annotations

from .semantic_ir import (
    Confidence,
    DialectRegion,
    DifficultyGuard,
    NodeId,
    Provenance,
    RawInstructionOp,
    SelectedValue,
    SelectionCase,
    SelectionKind,
    SemanticModule,
    SemanticRoutine,
    SourceSpan,
    SyntaxStatement,
    value_type_for_signature,
)
from ..source.model import Program, Statement
from .op_ir import semantic_operation
from .variable_ir import parse_expression, syntax_expression_bindings


def build_semantic_module(program: Program) -> SemanticModule:
    module = SemanticModule(
        source=program.source,
        source_game=program.game,
        profile=program.game,
        resources={name: list(entries) for name, entries in program.resources.items()},
        routine_signatures=list(program.routine_signatures),
    )
    module.top_level = [dialect_statement(program, "", statement) for statement in program.top_level]
    for function in program.functions:
        routine = SemanticRoutine(name=function.name, params=function.params)
        for statement in function.statements:
            if statement.kind != "instruction" or "opcode" not in statement.attrs:
                routine.body.append(dialect_statement(program, function.name, statement))
                continue
            opcode = int(statement.attrs.get("opcode", -1))
            args = [str(arg) for arg in statement.attrs.get("args", [])]
            operation = semantic_operation(
                program.game,
                opcode,
                args,
                statement.line_no,
                statement.difficulty,
                routine=function.name,
                source=program.source,
                raw=statement.raw,
            )
            selected_values = difficulty_selected_values(
                statement.attrs.get("difficulty_literals", []),
                program.game,
            )
            operation.selected_values = selected_values
            if (
                operation.annotations.get("dialect_operation", "").startswith("raw.")
                or operation.provenance.confidence is not Confidence.DOCUMENTED
            ):
                routine.body.append(
                    RawInstructionOp(
                        node_id=operation.node_id,
                        opcode=opcode,
                        args=args,
                        guard=DifficultyGuard.from_marker(statement.difficulty),
                        selected_values=selected_values,
                        provenance=operation.provenance,
                    )
                )
            else:
                routine.body.append(operation)
        module.routines.append(routine)
    return module


def difficulty_selected_values(literals: object, game: str = "") -> list[SelectedValue]:
    """Lift ordered thecl difficulty-switch results without guessing stack aliases."""

    groups = [literals] if isinstance(literals, dict) else literals
    if not isinstance(groups, list):
        return []
    selected: list[SelectedValue] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        cases: list[SelectionCase] = []
        for marker, raw_value in group.items():
            text = str(raw_value)
            cases.append(
                SelectionCase(
                    guard=DifficultyGuard.from_marker(str(marker)),
                    value=parse_expression(
                        game,
                        text,
                        value_type_for_signature("", 0, text),
                    ),
                )
            )
        if cases:
            selected.append(
                SelectedValue(
                    selector=SelectionKind.DIFFICULTY,
                    cases=tuple(cases),
                )
            )
    return selected


def dialect_statement(program: Program, routine: str, statement: Statement) -> SyntaxStatement:
    attributes = dict(statement.attrs)
    raw_region = attributes.pop("dialect_region", None)
    return SyntaxStatement(
        node_id=NodeId.for_statement(routine, statement.line_no),
        statement_kind=statement.kind,
        text=statement.text,
        attributes=attributes,
        guard=DifficultyGuard.from_marker(statement.difficulty),
        selected_values=difficulty_selected_values(
            statement.attrs.get("difficulty_literals", []),
            program.game,
        ),
        expressions=syntax_expression_bindings(
            program.game,
            statement.kind,
            statement.attrs,
            statement.text,
        ),
        dialect_region=(
            DialectRegion.from_dict(dict(raw_region))
            if isinstance(raw_region, dict)
            else None
        ),
        provenance=Provenance(
            game=program.game,
            routine=routine,
            span=SourceSpan(program.source, statement.line_no, statement.line_no),
            raw=statement.raw,
            confidence=Confidence.DOCUMENTED,
        ),
    )


def semantic_module_summary(module: SemanticModule) -> dict[str, int]:
    semantic = 0
    raw = 0
    dialect = len(module.top_level)
    for routine in module.routines:
        for node in routine.body:
            if node.node == "semantic_operation":
                semantic += 1
            elif node.node == "raw_instruction":
                raw += 1
            else:
                dialect += 1
    return {
        "routines": len(module.routines),
        "routine_signatures": len(module.routine_signatures),
        "semantic_ops": semantic,
        "raw_instruction_ops": raw,
        "dialect_statement_ops": dialect,
    }
