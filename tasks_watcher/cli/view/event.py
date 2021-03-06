from collections import defaultdict
from datetime import datetime, timedelta
from typing import Sequence

import typer

from ...models import Event
from ...time_diff import time_diff, time_diff_to_str
from .aligned import print_aligned
from .task import get_styled_task_name


def get_status_str(is_in_progress: bool) -> str:
    if not is_in_progress:
        status_str = typer.style("Done", fg=typer.colors.GREEN, bold=True)
    else:
        status_str = typer.style("In progress", fg=typer.colors.WHITE, bold=True)

    return f"[{status_str.rjust(11)}]"


def get_row_from(event: Event) -> Sequence[str]:
    time_diff_str = time_diff(event.started_at, event.stopped_at or datetime.now())
    time_diff_str = typer.style(time_diff_str, fg=typer.colors.YELLOW, bold=True)
    status_str = get_status_str(event.stopped_at is None)

    is_finished = event.stopped_at is not None
    if is_finished:
        time_str = f"took {time_diff_str}"
    else:
        time_str = f"started {time_diff_str} ago"

    return [status_str, event.task.name, time_str]


def print_report(all_events: Sequence[Event]) -> None:
    events_per_task = defaultdict(list)

    for event in all_events:
        events_per_task[event.task.id].append(event)

    table = []
    time_sum = timedelta()

    for events in events_per_task.values():
        total_time = timedelta()
        is_in_progress = False

        for event in events:
            if event.stopped_at is None:
                is_in_progress = True
            total_time += (event.stopped_at or datetime.now()) - event.started_at

        status_str = get_status_str(is_in_progress)
        time_str = time_diff_to_str(total_time)
        task_name = get_styled_task_name(events[0].task)
        time_sum += total_time
        table.append([status_str, task_name, time_str])

    print_aligned(table)

    time_sum_str = typer.style(time_diff_to_str(time_sum), fg=typer.colors.GREEN)
    typer.echo(f"\nYou reported {time_sum_str}")
