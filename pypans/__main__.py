"""Contains interfaces for package tools executor."""
import sys
import click
from termcolor import colored
from pypans.project import Project, User  # noqa: I100


@click.command()
@click.option("--start", "-s", show_default=True, is_flag=True, help="Starts python project composer")
def easypan(start: bool) -> None:
    """Runs `pypan` command line utility.

    Program allows to interactively compose fresh python project from the scratch.
    """
    if start:
        project: Project = Project(
            name=input(colored(">>> Please name your application (e.g bomber): ", "green")).lower(),
            user=User(
                name=input(colored(">>> Please enter your username (e.g John Udot): ", "green")),
                email=input(colored(">>> Please enter your email (e.g user@gmail.com): ", "green")),
            ),
        )
        project.build_package()
        project.build_tests()
        project.build_meta()
        sys.stdout.write(f'{colored("🐍 Successfully created fresh python project 🐍", "magenta")}\n')
    else:
        click.echo(click.get_current_context().get_help())


if __name__ == "__main__":
    easypan()  # pylint:disable=no-value-for-parameter
