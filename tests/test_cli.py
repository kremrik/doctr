from docstring_to_readme.cli import (
    overwrite_at_pos,
    create_or_append_to_readme,
)
import unittest


README = """# Title

## Sub-heading 1 1
Words

## Sub-heading 1 2
More words

### Sub-heading 2
Definitely more words

### Sub-heading 2
Wow, more words"""


class test_overwrite_at_pos(unittest.TestCase):
    def test(self):
        section = "# Title"
        gold = 0
        output = overwrite_at_pos(section, README)
        self.assertEqual(gold, output)


class test_create_or_append_to_readme(unittest.TestCase):
    def test(self):
        section = "#### Sub-heading 4"
        gold = README + "\n\n" + section
        output = create_or_append_to_readme(
            section, README
        )
        self.assertEqual(gold, output)

    def test_with_overwrite_at(self):
        section = "#### Sub-heading 4"
        append_at = 2
        gold = "# Title" + "\n\n" + section
        output = create_or_append_to_readme(
            section, README, append_at
        )
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
