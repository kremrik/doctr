from docstring_to_readme.parsers.python_to_graph import (
    python_to_graph,
)
from docstring_to_readme.parsers.readme_to_graph import (
    readme_to_graph,
)
from docstring_to_readme.parsers.graph_to_readme import (
    dumps,
)
from docstring_to_readme.traverse import update

import argparse
from sys import argv
from typing import List


def main(arguments: List[str]) -> None:
    args = cli(arguments)
    path = args.path
    path = path if not path.endswith("/") else path[:-1]
    level = args.level
    readme = args.readme

    updated_graph = update_readme_graph(
        readme_path=readme, doc_path=path, level=level
    )

    update_readme(graph=updated_graph, path=readme)


def update_readme_graph(
    readme_path: str, doc_path: str, level: int
) -> dict:
    try:
        readme = open(readme_path, "r").read()
    except FileNotFoundError:
        readme = ""

    readme_graph = readme_to_graph(readme)

    doc_graph = python_to_graph(doc_path, level)
    updated = update(readme_graph, doc_graph)

    return updated


def update_readme(graph: dict, path: str) -> None:
    to_markdown = dumps(graph)

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
