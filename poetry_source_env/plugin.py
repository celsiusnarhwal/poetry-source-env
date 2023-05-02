import os
import re
from os.path import expandvars

from cleo.io.io import IO
from dict_deep import deep_get
from poetry.core.toml.file import TOMLFile
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.legacy_repository import LegacyRepository
from pydantic import BaseSettings, validate_arguments
from typing_extensions import Self


class PSPConfig(BaseSettings):
    prefix: str = "POETRY_REPOSITORIES_"
    env: bool = True
    toml: bool = True

    @classmethod
    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def load(cls, file: TOMLFile) -> Self:
        pyproject = file.read()
        return cls.parse_obj(deep_get(pyproject, "tool.poetry-source-env") or {})


class PoetrySourcePlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO = None) -> None:
        config: PSPConfig = PSPConfig.load(poetry.pyproject.file)

        if config.env:
            repositories = {}
            pattern = re.compile(rf"{config.prefix}(?P<name>[A-Z_]+)_URL")

            for env_key in os.environ.keys():
                match = pattern.match(env_key)
                if match:
                    repositories[match.group("name").lower().replace("_", "-")] = {
                        "env_name": match.group("name"),
                        "url": os.environ[env_key],
                    }

            for name, repository in repositories.items():
                repo = LegacyRepository(name, repository["url"])
                default = (
                    os.getenv(f"{config.prefix}{repository['env_name']}_DEFAULT")
                    == "true"
                )
                secondary = (
                    os.getenv(f"{config.prefix}{repository['env_name']}_SECONDARY")
                    == "true"
                )

                poetry.pool.add_repository(repo, default, secondary)

        if config.toml:
            for repository in poetry.pool.repositories:
                definition = next(
                    (
                        source
                        for source in poetry.get_sources()
                        if source.name == repository.name
                    ),
                    None,
                )

                if definition:
                    poetry.pool.remove_repository(repository.name)
                    repo = LegacyRepository(
                        expandvars(definition.name), expandvars(definition.url)
                    )
                    poetry.pool.add_repository(
                        repo, definition.default, definition.secondary
                    )
