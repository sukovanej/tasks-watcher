import typer

from .cateogries import categories_app
from .common import complete_task_name
from .database import event_repository, repository
from .tasks import tasks_app

app = typer.Typer()
app.add_typer(categories_app, name="categories")
app.add_typer(tasks_app, name="tasks")


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


def entrypoint():
    repository.connect()
    app()


if __name__ == "__main__":
    entrypoint()
