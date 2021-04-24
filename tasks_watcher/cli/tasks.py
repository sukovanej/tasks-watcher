from typing import Optional

import typer

from .common import complete_category_name, complete_task_name
from .database import category_repository, task_repository
from .view.task import print_tasks

tasks_app = typer.Typer()


CATEGORY_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_category_name, help="Category name"
)
TASK_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_task_name, help="Task name"
)
DESCRIPTION_TYPER_OPTION = typer.Option(None, help="Task description")


@tasks_app.command(help="List all the tasks")
def list():
    tasks = task_repository.list_all()
    print_tasks(tasks)


@tasks_app.command(help="Add a new task")
def add(
    name: str,
    category: str = CATEGORY_NAME_TYPER_OPTION,
    description: Optional[str] = DESCRIPTION_TYPER_OPTION,
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


@tasks_app.command(help="Update an existing task")
def update(
    name: str = TASK_NAME_TYPER_OPTION,
    new_name: Optional[str] = None,
    new_category: Optional[str] = CATEGORY_NAME_TYPER_OPTION,
    new_description: Optional[str] = DESCRIPTION_TYPER_OPTION,
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
def delete(task: str = TASK_NAME_TYPER_OPTION):
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
