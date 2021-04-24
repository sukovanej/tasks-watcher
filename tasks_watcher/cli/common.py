from typing import List, Tuple

from .database import project_repository, task_repository


def complete_project_name(incomplete: str) -> List[str]:
    projects = project_repository.search_by_name(incomplete)
    project_names = [c.name for c in projects]
    return project_names


def complete_task_name(incomplete: str) -> List[Tuple[str, str]]:
    projects = task_repository.search_by_name(incomplete)
    project_names = [(c.name, c.project.name) for c in projects]
    return project_names
