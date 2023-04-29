import os
import re

from cleo.io.io import IO
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.legacy_repository import LegacyRepository


class PoetrySourcePlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO = None) -> None:
        repositories = {}
        pattern = re.compile(r"POETRY_REPOSITORIES_(?P<name>[A-Z_]+)_URL")

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
                os.getenv(f"POETRY_REPOSITORIES_{repository['env_name']}_DEFAULT")
                == "true"
            )
            secondary = (
                os.getenv(f"POETRY_REPOSITORIES_{repository['env_name']}_SECONDARY")
                == "true"
            )

            poetry.pool.add_repository(repo, default, secondary)
