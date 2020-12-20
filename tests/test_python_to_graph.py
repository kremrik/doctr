from doctr import graph as g
from doctr.parsers.python_to_graph import (
    ast_to_graph,
    function_to_graph,
)
import ast
import unittest


EMPTY_MODULE = ast.parse("""""")

ONE_FNC_NO_PREAMBLE = ast.parse(
    """
def test(x):
    '''some text'''
    pass
"""
)

TWO_FNC_W_PREAMBLE = ast.parse(
    """
'''this is an intro'''

def test(x):
    '''some text'''
    pass

def test2(x):
    '''some text2'''
    pass
"""
)


class test_ast_to_graph(unittest.TestCase):
    def test_empty_module(self):
        module = EMPTY_MODULE
        name = "test"
        level = 3
        gold = g.Node()
        output = ast_to_graph(module, name, level)
        self.assertEqual(gold, output)

    def test_one_fnc_no_preamble(self):
        module = ONE_FNC_NO_PREAMBLE
        name = "module"
        level = 3
        gold = g.Node(
            section="### module",
            children=[
                g.Node(
                    section="#### test", body="some text"
                )
            ],
        )
        output = ast_to_graph(module, name, level)
        self.assertEqual(gold, output)

    def test_two_fnc_w_preamble(self):
        module = TWO_FNC_W_PREAMBLE
        name = "module"
        level = 3
        gold = g.Node(
            section="### module",
            body="this is an intro",
            children=[
                g.Node(
                    section="#### test", body="some text"
                ),
                g.Node(
                    section="#### test2", body="some text2"
                ),
            ],
        )
        output = ast_to_graph(module, name, level)
        self.assertEqual(gold, output)


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

ONE_FNC_W_DOCSTRING_W_EXAMPLES = ast.parse(
    """
def fnc(x):
    '''This fnc does things
    
    Examples:
        >>> from foo import bar
    '''
    print(x)
"""
).body[0]

ONE_FNC_W_DOCSTRING_W_EXAMPLE = ast.parse(
    """
def fnc(x):
    '''This fnc does things
    
    Example:
        >>> from foo import bar
    '''
    print(x)
"""
).body[0]


class test_function_to_graph(unittest.TestCase):
    def test_module_with_one_fnc_no_docstrings(self):
        module = ONE_FNC_NO_DOCSTRING
        level = 4
        gold = g.Node()
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_no_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_NO_EXAMPLE
        level = 4
        gold = g.Node(
            section="#### fnc", body="This fnc does things"
        )
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_w_examples(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_W_EXAMPLES
        level = 4
        gold = g.Node(
            section="#### fnc",
            body="This fnc does things\n```python\n>>> from foo import bar\n```",
        )
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_w_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_W_EXAMPLE
        level = 4
        gold = g.Node(
            section="#### fnc",
            body="This fnc does things\n```python\n>>> from foo import bar\n```",
        )
        output = function_to_graph(module, level)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
