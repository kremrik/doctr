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
        gold = "#### `fnc`\nno example"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_example(self):
        module = ast.parse(FNC_EXAMPLE)
        gold = "#### `fnc`\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_multi_example(self):
        module = ast.parse(MODULE_EXAMPLE)
        gold = "#### `fnc`\n\n```python\n>>> import json\n>>> print(json)\n```\n\n#### `fnc2`\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_rst_example(self):
        module = ast.parse(RST_EXAMPLE)
        gold = "#### `fnc`\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)

    def test_preamble_example(self):
        module = ast.parse(PREAMBLE_EXAMPLE)
        gold = "#### `fnc`\nThis is fnc\n\n```python\n>>> import json\n>>> print(json)\n```"
        output = module_to_sections(module)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
