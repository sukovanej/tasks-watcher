from typing import List, Optional
from datetime import datetime

from ..models import Event
from .repository import Repository


class EventRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> List[Event]:
        self._repository.execute(
            """
            SELECT e.created_at, e.started_at, e.stopped_at, t.id, t.created_at, t.name, t.description, c.id, c.created_at, c.name
            FROM events e
            JOIN tasks t ON t.id = e.task_id;
            JOIN categories c ON c.id = t.category_id;
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
            "UPDATE events SET stopped_at = ? WHERE stopped_at is NULL RETURNING id;",
            (datetime.now(),),
        )
        self._repository.fetchall()
