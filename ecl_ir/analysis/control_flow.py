from __future__ import annotations

from dataclasses import dataclass

from ..canonical.semantic_ir import SemanticRoutine, SyntaxStatement


@dataclass(frozen=True, slots=True)
class ControlFlowEdge:
    source_index: int
    target_index: int
    kind: str


@dataclass(frozen=True, slots=True)
class RoutineControlFlow:
    edges: tuple[ControlFlowEdge, ...]
    cyclic_node_ids: frozenset[str]
    unresolved_targets: tuple[str, ...] = ()


def analyze_routine_control_flow(routine: SemanticRoutine) -> RoutineControlFlow:
    """Build a source-level CFG and identify nodes contained in cycles."""

    body = routine.body
    labels = {
        str(node.attributes.get("name")): index
        for index, node in enumerate(body)
        if isinstance(node, SyntaxStatement)
        and node.statement_kind == "label"
        and node.attributes.get("name")
    }
    edges: list[ControlFlowEdge] = []
    unresolved: list[str] = []

    for index, node in enumerate(body):
        kind = node.statement_kind if isinstance(node, SyntaxStatement) else ""
        if kind in {"goto", "conditional_goto"}:
            label = str(node.attributes.get("label") or "")
            target = labels.get(label)
            if target is None:
                unresolved.append(label)
            else:
                edges.append(ControlFlowEdge(index, target, "branch"))
        if index + 1 >= len(body) or kind in {"goto", "return"}:
            continue
        edges.append(ControlFlowEdge(index, index + 1, "fallthrough"))

    adjacency: list[list[int]] = [[] for _ in body]
    for edge in edges:
        adjacency[edge.source_index].append(edge.target_index)
    cyclic_indices = _cyclic_indices(adjacency)
    return RoutineControlFlow(
        edges=tuple(edges),
        cyclic_node_ids=frozenset(str(body[index].node_id) for index in cyclic_indices),
        unresolved_targets=tuple(dict.fromkeys(target for target in unresolved if target)),
    )


def _cyclic_indices(adjacency: list[list[int]]) -> set[int]:
    index_counter = 0
    indices = [-1] * len(adjacency)
    lowlinks = [0] * len(adjacency)
    stack: list[int] = []
    on_stack: set[int] = set()
    cyclic: set[int] = set()

    def visit(node: int) -> None:
        nonlocal index_counter
        indices[node] = index_counter
        lowlinks[node] = index_counter
        index_counter += 1
        stack.append(node)
        on_stack.add(node)

        for target in adjacency[node]:
            if indices[target] == -1:
                visit(target)
                lowlinks[node] = min(lowlinks[node], lowlinks[target])
            elif target in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[target])

        if lowlinks[node] != indices[node]:
            return
        component: list[int] = []
        while stack:
            member = stack.pop()
            on_stack.remove(member)
            component.append(member)
            if member == node:
                break
        if len(component) > 1 or any(member in adjacency[member] for member in component):
            cyclic.update(component)

    for node in range(len(adjacency)):
        if indices[node] == -1:
            visit(node)
    return cyclic


__all__ = ["ControlFlowEdge", "RoutineControlFlow", "analyze_routine_control_flow"]
