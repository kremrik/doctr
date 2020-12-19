from docstring_to_readme import graph as g
from docstring_to_readme.parsers.readme_to_graph import (
    readme_to_graph,
)
import unittest


class test_readme_to_graph(unittest.TestCase):
    def test_null_readme(self):
        readme = ""
        gold = g.Node(section="$root")
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)

    @unittest.skip("")
    def test_no_section_with_body(self):
        # TODO: this behavior might need to change
        readme = "Some text"
        gold = {}
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)

    def test_section_no_body_no_children(self):
        readme = "# Title"
        gold = g.Node(
            section="$root",
            children=[g.Node(section="# Title")],
        )
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)

    def test_increasingly_nested(self):
        readme = "# Title\nText\n\n## Subtitle\nMore text\n\n### Sub-subtitle\neven more text"
        gold = g.Node(
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
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)

    def test_mult_same_level_children(self):
        readme = "# Title\nText\n\n## Subtitle\nMore text\n\n## Subtitle 2\neven more text"
        gold = g.Node(
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
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)

    def test_variable_level_children(self):
        readme = "# Title\nText\n\n## Subtitle\nText\n\n### Subtitle 2\nText\n\n## Subtitle 3\nText"
        gold = g.Node(
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
        output = readme_to_graph(readme)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
