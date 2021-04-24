from typing import Sequence

import typer

from ...models import Task
from .aligned import print_aligned


def print_tasks(all_tasks: Sequence[Task]) -> None:
    tasks = []

    for task in all_tasks:
        task_project_str = f"[{task.project.name}]"
        task_name_str = typer.style(task.name, fg=typer.colors.YELLOW)
        tasks.append([task_project_str, task_name_str])

    print_aligned(tasks)
