import ast
from ast import get_docstring
from collections import namedtuple
from typing import List


# https://gabrielelanaro.github.io/blog/2014/12/12/extract-docstrings.html


fnc_example = namedtuple(
    "fnc_example", ["name", "example"]
)


# API
# ---------------------------------------------------------
def file_as_ast(filename: str) -> ast.Module:
    with open(filename) as fd:
        file_contents = fd.read()
    return ast.parse(file_contents)


def module_to_sections(module: ast.Module) -> str:
    fncs = get_fncs_and_docstrs(module)
    sections = []

    for fnc in fncs:
        section = create_section(fnc)
        if section:
            sections.append(section)

    return "\n\n".join(sections)


# functions that operate on AST objects
# ---------------------------------------------------------
def get_fncs_and_docstrs(
    module: ast.Module,
) -> List[fnc_example]:
    fncs = functions_from_ast(module)

    return [
        fnc_example(fnc_name(fnc), fnc_docstring(fnc))
        for fnc in fncs
    ]


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


def fnc_docstring(
    fnc: ast.FunctionDef, dialect: str = "rst"
) -> str:
    return example_from_docstring(
        ast.get_docstring(fnc), dialect
    )


# functions that operate on fnc_example objects
# ---------------------------------------------------------
"""
These functions should do something to convert a
`fnc_example` to a section in a markdown README, possibly
including a way to create a link to that section
"""


def create_section(sect_obj: fnc_example) -> str:
    header = name_to_title(sect_obj.name, indent=3)
    codeblock = example_to_codeblock(sect_obj.example)

    if not codeblock:
        return ""

    return header + "\n" + codeblock


def example_to_codeblock(example: str) -> str:
    if not example:
        return ""

    before = "```python\n"
    after = "\n```"
    return before + example + after


def name_to_title(name: str, indent: int) -> str:
    section = "#" * indent + " "
    return section + name


# functions that operate on docstrings
# ---------------------------------------------------------
def example_from_docstring(
    docstring: str, dialect: str
) -> str:
    if dialect == "rst":
        return rst(docstring)
    else:
        raise NotImplementedError(
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
