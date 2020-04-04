"""Contains interfaces for package tools executor."""
import os
import shutil
import site
from abc import abstractmethod
from dataclasses import dataclass
from typing import IO
from punish.style import AbstractStyle
from termcolor import colored

SITE: str = os.path.join(site.getsitepackages()[0], os.path.dirname(__file__))
NEW_LINE: str = "\n"


def _write_to_file(path: str, content: str, mode: str = "a") -> None:
    with open(path, mode) as file:  # type: IO[str]
        file.write(content)


def _replace_content(path: str, from_replace: str, to_replace: str) -> None:
    with open(path) as file:  # type: IO[str]
        _write_to_file(path, content=file.read().replace(from_replace, to_replace), mode="w")


class Package(AbstractStyle):
    @abstractmethod
    def init(self) -> None:
        pass


@dataclass
class User(AbstractStyle):
    name: str
    email: str


class Meta:
    FLAKE: str = ".flake8"
    PYDOC: str = ".pydocstyle"
    PYLINT: str = ".pylintrc"
    MYPY: str = "mypy.ini"
    BLACK: str = "pyproject.toml"
    TRAVIS: str = ".travis.yml"
    PYTEST: str = "pytest.ini"
    ANALYSER: str = "analyse-source-code.sh"
    ICON: str = "icon.png"
    GITIGNORE: str = ".gitignore"
    AUTHORS: str = "AUTHORS.md"
    CHANGELOG: str = "CHANGELOG.md"
    REQUIREMENTS: str = "requirements.txt"
    DEV_REQUIREMENTS: str = "requirements-dev.txt"
    README: str = "README.md"
    LICENSE: str = "LICENSE.md"
    MANIFEST: str = "MANIFEST.in"
    PYPIRC: str = ".pypirc"
    SETUP: str = "setup.py"

    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user

    def copy_all(self, from_path: str = "./") -> None:
        for file in filter(str.isupper, dir(self)):
            shutil.copyfile(os.path.join(from_path, eval(f'self.{file}')), eval(f'self.{file}'))

    def build_analyser(self) -> None:
        _replace_content(self.ANALYSER, from_replace="<package>", to_replace=self._name)

    def build_readme(self) -> None:
        _replace_content(self.README, from_replace="<project>", to_replace=self._name)
        _replace_content(self.README, from_replace="<username>", to_replace=self._user.name)
        _replace_content(self.README, from_replace="<email>", to_replace=self._user.email)

    def build_license(self) -> None:
        _replace_content(self.LICENSE, from_replace="<package>", to_replace=self._name)

    def build_packaging(self) -> None:
        _replace_content(self.MANIFEST, from_replace="<project>", to_replace=self._name)
        _replace_content(self.PYPIRC, from_replace="<username>", to_replace=self._user.name)
        _replace_content(self.SETUP, from_replace="package", to_replace=self._name)

    def build_pytest(self) -> None:
        _replace_content(self.PYTEST, from_replace="<package>", to_replace=self._name)

    def build_authors(self) -> None:
        _replace_content(self.AUTHORS, from_replace="<username>", to_replace=self._user.name)
        _replace_content(self.AUTHORS, from_replace="<email>", to_replace=self._user.email)


class Application(Package):
    def __init__(self, name: str, user: User) -> None:
        self._name: str = name
        self._user: User = user

    def init(self) -> None:
        os.mkdir(self._name)
        _write_to_file(
            path=os.path.join(self._name, "__init__.py"),
            content=(
                f'"""Package contains a set of interfaces to operate `{self._name}` application.""" {NEW_LINE * 2}'
                f'__author__: str = "{self._user.name}"{NEW_LINE}__email__: str ='
                f' "{self._user.email}"{NEW_LINE}__version__: str = "0.0.0"{NEW_LINE}'
            ),
        )

    def make_as_tool(self) -> None:
        _write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{NEW_LINE * 3}def main() -> None:{NEW_LINE}    """Runs `{self._name}` command line tool."""'
                f"{NEW_LINE * 2}    pass{NEW_LINE * 3}"
                f'if __name__ == "__main__":{NEW_LINE}    pass{NEW_LINE}'
            ),
        )


class Tests(Package):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._tests: str = self.__class__.__name__.lower()

    def init(self) -> None:
        os.mkdir(self._tests)
        _write_to_file(
            path=os.path.join(self._tests, "__init__.py"),
            content=f'"""Package contains a set of interfaces to test `{self._name}` application."""{NEW_LINE}',
        )

    def make_helpers(self) -> None:
        _write_to_file(
            path=os.path.join(self._tests, "markers.py"),
            content=(
                f"import _pytest.mark{NEW_LINE}import pytest{NEW_LINE * 2}"
                f"unit: _pytest.mark.MarkDecorator = pytest.mark.unit{NEW_LINE}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "conftest.py"),
            content=(
                f"from _pytest.config.argparsing import Parser{NEW_LINE}"
                f"from _pytest.fixtures import SubRequest{NEW_LINE}import pytest{NEW_LINE}"
            ),
        )
        _write_to_file(
            path=os.path.join(self._tests, "test_sample.py"),
            content=f"import pytest{NEW_LINE * 3}" f"def test_me() -> None:{NEW_LINE}    assert True{NEW_LINE}",
        )


class Project(AbstractStyle):
    def __init__(self, name: str, user: User) -> None:
        self._app: Application = Application(name, user)
        self._tests: Tests = Tests(name)
        self._meta: Meta = Meta(name, user)

    def build_package(self) -> None:
        self._app.init()
        self._app.make_as_tool()

    def build_tests(self) -> None:
        self._tests.init()
        self._tests.make_helpers()

    def build_meta(self) -> None:
        self._meta.copy_all(from_path=SITE)
        self._meta.build_analyser()
        self._meta.build_authors()
        self._meta.build_license()
        self._meta.build_packaging()
        self._meta.build_pytest()
        self._meta.build_readme()


def easypan() -> None:
    """Runs `pypan` command line tool."""
    project = Project(
        name=input(colored(">>> Please name your application (e.g bomber): ", "green")).lower(),
        user=User(
            name=input(colored(">>> Please enter your username (e.g John Udot): ", "green")),
            email=input(colored(">>> Please enter your email (e.g user@gmail.com): ", "green")),
        ),
    )
    project.build_package()
    project.build_tests()
    project.build_meta()


if __name__ == "__main__":
    easypan()
