pre-commit-text [![tag](https://img.shields.io/github/v/tag/boidolr/pre-commit-text?sort=semver)](https://github.com/boidolr/pre-commit-text/tags) [![Build](https://github.com/boidolr/pre-commit-text/actions/workflows/continous-integration.yml/badge.svg)](https://github.com/boidolr/pre-commit-text/actions/workflows/continous-integration.yml) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
================

Git hooks to modify (text) files for use with the [pre-commit](https://github.com/pre-commit/pre-commit) framework. For details see the list of available hooks below.

## Using pre-commit-text with pre-commit

Add this to your `.pre-commit-config.yaml`:
```
    -   repo: https://github.com/boidolr/pre-commit-text
        rev: v1.1.0  # Use the ref you want to point at
        hooks:
        -   id: pretty-format-yaml
        -   id: replace-tabs
        # -   id: ...
```
For an extended example see [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

## Available hooks

- **`pretty-format-yaml`**: Format yaml files.
- **`properties-whitespace`**: Remove whitespace around equal signs in property files.
  Implemented using the `search-replace` hook.
- **`replace-tabs`**: Replace tabs in files.
    - `--tabsize` spaces to replace a tab with.
- **`search-replace`**: Replace patterns in files.
    - `--search` regular expression to use for search.
    - `--replacement` replacement for matches.
