"""Contains interfaces for managing python project."""
import os
import site
import sys
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from punish.style import AbstractStyle
from pypans.file import Template, replace_content, write_to_file

SITE_TEMPLATE: str = os.path.join(
    site.getsitepackages()[0], os.path.dirname(__file__), "template"  # pylint:disable=no-member
)
NEW_LINE: str = "\n"


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
        replace_content(Template.SETUP.value, from_replace="tool", to_replace=self._name)
        replace_content(
            Template.RUNTIME.value,
            from_replace="<version>",
            to_replace=".".join(map(str, sys.version_info[:3])),
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
                f' {NEW_LINE * 2}__author__: str = "{self._user.name}"{NEW_LINE}__email__: str ='
                f' "{self._user.email}"{NEW_LINE}__version__: str = "0.0.0"{NEW_LINE}'
            ),
        )

    def make_as_tool(self) -> None:
        """Creates executable file."""
        write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{NEW_LINE * 3}def main() -> None:{NEW_LINE}    """'
                f'Runs `{self._name}` application."""'
                f"{NEW_LINE * 2}    pass{NEW_LINE * 3}"
                f'if __name__ == "__main__":{NEW_LINE}    pass{NEW_LINE}'
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
            f'`{self._name}` application."""{NEW_LINE}',
        )

    def make_helpers(self) -> None:
        """Creates tests helpers."""
        write_to_file(
            path=os.path.join(self._tests, "markers.py"),
            content=(
                f"import _pytest.mark{NEW_LINE}import pytest{NEW_LINE * 2}"
                f"unit: _pytest.mark.MarkDecorator = pytest.mark.unit{NEW_LINE}"
            ),
        )
        write_to_file(
            path=os.path.join(self._tests, "conftest.py"),
            content=(
                f"from _pytest.config.argparsing import Parser{NEW_LINE}"
                f"from _pytest.fixtures import SubRequest{NEW_LINE}import pytest{NEW_LINE}"
            ),
        )
        write_to_file(
            path=os.path.join(self._tests, "test_sample.py"),
            content=f"import pytest{NEW_LINE * 3}"
            f"def test_me() -> None:{NEW_LINE}    assert True{NEW_LINE}",
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
        Template.files_from(from_path=SITE_TEMPLATE)
        self._builder.meta.build_analyser()
        self._builder.meta.build_authors()
        self._builder.meta.build_license()
        self._builder.meta.build_packaging()
        self._builder.meta.build_pytest()
        self._builder.meta.build_readme()
