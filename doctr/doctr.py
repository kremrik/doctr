from doctr.cli import cli
from doctr.parsers.python_to_graph import (
    python_to_graph,
)
from doctr.parsers.readme_to_graph import (
    readme_to_graph,
)
from doctr.parsers.graph_to_readme import (
    dumps,
)
from doctr.traverse import update

from typing import List


def doctr(arguments: List[str]) -> None:
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
