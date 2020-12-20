from doctr.graph import (
    Node,
    node_section,
    node_body,
    node_children,
)
import unittest


class test_node(unittest.TestCase):
    def test_falsy_bool(self):
        graph = Node()
        self.assertFalse(graph)

    def test_truthy_bool(self):
        graph = Node("# Title")
        self.assertTrue(graph)

    def test_falsy_equality(self):
        g1 = Node()
        g2 = Node()
        self.assertEqual(g1, g2)

    def test_truthy_equality(self):
        g1 = Node("# Title")
        g2 = Node("# Title")
        self.assertEqual(g1, g2)

    def test_truthy_equality_with_children(self):
        g1 = Node("# Title", children=Node("## Subtitle"))
        g2 = Node("# Title", children=Node("## Subtitle"))
        self.assertEqual(g1, g2)

    def test_falsy_equality_with_children(self):
        g1 = Node("# Title", children=Node("## Subtitle"))
        g2 = Node("# Title", children=Node("## OOPS"))
        self.assertNotEqual(g1, g2)


class test_getters(unittest.TestCase):

    graph = {
        "section": "# Title",
        "body": "Some text",
        "children": [
            {
                "section": "## Subtitle",
                "body": "Some subtext",
                "children": [],
            }
        ],
    }

    def test_section(self):
        gold = "# Title"
        output = node_section(self.graph)
        self.assertEqual(gold, output)

    def test_body(self):
        gold = "Some text"
        output = node_body(self.graph)
        self.assertEqual(gold, output)

    def test_children(self):
        gold = [
            {
                "section": "## Subtitle",
                "body": "Some subtext",
                "children": [],
            }
        ]
        output = node_children(self.graph)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
