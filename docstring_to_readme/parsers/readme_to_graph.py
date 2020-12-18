from docstring_to_readme import graph as g

from collections import deque
from typing import IO, List, Tuple


__all__ = ["readme_to_graph"]


def readme_to_graph(readme: str) -> dict:
    if not readme:
        return root_node()

    lines = [line.lstrip() for line in readme.split("\n")]
    indices = section_indices(lines)
    groups = indices_to_groups(lines, indices)
    nodes = groups_to_nodes(groups)
    graph = nodes_to_graph(nodes)
    return graph


def section_indices(lines: List[str]) -> List[int]:
    return [
        idx
        for idx, line in enumerate(lines)
        if line.startswith("#")
    ]


def indices_to_groups(
    lines: List[str], indices: List[int]
) -> List[Tuple[str]]:
    output = []

    for idx, sect_pos in enumerate(indices):
        bgn = sect_pos + 1
        end = None
        if idx < len(indices) - 1:
            end = indices[idx + 1] - 1

        section = lines[sect_pos]
        body = "\n".join(lines[bgn:end])

        output.append((section, body))

    return output


def groups_to_nodes(
    groups: List[Tuple[str]],
) -> List[dict]:
    # TODO: handle pretty_section
    return [
        g.Node(section=group[0], body=group[1])
        for group in groups
    ]


def nodes_to_graph(nodes: List[dict]) -> dict:
    nodes = deque(nodes)
    node_stack = [root_node()]
    children_stack = [[]]

    while nodes:
        this = nodes.popleft()
        next = nodes[0] if len(nodes) else {}

        if not node_stack:
            # print(1)
            node_stack.append(this)
        elif not next or g.level(next) == g.level(this):
            # print(2)
            children_stack[-1].append(this)
        elif g.level(next) > g.level(this):
            # print(3)
            node_stack.append(this)
            children_stack.append([])
        elif g.level(next) < g.level(this):
            # print(4)
            children_stack[-1].append(this)
            n = node_stack.pop()
            c = children_stack.pop()
            layered = g.add_children(n, c)
            children_stack[-1].append(layered)
        # print(node_stack, children_stack, sep="\n")

    while node_stack:
        # print(node_stack, children_stack, sep="\n", end="\n\n")
        n = node_stack.pop()
        c = children_stack.pop()
        layered = g.add_children(n, c)

        if children_stack:
            # print(node_stack, children_stack, sep="\n")
            children_stack[-1].append(layered)
        else:
            # print(node_stack, children_stack, sep="\n")
            return layered


def root_node() -> dict:
    return g.Node(section="$root")
