from docstring_to_readme.traverse import replace_at_root
import unittest


@unittest.skip("")
class test_replace_at_root(unittest.TestCase):
    def test_null_both(self):
        graph1 = {}
        graph2 = {}
        gold = {}
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_null_left(self):
        graph1 = {}
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

    def test_null_right(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        graph2 = {}
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

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

    def test_right_is_more_nested_than_left(self):
        graph1 = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "",
            "children": [],
        }
        gold = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    def test_same_level_different_nodes(self):
        graph1 = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "",
            "children": [],
        }
        gold = {
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    @unittest.skip("")
    def test_replace_children_that_match(self):
        graph1 = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "pretty_section": "## Subtitle 1",
                    "body": "Subtext 1",
                    "children": [],
                },
                {
                    "section": "## Subtitle 2",
                    "pretty_section": "## Subtitle 2",
                    "body": "Subtext 2",
                    "children": [],
                },
            ],
        }
        graph2 = {
            "section": "## Subtitle 1",
            "pretty_section": "## Subtitle 1",
            "body": "Different subtext 1",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "pretty_section": "## Subtitle 1",
                    "body": "Different Subtext 1",
                    "children": [],
                },
                {
                    "section": "## Subtitle 2",
                    "pretty_section": "## Subtitle 2",
                    "body": "Subtext 2",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    @unittest.skip("")
    def test_entirely_new_child_node(self):
        graph1 = {
            "section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "body": "Subtext 1",
                    "children": [],
                }
            ],
        }
        graph2 = {
            "section": "## Subtitle 2",
            "body": "Subtext 2",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "body": "Subtext 1",
                    "children": [],
                },
                {
                    "section": "## Subtitle 2",
                    "body": "Subtext 2",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)

    @unittest.skip("")
    def test_graph2_is_greater_than_graph1(self):
        """
        Purpose is to make sure that we don't add nodes to
        the graph that are "higher up" than graph1
        """

        graph1 = {
            "section": "## Title",
            "body": "Some text",
            "children": [],
        }
        graph2 = {
            "section": "# Title",
            "body": "Different text",
            "children": [],
        }
        gold = {
            "section": "## Title",
            "body": "Different text",
            "children": [],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)
        # raise error instead??

    @unittest.skip("")
    def test_graph2_gets_slotted_correctly(self):
        """
        Purpose of this is to make sure we correctly insert
        a node with awareness of "#" prefixes
        """

        graph1 = {
            "section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "body": "Subtext 1",
                    "children": [
                        {
                            "section": "### Sub-subtitle",
                            "body": "sub-subtext",
                            "children": [],
                        }
                    ],
                }
            ],
        }
        graph2 = {
            "section": "## Subtitle 2",
            "body": "Subtext 2",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "body": "Some text",
            "children": [
                {
                    "section": "## Subtitle 1",
                    "body": "Subtext 1",
                    "children": [
                        {
                            "section": "### Sub-subtitle",
                            "body": "sub-subtext",
                            "children": [],
                        }
                    ],
                },
                {
                    "section": "## Subtitle 2",
                    "body": "Subtext 2",
                    "children": [],
                },
            ],
        }
        output = replace_at_root(graph1, graph2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
