from typing import Sequence

from ..models import Project
from .repository import Repository


class ProjectRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> Sequence[Project]:
        self._repository.execute("SELECT * FROM projects;")
        return self._repository.fetchall_using_model(Project)

    def add(self, name: str) -> None:
        self._repository.execute("INSERT INTO projects (name) VALUES (?);", (name,))
        self._repository.commit()

    def delete(self, id: int) -> None:
        self._repository.execute("DELETE FROM projects WHERE id = ?;", (id,))
        self._repository.commit()

    def search_by_name(self, name: str) -> Sequence[Project]:
        self._repository.execute(
            "SELECT * FROM projects WHERE INSTR(name, ?) > 0", (name,)
        )
        return self._repository.fetchall_using_model(Project)
