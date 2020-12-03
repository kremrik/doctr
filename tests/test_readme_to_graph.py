from docstring_to_readme.readme_to_graph import loads
import unittest


@unittest.skip("")
class test_readme_to_graph(unittest.TestCase):
    def test_null_readme(self):
        readme = ""
        gold = {}
        output = loads(readme)
        self.assertEqual(gold, output)

    def test_section_no_body_no_children(self):
        readme = "# Title"
        gold = {"# Title": {"body": "", "children": {}}}
        output = loads(readme)
        self.assertEqual(gold, output)

    def test_no_section_with_body(self):
        # TODO: this behavior might need to change
        readme = "Some text"
        gold = {}
        output = loads(readme)
        self.assertEqual(gold, output)

    def test_section_with_body_no_children(self):
        readme = "# Title\nSome text"
        gold = {
            "# Title": {
                "body": "Some text",
                "children": {},
            }
        }
        output = loads(readme)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
