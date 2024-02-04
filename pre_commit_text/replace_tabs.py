#!/usr/bin/env python3
import argparse
import pathlib
import sys
from collections.abc import Sequence
from operator import methodcaller


def _replace_tabs(filename: str, tabsize: int) -> int:
    with pathlib.Path(filename).open("rb") as fh:
        content = fh.readlines()

    lines = list(map(methodcaller("replace", b"\t", b" " * tabsize), content))
    if lines != content:
        print(f"fixed {filename}")
        with pathlib.Path(filename).open("wb") as fh:
            fh.writelines(lines)
        return 1

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to replace tabs in")
    parser.add_argument(
        "-t",
        "--tabsize",
        default=4,
        type=int,
        help="Spaces to replace tabs with (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    ret = 0
    for filename in args.filenames:
        ret |= _replace_tabs(filename, args.tabsize)
    return ret


if __name__ == "__main__":
    sys.exit(main())
