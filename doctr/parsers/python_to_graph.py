from doctr import graph as g

import ast
import re
from typing import List, Optional
from os import listdir
from os.path import (
    abspath,
    basename,
    splitext,
    isdir,
    isfile,
    join,
)


# convert anything
# ---------------------------------------------------------
def python_to_graph(path: str, level: int) -> dict:
    if isdir(path):
        section = splitext(basename(path))[0]
        section = "#" * level + " " + section

        children = [
            python_to_graph(child, level + 1)
            for child in abs_listdir(path)
        ]
        children = [child for child in children if child]

        if children:
            return g.Node(
                section=section, children=children
            )

    if isfile(path):
        return module_to_graph(path, level)


def abs_listdir(path: str) -> List[Optional[str]]:
    try:
        list_dir = listdir(path)
    except FileNotFoundError:
        print(f"The package '{path}' does not exist")
        exit(1)  # TODO: appropriate here?

    py_files = [
        f
        for f in list_dir
        if f.endswith(".py") or isdir(f)
    ]

    abs_path_py_files = [
        join(abspath(path), f) for f in py_files
    ]

    if abs_path_py_files:
        return abs_path_py_files

    return []


# convert module
# ---------------------------------------------------------
def module_to_graph(path: str, level: int) -> dict:
    name = splitext(basename(path))[0]
    module = read_module(path)

    if not module.body:
        return {}

    output = ast_to_graph(
        module=module, name=name, level=level
    )

    return output


def read_module(path: str) -> ast.Module:
    try:
        with open(path, "r") as m:
            return module_to_ast(m.read())
    except FileNotFoundError:
        print(f"Module '{path}' does not exist")
        exit(1)


def module_to_ast(module: str) -> ast.Module:
    return ast.parse(module)


def ast_to_graph(
    module: ast.Module, name: str, level: int
) -> dict:
    section = "#" * level + " " + name

    children = [
        graph
        for graph in convert_objects(module, level + 1)
        if graph
    ]

    body = module_preamble(module)

    if not children and not body:
        return {}

    if not body:
        return g.Node(section=section, children=children)

    return g.Node(
        section=section, body=body, children=children
    )


def module_preamble(module: ast.Module) -> str:
    filt = [
        a
        for a in [
            obj
            for obj in module.body
            if isinstance(obj, ast.Expr)
        ]
        if isinstance(a.value, ast.Str)
    ]

    if not filt:
        return ""

    return filt[0].value.s.strip()


def convert_objects(
    module: ast.Module, level: int
) -> List[dict]:
    # this should handle classes, too
    return [
        function_to_graph(obj, level)
        for obj in module.body
        if isinstance(obj, ast.FunctionDef)
    ]


# convert function
# ---------------------------------------------------------
def function_to_graph(
    obj: ast.FunctionDef, level: int
) -> dict:
    docstring = ast.get_docstring(obj)
    preamble = preamble_from_docstring(docstring)
    example = example_from_rst_docstring(docstring)
    section = obj.name
    section = "#" * level + " " + section

    if not preamble and not example:
        return {}

    if preamble and not example:
        return g.Node(section=section, body=preamble)

    body = preamble + "\n" + example
    return g.Node(section=section, body=body)


def preamble_from_docstring(docstring: str) -> str:
    """
    Return falsy if nothing found at top of docstring
    """

    # https://stackoverflow.com/questions/13209288/split-string-based-on-regex
    RST_BLOCKS = re.compile(r"[\n](?=[A-Z][a-z]+:\n)")
    RST_SECTION = re.compile(r"[A-Z][a-z]+:\n")

    if not docstring:
        return ""

    split_by_block = RST_BLOCKS.split(docstring)
    first_chunk = split_by_block[0]

    if RST_SECTION.match(first_chunk):
        return ""
    return first_chunk.strip()


def example_from_rst_docstring(docstring: str) -> str:
    """
    Return falsy if no `Examples:` block found
    """

    examples_blocks = ["Example:", "Examples:"]
    hlite = ".. highlight::"
    cbloc = ".. code-block::"

    if not docstring:
        return ""

    example_exists = [
        example in docstring for example in examples_blocks
    ]
    pick_block = [
        idx for idx, e in enumerate(example_exists) if e
    ]

    if not pick_block:
        return ""
    else:
        example_block = examples_blocks[pick_block[0]]

    examples = docstring.split(example_block)[1]

    lines_wo_rst_example = [
        line
        for line in examples.split("\n")
        if hlite not in line and cbloc not in line
    ]

    block_indent = None
    for line in lines_wo_rst_example:
        if not line:
            continue
        block_indent = len(line) - len(line.lstrip())
        break

    output = []
    for line in lines_wo_rst_example:
        if line == "":  # must be a newline
            output.append(line)
            continue

        indent = len(line) - len(line.lstrip())

        if indent < block_indent:
            break

        if indent >= block_indent:
            output.append(line[block_indent:])

    output = "\n".join(output).strip()

    return "```python\n" + output + "\n```"
