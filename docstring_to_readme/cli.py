from docstring_to_readme.parser import (
    file_as_ast,
    module_to_sections,
)

import argparse
from argparse import RawDescriptionHelpFormatter
import shutil
from sys import argv
from typing import List


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


def create_or_append_to_readme(sections: str) -> None:
    # TODO: needs to accept another arg defining where to
    #  begin appending/overwriting. For example, if it's
    #  passed "## API", it need to know to find the END of
    #  the block defined by "## API", and append after that

    readme = "./README.md"
    backup = "./.README-backup.md"
    shutil.copyfile(readme, backup)

    with open(readme, "a") as f:
        f.write("\n\n")
        f.write(sections)


def main() -> None:
    arguments = argv[1:]

    args = cli_parser(arguments)

    module = file_as_ast(args.module)
    sections = module_to_sections(module)

    create_or_append_to_readme(sections)
