from docstring_to_readme import graph as g


def replace_at_root(graph1: dict, graph2: dict) -> dict:
    # cases not involving child nodes
    # -------------------------------
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

    # CASE 1: graph2 more # than graph1
    if g.gt(graph2, graph1):
        return graph1

    for child in g.node_children(graph1):
        # CASE 2: graph2 needs to replace a child of graph1
        # CASE 3: graph2 needs to be added as a child of graph1
        pass
