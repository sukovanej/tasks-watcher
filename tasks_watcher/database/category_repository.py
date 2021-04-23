from typing import List

from ..models import Category
from .repository import Repository


class CategoryRepository:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    def list_all(self) -> List[Category]:
        self._repository.execute("SELECT * FROM categories;")
        return self._repository.fetchall_using_model(Category)

    def add(self, name: str) -> None:
        self._repository.execute("INSERT INTO categories (name) VALUES (?);", (name,))
        self._repository.commit()

    def delete(self, id: int) -> None:
        self._repository.execute("DELETE FROM categories WHERE id = ?;", (id,))
        self._repository.commit()

    def search_by_name(self, name: str) -> List[Category]:
        self._repository.execute(
            "SELECT * FROM categories WHERE INSTR(name, ?) > 0", (name,)
        )
        return self._repository.fetchall_using_model(Category)
