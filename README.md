pre-commit-text
[![tag](https://img.shields.io/github/v/tag/boidolr/pre-commit-text?sort=semver)](https://github.com/boidolr/pre-commit-text/tags)
![python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fboidolr%2Fpre-commit-text%2Fmain%2Fpyproject.toml)
[![Build](https://github.com/boidolr/pre-commit-text/actions/workflows/continous-integration.yml/badge.svg)](https://github.com/boidolr/pre-commit-text/actions/workflows/continous-integration.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
================

Scripts that can work as `git` hooks to modify (text) files.
These scripts can be called directly or with the provided configuration for the [pre-commit](https://github.com/pre-commit/pre-commit) framework.
For details see below.


## Using pre-commit-text with pre-commit

Add this to your `.pre-commit-config.yaml`:
```
    -   repo: https://github.com/boidolr/pre-commit-text
        rev: v1.2.16  # Use the ref you want to point at
        hooks:
        -   id: pretty-format-yaml
        -   id: replace-tabs
        # -   id: ...
```
For an extended example see [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

### Available hooks

- **`pretty-format-yaml`**: Format yaml files.
    - `--mapping` space to use as offset for mappings.
    - `--sequence` space to use as offset for sequences (default is value for mapping plus two).
    - `--preserve-quotes` whether to keep quoting as is or change to default.
- **`properties-whitespace`**: Remove whitespace around equal signs in property files.
  Implemented using the `search-replace` hook.
- **`replace-tabs`**: Replace tabs in files.
    - `--tabsize` spaces to replace a tab with.
- **`search-replace`**: Replace patterns in files.
    - `--search` regular expression to use for search.
    - `--replacement` replacement for matches.


## Using scripts directly

Install the package to get access to the scripts defined as command line entry points in [`pyproject.toml`](./pyproject.toml).
The scripts accept the arguments given for the pre-commit hooks. Additionally they exepect to receive the file names to work on.

An example invocation could be `uvx --from 'git+https://github.com/boidolr/pre-commit-text.git' format-yaml --preserve-quotes .github/release.yml`.

Available entry points are:

- `format-yaml`
- `replace-tabs`
- `search-replace`
