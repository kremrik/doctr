from docstring_to_readme import graph as g


def replace_at_root(graph1: dict, graph2: dict) -> dict:
    if not graph1:
        return graph2

    if not graph2:
        return graph1

    # if graphs are the same, return left
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
    add_graph2 = True
    for child in g.node_children(graph1):
        res = replace_at_root(child, graph2)
        if res and g.truth_value(res):
            children.append(res)
            add_graph2 = False

        elif res and not g.truth_value(res):
            add_graph2 = False
        else:
            children.append(child)

    if add_graph2 and g.gt(graph2, graph1):
        children.append(graph2)

    return g.node(
        section=g.node_section(graph1),
        pretty_section=g.node_p_section(graph1),
        body=g.node_body(graph1),
        children=children,
    )
