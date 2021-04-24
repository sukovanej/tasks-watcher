from ..config import app_dir
from ..database.event_repository import EventRepository
from ..database.project_repository import ProjectRepository
from ..database.repository import Repository
from ..database.task_repository import TaskRepository

database_path = app_dir / "tasks_watcher.db"

repository = Repository(database_path)
project_repository = ProjectRepository(repository)
task_repository = TaskRepository(repository)
event_repository = EventRepository(repository)
