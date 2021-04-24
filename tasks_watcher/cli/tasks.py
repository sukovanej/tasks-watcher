from typing import Optional

import typer

from .common import complete_category_name, complete_task_name
from .database import category_repository, task_repository

tasks_app = typer.Typer()


@tasks_app.command(help="List all the tasks")
def list():
    tasks = task_repository.list_all()
    for task in tasks:
        typer.echo(f"[{task.id}] {task.name}")


@tasks_app.command(help="Add a new task")
def add(
    name: str,
    category: str = typer.Option("Category", autocompletion=complete_category_name),
    description: Optional[str] = None,
) -> None:
    categories = category_repository.search_by_name(category)

    if len(categories) > 1:
        typer.echo("There are multiple such categories:")
        for category_sql in categories:
            typer.echo(f" - {category_sql.name}")

        typer.Exit()
    elif len(categories) == 0:
        typer.echo("No task found")
        typer.Exit()

    task_repository.add(name, categories[0].id, description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Update a new task")
def update(
    name: str = typer.Option(..., autocompletion=complete_task_name),
    new_name: Optional[str] = None,
    new_category: Optional[str] = typer.Option(
        "Category", autocompletion=complete_category_name
    ),
    new_description: Optional[str] = None,
) -> None:
    new_category_id = None

    if new_category is not None:
        categories = category_repository.search_by_name(new_category)

        if len(categories) > 1:
            typer.echo("There are multiple such ategories:")
            for category_sql in categories:
                typer.echo(f" - {category_sql.name}")

            typer.Exit()
        elif len(categories) == 0:
            typer.echo("No task found")
            typer.Exit()
        else:
            new_category_id = categories[0].id

    tasks = task_repository.search_by_name(name)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit(1)
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit(1)

    task_repository.update(tasks[0].id, new_name, new_category_id, new_description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Delete a task")
def delete(task: str = typer.Option("Task", autocompletion=complete_task_name)):
    tasks = task_repository.search_by_name(task)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit()
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit()

    task_repository.delete(tasks[0].id)
    typer.echo("Done")
