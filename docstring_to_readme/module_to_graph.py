from docstring_to_readme import graph as g

import ast
import re
from typing import List, Tuple, Union


"""
Modules should break down into the following parts:
1. the module/file name should be the parent node, with any
    module-level docstrings as the body and the module name
    as the section. children will be the functions
2. each function will break into the function's name
    (mapping to section) and the Example field of the
    docstring, if any, (mapping to body)

somewhere along the line there should be an indication of
what level to begin things at (ie, what number of # should)
the module node get?)
"""


def loads(module: str) -> dict:
    if not module:
        return {}

    as_ast = module_to_ast(module)

    graphs = [
        graph
        for graph in module_to_graphs(as_ast)
        if graph
    ]

    if not graphs:
        return {}

    return graphs


def module_to_ast(module: str) -> ast.Module:
    return ast.parse(module)


def module_to_graphs(module: ast.Module) -> List[dict]:
    return [obj_to_graph(obj) for obj in module.body]


def obj_to_graph(
    obj: Union[ast.FunctionDef, ast.ClassDef]
) -> dict:
    docstring = ast.get_docstring(obj)
    preamble = preamble_from_docstring(docstring)
    example = example_from_rst_docstring(docstring)
    section = obj.name

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

    examples_block = "Examples:"
    hlite = ".. highlight::"
    cbloc = ".. code-block::"

    if not docstring:
        return ""

    if examples_block not in docstring:
        return ""

    examples = docstring.split(examples_block)[1]

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
