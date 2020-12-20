from doctr import graph as g
from doctr.traverse import update, contains
import unittest


class test_update(unittest.TestCase):
    def test_same_graph(self):
        graph1 = g.Node(
            section="# Title", body="Some text"
        )
        graph2 = g.Node(
            section="# Title", body="Some text"
        )
        gold = g.Node()

        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    def test_append_new_node(self):
        graph1 = g.Node(
            section="# Title",
            children=[
                g.Node(section="## Subtitle", body="text")
            ],
        )
        graph2 = g.Node(
            section="## Subtitle 2", body="text"
        )
        gold = g.Node(
            section="# Title",
            children=[
                g.Node(section="## Subtitle", body="text"),
                g.Node(
                    section="## Subtitle 2", body="text"
                ),
            ],
        )

        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    def test_remove_child_node(self):
        graph1 = g.Node(
            section="# Title",
            children=[
                g.Node(section="## Subtitle", body="text")
            ],
        )
        graph2 = g.Node(section="## Subtitle")
        gold = g.Node(section="# Title")

        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    def test_update_child_node(self):
        graph1 = g.Node(
            section="# Title",
            children=[
                g.Node(section="## Subtitle", body="text")
            ],
        )
        graph2 = g.Node(
            section="## Subtitle", body="NEW TEXT"
        )
        gold = g.Node(
            section="# Title",
            children=[
                g.Node(
                    section="## Subtitle", body="NEW TEXT"
                )
            ],
        )

        output = update(graph1, graph2)
        self.assertEqual(gold, output)


class test_contains(unittest.TestCase):
    def test_different_section_same_p_section(self):
        graph1 = g.Node(
            section="# Title", body="Some text"
        )
        graph2 = g.Node(
            section="# Title", body="Some text"
        )
        gold = True
        output = contains(graph1, graph2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
