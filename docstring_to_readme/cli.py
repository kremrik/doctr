from os import read
from docstring_to_readme.parser import (
    file_as_ast,
    module_to_sections,
)

import argparse
from argparse import RawDescriptionHelpFormatter
import shutil
from sys import argv
from typing import List, Optional


def cli_parser(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="A tool for documentation",
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-m",
        "--module",
        required=True,
        help="Path to Python module",
    )

    parser.add_argument(
        "-o",
        "--overwrite-at",
        required=False,
        default="",
        help="The section after which to append docs",
    )

    parser.add_argument(
        "-l",
        "--level",
        required=False,
        default=3,
        help="The number of '#' to use for each section",
    )

    return parser.parse_args(arguments)


def overwrite_at_pos(section: str, readme: str) -> int:
    readme_lines = readme.split("\n")
    pos = None

    for idx, line in enumerate(readme_lines):
        if section in line:
            pos = idx
            break

    if pos is not None:
        return pos
    else:
        msg = "Section '{}' not found".format(section)
        raise RuntimeError(msg)


def create_or_append_to_readme(
    section: str,
    readme: str,
    append_at: Optional[int] = None,
) -> str:
    section_separator = "\n\n"

    if append_at:
        readme = "\n".join(readme.split("\n")[:append_at])

    return readme.strip() + section_separator + section


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        output = f.read()
    return output


def write_file(filepath: str, data: str) -> None:
    with open(filepath, "w") as f:
        f.write(data)


def backup_readme(filepath: str) -> None:
    readme = filepath
    backup = readme + ".bak"
    shutil.copyfile(readme, backup)


def main() -> None:
    filepath = "./README.md"
    arguments = argv[1:]
    args = cli_parser(arguments)

    backup_readme(filepath)

    readme = read_file(filepath)
    module = file_as_ast(args.module)
    sections = module_to_sections(module)
    overwrite_at = args.overwrite_at

    if overwrite_at:
        append_at = overwrite_at_pos(overwrite_at, readme)
    else:
        append_at = overwrite_at  # defaults to None

    new_readme = create_or_append_to_readme(
        section=sections,
        readme=readme,
        append_at=append_at,
    )

    write_file(filepath, new_readme)
