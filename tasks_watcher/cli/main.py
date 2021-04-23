from datetime import datetime

import typer

from ..time_diff import time_diff
from ..models import Event
from .cateogries import categories_app
from .common import complete_task_name
from .database import event_repository, repository
from .tasks import tasks_app
from .aligned import print_aligned

app = typer.Typer()
app.add_typer(categories_app, name="categories")
app.add_typer(tasks_app, name="tasks")


def get_row_from(event: Event) -> None:
    task = event.task
    is_finished = event.stopped_at is not None

    time_diff_str = time_diff(event.started_at, event.stopped_at or datetime.now())

    if is_finished:
        time_str = f"took {time_diff_str}"
        status_str = typer.style("Done", fg=typer.colors.GREEN, bold=True)
    else:
        time_str = f"started {time_diff_str} ago"
        status_str = typer.style("In progress", fg=typer.colors.WHITE, bold=True)

    status_str = f"[{status_str.rjust(11)}]"

    return [status_str, task.name, time_str]


@app.command()
def init() -> None:
    repository.initialize()
    typer.echo(f"database initialized")


@app.command()
def start(
    task_id: int = typer.Option("Task", autocompletion=complete_task_name)
) -> None:
    event_repository.start(task_id)
    typer.echo(f"{task_id} started")


@app.command()
def stop() -> None:
    stopped_event = event_repository.stop()
    typer.echo(f"stopped")


@app.command()
def show() -> None:
    active_event = event_repository.get_active()
    if active_event is None:
        typer.echo(f"no active task, you lazy pig")
    else:
        print_event(active_event)


@app.command()
def events() -> None:
    events = event_repository.list_all()
    table = [get_row_from(e) for e in events]
    print_aligned(table)


@app.command()
def report() -> None:
    events = event_repository.list_today()
    table = [get_row_from(e) for e in events]
    print_aligned(table)


def entrypoint():
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
