# poetry-source-env

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-source-env?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-source-env)
[![PyPI](https://img.shields.io/pypi/v/poetry-source-env?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-source-env)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/poetry-source-env?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-source-env/releases)
[![PyPI - License](https://img.shields.io/pypi/l/poetry-source-env?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-source-env/blob/main/LICENSE.md)
[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)

poetry-source-env is a Poetry plugin that allows for [package sources](https://python-poetry.org/docs/repositories/#package-sources)
to be defined in environment variables. This lets you define private package sources for your project without exposing
their URLs in `pyproject.toml`.

This plugin is intended as a workaround for python-poetry/poetry#5958 and will be deprecated if its functionality
is ever implemented in Poetry itself.

## Installation

```bash
poetry self add poetry-source-env
```

## Usage

Normally, you would define a package source in `pyproject.toml` like this:

```toml
[[tool.poetry.source]]
name = "my-epic-source"
url = "https://pkg.celsiusnarhwal.dev"
default = false
secondary = false

```

With poetry-source-env, you can define this source via environment variables, similar to how you can already
configure [publishable repositories](https://python-poetry.org/docs/repositories/#publishable-repositories:~:text=Alternatively%2C%20you%20can%20use%20environment%20variables%20to%20provide%20the%20credentials%3A):

```bash
export POETRY_REPOSITORIES_MY_EPIC_SOURCE_URL=https://pkg.celsiusnarhwal.dev
export POETRY_REPOSITORIES_MY_EPIC_SOURCE_DEFAULT=false
export POETRY_REPOSITORIES_MY_EPIC_SOURCE_SECONDARY=false
```

If your source requires authentication, Poetry already supports defining its credentials via environment variables:

```bash
export POETRY_HTTP_BASIC_MY_EPIC_SOURCE_USERNAME=celsiusnarhwal
export POETRY_HTTP_BASIC_MY_EPIC_SOURCE_PASSWORD=superdupersecret
```

## License

poetry-source-env is licensed under the [MIT License](https://github.com/celsiusnarhwal/poetry-source-env/blob/main/LICENSE.md).
