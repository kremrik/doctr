from docstring_to_readme.readme_to_graph import loads
import unittest


class test_readme_to_graph(unittest.TestCase):
    def test_null_readme(self):
        readme = ""
        gold = {
            "section": "$root",
            "pretty_section": "$root",
            "body": "",
            "children": [],
        }
        output = loads(readme)
        self.assertEqual(gold, output)

    @unittest.skip("")
    def test_no_section_with_body(self):
        # TODO: this behavior might need to change
        readme = "Some text"
        gold = {}
        output = loads(readme)
        self.assertEqual(gold, output)

    def test_section_no_body_no_children(self):
        readme = "# Title"
        gold = {
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
        output = loads(readme)
        print(output)
        self.assertEqual(gold, output)

    def test_increasingly_nested(self):
        readme = "# Title\nText\n\n## Subtitle\nMore text\n\n### Sub-subtitle\neven more text"
        gold = {
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
        output = loads(readme)
        print(output)
        self.assertEqual(gold, output)

    def test_mult_same_level_children(self):
        readme = "# Title\nText\n\n## Subtitle\nMore text\n\n## Subtitle 2\neven more text"
        gold = {
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
        output = loads(readme)
        self.assertEqual(gold, output)

    def test_variable_level_children(self):
        readme = "# Title\nText\n\n## Subtitle\nText\n\n### Subtitle 2\nText\n\n## Subtitle 3\nText"
        gold = {
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
        output = loads(readme)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
