import os
import shutil
from enum import Enum
from typing import IO


def write_to_file(path: str, content: str, mode: str = "a") -> None:
    with open(path, mode) as file:  # type: IO[str]
        file.write(content)


def replace_content(path: str, from_replace: str, to_replace: str) -> None:
    with open(path) as file:  # type: IO[str]
        write_to_file(path, content=file.read().replace(from_replace, to_replace), mode="w")


class File(Enum):
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

    @classmethod
    def templates_from(cls, from_path: str = "./") -> None:
        for file in File:  # type: File
            shutil.copyfile(os.path.join(from_path, file.value), file.value)
