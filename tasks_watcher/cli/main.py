from datetime import datetime, timedelta

import typer

from .common import (
    complete_task_name,
    complete_unfinished_task_name,
    search_task_or_fail,
    task_repository,
)
from .database import event_repository, repository
from .projects import projects_app
from .tasks import tasks_app
from .view.aligned import print_aligned
from .view.event import get_row_from, print_report
from .view.timeline import timeline

app = typer.Typer()
app.add_typer(projects_app, name="projects", help="Projects for tasks")
app.add_typer(tasks_app, name="tasks", help="Tasks you are working on")


@app.command(help="Initialize the database")
def init() -> None:
    repository.initialize()
    typer.echo("database initialized")


@app.command(help="Start working on a task")
def start(task: str = typer.Option("Task", autocompletion=complete_task_name)) -> None:
    task_sql = search_task_or_fail(task)

    last_event = event_repository.get_last()

    if last_event is not None:
        stopped_at = last_event.stopped_at or datetime.now()
        last_event_duration = stopped_at - last_event.started_at

        if last_event_duration < timedelta(minutes=1):
            delete_last_event = typer.confirm(
                "The previous event took less then 1min, I can delete it, huh?"
            )

            if delete_last_event:
                event_repository.delete(last_event.id)

    event_repository.stop()
    event_repository.start(task_sql.id)

    task_str = typer.style(task_sql.name, fg=typer.colors.YELLOW)
    typer.echo(f"Task {task_str} started!")


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

    if len(all_events) == 0:
        typer.echo("Nothing reported today yet :(")
        raise typer.Exit()

    typer.secho("Tasks", bold=True, fg=typer.colors.BRIGHT_CYAN)
    typer.secho("-" * 30 + "\n", bold=True, fg=typer.colors.BRIGHT_CYAN)

    print_report(all_events)

    typer.secho("\nTimeline", bold=True, fg=typer.colors.BRIGHT_CYAN)
    typer.secho("-" * 30 + "\n", bold=True, fg=typer.colors.BRIGHT_CYAN)

    timeline(all_events)


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


@app.command(help="Finish a task")
def finish(
    task: str = typer.Option(
        ..., autocompletion=complete_unfinished_task_name, help="Task name"
    )
):
    task_sql = search_task_or_fail(task)
    task_repository.finish(task_sql.id)
    typer.echo("Done")


def entrypoint() -> None:
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
