from typing import Optional

import typer

from .common import (
    complete_project_name,
    complete_task_name,
    search_project_or_fail,
    search_task_or_fail,
)
from .database import task_repository
from .view.task import print_tasks

tasks_app = typer.Typer()


PROJECT_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_project_name, help="Project name"
)
TASK_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_task_name, help="Task name"
)
DESCRIPTION_TYPER_OPTION = typer.Option(None, help="Task description")


@tasks_app.command(help="List all the tasks")
def list(
    full: bool = False,
    unfinished: bool = False,
    project: Optional[str] = typer.Option(
        None, autocompletion=complete_project_name, help="Project name"
    ),
) -> None:
    if unfinished:
        tasks = task_repository.list_all_unfinished(project)
    else:
        tasks = task_repository.list_all(project)
    print_tasks(tasks, full)


@tasks_app.command(help="Add a new task")
def add(
    name: str,
    project: str = PROJECT_NAME_TYPER_OPTION,
    description: Optional[str] = DESCRIPTION_TYPER_OPTION,
) -> None:
    project_sql = search_project_or_fail(project)
    task_repository.add(name, project_sql.id, description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Update an existing task")
def update(
    name: str = TASK_NAME_TYPER_OPTION,
    new_name: Optional[str] = typer.Option(None, help="Change the name"),
    new_project: Optional[str] = typer.Option(
        None, autocompletion=complete_project_name, help="Assign to a different project"
    ),
    new_description: Optional[str] = typer.Option(None, help="Modify the description"),
) -> None:
    new_project_id = None

    if new_project is not None:
        project_sql = search_project_or_fail(new_project)
        new_project_id = project_sql.id

    task_sql = search_task_or_fail(name)
    task_repository.update(task_sql.id, new_name, new_project_id, new_description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Delete a task")
def delete(task: str = TASK_NAME_TYPER_OPTION):
    task_sql = search_task_or_fail(task)
    task_repository.delete(task_sql.id)
    typer.echo("Done")
