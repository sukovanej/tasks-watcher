from datetime import datetime, timedelta
from typing import Sequence

import typer

from ...models import Project, Event, Task

BREAK_PROJECT = Project(id=-1, created_at=datetime.now(), name="-")
BREAK_TASK = Task(id=-1, created_at=datetime.now(), name="-", project=BREAK_PROJECT)


def create_empty_event(started_at: datetime, stopped_at: datetime) -> Event:
    now = datetime.now()
    return Event(
        id=-1,
        created_at=now,
        started_at=started_at,
        stopped_at=stopped_at,
        task=BREAK_TASK,
    )


def get_time_range_str(event: Event) -> str:
    start, end = event.started_at, event.stopped_at
    start_str = f"{start.hour:02d}:{start.minute:02d}"
    end_str = "now" if end is None else f"{end.hour:02d}:{end.minute:02d}"
    return f"{start_str} - {end_str}"


def timeline(events: Sequence[Event]) -> None:
    max_gap = timedelta(minutes=5)
    now = datetime.now()
    start_of_day = now.replace(minute=0, hour=0)
    first_event = events[0]
    filled_events = [create_empty_event(start_of_day, first_event.started_at)]

    for event in events:
        previous_event = filled_events[-1]
        stopped_at = previous_event.stopped_at

        # the same task was reported with a small time gap again => merge it together
        if (
            stopped_at is not None
            and event.started_at - stopped_at < max_gap
            and event.task == previous_event.task
        ):
            previous_event.stopped_at = event.stopped_at
            continue

        if stopped_at is not None and (event.started_at - stopped_at > max_gap):
            break_event = create_empty_event(stopped_at, event.started_at)
            filled_events.append(break_event)

        filled_events.append(event)

    for event in filled_events:
        time_str = get_time_range_str(event).ljust(14)
        color = typer.colors.WHITE

        if event.task != BREAK_TASK:
            color = typer.colors.YELLOW

        task_str = typer.style(event.task.name, fg=color)
        typer.echo(f"{time_str} {task_str}")
