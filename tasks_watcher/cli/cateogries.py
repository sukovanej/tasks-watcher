import typer

from .database import category_repository
from .common import complete_category_name

categories_app = typer.Typer()


@categories_app.command()
def list():
    categories = category_repository.list_all()
    for category in categories:
        typer.echo(f"[{category.id}] {category.name}")


@categories_app.command()
def add(name: str):
    categories = category_repository.add(name)
    typer.echo(f"{name} added to categories")


@categories_app.command()
def delete(id: int = typer.Option("Task", autocompletion=complete_category_name)):
    categories = category_repository.delete(id)
    typer.echo(f"Done")
