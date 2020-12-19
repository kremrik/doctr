from docstring_to_readme import graph as g
from docstring_to_readme.parsers.module_to_graph import (
    ast_to_graph,
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


if __name__ == "__main__":
    unittest.main()
