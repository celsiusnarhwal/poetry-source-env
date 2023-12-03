import os
import re
from os.path import expandvars

from cleo.io.io import IO
from dict_deep import deep_get
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.legacy_repository import LegacyRepository
from poetry.repositories.repository import Repository
from poetry.repositories.repository_pool import Priority, RepositoryPool
from poetry.toml.file import TOMLFile
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

        def update_sources(poetry: Poetry, repo: Repository):
            poetry_config = poetry.pyproject.poetry_config
            new_config = {
                "name": repo.name.lower(),
                "priority": poetry.pool.get_priority(repo.name).name,
            }
            if new_config["name"] != "pypi":
                new_config["url"] = repo.url

            for index, old_source in enumerate(poetry_config.get("source", [])):
                if old_source.get("name") == new_config["name"]:
                    poetry_config["source"][index].update(new_config)
                    break
            else:
                poetry_config.setdefault("source", [])
                poetry_config["source"].append(new_config)

        def add_or_replace_repository(
            poetry: Poetry, repo: Repository, priority: Priority
        ) -> None:
            # replace DEFAULT priority with PRIMARY
            if priority is Priority.DEFAULT:
                for _repo in (
                    x
                    for x in poetry.pool.all_repositories
                    if poetry.pool.get_priority(x.name) is Priority.DEFAULT
                ):
                    poetry.pool.remove_repository(_repo.name)
                    poetry.pool.add_repository(_repo, priority=Priority.PRIMARY)

            # remove repository if already exists
            if poetry.pool.has_repository(repo.name):
                poetry.pool.remove_repository(repo.name)
            poetry.pool.add_repository(repo, priority=priority)
            update_sources(poetry, repo)

        if config.env:
            repositories = {}
            _prefix = re.escape(config.prefix)
            pattern = re.compile(rf"{_prefix}(?P<name>[A-Z_]+)_URL")

            for env_key in os.environ.keys():
                match = pattern.match(env_key)
                if match:
                    repositories[match.group("name").lower().replace("_", "-")] = {
                        "env_name": match.group("name"),
                        "url": os.environ[env_key],
                    }

            for name, repository in repositories.items():
                if name == "pypi":
                    repo = poetry.pool.repository("PyPI")
                else:
                    repo = LegacyRepository(name, repository["url"])

                priority_name = os.getenv(
                    f"{config.prefix}{repository['env_name']}_PRIORITY", "primary"
                )

                priorities = {
                    "default": Priority.DEFAULT,
                    "primary": Priority.PRIMARY,
                    "supplemental": Priority.SUPPLEMENTAL,
                    "explicit": Priority.EXPLICIT,
                }

                priority = priorities.get(priority_name.casefold(), Priority.PRIMARY)

                add_or_replace_repository(poetry, repo, priority)

        if config.toml:
            for cfg_repo in (
                x for x in poetry.get_sources() if x.name.lower() != "pypi"
            ):
                repo = LegacyRepository(
                    expandvars(cfg_repo.name), expandvars(cfg_repo.url)
                )
                add_or_replace_repository(poetry, repo, priority)
