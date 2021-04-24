import typer

from .cateogries import categories_app
from .common import complete_task_name
from .database import event_repository, repository
from .tasks import tasks_app
from .view.aligned import print_aligned
from .view.event import get_row_from, print_report

app = typer.Typer()
app.add_typer(categories_app, name="categories", help="Categories for tasks")
app.add_typer(tasks_app, name="tasks", help="Tasks you are working on")


@app.command(help="Initialize the database")
def init() -> None:
    repository.initialize()
    typer.echo(f"database initialized")


@app.command(help="Start working on a task")
def start(
    task_id: int = typer.Option("Task", autocompletion=complete_task_name)
) -> None:
    event_repository.start(task_id)
    typer.echo(f"{task_id} started")


@app.command(help="Stop the current task")
def stop() -> None:
    stopped_event = event_repository.stop()
    typer.echo(f"stopped")


@app.command(help="Show what you're doing right now")
def show() -> None:
    active_event = event_repository.get_active()
    if active_event is None:
        typer.echo(f"no active task, you lazy pig")
    else:
        typer.echo(" ".join(get_row_from(active_event)))


@app.command(help="Get all the recorded events")
def events() -> None:
    events = event_repository.list_all()
    table = [get_row_from(e) for e in events]
    print_aligned(table)


@app.command(help="Show how you're doing today")
def report() -> None:
    events = event_repository.list_today()
    print_report(events)


@app.command(help="Print tasks from yesterday")
def standup() -> None:
    events = event_repository.list_yesterday()
    print_report(events)


def entrypoint():
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
