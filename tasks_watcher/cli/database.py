from os.path import expanduser
from pathlib import Path

from ..database.category_repository import CategoryRepository
from ..database.event_repository import EventRepository
from ..database.repository import Repository
from ..database.task_repository import TaskRepository

database_path = Path(expanduser("~")) / "tasks_watcher.db"

repository = Repository(database_path)
category_repository = CategoryRepository(repository)
task_repository = TaskRepository(repository)
event_repository = EventRepository(repository)
