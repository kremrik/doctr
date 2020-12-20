from doctr import graph as g

from typing import IO


__all__ = ["dump", "dumps"]


def dump(handler: IO, graph: dict) -> None:
    handler.write(dumps(graph))


def dumps(graph: dict) -> str:
    if not graph:
        return ""

    section = g.node_section(graph)
    body = g.node_body(graph)

    children = "\n\n".join(
        child
        for child in [
            dumps(c) for c in g.node_children(graph)
        ]
        if child
    )

    if section == "$root":
        return children

    if body and children:
        return section + "\n" + body + "\n\n" + children

    if not body and children:
        return section + "\n\n" + children

    if not body and not children:
        return section

    if body and not children:
        return section + "\n" + body
