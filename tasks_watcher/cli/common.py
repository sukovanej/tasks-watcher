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


def search_task_or_fail(task: str) -> Task:
    tasks = task_repository.search_by_name(task)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit()
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit()

    return tasks[0]


def search_project_or_fail(project: str) -> Project:
    projects = project_repository.search_by_name(project)

    if len(projects) > 1:
        typer.echo("There are multiple such ategories:")
        for project_sql in projects:
            typer.echo(f" - {project_sql.name}")

        typer.Exit()
    elif len(projects) == 0:
        typer.echo("No task found")
        typer.Exit()

    return projects[0]
