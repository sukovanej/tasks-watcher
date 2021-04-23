from typing import List, Optional

from ..models import Task
from .repository import Repository


class TaskRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> List[Task]:
        self._repository.execute(
            """
            SELECT t.id, t.created_at, t.name, t.description, c.id, c.created_at, c.name
            FROM tasks t
            JOIN categories c ON c.id = t.category_id;
            """
        )
        return self._repository.fetchall_using_model(Task)

    def add(self, name: str, category_id: int, description: Optional[str]) -> None:
        self._repository.execute(
            "INSERT INTO tasks (name, category_id, description) VALUES (?, ?, ?);",
            (name, category_id, description),
        )
        self._repository.commit()

    def search_by_name(self, name: str) -> List[Task]:
        self._repository.execute(
            """
            SELECT t.id, t.created_at, t.name, t.description, c.id, c.created_at, c.name FROM tasks t 
            JOIN categories c
            WHERE INSTR(t.name, ?) > 0
            """,
            (name,),
        )
        return self._repository.fetchall_using_model(Task)

    def delete(self, id: int) -> None:
        self._repository.execute("DELETE FROM tasks WHERE id = ?;", (id,))
        self._repository.commit()
