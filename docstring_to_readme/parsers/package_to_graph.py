from docstring_to_readme import graph as g
from docstring_to_readme.parsers.module_to_graph import (
    module_to_graph,
)

import os
from typing import List, Optional


def package_to_graph(path: str, level: int = 2) -> dict:
    if path.endswith("/"):
        path = path[:-1]

    py_files = abs_listdir(path)

    if not py_files:
        return {}

    children = [
        module_to_graph(path, level + 1)
        for path in py_files
    ]

    filt = [g for g in children if g]

    if not filt:
        return {}

    section = os.path.split(path)[-1]

    output = g.Node(section=section, children=filt)

    return output


def abs_listdir(path: str) -> List[Optional[str]]:
    try:
        listdir = os.listdir(path)
    except FileNotFoundError:
        print(f"The package '{path}' does not exist")
        exit(1)  # TODO: appropriate here?

    py_files = [f for f in listdir if f.endswith(".py")]

    abs_path_py_files = [
        os.path.join(os.path.abspath(path), f)
        for f in py_files
    ]

    if abs_path_py_files:
        return abs_path_py_files

    return []
