# Changelog[^1]

All notable changes to poetry-source-env will be documented here. Breaking changes are marked with a 🚩.

poetry-source-env adheres to [semantic versioning](https://semver.org/spec/v2.0.0.html).

## <a name="1-1-0">[1.1.0] - 2023-05-01</a>

### Added

- poetry-source-env can now expand environment variables in the `[tool.poetry.source]` section of `pyproject.toml`.
  For example, this:

  ```bash
  export INDEX_URL="https://pkg.celsiusnarhwal.dev"
  ```

  ```toml
  [[tool.poetry.source]]
  name = "my-epic-source"
  url = "${INDEX_URL}"

  ```

  will now become:

  ```toml
  [[tool.poetry.source]]
  name = "my-epic-source"
  url = "https://pkg.celsiusnarhwal.dev"

  ```

- poetry-source-env's behavior can now be configured via the `[tool.poetry-source-env]` section of `pyproject.toml`.
  Available configuration options are documented in the [README](README.md#configuration).

## <a name="1-0-1">[1.0.1] - 2023-04-29</a>

No user-facing changes are introduced in this release.

## <a name="1-0-0">[1.0.0] - 2023-04-29</a>

This is the initial release of poetry-env-source.

[^1]: Based on [Keep a Changelog](https://keepachangelog.com).
