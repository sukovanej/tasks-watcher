from datetime import datetime
from typing import Optional, Sequence

from ..models import Event
from .project_repository import ALL_PROJECT_COLUMNS
from .repository import Repository
from .task_repository import ALL_TASK_COLUMNS

ALL_EVENT_COLUMNS = "e.id, e.created_at, e.started_at, e.stopped_at"

BASE_QUERY = f"""
    SELECT {ALL_EVENT_COLUMNS}, {ALL_TASK_COLUMNS}, {ALL_PROJECT_COLUMNS}
    FROM events e
    JOIN tasks t ON t.id = e.task_id
    JOIN projects p ON p.id = t.project_id
"""


class EventRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> Sequence[Event]:
        self._repository.execute(f"{BASE_QUERY};")
        return self._repository.fetchall_using_model(Event)

    def get_active(self) -> Optional[Event]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE e.stopped_at is null;
            """
        )
        return self._repository.fetch_using_model(Event)

    def list_today(self) -> Sequence[Event]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE date(e.started_at) = date('now', 'localtime');
            """
        )
        return self._repository.fetchall_using_model(Event)

    def list_yesterday(self) -> Sequence[Event]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE date(e.started_at) = date('now', '-1 day', 'localtime');
            """
        )
        return self._repository.fetchall_using_model(Event)

    def start(self, task_id: int) -> None:
        self._repository.execute(
            "INSERT INTO events (task_id, started_at) VALUES (?, ?);",
            (task_id, datetime.now()),
        )
        self._repository.commit()

    def stop(self) -> None:
        self._repository.execute(
            "UPDATE events SET stopped_at = ? WHERE stopped_at is NULL;",
            (datetime.now(),),
        )
        self._repository.commit()
