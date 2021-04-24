import typer

from .common import complete_project_name
from .database import project_repository

projects_app = typer.Typer()


@projects_app.command(help="Display all the projects")
def list():
    projects = project_repository.list_all()
    for project in projects:
        typer.echo(f"[{project.id}] {project.name}")


@projects_app.command(help="Add a new task project")
def add(name: str):
    project_repository.add(name)
    typer.echo(f"{name} added to projects")


@projects_app.command(help="Delete a project")
def delete(id: int = typer.Option("Task", autocompletion=complete_project_name)):
    project_repository.delete(id)
    typer.echo("Done")
