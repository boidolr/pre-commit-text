import argparse
import io
import pathlib
import re
import sys
from collections.abc import Sequence
from functools import partial
from itertools import takewhile

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


def _format_yaml_doc(yaml: YAML, document: str) -> str:
    doc = yaml.load(document)
    if isinstance(doc, list | dict):
        output = io.StringIO()
        yaml.dump(doc, output)
        return output.getvalue()
    return document


def _format_yaml(yaml: YAML, filename: str) -> int:
    with pathlib.Path(filename).open(encoding="utf-8") as fh:
        lines = fh.readlines()

    def is_comment(line: str) -> bool:
        return line.startswith("#")

    head = "".join(takewhile(is_comment, lines))
    content = "".join(lines)
    content = content if not content.startswith(head) else content[len(head) :]

    docs = re.split(r"^---\s*\n", content, flags=re.MULTILINE)
    processed_docs = list(filter(None, map(partial(_format_yaml_doc, yaml), docs)))

    doc_separator = "---\n"
    use_separator_before_docs = len(processed_docs) > 1 or (len(head) > 0 and content.startswith("---"))
    prefix = doc_separator if use_separator_before_docs else ""
    processed_content = prefix + doc_separator.join(processed_docs)

    if content != processed_content:
        print(f"fixed {filename}")
        with pathlib.Path(filename).open("w", encoding="utf-8") as fh:
            fh.write(head)
            fh.write(processed_content)
        return 1

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to format")
    parser.add_argument(
        "-m",
        "--mapping",
        default=2,
        type=int,
        help="Spaces to map with (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--offset",
        type=int,
        help="Spaces to offset with (default: same as mapping)",
    )
    parser.add_argument(
        "-s",
        "--sequence",
        type=int,
        help="Spaces to sequence with (default: mapping + 2)",
    )
    parser.add_argument(
        "--preserve-quotes",
        dest="preserve_quotes",
        action="store_true",
        help="Whether to keep quoting as is (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    yaml = YAML()
    yaml.indent(
        mapping=args.mapping,
        sequence=(args.mapping + 2) if args.sequence is None else args.sequence,
        offset=args.mapping if args.offset is None else args.offset,
    )
    yaml.preserve_quotes = args.preserve_quotes
    yaml.width = sys.maxsize  # type: ignore

    ret = 0
    for filename in args.filenames:
        try:
            ret |= _format_yaml(yaml, filename)
        except YAMLError:  # noqa: PERF203
            ret = 1
            print(f"{filename} could not be parsed")
    return ret


if __name__ == "__main__":
    sys.exit(main())
