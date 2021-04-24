from typing import Optional

import typer

from .common import complete_category_name, complete_task_name
from .database import task_repository

tasks_app = typer.Typer()


@tasks_app.command(help="List all the tasks")
def list():
    tasks = task_repository.list_all()
    for task in tasks:
        typer.echo(f"[{task.id}] {task.name}")


@tasks_app.command(help="Add a new task")
def add(
    name: str,
    category: int = typer.Option("Category", autocompletion=complete_category_name),
    description: Optional[str] = None,
) -> None:
    task_repository.add(name, category, description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Delete a task")
def delete(id: int = typer.Option("Task", autocompletion=complete_task_name)):
    task_repository.delete(id)
    typer.echo("Done")
