import ast
import re
from typing import List, Tuple


# API
# ---------------------------------------------------------
def file_as_ast(filename: str) -> ast.Module:
    """
    Function to convert a file to an AST object
    """

    with open(filename) as fd:
        file_contents = fd.read()
    return ast.parse(file_contents)


def module_to_sections(module: ast.Module) -> str:
    """
    Function to convert an AST module to Markdown sections

    Examples:
        >>> from docstring_to_readme.parser import module_to_sections
        >>> import ast
        >>> module = ast.parse("def fnc():\\n    '''hello'''\\n    pass")
        >>> module_to_sections(module)
        '#### `fnc`\\nhello'
    """

    section_components = get_names_and_docstrings(module)

    sections = [
        create_section(*sc) for sc in section_components
    ]

    return "\n\n".join([s for s in sections if s])


# get names and docstrings from ast object
# ---------------------------------------------------------
def get_names_and_docstrings(
    module: ast.Module,
) -> List[Tuple[str, str]]:
    functions = functions_from_ast(module)

    return [
        (fnc_name(fnc), fnc_docstring(fnc))
        for fnc in functions
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


def fnc_docstring(fnc: ast.FunctionDef) -> str:
    return ast.get_docstring(fnc)


# function to create a section from name and docstring
# ---------------------------------------------------------
def create_section(name: str, docstring: str) -> str:
    header = name_to_title(name)
    preamble = preamble_from_docstring(docstring)
    codeblock = example_to_codeblock(docstring)

    if not preamble and not codeblock:
        return ""

    if preamble and not codeblock:
        return header + "\n" + preamble

    if codeblock and not preamble:
        return header + "\n\n" + codeblock

    return header + "\n" + preamble + "\n\n" + codeblock


def name_to_title(name: str, indent: int = 4) -> str:
    section = "#" * indent + " "
    return section + "`{}`".format(name)


def example_to_codeblock(docstring: str) -> str:
    example = example_from_docstring(docstring)

    if not example:
        return ""

    before = "```python\n"
    after = "\n```"
    return before + example + after


# functions that operate on docstrings
# ---------------------------------------------------------
# https://stackoverflow.com/questions/13209288/split-string-based-on-regex
RST_BLOCKS = re.compile(r"[\n](?=[A-Z][a-z]+:\n)")
RST_SECTION = re.compile(r"[A-Z][a-z]+:\n")


def preamble_from_docstring(docstring: str) -> str:
    if not docstring:
        return ""

    split_by_block = RST_BLOCKS.split(docstring)
    first_chunk = split_by_block[0]

    if RST_SECTION.match(first_chunk):
        return ""
    return first_chunk.strip()


def example_from_docstring(
    docstring: str, dialect: str = "rst"
) -> str:
    if dialect == "rst":
        return rst_example(docstring)
    else:
        raise NotImplementedError(
            "Dialect '{}' not implemented".format(dialect)
        )


def rst_example(docstring: str) -> str:
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
    return output
