from docstring_to_readme.graph import (
    node,
    node_section,
    node_body,
    node_children,
)
import unittest


class test_node(unittest.TestCase):
    def test_falsy_bool(self):
        graph = node()
        self.assertFalse(graph)

    def test_truthy_bool(self):
        graph = node("# Title")
        self.assertTrue(graph)

    def test_falsy_equality(self):
        g1 = node()
        g2 = node()
        self.assertEqual(g1, g2)

    def test_truthy_equality(self):
        g1 = node("# Title")
        g2 = node("# Title")
        self.assertEqual(g1, g2)

    def test_truthy_equality_with_children(self):
        g1 = node("# Title", children=node("## Subtitle"))
        g2 = node("# Title", children=node("## Subtitle"))
        self.assertEqual(g1, g2)

    def test_falsy_equality_with_children(self):
        g1 = node("# Title", children=node("## Subtitle"))
        g2 = node("# Title", children=node("## OOPS"))
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
