from typing import List, Tuple

import typer

from ..models import Project, Task
from .database import project_repository, task_repository


def complete_project_name(incomplete: str) -> List[str]:
    projects = project_repository.search_by_name(incomplete)
    project_names = [c.name for c in projects]
    return project_names


def complete_task_name(incomplete: str) -> List[Tuple[str, str]]:
    projects = task_repository.search_by_name(incomplete)
    project_names = [(c.name, c.project.name) for c in projects]
    return project_names


def complete_unfinished_task_name(incomplete: str) -> List[Tuple[str, str]]:
    projects = task_repository.search_by_name_unfinished(incomplete)
    project_names = [(c.name, c.project.name) for c in projects]
    return project_names


def check_int_input_in_range(input_str: str, start: int, end: int) -> int:
    if not input_str.isdigit():
        typer.echo("I expected integer value :(")
        raise typer.Exit(1)

    value_int = int(input_str)

    if value_int > end or value_int < start:
        typer.echo(f"Please choose a value in range {start} - {end}")
        raise typer.Exit(1)

    return value_int


def search_task_or_fail(task: str) -> Task:
    tasks = task_repository.search_by_name(task)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for id, task_sql in enumerate(tasks):
            typer.echo(f" [{id + 1}] {task_sql.name}")

        task_id_str = typer.prompt("What task do you mean?")
        task_id = check_int_input_in_range(task_id_str, 1, len(tasks))
        return tasks[task_id - 1]

    elif len(tasks) == 0:
        typer.echo("No task found")
        raise typer.Exit()

    return tasks[0]


def search_project_or_fail(project: str) -> Project:
    projects = project_repository.search_by_name(project)

    if len(projects) > 1:
        typer.echo("There are multiple such ategories:")
        for project_sql in projects:
            typer.echo(f" - {project_sql.name}")

        raise typer.Exit()
    elif len(projects) == 0:
        typer.echo("No task found")
        raise typer.Exit()

    return projects[0]
