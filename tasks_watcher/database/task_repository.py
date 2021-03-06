from datetime import datetime
from typing import Optional, Sequence

from ..models import Task
from .project_repository import ALL_PROJECT_COLUMNS
from .repository import Repository

ALL_TASK_COLUMNS = "t.id, t.created_at, t.name, t.description, t.finished_at"

BASE_QUERY = f"""
    SELECT {ALL_TASK_COLUMNS}, {ALL_PROJECT_COLUMNS}
    FROM tasks t
    JOIN projects p ON p.id = t.project_id
"""


class TaskRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self, project: Optional[str] = None) -> Sequence[Task]:
        where_query = ""
        if project is not None:
            where_query = "WHERE p.name = ?"

        all_parameters = [project]
        parameters = tuple(p for p in all_parameters if p is not None)

        self._repository.execute(f"{BASE_QUERY} {where_query};", parameters)
        return self._repository.fetchall_using_model(Task)

    def list_all_unfinished(self, project: Optional[str] = None) -> Sequence[Task]:
        where_query = ""
        if project is not None:
            where_query = "AND p.name = ?"

        all_parameters = [project]
        parameters = tuple(p for p in all_parameters if p is not None)

        self._repository.execute(
            f"{BASE_QUERY} WHERE t.finished_at is NULL {where_query};", parameters
        )
        return self._repository.fetchall_using_model(Task)

    def add(self, name: str, project_id: int, description: Optional[str]) -> None:
        self._repository.execute(
            "INSERT INTO tasks (name, project_id, description) VALUES (?, ?, ?);",
            (name, project_id, description),
        )
        self._repository.commit()

    def search_by_name(self, name: str) -> Sequence[Task]:
        self._repository.execute(f"{BASE_QUERY} WHERE INSTR(t.name, ?) > 0;", (name,))
        return self._repository.fetchall_using_model(Task)

    def search_by_name_unfinished(self, name: str) -> Sequence[Task]:
        self._repository.execute(
            f"{BASE_QUERY} WHERE INSTR(t.name, ?) > 0 AND t.finished_at is NULL;",
            (name,),
        )
        return self._repository.fetchall_using_model(Task)

    def delete(self, task_id: int) -> None:
        self._repository.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        self._repository.commit()

    def finish(self, task_id: int) -> None:
        self._repository.execute(
            "UPDATE tasks SET finished_at = ? WHERE id = ?;",
            (datetime.now(), task_id),
        )
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
