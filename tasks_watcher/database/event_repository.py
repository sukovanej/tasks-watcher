from datetime import datetime
from typing import List, Optional

from ..models import Event
from .repository import Repository

BASE_QUERY = """
    SELECT e.id, e.created_at, e.started_at, e.stopped_at, t.id, t.created_at,
        t.name, t.description, c.id, c.created_at, c.name
    FROM events e
    JOIN tasks t ON t.id = e.task_id
    JOIN categories c ON c.id = t.category_id
"""


class EventRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> List[Event]:
        self._repository.execute(f"{BASE_QUERY};")
        return self._repository.fetchall_using_model(Event)

    def get_active(self) -> List[Event]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE e.stopped_at is null;
            """
        )
        return self._repository.fetch_using_model(Event)

    def list_today(self) -> List[Event]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE date(e.started_at) = date('now', 'localtime');
            """
        )
        return self._repository.fetchall_using_model(Event)

    def list_yesterday(self) -> List[Event]:
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
