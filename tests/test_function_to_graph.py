from docstring_to_readme.parsers.function_to_graph import (
    function_to_graph,
)
import ast
import unittest


ONE_FNC_NO_DOCSTRING = ast.parse(
    """
def fnc(x):
    print(x)
"""
).body[0]

ONE_FNC_W_DOCSTRING_NO_EXAMPLE = ast.parse(
    """
def fnc(x):
    '''This fnc does things'''
    print(x)
"""
).body[0]

ONE_FNC_W_DOCSTRING_W_EXAMPLE = ast.parse(
    """
def fnc(x):
    '''This fnc does things
    
    Examples:
        >>> from foo import bar
    '''
    print(x)
"""
).body[0]


class test_function_to_graph(unittest.TestCase):
    def test_module_with_one_fnc_no_docstrings(self):
        module = ONE_FNC_NO_DOCSTRING
        level = 4
        gold = {}
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_no_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_NO_EXAMPLE
        level = 4
        gold = {
            "section": "#### fnc",
            "pretty_section": "#### fnc",
            "body": "This fnc does things",
            "children": [],
        }
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_w_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_W_EXAMPLE
        level = 4
        gold = {
            "section": "#### fnc",
            "pretty_section": "#### fnc",
            "body": "This fnc does things\n```python\n>>> from foo import bar\n```",
            "children": [],
        }
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
