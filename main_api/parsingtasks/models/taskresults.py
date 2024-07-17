from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Column, JSON

from main_api.db.mixins import TimeStampMixin


class TaskResultsBase(SQLModel):
    body: dict = Field(default={}, sa_column=Column(JSON))
    meta: dict = Field(default={}, sa_column=Column(JSON))
    task_id: Optional[int] = Field(nullable=False, foreign_key='task.id')

class TaskResults(TimeStampMixin, TaskResultsBase, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates='results')

class TaskResultsRead(TaskResultsBase):
    id: int


class TaskResultsCreate(TaskResultsBase):
    pass


class TaskResultsUpdate(TaskResultsBase):
    pass