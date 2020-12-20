import argparse
from typing import List


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
