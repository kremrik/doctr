from doctr import graph as g
from doctr.parsers.graph_to_readme import (
    dumps,
)
import unittest


class test_graph_to_readme(unittest.TestCase):
    def test_null_graph(self):
        graph = g.Node()
        gold = ""
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_section_no_body_no_children(self):
        graph = g.Node(
            section="$root",
            children=[g.Node(section="# Title")],
        )
        gold = "# Title"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_increasingly_nested(self):
        graph = g.Node(
            section="$root",
            children=[
                g.Node(
                    section="# Title",
                    body="Text",
                    children=[
                        g.Node(
                            section="## Subtitle",
                            body="More text",
                            children=[
                                g.Node(
                                    section="### Sub-subtitle",
                                    body="even more text",
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        gold = "# Title\nText\n\n## Subtitle\nMore text\n\n### Sub-subtitle\neven more text"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_mult_same_level_children(self):
        graph = g.Node(
            section="$root",
            children=[
                g.Node(
                    section="# Title",
                    body="Text",
                    children=[
                        g.Node(
                            section="## Subtitle",
                            body="More text",
                        ),
                        g.Node(
                            section="## Subtitle 2",
                            body="even more text",
                        ),
                    ],
                )
            ],
        )
        gold = "# Title\nText\n\n## Subtitle\nMore text\n\n## Subtitle 2\neven more text"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_variable_level_children(self):
        graph = g.Node(
            section="$root",
            children=[
                g.Node(
                    section="# Title",
                    body="Text",
                    children=[
                        g.Node(
                            section="## Subtitle",
                            body="Text",
                            children=[
                                g.Node(
                                    section="### Subtitle 2",
                                    body="Text",
                                )
                            ],
                        ),
                        g.Node(
                            section="## Subtitle 3",
                            body="Text",
                        ),
                    ],
                )
            ],
        )
        gold = "# Title\nText\n\n## Subtitle\nText\n\n### Subtitle 2\nText\n\n## Subtitle 3\nText"
        output = dumps(graph)
        self.assertEqual(gold, output)

    def test_variable_children_of_root(self):
        graph = g.Node(
            section="$root",
            children=[
                g.Node(
                    section="# Title",
                    children=[
                        g.Node(
                            section="## Purpose",
                            body="test",
                        )
                    ],
                ),
                g.Node(
                    section="### temp",
                    body="Top level docstring",
                    children=[
                        g.Node(
                            section="#### bar",
                            body="this is bar",
                        ),
                        g.Node(
                            section="#### baz",
                            body="this is baz\n```python\n>>> from temp import baz\n```",
                        ),
                    ],
                ),
            ],
        )
        gold = "# Title\n\n## Purpose\ntest\n\n### temp\nTop level docstring\n\n#### bar\nthis is bar\n\n#### baz\nthis is baz\n```python\n>>> from temp import baz\n```"
        output = dumps(graph)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
