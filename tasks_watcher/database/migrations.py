from dataclasses import dataclass


@dataclass
class DatabaseMigration:
    description: str
    version: int
    sql: str


MIGRATIONS = [
    DatabaseMigration(
        description="initial migration",
        version=1,
        sql="""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                name TEXT NOT NULL,
                project_id INTEGER NOT NULL,
                description TEXT,

                FOREIGN KEY(project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                started_at TIMESTAMP NOT NULL,
                stopped_at TIMESTAMP DEFAULT NULL,
                task_id INTEGER,
                name TEXT DEFAULT NULL,

                FOREIGN KEY(task_id) REFERENCES tasks(id)
            );
        """,
    ),
    DatabaseMigration(
        description="add finished_at column to tasks",
        version=2,
        sql="ALTER TABLE tasks ADD COLUMN finished_at TIMESTAMP DEFAULT NULL;",
    ),
]
