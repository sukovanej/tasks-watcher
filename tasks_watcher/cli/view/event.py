from collections import defaultdict
from datetime import datetime, timedelta
from typing import Sequence

import typer

from ...models import Event
from ...time_diff import time_diff, time_diff_to_str
from .aligned import print_aligned


def get_status_str(event: Event) -> str:
    is_finished = event.stopped_at is not None

    if is_finished:
        status_str = typer.style("Done", fg=typer.colors.GREEN, bold=True)
    else:
        status_str = typer.style("In progress", fg=typer.colors.WHITE, bold=True)

    return f"[{status_str.rjust(11)}]"


def get_row_from(event: Event) -> Sequence[str]:
    time_diff_str = time_diff(event.started_at, event.stopped_at or datetime.now())
    time_diff_str = typer.style(time_diff_str, fg=typer.colors.YELLOW, bold=True)
    status_str = get_status_str(event)

    is_finished = event.stopped_at is not None
    if is_finished:
        time_str = f"took {time_diff_str}"
    else:
        time_str = f"started {time_diff_str} ago"

    return [status_str, event.task.name, time_str]


def print_report(events: Sequence[Event]) -> None:
    events_per_task = defaultdict(list)

    for event in events:
        events_per_task[event.task.id].append(event)

    table = []

    for events in events_per_task.values():
        total_time = timedelta()

        for event in events:
            total_time += (event.stopped_at or datetime.now()) - event.started_at

        status_str = get_status_str(events[0])
        time_str = time_diff_to_str(total_time)
        table.append([status_str, events[0].task.name, time_str])

    print_aligned(table)
