"""Contains interfaces for package tools executor."""
from termcolor import colored
from pypans.project import User, Project


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
