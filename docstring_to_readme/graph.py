from typing import List, Optional


# graph node abstraction
# ---------------------------------------------------------
def Node(
    section: Optional[str] = "",
    pretty_section: Optional[str] = "",
    body: Optional[str] = "",
    children: Optional[List[dict]] = None,
) -> dict:
    if not section:
        return {}

    return {
        "section": section,
        "pretty_section": pretty_section or section,
        "body": body,
        "children": children or [],
    }


# implementation-agnostic node attribute accessors
# ---------------------------------------------------------
def node_section(node: dict) -> str:
    return node["section"]


def node_p_section(node: dict) -> str:
    return node["pretty_section"]


def node_body(node: dict) -> str:
    return node["body"]


def node_children(node: dict) -> dict:
    return node["children"]


# non-mutating mutators
# ---------------------------------------------------------
def add_child(node: dict, child: dict) -> dict:
    return Node(
        section=node_section(node),
        pretty_section=node_p_section(node),
        body=node_body(node),
        children=node_children(node) + [child],
    )


def add_children(node: dict, children: List[dict]) -> dict:
    return Node(
        section=node_section(node),
        pretty_section=node_p_section(node),
        body=node_body(node),
        children=node_children(node) + children,
    )


# combinations of accessors
# ---------------------------------------------------------
def get_child_node(node: dict, section: str) -> dict:
    for child in node_children(node):
        if node_section(child) == section:
            return child
    return {}


def level(node: dict) -> int:
    sect = node_p_section(node)
    levl = sect.count("#")
    return levl


def gt(node1: dict, node2: dict) -> bool:
    return level(node1) > level(node2)


def lt(node1: dict, node2: dict) -> bool:
    return level(node1) < level(node2)


def eq(node1: dict, node2: dict) -> bool:
    return level(node1) == level(node2)


def truth_value(node: dict) -> bool:
    if not node_body(node) and not node_children(node):
        return False
    return True
