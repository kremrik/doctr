from docstring_to_readme import graph as g

import ast
import re
from typing import Union


def function_to_graph(
    obj: Union[ast.FunctionDef, ast.ClassDef], level: int
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
