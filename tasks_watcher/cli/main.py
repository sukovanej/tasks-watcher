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
    typer.echo("database initialized")


@app.command(help="Start working on a task")
def start(
    task_id: int = typer.Option("Task", autocompletion=complete_task_name)
) -> None:
    event_repository.start(task_id)
    typer.echo(f"{task_id} started")


@app.command(help="Stop the current task")
def stop() -> None:
    event_repository.stop()
    typer.echo("stopped")


@app.command(help="Show what you're doing right now")
def show() -> None:
    active_event = event_repository.get_active()
    if active_event is None:
        typer.echo("no active task, you lazy pig")
    else:
        typer.echo(" ".join(get_row_from(active_event)))


@app.command(help="Get all the recorded events")
def events() -> None:
    all_events = event_repository.list_all()
    table = [get_row_from(e) for e in all_events]
    print_aligned(table)


@app.command(help="Show how you're doing today")
def report() -> None:
    all_events = event_repository.list_today()
    print_report(all_events)


@app.command(help="Print tasks from yesterday")
def standup() -> None:
    yesterday_events = event_repository.list_yesterday()
    task_names = {
        typer.style(e.task.name, fg=typer.colors.YELLOW, bold=True)
        for e in yesterday_events
    }
    if task_names:
        tasks_str = ", ".join(sorted(task_names))
        typer.echo(f"Yesterday you worked on {tasks_str}")
    else:
        typer.echo("There is nothing from yesterday. Were you even working? :(")


def entrypoint() -> None:
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
