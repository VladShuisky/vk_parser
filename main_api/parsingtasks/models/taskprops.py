from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Column, JSON

from main_api.db.mixins import TimeStampMixin


class TaskPropsBase(SQLModel):
    body: dict = Field(default={}, sa_column=Column(JSON))
    meta: dict = Field(default={}, sa_column=Column(JSON))
    task_id: Optional[int] = Field(default=None, foreign_key='task.id')


class TaskProps(TimeStampMixin, TaskPropsBase, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates='props')


class TaskPropsRead(TaskPropsBase):
    id: int


class TaskPropsUpdate(TaskPropsBase):
    pass


class TaskPropsCreate(TaskPropsBase):
    pass