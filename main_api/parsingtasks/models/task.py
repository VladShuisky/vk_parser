from datetime import datetime
from typing import Optional
from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from main_api.db.mixins import TimeStampMixin


class TaskBase(SQLModel):
    unique_name: str = Field(max_length=255, unique=True)
    start_datetime: Optional[datetime] = Field(nullable=True)
    finish_datetime: Optional[datetime] = Field(nullable=True)


class Task(TimeStampMixin, TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    props: Optional["TaskProps"] = Relationship(back_populates='task')
    results: Optional["TaskResults"] = Relationship(back_populates='task')


class TaskRead(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass