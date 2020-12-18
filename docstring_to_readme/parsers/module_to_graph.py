from docstring_to_readme import graph as g
from docstring_to_readme.parsers.function_to_graph import (
    function_to_graph,
)

import ast
from typing import List
from os.path import basename, splitext


__all__ = ["module_to_graph"]


def module_to_graph(path: str, level: int = 3) -> dict:
    name = splitext(basename(path))[0]
    module = read_module(path)

    if not module.body:
        return {}

    return ast_to_graph(
        module=module, name=name, level=level
    )


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
        obj
        for obj in module.body
        if isinstance(obj, ast.Expr)
    ]

    if not filt:
        return ""

    return filt[0].value.s


def convert_objects(
    module: ast.Module, level: int
) -> List[dict]:
    # this should handle classes, too
    return [
        function_to_graph(obj, level)
        for obj in module.body
        if isinstance(obj, ast.FunctionDef)
    ]
