import typer

from .common import (complete_task_name, complete_unfinished_task_name,
                     task_repository)
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
    tasks = task_repository.search_by_name(task)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit()
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit()

    event_repository.stop()
    event_repository.start(tasks[0].id)

    task_str = typer.style(tasks[0].name, fg=typer.colors.YELLOW)
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
    tasks = task_repository.search_by_name(task)

    if len(tasks) > 1:
        typer.echo("There are multiple such tasks:")
        for task_sql in tasks:
            typer.echo(f" - {task_sql.name}")

        typer.Exit()
    elif len(tasks) == 0:
        typer.echo("No task found")
        typer.Exit()

    task_repository.finish(tasks[0].id)
    typer.echo("Done")


def entrypoint() -> None:
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
