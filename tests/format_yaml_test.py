from pre_commit_text.format_yaml import main


def test_format_yaml_empty_comment(tmp_path):
    path = tmp_path / "file"
    path.write_text("## empty yaml file header\n# comments need to be kept\n---\n")

    assert main((str(path),)) == 0
    assert (
        path.read_text("utf-8")
        == "## empty yaml file header\n# comments need to be kept\n---\n"
    )


def test_format_yaml_single_document(tmp_path):
    path = tmp_path / "file"
    path.write_text("root:\n  test: \"test\"\n  foo: 'bar'\n")

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == "root:\n  test: test\n  foo: bar\n"


def test_format_yaml_single_document_preserve_qoutes(tmp_path):
    path = tmp_path / "file"
    path.write_text("root:\n  test: \"test\"\n  foo: 'bar'\n")

    assert main((str(path), "--preserve-quotes")) == 0
    assert path.read_text("utf-8") == "root:\n  test: \"test\"\n  foo: 'bar'\n"


def test_format_yaml_single_document_multi_line_string(tmp_path):
    path = tmp_path / "file"
    path.write_text("root:\n  test: |\n   'bar'\n   'baz'\n")

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == "root:\n  test: |\n    'bar'\n    'baz'\n"


def test_format_yaml_single_document_array(tmp_path):
    path = tmp_path / "file"
    path.write_text("test:\n      - 1\n      - 2\n")

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == "test:\n  - 1\n  - 2\n"


def test_format_yaml_single_document_flat_sequence(tmp_path):
    path = tmp_path / "file"
    path.write_text("      - 1\n      - 2\n      - 3\n")

    assert main((str(path), "-m", "2", "-o", "0", "-s", "2")) == 1
    assert path.read_text("utf-8") == "- 1\n- 2\n- 3\n"


def test_format_yaml_text_file(tmp_path):
    path = tmp_path / "file"
    path.write_text("Text line\n    with indenting\n")

    assert main((str(path),)) == 0
    assert path.read_text("utf-8") == "Text line\n    with indenting\n"


def test_format_yaml_multi_document_comment(tmp_path):
    path = tmp_path / "file"
    path.write_text(
        "## empty yaml file header\n# comments need to be kept\n---\nfoo:  bar"
    )

    assert main((str(path),)) == 1
    assert (
        path.read_text("utf-8")
        == "## empty yaml file header\n# comments need to be kept\n---\nfoo: bar\n"
    )


def test_format_yaml_multi_document_separates_comments(tmp_path):
    path = tmp_path / "file"
    path.write_text(
        "## empty yaml file header\n# comments need to be kept\nfoo:  bar\n---\nbaz: qux\n"
    )

    assert main((str(path),)) == 1
    assert (
        path.read_text("utf-8")
        == "## empty yaml file header\n# comments need to be kept\n---\nfoo: bar\n---\nbaz: qux\n"
    )


def test_format_yaml_multi_document_remove_empty_docs(tmp_path):
    path = tmp_path / "file"
    path.write_text("---\na: 1\n---\n---\nb: 2\n")

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == "---\na: 1\n---\nb: 2\n"


def test_format_yaml_multi_document_complex(tmp_path):
    example = (
        "  first:\n"
        "     test:\n"
        "          - val\n"
        "            part\n"
        "---\n"
        "second:\n"
        "        test:\n"
        "          - 1\n"
        "          - 2\n"
        "---\n"
        "This is a primitive doc.\n"
        "Line of text.\n"
        "\n"
        "Last line of doc.\n"
        "---\n"
        "third:\n"
        "  # comment\n"
        "  data: abc123\n"
        "---\n"
    )
    result = (
        "---\n"
        "first:\n"
        "  test:\n"
        "    - val part\n"
        "---\n"
        "second:\n"
        "  test:\n"
        "    - 1\n"
        "    - 2\n"
        "---\n"
        "This is a primitive doc.\n"
        "Line of text.\n"
        "\n"
        "Last line of doc.\n"
        "---\n"
        "third:\n"
        "  # comment\n"
        "  data: abc123\n"
    )
    path = tmp_path / "file"
    path.write_text(example)

    assert main((str(path),)) == 1
    assert path.read_text("utf-8") == result
