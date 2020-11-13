from docstring_to_readme.parser import example_from_docstring
import unittest


class test_example_from_docstring(unittest.TestCase):

    def test_no_defined(self):
        docstring = 'No examples!'
        gold = ''
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_one_line(self):
        docstring = 'Examples:\n    >>> import json\n'
        gold = '>>> import json'
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_multi_line(self):
        docstring = 'Examples:\n    >>> import json\n    >>> print(json)\n'
        gold = '>>> import json\n>>> print(json)'
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_multi_line_with_extra_indents(self):
        docstring = 'Examples:\n    >>> for i in [1, 2]:\n    ... print(i)\n'
        gold = '>>> for i in [1, 2]:\n... print(i)'
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_simple_with_extra_rst_formatters(self):
        docstring = 'Examples:\n    .. highlight:: python\n    .. code-block:: python\n\n        >>> import json'
        gold = '>>> import json'
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
