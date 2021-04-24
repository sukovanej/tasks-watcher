from os.path import expanduser
from pathlib import Path

from ..database.event_repository import EventRepository
from ..database.project_repository import ProjectRepository
from ..database.repository import Repository
from ..database.task_repository import TaskRepository

database_path = Path(expanduser("~")) / "tasks_watcher.db"

repository = Repository(database_path)
project_repository = ProjectRepository(repository)
task_repository = TaskRepository(repository)
event_repository = EventRepository(repository)
