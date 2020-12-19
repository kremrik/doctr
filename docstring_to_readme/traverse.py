from docstring_to_readme import graph as g

from copy import deepcopy


__all__ = ["update"]


def update(graph1: dict, graph2: dict) -> dict:
    if graph1 == graph2:
        return {}

    graph1 = deepcopy(graph1)

    if not contains(graph1, graph2):
        children = g.node_children(graph1)
        children.append(graph2)

        return g.Node(
            section=g.node_section(graph1),
            body=g.node_body(graph1),
            children=children,
        )

    if not g.truth_value(graph2):
        return remove_node(graph1, graph2)

    return update_node(graph1, graph2)


def contains(search_graph: dict, find_graph: dict) -> bool:
    if g.node_p_section(search_graph) == g.node_p_section(
        find_graph
    ):
        return True

    children = g.node_children(search_graph)
    for child in children:
        return contains(child, find_graph)

    return False


def remove_node(
    remove_from: dict, target_node: dict
) -> dict:
    return _modify(
        mod_graph=remove_from,
        mod_with=target_node,
        on_eq={},
    )


def update_node(
    update_in: dict, target_node: dict
) -> dict:
    return _modify(
        mod_graph=update_in,
        mod_with=target_node,
        on_eq=target_node,
    )


def _modify(
    mod_graph: dict, mod_with: dict, on_eq: dict
) -> dict:
    if g.node_p_section(mod_graph) == g.node_p_section(
        mod_with
    ):
        return on_eq

    children = g.node_children(mod_graph)
    new_children = []

    for child in children:
        res = _modify(child, mod_with, on_eq)
        if res:
            new_children.append(res)

        return g.Node(
            section=g.node_section(mod_graph),
            body=g.node_body(mod_graph),
            children=new_children,
        )

    return mod_with
