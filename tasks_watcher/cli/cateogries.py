import typer

from .common import complete_category_name
from .database import category_repository

categories_app = typer.Typer()


@categories_app.command(help="Display all the categories")
def list():
    categories = category_repository.list_all()
    for category in categories:
        typer.echo(f"[{category.id}] {category.name}")


@categories_app.command(help="Add a new task category")
def add(name: str):
    category_repository.add(name)
    typer.echo(f"{name} added to categories")


@categories_app.command(help="Delete a category")
def delete(id: int = typer.Option("Task", autocompletion=complete_category_name)):
    category_repository.delete(id)
    typer.echo(f"Done")
