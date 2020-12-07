from docstring_to_readme import graph as g


def replace_at_root(graph1: dict, graph2: dict) -> dict:
    if graph1 == graph2:
        return graph1

    res = _replace_at_root(graph1, graph2)
    if res == graph1:
        children = g.node_children(graph1)
        children.append(graph2)

        return g.node(
            section=g.node_section(graph1),
            pretty_section=g.node_p_section(graph1),
            body=g.node_body(graph1),
            children=children,
        )

    return res


def _replace_at_root(graph1: dict, graph2: dict) -> dict:
    if graph1 == graph2:
        return graph1

    # if pretty_section's are the same, replace with right
    if g.node_p_section(graph1) == g.node_p_section(
        graph2
    ):
        return graph2

    # graph2 less # than graph1, instant falsy return
    if g.lt(graph2, graph1):
        return {}

    # already know pretty sections don't match, and so if
    # these two graphs are on the same level, we can safely
    # assume that graph2 needs to be added
    if g.eq(graph1, graph2):
        return {}

    children = []
    for child in g.node_children(graph1):
        res = _replace_at_root(child, graph2)
        if res and g.truth_value(res):
            children.append(res)
        elif res and not g.truth_value(res):
            # "remove" node
            pass
        else:
            children.append(child)

    return g.node(
        section=g.node_section(graph1),
        pretty_section=g.node_p_section(graph1),
        body=g.node_body(graph1),
        children=children,
    )
