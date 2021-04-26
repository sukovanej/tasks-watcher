from typing import Optional

import typer

from .common import (
    complete_project_name,
    complete_event_name,
    search_project_or_fail,
    search_event_or_fail,
)
from .database import event_repository
from .view.event import print_events

events_app = typer.Typer()


PROJECT_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_project_name, help="Project name"
)
TASK_NAME_TYPER_OPTION = typer.Option(
    ..., autocompletion=complete_event_name, help="Event name"
)
DESCRIPTION_TYPER_OPTION = typer.Option(None, help="Event description")


@events_app.command(help="List all the events")
def list() -> None:
    events = event_repository.list_all(project)
    print_events(events, full)


@events_app.command(help="Add a new event")
def add(
    name: str,
    project: str = PROJECT_NAME_TYPER_OPTION,
    description: Optional[str] = DESCRIPTION_TYPER_OPTION,
) -> None:
    project_sql = search_project_or_fail(project)
    event_repository.add(name, project_sql.id, description)
    typer.echo(f"{name} added")


@events_app.command(help="Update an existing event")
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

    event_sql = search_event_or_fail(name)
    event_repository.update(event_sql.id, new_name, new_project_id, new_description)
    typer.echo(f"{name} added")


@events_app.command(help="Delete a event")
def delete(event: str = TASK_NAME_TYPER_OPTION):
    event_sql = search_event_or_fail(event)
    event_repository.delete(event_sql.id)
    typer.echo("Done")
