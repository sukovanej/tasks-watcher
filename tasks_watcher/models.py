from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    created_at: datetime
    name: str

    @classmethod
    def from_db(cls, row: tuple) -> Project:
        return cls(id=row[0], created_at=row[1], name=row[2])


class Task(BaseModel):
    id: int
    created_at: datetime
    name: str
    project: Project
    description: Optional[str] = None
    finished_at: Optional[datetime]

    @classmethod
    def from_db(cls, row: tuple) -> Task:
        return cls(
            id=row[0],
            created_at=row[1],
            name=row[2],
            description=row[3],
            finished_at=row[4],
            project=Project.from_db(row[5:]),
        )


class Event(BaseModel):
    id: int
    created_at: datetime
    started_at: datetime
    stopped_at: Optional[datetime] = None
    task: Task

    @classmethod
    def from_db(cls, row: tuple) -> Event:
        return cls(
            id=row[0],
            created_at=row[1],
            started_at=row[2],
            stopped_at=row[3],
            task=Task.from_db(row[4:]),
        )
