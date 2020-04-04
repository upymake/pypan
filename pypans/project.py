import os
import site
from abc import abstractmethod
from dataclasses import dataclass
from punish.style import AbstractStyle
from pypans.file import write_to_file, replace_content, File

SITE_TEMPLATE: str = os.path.join(site.getsitepackages()[0], os.path.dirname(__file__), "template")
NEW_LINE: str = "\n"


class Package(AbstractStyle):
    @abstractmethod
    def init(self) -> None:
        pass


@dataclass
class User(AbstractStyle):
    name: str
    email: str


class _Meta(AbstractStyle):
    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user

    def build_analyser(self) -> None:
        replace_content(File.ANALYSER.value, from_replace="<package>", to_replace=self._name)

    def build_readme(self) -> None:
        replace_content(File.README.value, from_replace="<project>", to_replace=self._name)
        replace_content(File.README.value, from_replace="<username>", to_replace=self._user.name)
        replace_content(File.README.value, from_replace="<email>", to_replace=self._user.email)

    def build_license(self) -> None:
        replace_content(File.LICENSE.value, from_replace="<package>", to_replace=self._name)

    def build_packaging(self) -> None:
        replace_content(File.MANIFEST.value, from_replace="<project>", to_replace=self._name)
        replace_content(File.PYPIRC.value, from_replace="<username>", to_replace=self._user.name)
        replace_content(File.SETUP.value, from_replace="package", to_replace=self._name)

    def build_pytest(self) -> None:
        replace_content(File.PYTEST.value, from_replace="<package>", to_replace=self._name)

    def build_authors(self) -> None:
        replace_content(File.AUTHORS.value, from_replace="<username>", to_replace=self._user.name)
        replace_content(File.AUTHORS.value, from_replace="<email>", to_replace=self._user.email)


class _Application(Package):
    def __init__(self, name: str, user: User) -> None:
        self._name: str = name
        self._user: User = user

    def init(self) -> None:
        os.mkdir(self._name)
        write_to_file(
            path=os.path.join(self._name, "__init__.py"),
            content=(
                f'"""Package contains a set of interfaces to operate `{self._name}` application.""" {NEW_LINE * 2}'
                f'__author__: str = "{self._user.name}"{NEW_LINE}__email__: str ='
                f' "{self._user.email}"{NEW_LINE}__version__: str = "0.0.0"{NEW_LINE}'
            ),
        )

    def make_as_tool(self) -> None:
        write_to_file(
            path=os.path.join(self._name, "__main__.py"),
            content=(
                f'"""Represents executable entrypoint for `{self._name}` application."""'
                f'{NEW_LINE * 3}def main() -> None:{NEW_LINE}    """Runs `{self._name}` command line tool."""'
                f"{NEW_LINE * 2}    pass{NEW_LINE * 3}"
                f'if __name__ == "__main__":{NEW_LINE}    pass{NEW_LINE}'
            ),
        )


class _Tests(Package):
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._tests: str = self.__class__.__name__.lower()

    def init(self) -> None:
        os.mkdir(self._tests)
        write_to_file(
            path=os.path.join(self._tests, "__init__.py"),
            content=f'"""Package contains a set of interfaces to test `{self._name}` application."""{NEW_LINE}',
        )

    def make_helpers(self) -> None:
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
            content=f"import pytest{NEW_LINE * 3}" f"def test_me() -> None:{NEW_LINE}    assert True{NEW_LINE}",
        )


class _Builder(AbstractStyle):
    def __init__(self, name: str, user: User) -> None:
        self._app: _Application = _Application(name, user)
        self._tests: _Tests = _Tests(name)
        self._meta: _Meta = _Meta(name, user)

    @property
    def app(self) -> _Application:
        return self._app

    @property
    def tests(self) -> _Tests:
        return self._tests

    @property
    def meta(self) -> _Meta:
        return self._meta


class Project(AbstractStyle):
    def __init__(self, name: str, user: User) -> None:
        self._builder: _Builder = _Builder(name, user)

    def build_package(self) -> None:
        self._builder.app.init()
        self._builder.app.make_as_tool()

    def build_tests(self) -> None:
        self._builder.tests.init()
        self._builder.tests.make_helpers()

    def build_meta(self) -> None:
        File.templates_from(from_path=SITE_TEMPLATE)
        self._builder.meta.build_analyser()
        self._builder.meta.build_authors()
        self._builder.meta.build_license()
        self._builder.meta.build_packaging()
        self._builder.meta.build_pytest()
        self._builder.meta.build_readme()
