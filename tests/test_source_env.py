from os import environ
from typing import TYPE_CHECKING
from unittest.mock import patch

from poetry.console.application import Application
from cleo.testers.application_tester import ApplicationTester

if TYPE_CHECKING:
    from cleo.testers.application_tester import ApplicationTester


class TestSourceEnv:
    def test_add_repo_primary(self, app_tester, config_dir, capsys):
        with patch.dict(
            environ,
            {
                "POETRY_REPOSITORIES_FOO_URL": "https://example.com/simple",
                "POETRY_REPOSITORIES_FOO_PRIORITY": "primary",
            },
        ):
            app_tester.application.reset_poetry()
            assert app_tester.execute("add --dry-run --no-cache aiodns") == 0

    def test_add_repo_default(self, app_tester, config_dir, capsys):
        with patch.dict(
            environ,
            {
                "POETRY_REPOSITORIES_FOO_URL": "https://example.com/simple",
                "POETRY_REPOSITORIES_FOO_PRIORITY": "default",
            },
        ):
            app_tester.application.reset_poetry()
            assert app_tester.execute("add --dry-run --no-cache aiodns") == 0

    def test_replace_pypi_priority(self, app_tester, config_dir, capsys):
        with patch.dict(
            environ,
            {
                "POETRY_REPOSITORIES_PYPI_URL": "https://example.com/simple",
                "POETRY_REPOSITORIES_PYPI_PRIORITY": "secondary",
            },
        ):
            app_tester.application.reset_poetry()
            assert app_tester.execute("add --dry-run --no-cache aiodns") == 0
