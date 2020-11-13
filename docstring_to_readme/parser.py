import ast
from collections import namedtuple
from typing import List


# https://gabrielelanaro.github.io/blog/2014/12/12/extract-docstrings.html


fnc_example = namedtuple(
    "fnc_example", ["name", "example"]
)


filename = "docstring_to_readme/temp.py"


# side-effecting functions
# ---------------------------------------------------------
def file_as_ast(filename: str) -> ast.Module:
    with open(filename) as fd:
        file_contents = fd.read()
    return ast.parse(file_contents)


# level
# ---------------------------------------------------------
def get_fncs_and_docstrs(
    module: ast.Module,
) -> List[fnc_example]:
    fncs = functions_from_ast(module)

    return [
        fnc_example(fnc_name(fnc), fnc_exampleing(fnc))
        for fnc in fncs
    ]


# functions that operate on AST objects
# ---------------------------------------------------------
"""
Functions should define a README section like `### fnc_name`
"""

def functions_from_ast(
    module: ast.Module,
) -> List[ast.FunctionDef]:
    return [
        node
        for node in module.body
        if isinstance(node, ast.FunctionDef)
    ]


def fnc_name(fnc: ast.FunctionDef) -> str:
    return fnc.name


def fnc_exampleing(fnc: ast.FunctionDef, dialect: str = "rst") -> str:
    return example_from_docstring(
        ast.get_docstring(fnc),
        dialect
    )


# functions that operate on fnc_example objects
# ---------------------------------------------------------
"""
These functions should do something to convert a
`fnc_example` to a section in a markdown README, possibly
including a way to create a link to that section
"""


# functions that operate on docstrings
# ---------------------------------------------------------
def example_from_docstring(
    docstring: str, dialect: str
) -> str:
    if dialect == "rst":
        return rst(docstring)
    else:
        raise NotImplemented(
            "Dialect '{}' not implemented".format(dialect)
        )


def rst(docstring: str) -> str:
    examples_block = "Examples:"
    hlite = ".. highlight::"
    cbloc = ".. code-block::"

    if not docstring:
        return ""

    if examples_block not in docstring:
        return ""

    examples = docstring.split(examples_block)[1]

    lines_wo_rst = [
        line
        for line in examples.split("\n")
        if hlite not in line and cbloc not in line
    ]

    block_indent = None
    for line in lines_wo_rst:
        if not line:
            continue
        block_indent = len(line) - len(line.lstrip())
        break
    
    output = []
    for line in lines_wo_rst:
        if line == "":  # must be a newline
            output.append(line)
            continue

        indent = len(line) - len(line.lstrip())

        if indent < block_indent:
            break

        if indent >= block_indent:
            output.append(line[block_indent:])

    return "\n".join(output).strip()
