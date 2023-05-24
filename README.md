# poetry-source-env

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-source-env?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-source-env)
[![PyPI](https://img.shields.io/pypi/v/poetry-source-env?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-source-env)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/poetry-source-env?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-source-env/releases)
[![PyPI - License](https://img.shields.io/pypi/l/poetry-source-env?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-source-env/blob/main/LICENSE.md)
[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)

poetry-source-env is a Poetry plugin that lets you define private package sources for your project without exposing
their URLs in `pyproject.toml`. It can load package source definitions from environment variables and expand environment
variables in the `tool.poetry.source` section of `pyproject.toml`.

This plugin is intended as a workaround for python-poetry/poetry#5958 and will be deprecated if comparable functionality
is ever implemented in Poetry itself.

Note that poetry-source-env cannot resolve repositories when installing other Poetry plugins (Poetry does not
load plugins when running `poetry self` commands). If you need a python-poetry/poetry#5958 workaround for installing Poetry
plugins, see https://github.com/python-poetry/poetry/issues/5958#issuecomment-1479183720.

## Installation

```bash
poetry self add poetry-source-env
```

## Usage

Normally, you would define a package source in `pyproject.toml` like this:

```toml
[[tool.poetry.source]]
name = "foo"
url = "https://foo.bar/simple"
priority = "supplemental"

```

With poetry-source-env, you can define this source via environment variables, similar to how you can already
configure [publishable repositories](https://python-poetry.org/docs/repositories/#publishable-repositories:~:text=Alternatively%2C%20you%20can%20use%20environment%20variables%20to%20provide%20the%20credentials%3A):

```bash
export POETRY_REPOSITORIES_FOO_URL=https://foo.bar/simple
export POETRY_REPOSITORIES_FOO_PRIORITY=supplemental
```

If you prefer to keep the source defined in `pyproject.toml`, you can opt to conceal its name or URL, in whole or
in part, behind environment variables:

```bash
export FOO_INDEX_NAME="foo"
export FOO_INDEX_URL="https://foo.bar/simple"
```

```toml
[[tool.poetry.source]]
name = "${FOO_INDEX_NAME}"
url = "${FOO_INDEX_URL}"
priority = "supplemental"

```

If your source requires authentication, Poetry already supports defining its credentials via environment variables:

```bash
export POETRY_HTTP_BASIC_FOO_USERNAME=celsiusnarhwal
export POETRY_HTTP_BASIC_FOO_PASSWORD=superdupersecret
```

## Configuration

poetry-source-env's behavior can be configured via the `tool.poetry-source-env` section of `pyproject.toml`.

Supported configuration options include:

| **Name** | **Type** | **Description**                                                                                                                   | **Required?** | **Default**            |
| -------- | -------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------- | ---------------------- |
| `prefix` | string   | The prefix which poetry-source-env should expect source-defining environment variables to use. Has no effect if `env` is `false`. | No            | `POETRY_REPOSITORIES_` |
| `env`    | boolean  | Whether to read package source definitions from environment variables.                                                            | No            | `true`                 |
| `toml`   | boolean  | Whether to expand environment variables in the `tool.poetry.source` section of `pyproject.toml`.                                  | No            | `true`                 |

## License

poetry-source-env is licensed under the [MIT License](https://github.com/celsiusnarhwal/poetry-source-env/blob/main/LICENSE.md).
