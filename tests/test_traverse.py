from docstring_to_readme.traverse import replace_at_root
import unittest
from json import dumps


class test_replace_at_root(unittest.TestCase):
    def test_same_graph(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_right_replaces_left(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Different text",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Different text",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_right_is_less_nested_than_left(self):
        graph1 = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "some text",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "some text",
            "children": [],
        }
        gold = {}
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_child_node_inserted(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [],
                }
            ],
        }
        graph2 = {
            "section": "## Subtitle 2",
            "pretty_section": "## Subtitle 2",
            "body": "text",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [],
                },
                {
                    "section": "## Subtitle 2",
                    "pretty_section": "## Subtitle 2",
                    "body": "text",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_child_node_replaced(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "old",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        graph2 = {
            "section": "### Subtitle",
            "pretty_section": "### Subtitle",
            "body": "NEW",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "NEW",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_child_node_added_at_end_deep_nesting(self):
        """
        If we encounter a brand new node, the desired
        behavior is to append to the end of the root
        graph's children
        """

        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "text",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        graph2 = {
            "section": "### Subtitle 2",
            "pretty_section": "### Subtitle 2",
            "body": "text",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "text",
                            "children": [],
                        },
                    ],
                },
                {
                    "section": "### Subtitle 2",
                    "pretty_section": "### Subtitle 2",
                    "body": "text",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_child_node_added_at_end_deep_middle(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "text",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        graph2 = {
            "section": "## Subtitle 2",
            "pretty_section": "## Subtitle 2",
            "body": "text",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "text",
                            "children": [],
                        }
                    ],
                },
                {
                    "section": "## Subtitle 2",
                    "pretty_section": "## Subtitle 2",
                    "body": "text",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_falsy_child_node_removed(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [
                {
                    "section": "## Subtitle",
                    "pretty_section": "## Subtitle",
                    "body": "text",
                    "children": [
                        {
                            "section": "### Subtitle",
                            "pretty_section": "### Subtitle",
                            "body": "text",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        graph2 = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "text",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
