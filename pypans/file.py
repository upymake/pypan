"""Contains interfaces for managing files."""
import os
import shutil
from enum import Enum
from typing import Any, IO


def write_to_file(path: str, content: str, mode: str = "a") -> None:
    """Writes content into filepath."""
    with open(path, mode) as file:  # type: IO[str]
        file.write(content)


def replace_content(path: str, from_replace: str, to_replace: str) -> None:
    """Replaces file content."""
    with open(path) as file:  # type: IO[str]
        write_to_file(path, content=file.read().replace(from_replace, to_replace), mode="w")


class Template(Enum):
    """Represents a template."""

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
    RUNTIME: str = "runtime.txt"
    SETUP: str = "setup.py"

    @classmethod
    def files_from(cls, from_path: str = "./") -> None:
        """Creates template files from given path."""
        for template in cls:  # type: Template
            shutil.copyfile(os.path.join(from_path, template.value), template.value)

    def __str__(self) -> Any:
        """Returns value of a template."""
        return self.value
