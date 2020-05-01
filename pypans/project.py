"""Contains interfaces for managing python project."""
import os
import site
import sys
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from punish.style import AbstractStyle
from pypans.file import Template, replace_content, write_to_file


class Line(Enum):
    """Represents string line."""

    NEW: str = "\n"

    def by_(self, times: int) -> str:
        """Multiplies line by given number.

        Args:
            times (int): a multiplier number
        """
        return self.value * times


def _copy_site_files_here() -> None:
    """Copies all files from site packaging location into current root location."""
    Template.files_from(
        from_path=os.path.join(
            site.getsitepackages()[0],  # pylint:disable=no-member
            os.path.dirname(__file__),
            "template",
        )
    )


class Package(AbstractStyle):
    """Represents an abstract interface for a package."""

    @abstractmethod
    def init(self) -> None:
        """Initializes a package content."""
        pass


@dataclass
class User(AbstractStyle):
    """Represents an abstract interface for user."""

    name: str
    email: str


class _Meta(AbstractStyle):
    """Represents meta content builder."""

    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user

    def build_analyser(self) -> None:
        """Builds analyser file."""
        replace_content(Template.ANALYSER.value, from_replace="<package>", to_replace=self._name)
        os.system(command=f"chmod a+x {Template.ANALYSER}")

    def build_readme(self) -> None:
        """Builds readme file."""
        replace_content(Template.README.value, from_replace="<package>", to_replace=self._name)
        replace_content(
            Template.README.value, from_replace="<username>", to_replace=self._user.name
        )
        replace_content(Template.README.value, from_replace="<email>", to_replace=self._user.email)

    def build_license(self) -> None:
        """Builds license file."""
        replace_content(
            Template.LICENSE.value, from_replace="<year>", to_replace=str(datetime.now().year)
        )
        replace_content(
            Template.LICENSE.value, from_replace="<username>", to_replace=self._user.name
        )

    def build_packaging(self) -> None:
        """Builds packaging files."""
        replace_content(
            Template.CHANGELOG.value,
            from_replace="<date>",
            to_replace="{:%d.%m.%Y}".format(datetime.now()),
        )
        replace_content(Template.MANIFEST.value, from_replace="<package>", to_replace=self._name)
        replace_content(
            Template.PYPIRC.value,
            from_replace="<username>",
            to_replace=self._user.name.lower().replace(" ", "."),
        )
        replace_content(Template.SETUP.value, from_replace="tooling", to_replace=self._name)
        replace_content(
            Template.RUNTIME.value,
            from_replace="<version>",
            to_replace=".".join(map(str, sys.version_info[:3])),
        )
        replace_content(
            Template.PROCFILE.value, from_replace="<package>", to_replace=self._name,
        )
        write_to_file(
            path=f"{self._name}.py",
            content=f"# flake8: noqa{Line.NEW.value}"
            f'"""Module contains entrypoint interfaces for an application."""{Line.NEW.by_(2)}'
            f"from {self._name} import app{Line.NEW.value}",
        )

    def build_pytest(self) -> None:
        """Builds pytest file."""
        replace_content(Template.PYTEST.value, from_replace="<package>", to_replace=self._name)

    def build_authors(self) -> None:
        """Builds authors file."""
        replace_content(
            Template.AUTHORS.value, from_replace="<username>", to_replace=self._user.name
        )
        replace_content(Template.AUTHORS.value, from_replace="<email>", to_replace=self._user.email)


class _Application(Package):
    """Represents application content builder."""

    def __init__(self, name: str, user: User) -> None:  # pylint: disable=super-init-not-called
        self._name: str = name
        self._user: User = user

    def init(self) -> None:
        """Initializes an application content."""
        os.mkdir(self._name)
        write_to_file(
            path=os.path.join(self._name, "__init__.py"),
            content=(
                f'"""Package contains a set of interfaces to operate `{self._name}` application."""'
                f" {Line.NEW.by_(2)}__author__: str = "
                f'"{self._user.name}"{Line.NEW.value}__email__: str ='
                f' "{self._user.email}"{Line.NEW.value}__license__: str = "MIT"{Line.NEW.value}'
                f'__copyright__: str = f"Copyright '
                f'{datetime.now().year}, {{__author__}}"{Line.NEW.value}'
                f'__version__: str = "0.0.0"{Line.NEW.by_(2)}'
                f"app = None{Line.NEW.value}"
            ),
        )

    def make_as_tool(self) -> None:
        """Creates executable file."""
        write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{Line.NEW.by_(3)}def main() -> None:{Line.NEW.value}    """'
                f'Runs `{self._name}` application."""'
                f"{Line.NEW.by_(2)}    pass{Line.NEW.by_(3)}"
                f'if __name__ == "__main__":{Line.NEW.value}    main(){Line.NEW.value}'
            ),
        )


class _Tests(Package):
    """Represents tests content builder."""

    def __init__(self, name: str) -> None:  # pylint: disable=super-init-not-called
        self._name: str = name
        self._tests: str = self.__class__.__name__.lower()[1:]

    def init(self) -> None:
        """Initializes tests content."""
        os.mkdir(self._tests)
        write_to_file(
            path=os.path.join(self._tests, "__init__.py"),
            content=f'"""Package contains a set of interfaces to test '
            f'`{self._name}` application."""{Line.NEW.value}',
        )

    def make_helpers(self) -> None:
        """Creates tests helpers."""
        write_to_file(
            path=os.path.join(self._tests, "markers.py"),
            content=(
                f"# flake8: noqa{Line.NEW.value}"
                f"import _pytest.mark{Line.NEW.value}import pytest{Line.NEW.by_(2)}"
                f"unit: _pytest.mark.MarkDecorator = pytest.mark.unit{Line.NEW.value}"
            ),
        )
        write_to_file(
            path=os.path.join(self._tests, "conftest.py"),
            content=(
                f"# flake8: noqa{Line.NEW.value}"
                f"from _pytest.config.argparsing import Parser{Line.NEW.value}"
                f"from _pytest.fixtures import "
                f"SubRequest{Line.NEW.value}import pytest{Line.NEW.value}"
            ),
        )
        write_to_file(
            path=os.path.join(self._tests, "test_sample.py"),
            content=f"# flake8: noqa{Line.NEW.value}"
            f"import pytest{Line.NEW.value}"
            f"from tests.markers import unit{Line.NEW.by_(2)}"
            f"pytestmark = unit{Line.NEW.by_(3)}"
            f"def test_me() -> None:{Line.NEW.value}    assert True{Line.NEW.value}",
        )


class _Builder(AbstractStyle):
    """Represents project builder."""

    def __init__(self, name: str, user: User) -> None:
        self._app: _Application = _Application(name, user)
        self._tests: _Tests = _Tests(name)
        self._meta: _Meta = _Meta(name, user)

    @property
    def app(self) -> _Application:
        """Returns application builder."""
        return self._app

    @property
    def tests(self) -> _Tests:
        """Returns tests builder."""
        return self._tests

    @property
    def meta(self) -> _Meta:
        """Returns meta builder."""
        return self._meta


class Project(AbstractStyle):
    """Represents a project."""

    def __init__(self, name: str, user: User) -> None:
        self._builder: _Builder = _Builder(name, user)

    def build_package(self) -> None:
        """Builds an application package."""
        self._builder.app.init()
        self._builder.app.make_as_tool()

    def build_tests(self) -> None:
        """Builds tests package."""
        self._builder.tests.init()
        self._builder.tests.make_helpers()

    def build_meta(self) -> None:
        """Builds meta files."""
        _copy_site_files_here()
        self._builder.meta.build_analyser()
        self._builder.meta.build_authors()
        self._builder.meta.build_license()
        self._builder.meta.build_packaging()
        self._builder.meta.build_pytest()
        self._builder.meta.build_readme()
