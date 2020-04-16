"""Contains interfaces for package tools executor."""
import os
import sys
import click
from termcolor import colored
from punish.style import AbstractStyle
from pypans.file import Template
from pypans.project import NEW_LINE, Project, User  # noqa: I100


def _write_as_colored(string: str, color: str) -> int:
    """Writes data into colored output.

    Returns number of characters to write.
    """
    return sys.stdout.write(f"{colored(string, color)}{NEW_LINE}")


class __Environment(AbstractStyle):
    """Representation of project environment."""

    def __init__(self, name: str, user: User) -> None:
        self._name = name
        self._user = user
        self._project: Project = Project(name, user)

    def setup_project(self) -> None:
        """Builds given project."""
        self._project.build_package()
        self._project.build_tests()
        self._project.build_meta()

    def setup_git(self) -> None:
        """Sets up git for a project."""

        def prepare(to_repo: str) -> None:
            os.system("git init")
            os.system(f"git config --local user.name {self._user.name}")
            os.system(f"git config --local user.email {self._user.email}")
            os.system(f"git remote add origin {to_repo}")

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
            _write_as_colored(
                string=f">>> 🚨 Setup with git is skipped for `{self._name}` project 🚨", color="red"
            )

    def install_requirements(self) -> None:
        """Installs project requirements."""

        def install_from(file: Template) -> None:  # noqa: VNE002
            os.system(f"pip install -r {file}")
            if file is Template.REQUIREMENTS:
                os.system(f"pip freeze > {file}")
            else:
                os.system(
                    "pip freeze | egrep "
                    f"'pytest|pdbpp|python|pydoc|black|pylint|mypy|flake8|cov' > {file}"
                )

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
            _write_as_colored(
                string=f">>> 🚨 Dependencies installation is skipped for `{self._name}` project 🚨",
                color="red",
            )


def __build_environment() -> None:
    """Builds fully-fledged environment."""
    _write_as_colored(
        string=">>> 🥘 Welcome to `pypan` python project builder utility 🥘", color="green"
    )
    _write_as_colored(string=">>>", color="green")
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
    _write_as_colored(string=">>>", color="green")
    _write_as_colored(
        string=f">>> 🐍 Successfully created fresh `{name}` python project 🐍", color="magenta"
    )


@click.command()
@click.option(
    "--start",
    show_default=True,
    is_flag=True,
    help=f"""

    Starts python project composer:{NEW_LINE}
      >>> Configure project packaging for `python`{NEW_LINE}
      >>> Configure testing environment with `pytest`{NEW_LINE}
      >>> Configure static code analysis and CI tools{NEW_LINE}
      >>> Configure readme and changelog{NEW_LINE}
      >>> Configure project requirements{NEW_LINE}
      >>> Configure `git` (optional){NEW_LINE}
      >>> Install python dependencies (optional){NEW_LINE}
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
