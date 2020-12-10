from docstring_to_readme.traverse import update
import unittest


class test_update(unittest.TestCase):

    # @unittest.skip("")
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
        gold = {}
        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    # @unittest.skip("")
    def test_append_new_node(self):
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
        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    # @unittest.skip("")
    def test_remove_child_node(self):
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
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "",
            "children": [],
        }
        gold = {
            "section": "# Title",
            "pretty_section": "# Title",
            "body": "",
            "children": [],
        }
        output = update(graph1, graph2)
        self.assertEqual(gold, output)

    # @unittest.skip("")
    def test_update_child_node(self):
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
            "section": "## Subtitle",
            "pretty_section": "## Subtitle",
            "body": "NEW TEXT",
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
                    "body": "NEW TEXT",
                    "children": [],
                }
            ],
        }
        output = update(graph1, graph2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
