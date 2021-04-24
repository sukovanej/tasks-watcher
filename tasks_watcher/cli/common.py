from typing import List, Tuple

from .database import category_repository, task_repository


def complete_category_name(incomplete: str) -> List[str]:
    categories = category_repository.search_by_name(incomplete)
    category_names = [c.name for c in categories]
    return category_names


def complete_task_name(incomplete: str) -> List[Tuple[str, str]]:
    categories = task_repository.search_by_name(incomplete)
    category_names = [(c.name, c.category.name) for c in categories]
    return category_names
