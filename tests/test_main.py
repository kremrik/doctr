from docstring_to_readme.main import (
    readme_to_sections,
    sections_to_readme,
)
import unittest


class test_readme_to_sections(unittest.TestCase):
    def test_one_heading_no_body(self):
        readme = "# Title"
        gold = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "",
            }
        ]
        output = readme_to_sections(readme)
        self.assertEqual(gold, output)

    def test_mult_heading(self):
        readme = "# Title\n## Subtitle"
        gold = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "",
            },
            {
                "heading": "## Subtitle",
                "pretty_heading": "## Subtitle",
                "body": "",
            },
        ]
        output = readme_to_sections(readme)
        self.assertEqual(gold, output)

    def test_mult_heading_with_mult_body(self):
        readme = "# Title\nText\n\n## Subtitle\nMore text"
        gold = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "Text\n",
            },
            {
                "heading": "## Subtitle",
                "pretty_heading": "## Subtitle",
                "body": "More text",
            },
        ]
        output = readme_to_sections(readme)
        self.assertEqual(gold, output)


class test_sections_to_readme(unittest.TestCase):
    def test_one_heading_no_body(self):
        readme = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "",
            }
        ]
        gold = "# Title"
        output = sections_to_readme(readme)
        self.assertEqual(gold, output)

    def test_mult_heading(self):
        readme = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "",
            },
            {
                "heading": "## Subtitle",
                "pretty_heading": "## Subtitle",
                "body": "",
            },
        ]
        gold = "# Title\n## Subtitle"
        output = sections_to_readme(readme)
        self.assertEqual(gold, output)

    def test_mult_heading_with_mult_body(self):
        readme = [
            {
                "heading": "# Title",
                "pretty_heading": "# Title",
                "body": "Text\n",
            },
            {
                "heading": "## Subtitle",
                "pretty_heading": "## Subtitle",
                "body": "More text",
            },
        ]
        gold = "# Title\nText\n\n## Subtitle\nMore text"
        output = sections_to_readme(readme)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
