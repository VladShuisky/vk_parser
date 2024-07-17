from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlmodel import Field, SQLModel
import sqlmodel

# from app.utils import tznow


class TimeStampMixin(SQLModel):

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