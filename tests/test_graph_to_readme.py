from docstring_to_readme.parsers.graph_to_readme import (
    dumps,
)
import unittest


class test_graph_to_readme(unittest.TestCase):
    def test_null_graph(self):
        graph = {}
        gold = ""
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_section_no_body_no_children(self):
        graph = {
            "section": "$root",
            "pretty_section": "$root",
            "body": "",
            "children": [
                {
                    "section": "# Title",
                    "pretty_section": "# Title",
                    "body": "",
                    "children": [],
                }
            ],
        }
        gold = "# Title"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_increasingly_nested(self):
        graph = {
            "section": "$root",
            "pretty_section": "$root",
            "body": "",
            "children": [
                {
                    "section": "# Title",
                    "pretty_section": "# Title",
                    "body": "Text",
                    "children": [
                        {
                            "section": "## Subtitle",
                            "pretty_section": "## Subtitle",
                            "body": "More text",
                            "children": [
                                {
                                    "section": "### Sub-subtitle",
                                    "pretty_section": "### Sub-subtitle",
                                    "body": "even more text",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        gold = "# Title\nText\n\n## Subtitle\nMore text\n\n### Sub-subtitle\neven more text"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_mult_same_level_children(self):
        graph = {
            "section": "$root",
            "pretty_section": "$root",
            "body": "",
            "children": [
                {
                    "section": "# Title",
                    "pretty_section": "# Title",
                    "body": "Text",
                    "children": [
                        {
                            "section": "## Subtitle",
                            "pretty_section": "## Subtitle",
                            "body": "More text",
                            "children": [],
                        },
                        {
                            "section": "## Subtitle 2",
                            "pretty_section": "## Subtitle 2",
                            "body": "even more text",
                            "children": [],
                        },
                    ],
                }
            ],
        }
        gold = "# Title\nText\n\n## Subtitle\nMore text\n\n## Subtitle 2\neven more text"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_variable_level_children(self):
        graph = {
            "section": "$root",
            "pretty_section": "$root",
            "body": "",
            "children": [
                {
                    "section": "# Title",
                    "pretty_section": "# Title",
                    "body": "Text",
                    "children": [
                        {
                            "section": "## Subtitle",
                            "pretty_section": "## Subtitle",
                            "body": "Text",
                            "children": [
                                {
                                    "section": "### Subtitle 2",
                                    "pretty_section": "### Subtitle 2",
                                    "body": "Text",
                                    "children": [],
                                }
                            ],
                        },
                        {
                            "section": "## Subtitle 3",
                            "pretty_section": "## Subtitle 3",
                            "body": "Text",
                            "children": [],
                        },
                    ],
                }
            ],
        }
        gold = "# Title\nText\n\n## Subtitle\nText\n\n### Subtitle 2\nText\n\n## Subtitle 3\nText"
        output = dumps(graph)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
