from docstring_to_readme.parsers import (
    module_to_graph,
    package_to_graph,
    readme_to_graph,
    graph_to_readme,
)
from docstring_to_readme.traverse import update

import argparse
from os.path import isdir
from sys import argv
from typing import Callable, List


def main(arguments: List[str]) -> None:
    args = cli(arguments)
    path = args.path
    level = args.level
    readme = args.readme

    updated_graph = update_readme_graph(
        readme_path=readme, doc_path=path, level=level
    )

    update_readme(graph=updated_graph, path=readme)


def update_readme_graph(
    readme_path: str, doc_path: str, level: int
) -> dict:
    readme_graph = readme_to_graph.readme_to_graph(
        open(readme_path, "r").read()
    )

    doc_graph = selector(doc_path)(doc_path, level)
    updated = update(readme_graph, doc_graph)

    print(readme_graph, doc_graph, sep="\n\n")

    return updated


def selector(path: str) -> Callable:
    # TODO: only handling one level of package nesting
    if isdir(path):
        return package_to_graph.package_to_graph
    return module_to_graph.module_to_graph


def update_readme(graph: dict, path: str) -> None:
    from json import dumps

    to_markdown = graph_to_readme.dumps(graph)

    with open(path, "w") as readme:
        readme.write(to_markdown)


def cli(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path",
        "-p",
        type=str,
        required=True,
        help="[REQUIRED] Path to package or module",
    )

    parser.add_argument(
        "--level",
        "-l",
        type=int,
        required=False,
        default=3,
        help="Number of '#' at top level",
    )

    parser.add_argument(
        "--readme",
        "-r",
        type=str,
        required=False,
        default="./README.md",
        help="Path to README to update",
    )

    return parser.parse_args(arguments)


if __name__ == "__main__":
    main(argv[1:])
