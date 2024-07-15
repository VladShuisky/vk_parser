from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field, SQLModel

# from app.utils import tznow


class TimeStampMixin:
    __name__: str
    __config__ = {}

    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    # created_time: Optional[datetime] = Field(
    #     default_factory=datetime.utcnow,
    #     sa_column=sa.Column(
    #         sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    #     ),
    # )
    # updated_time: Optional[datetime] = Field(
    #     default_factory=datetime.utcnow,
    #     sa_column=sa.Column(
    #         sa.DateTime(timezone=True),
    #         onupdate=sa.func.now(),
    #         server_default=sa.func.now(),
    #         nullable=False,
    #     ),
    # )