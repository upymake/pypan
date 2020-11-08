"""Contains interfaces for package tools executor."""
import os
import sys
from enum import Enum
import click
from termcolor import colored
from punish.style import AbstractStyle
from pypans import __version__
from pypans.file import Template
from pypans.project import Line, Project, User  # noqa: I100


class _Emoji(Enum):
    """The class represents `emoji` item."""

    SIREN: str = "🚨"
    PAN: str = "🥘"
    SNAKE: str = "🐍"

    def __str__(self) -> str:
        """Returns emoji value."""
        return self.value


class _Output(AbstractStyle):
    """A command line output."""

    def __init__(self, color: str) -> None:
        self._color: str = color

    def write(self, string: str) -> int:
        """Writes data into colored output.

        Args:
            string (str): given string.

        Returns number of characters to write.
        """
        return sys.stdout.write(f"{colored(string, self._color)}{Line.NEW}")


class _Environment(AbstractStyle):
    """Representation of project environment."""

    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user
        self._project: Project = Project(name, user)
        self.__red_out: _Output = _Output(color="red")

    def setup_project(self) -> None:
        """Builds given project."""
        self._project.build_package()
        self._project.build_tests()
        self._project.build_meta()

    def setup_git(self) -> None:
        """Sets up git for a project."""

        def prepare(to_repo: str) -> None:
            os.system(command="git init")
            os.system(command=f"git config --local user.name {self._user.name}")
            os.system(
                command=f"git config --local user.email {self._user.email}"
            )
            os.system(command=f"git remote add origin {to_repo}")

        git: str = input(
            colored(
                f">>> Would you like to setup git for `{self._name}` project? (yes/no): ",
                color="green",
            )
        )
        if git == "yes":
            prepare(
                to_repo=input(
                    colored(
                        ">>> Please enter github repo (e.g git@github:user/project.git): ",
                        color="green",
                    )
                )
            )
        else:
            self.__red_out.write(
                string=(
                    f">>> {_Emoji.SIREN} Setup with git is skipped for "
                    f"`{self._name}` project {_Emoji.SIREN}"
                )
            )

    def install_requirements(self) -> None:
        """Installs project requirements."""

        def install_from(file: Template) -> None:  # noqa: VNE002
            os.system(command=f"pip install -r {file}")
            if file is Template.REQUIREMENTS:
                os.system(command=f"pip freeze > {file}")
            elif file is Template.DEV_REQUIREMENTS:
                os.system(
                    "pip freeze | egrep 'pytest|pdbpp|python|pydoc|"
                    f"black|pylint|mypy|flake8|cov|manifest|gate' > {file}"
                )
            else:
                raise ValueError(f"'{file}' template is not supported!")

        install: str = input(
            colored(
                f">>> Would you like to install dependencies for "
                f"`{self._name}` project? (yes/no): ",
                color="green",
            )
        )
        if install == "yes":
            install_from(file=Template.REQUIREMENTS)
            install_from(file=Template.DEV_REQUIREMENTS)
        else:
            self.__red_out.write(
                string=(
                    f">>> {_Emoji.SIREN} Dependencies installation is skipped"
                    f" for `{self._name}` project {_Emoji.SIREN}"
                )
            )


def _build_environment() -> None:
    """Builds fully-fledged environment."""
    green_output: _Output = _Output(color="green")
    green_output.write(
        string=f">>> {_Emoji.PAN} Welcome to `pypan` python project "
        f"builder utility {_Emoji.PAN}",
    )
    green_output.write(string=">>>")
    name: str = input(
        colored(">>> Please name your application (e.g bomber): ", "green")
    )
    environment: _Environment = _Environment(
        name=name,
        user=User(
            name=input(
                colored(
                    ">>> Please enter your username (e.g John Udot): ", "green"
                )
            ),
            email=input(
                colored(
                    ">>> Please enter your email (e.g user@gmail.com): ",
                    "green",
                )
            ),
        ),
    )
    environment.setup_project()
    environment.setup_git()
    environment.install_requirements()
    green_output.write(string=">>>")
    _Output(color="magenta").write(
        string=(
            f">>>  {_Emoji.SNAKE} Successfully created fresh "
            f"`{name}` python project  {_Emoji.SNAKE}"
        )
    )


@click.command()
@click.option(
    "--start",
    show_default=True,
    is_flag=True,
    help=f"""

    Starts python project composer:{Line.NEW}
      >>> Configure project packaging for `python`{Line.NEW}
      >>> Configure testing environment with `pytest`{Line.NEW}
      >>> Configure static code analysis and CI tools{Line.NEW}
      >>> Configure readme and changelog{Line.NEW}
      >>> Configure project requirements{Line.NEW}
      >>> Configure `git` (optional){Line.NEW}
      >>> Install python dependencies (optional){Line.NEW}
    """,
)
@click.option(
    "--version", "-v", is_flag=True, default=False, help="Display tool version."
)
def _easypan(start: bool, version: bool) -> None:
    """Runs `pypan` command line utility.

    Program allows to interactively compose
    python project template from the scratch.
    """
    if start:
        return _build_environment()
    if version:
        return click.echo(f'Version {__version__}')
    return click.echo(click.get_current_context().get_help())


if __name__ == "__main__":
    _easypan()  # pylint:disable=no-value-for-parameter
