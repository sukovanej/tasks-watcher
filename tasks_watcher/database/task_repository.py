from typing import Optional, Sequence

from ..models import Task
from .repository import Repository


BASE_QUERY = """
    SELECT t.id, t.created_at, t.name, t.description, c.id, c.created_at, c.name
    FROM tasks t
    JOIN projects c ON c.id = t.project_id
"""


class TaskRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> Sequence[Task]:
        self._repository.execute("{BASE_QUERY};")
        return self._repository.fetchall_using_model(Task)

    def add(self, name: str, project_id: int, description: Optional[str]) -> None:
        self._repository.execute(
            "INSERT INTO tasks (name, project_id, description) VALUES (?, ?, ?);",
            (name, project_id, description),
        )
        self._repository.commit()

    def search_by_name(self, name: str) -> Sequence[Task]:
        self._repository.execute(
            f"""
            {BASE_QUERY}
            WHERE INSTR(t.name, ?) > 0
            """,
            (name,),
        )
        return self._repository.fetchall_using_model(Task)

    def delete(self, task_id: int) -> None:
        self._repository.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        self._repository.commit()

    def update(
        self,
        task_id: int,
        new_name: Optional[str],
        new_project_id: Optional[int],
        new_description: Optional[str],
    ) -> None:
        update_name_query, update_project_query, update_description_query = [None] * 3

        if new_name is not None:
            update_name_query = "name = ?"
        elif new_project_id is not None:
            update_project_query = "project_id = ?"
        elif new_description is not None:
            update_description_query = "description = ?"

        all_queries = [
            update_name_query,
            update_project_query,
            update_description_query,
        ]

        if not any(all_queries):
            raise Exception("Nothing's gonna be updated")

        all_values = [new_name, new_project_id, new_description, task_id]

        update_queries = ", ".join([q for q in all_queries if q is not None])
        values = [v for v in all_values if v is not None]

        self._repository.execute(
            f"UPDATE tasks SET {update_queries} WHERE id = ?;", tuple(values)
        )
        self._repository.commit()
