from docstring_to_readme import graph as g


def replace_at_root(graph1: dict, graph2: dict) -> dict:
    if graph1 == graph2:
        return {}

    if not contains(graph1, graph2):
        children = g.node_children(graph1)
        children.append(graph2)

        return g.node(
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
    if g.node_p_section(remove_from) == g.node_p_section(
        target_node
    ):
        return {}

    children = g.node_children(remove_from)
    new_children = []

    for child in children:
        res = remove_node(child, target_node)
        if res:
            new_children.append(res)

        return g.node(
            section=g.node_section(remove_from),
            body=g.node_body(remove_from),
            children=new_children,
        )

    return remove_from


def update_node(
    update_in: dict, target_node: dict
) -> dict:
    if g.node_p_section(update_in) == g.node_p_section(
        target_node
    ):
        return target_node

    children = g.node_children(update_in)
    new_children = []

    for child in children:
        res = update_node(child, target_node)
        new_children.append(res)

        return g.node(
            section=g.node_section(update_in),
            body=g.node_body(update_in),
            children=new_children,
        )
