from docstring_to_readme.parser import (
    module_to_sections,
    example_from_docstring,
    example_to_codeblock,
    name_to_title,
)
import ast
import unittest


FNC_NO_EXAMPLE = '''
def fnc():
    """no example"""
    pass
'''


FNC_EXAMPLE = '''
def fnc():
    """
    Examples:
        >>> import json
        >>> print(json)
    """
    pass
'''

MODULE_EXAMPLE = '''
def fnc():
    """
    Examples:
        >>> import json
        >>> print(json)
    """
    pass

def fnc2():
    """
    Examples:
        >>> import json
        >>> print(json)
    """
    pass
'''

RST_EXAMPLE = '''
def fnc():
    """
    Examples:
        .. highlight:: python
        .. code-block:: python

            >>> import json
            >>> print(json)

    Args:
        text

    Returns:
        text
    """
    pass
'''

PREAMBLE_EXAMPLE = '''
def fnc():
    """
    This is fnc

    Examples:
        >>> import json
        >>> print(json)
    """
    pass
'''


class test_module_to_sections(unittest.TestCase):
    def test_wo_example(self):
        module = ast.parse(FNC_NO_EXAMPLE)
        gold = "### fnc\nno example"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_example(self):
        module = ast.parse(FNC_EXAMPLE)
        gold = "### fnc\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_multi_example(self):
        module = ast.parse(MODULE_EXAMPLE)
        gold = "### fnc\n\n```python\n>>> import json\n>>> print(json)\n```\n\n### fnc2\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_rst_example(self):
        module = ast.parse(RST_EXAMPLE)
        gold = "### fnc\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_preamble_example(self):
        module = ast.parse(PREAMBLE_EXAMPLE)
        gold = "### fnc\nThis is fnc\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)


@unittest.skip("implementation details")
class test_example_from_docstring(unittest.TestCase):
    def test_no_defined(self):
        docstring = "No examples!"
        gold = ""
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_one_line(self):
        docstring = "Examples:\n    >>> import json\n"
        gold = ">>> import json"
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_multi_line(self):
        docstring = "Examples:\n    >>> import json\n    >>> print(json)\n"
        gold = ">>> import json\n>>> print(json)"
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_multi_line_with_extra_indents(self):
        docstring = "Examples:\n    >>> for i in [1, 2]:\n    ... print(i)\n"
        gold = ">>> for i in [1, 2]:\n... print(i)"
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)

    def test_simple_with_extra_rst_formatters(self):
        docstring = "Examples:\n    .. highlight:: python\n    .. code-block:: python\n\n        >>> import json"
        gold = ">>> import json"
        output = example_from_docstring(docstring, "rst")
        self.assertEqual(gold, output)


@unittest.skip("implementation details")
class test_example_to_codeblock(unittest.TestCase):
    def test(self):
        example = ">>> import json"
        gold = "```python\n>>> import json\n```"
        output = example_to_codeblock(example)
        self.assertEqual(gold, output)


@unittest.skip("implementation details")
class test_name_to_title(unittest.TestCase):
    def test(self):
        name = "cool_fnc"
        gold = "### cool_fnc"
        output = name_to_title(name, 3)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
