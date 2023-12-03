from os import environ
from pathlib import Path
import shutil
from typing import TYPE_CHECKING
from typing import Iterator
from unittest.mock import patch

from cleo.testers.application_tester import ApplicationTester
from poetry.config.config import Config
from poetry.config.dict_config_source import DictConfigSource
from poetry.console.application import Application
from poetry.factory import Factory
from poetry.utils.env import EnvManager
from poetry.utils.env import VirtualEnv

import pytest

if TYPE_CHECKING:
    from poetry.poetry import Poetry


@pytest.fixture()
def config_dir(tmp_path: Path) -> Path:
    path = tmp_path / "config"
    path.mkdir()
    return path


@pytest.fixture(autouse=True)
def mock_user_config_dir(config_dir: Path) -> None:
    patch("poetry.locations.CONFIG_DIR", config_dir).start()
    patch("poetry.config.config.CONFIG_DIR", config_dir).start()


@pytest.fixture
def config_cache_dir(tmp_path: Path) -> Path:
    path = tmp_path / ".cache" / "pypoetry"
    path.mkdir(parents=True)
    return path


@pytest.fixture
def config_source(config_cache_dir: Path) -> DictConfigSource:
    source = DictConfigSource()
    source.add_property("cache-dir", str(config_cache_dir))

    return source


@pytest.fixture
def project_directory() -> str:
    return "simple_project"


@pytest.fixture(autouse=True)
def config(config_source: DictConfigSource) -> Config:
    c = Config()
    c.merge(config_source.config)
    c.set_config_source(config_source)

    patch("poetry.config.config.Config.create", return_value=c).start()
    patch("poetry.config.config.Config.set_config_source").start()

    return c


@pytest.fixture
def poetry_factory(project_directory: str, config: Config) -> "Poetry":
    p = Factory().create_poetry(Path(__file__).parent / "data" / project_directory)

    return p


@pytest.fixture
def app(poetry_factory: "Poetry", config_dir) -> Application:
    class TestApplication(Application):
        def __init__(self, poetry: "Poetry") -> None:
            super().__init__()
            self._poetry = poetry

        def reset_poetry(self) -> None:
            poetry = self._poetry
            assert poetry is not None
            self._poetry = Factory().create_poetry(poetry.file.path.parent)
            self._poetry.set_pool(poetry.pool)
            self._poetry.set_config(poetry.config)

    return TestApplication(poetry_factory)


@pytest.fixture
def app_tester(app: Application) -> ApplicationTester:
    return ApplicationTester(app)
