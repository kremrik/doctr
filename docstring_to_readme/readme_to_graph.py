from docstring_to_readme.graph import Node

from typing import List, Tuple


def load():
    pass


def loads(readme: str) -> dict:
    if not readme:
        return Node(section="$root")

    if not readme.lstrip().startswith("#"):
        return {}

    lines = readme.strip().split("\n")

    for line in lines:
        if line.startswith("#"):
            pass


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
        next_idx = None
        if idx < len(indices) - 1:
            next_idx = indices[idx + 1] - 1

        section = lines[sect_pos]
        bgn = sect_pos + 1
        body = "\n".join(lines[bgn:next_idx])

        output.append((section, body))

    return output


def groups_to_nodes(
    groups: List[Tuple[str]],
) -> List[dict]:
    # TODO: handle pretty_section
    return [
        Node(section=group[0], body=group[1])
        for group in groups
    ]
