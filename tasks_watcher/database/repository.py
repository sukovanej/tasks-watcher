from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List, Optional, Type, TypeVar

from ..models import Event, Project, Task

T = TypeVar("T", Project, Task, Event)


class Repository:
    def __init__(self, filename: Path) -> None:
        self.__filename = filename
        self.__connection: Optional[sqlite3.Connection] = None
        self.__cursor: Optional[sqlite3.Cursor] = None

    @property
    def _connection(self) -> sqlite3.Connection:
        if self.__connection is None:
            self.__connection = sqlite3.connect(str(self.__filename))
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        if self.__cursor is None:
            raise Exception("cursor not started")
        return self.__cursor

    def connect(self) -> None:
        self.__cursor = self._connection.cursor()

    def initialize(self) -> None:
        self.connect()
        self.cursor.executescript(
            """
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
            """
        )

    def fetchall_using_model(self, model: Type[T]) -> List[T]:
        rows = self.cursor.fetchall()
        return [model.from_db(v) for v in rows]

    def fetch_using_model(self, model: Type[T]) -> Optional[T]:
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return None
        elif len(rows) != 1:
            raise Exception("Returned more then 1 row")

        return model.from_db(rows[0])

    def commit(self) -> None:
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def execute(self, sql: str, parameters: Iterable = tuple()) -> None:
        self.cursor.execute(sql, parameters)

    def fetchall(self) -> list:
        return self.cursor.fetchall()
