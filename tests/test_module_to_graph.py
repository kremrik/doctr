from docstring_to_readme.module_to_graph import loads
import unittest


EMPTY_MODULE = ""

ONE_FNC_NO_DOCSTRING = """
def fnc(x):
    print(x)
"""

ONE_FNC_W_DOCSTRING_NO_EXAMPLE = """
def fnc(x):
    '''This fnc does things'''
    print(x)
"""

ONE_FNC_W_DOCSTRING_W_EXAMPLE = """
def fnc(x):
    '''This fnc does things
    
    Examples:
        >>> from foo import bar
    '''
    print(x)
"""


class test_loads(unittest.TestCase):
    def test_empty_module(self):
        module = EMPTY_MODULE
        gold = {}
        output = loads(module)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_no_docstrings(self):
        module = ONE_FNC_NO_DOCSTRING
        gold = {}
        output = loads(module)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_no_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_NO_EXAMPLE
        gold = [
            {
                "section": "fnc",
                "pretty_section": "fnc",
                "body": "This fnc does things",
                "children": [],
            }
        ]
        output = loads(module)
        self.assertEqual(gold, output)

    def test_module_with_one_fnc_w_docstring_w_example(
        self,
    ):
        module = ONE_FNC_W_DOCSTRING_W_EXAMPLE
        gold = [
            {
                "section": "fnc",
                "pretty_section": "fnc",
                "body": "This fnc does things\n```python\n>>> from foo import bar\n```",
                "children": [],
            }
        ]
        output = loads(module)
        print(output)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
