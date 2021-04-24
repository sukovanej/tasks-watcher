from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    created_at: datetime
    name: str

    @classmethod
    def from_db(cls, row: tuple) -> Category:
        return cls(id=row[0], created_at=row[1], name=row[2])


class Task(BaseModel):
    id: int
    created_at: datetime
    name: str
    category: Category
    description: Optional[str] = None

    @classmethod
    def from_db(cls, row: tuple) -> Task:
        return cls(
            id=row[0],
            created_at=row[1],
            name=row[2],
            description=row[3],
            category=Category.from_db(row[4:]),
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
