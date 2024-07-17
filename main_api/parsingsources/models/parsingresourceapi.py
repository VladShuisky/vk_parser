from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from main_api.db.mixins import TimeStampMixin


class ParsingResourceApiBase(SQLModel):
    name: str = Field(unique=True, nullable=False, max_length=255)
    base_url: str = Field(unique=True, nullable=False, max_length=255)


class ParsingResourceApi(TimeStampMixin, ParsingResourceApiBase, table=True):
    id: int = Field(primary_key=True, default=None)
    credentials: List["ParsingAccountApiCredentials"] = Relationship(back_populates='resource_api')


class ParsingResouceApiRead(ParsingResourceApiBase):
    id: int


class ParsingResourseApiCreate(ParsingResourceApiBase):
    pass


class ParsingResourceApiUpdate(ParsingResourceApiBase):
    pass
