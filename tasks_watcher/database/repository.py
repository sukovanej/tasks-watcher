from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List, Optional, Type, TypeVar

import typer

from ..models import Event, Project, Task
from .migrations import MIGRATIONS

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
        self.cursor.execute("PRAGMA user_version;")
        current_version = self.cursor.fetchone()[0]
        typer.echo(f"Current migration: {current_version}")

        for migration in MIGRATIONS:
            if migration.version <= current_version:
                typer.echo(
                    f"[{migration.version}] up-to-date, skpping - {migration.description}"
                )
            else:
                typer.echo(f"[{migration.version}] applying - {migration.description}")
                self.cursor.executescript(migration.sql)
                self.cursor.execute("PRAGMA user_version = ?;", (migration.version,))

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
