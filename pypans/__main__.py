"""Contains interfaces for package tools executor."""
import os
import sys
import click
from termcolor import colored
from punish.style import AbstractStyle
from pypans.file import Template
from pypans.project import Line, Project, User  # noqa: I100


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
        return sys.stdout.write(f"{colored(string, self._color)}{Line.NEW.value}")


class __Environment(AbstractStyle):
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
            os.system(command=f"git config --local user.email {self._user.email}")
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
                string=f">>> 🚨 Setup with git is skipped for `{self._name}` project 🚨",
            )

    def install_requirements(self) -> None:
        """Installs project requirements."""

        def install_from(file: Template) -> None:  # noqa: VNE002
            os.system(command=f"pip install -r {file}")
            if file is Template.REQUIREMENTS:
                os.system(command=f"pip freeze > {file}")
            elif file is Template.DEV_REQUIREMENTS:
                os.system(
                    "pip freeze | egrep "
                    f"'pytest|pdbpp|python|pydoc|black|pylint|mypy|flake8|cov|manifest' > {file}"
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
                string=f">>> 🚨 Dependencies installation is skipped for `{self._name}` project 🚨",
            )


def __build_environment() -> None:
    """Builds fully-fledged environment."""
    green_output: _Output = _Output(color="green")
    green_output.write(string=">>> 🥘 Welcome to `pypan` python project builder utility 🥘",)
    green_output.write(string=">>>")
    name: str = input(colored(">>> Please name your application (e.g bomber): ", "green"))
    environment: __Environment = __Environment(
        name=name,
        user=User(
            name=input(colored(">>> Please enter your username (e.g John Udot): ", "green")),
            email=input(colored(">>> Please enter your email (e.g user@gmail.com): ", "green")),
        ),
    )
    environment.setup_project()
    environment.setup_git()
    environment.install_requirements()
    green_output.write(string=">>>")
    _Output(color="magenta").write(
        string=f">>> 🐍 Successfully created fresh `{name}` python project 🐍"
    )


@click.command()
@click.option(
    "--start",
    show_default=True,
    is_flag=True,
    help=f"""

    Starts python project composer:{Line.NEW.value}
      >>> Configure project packaging for `python`{Line.NEW.value}
      >>> Configure testing environment with `pytest`{Line.NEW.value}
      >>> Configure static code analysis and CI tools{Line.NEW.value}
      >>> Configure readme and changelog{Line.NEW.value}
      >>> Configure project requirements{Line.NEW.value}
      >>> Configure `git` (optional){Line.NEW.value}
      >>> Install python dependencies (optional){Line.NEW.value}
    """,
)
def easypan(start: bool) -> None:
    """Runs `pypan` command line utility.

    Program allows to interactively compose python project template from the scratch.
    """
    if start:
        __build_environment()
    else:
        click.echo(click.get_current_context().get_help())


if __name__ == "__main__":
    easypan()  # pylint:disable=no-value-for-parameter
