from typing import Sequence

import typer

from ...models import Task
from .aligned import print_aligned


def get_styled_task_name(task: Task) -> str:
    color = typer.colors.YELLOW

    if task.finished_at is not None:
        color = typer.colors.GREEN

    return typer.style(task.name, fg=color)


def print_tasks(all_tasks: Sequence[Task], full: bool) -> None:
    tasks = []

    for task in all_tasks:
        task_project_str = f"[{task.project.name}]"
        task_name_str = get_styled_task_name(task)
        tasks.append([task_project_str, task_name_str])

        if full and task.description:
            tasks.append(["", task.description])

    print_aligned(tasks)
