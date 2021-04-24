from typing import Optional

import typer

from .common import complete_project_name, complete_task_name
from .database import project_repository, task_repository
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
def list():
    tasks = task_repository.list_all()
    print_tasks(tasks)


@tasks_app.command(help="Add a new task")
def add(
    name: str,
    project: str = PROJECT_NAME_TYPER_OPTION,
    description: Optional[str] = DESCRIPTION_TYPER_OPTION,
) -> None:
    projects = project_repository.search_by_name(project)

    if len(projects) > 1:
        typer.echo("There are multiple such projects:")
        for project_sql in projects:
            typer.echo(f" - {project_sql.name}")

        typer.Exit()
    elif len(projects) == 0:
        typer.echo("No task found")
        typer.Exit()

    task_repository.add(name, projects[0].id, description)
    typer.echo(f"{name} added")


@tasks_app.command(help="Update an existing task")
def update(
    name: str = TASK_NAME_TYPER_OPTION,
    new_name: Optional[str] = None,
    new_project: Optional[str] = PROJECT_NAME_TYPER_OPTION,
    new_description: Optional[str] = DESCRIPTION_TYPER_OPTION,
) -> None:
    new_project_id = None

    if new_project is not None:
        projects = project_repository.search_by_name(new_project)

        if len(projects) > 1:
            typer.echo("There are multiple such ategories:")
            for project_sql in projects:
                typer.echo(f" - {project_sql.name}")

            typer.Exit()
        elif len(projects) == 0:
            typer.echo("No task found")
            typer.Exit()
        else:
            new_project_id = projects[0].id

    tasks = task_repository.search_by_name(name)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit(1)
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit(1)

    task_repository.update(tasks[0].id, new_name, new_project_id, new_description)
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
