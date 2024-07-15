from typing import Dict, Optional
from sqlmodel import Field, Relationship, SQLModel, Column, JSON

from main_api.db.mixins import TimeStampMixin


class ParsingAccountApiCredentialsBase(SQLModel):
    access_token: str = Field(nullable=False, unique=True)
    account_name: Optional[str] = Field(nullable=True)
    account_last_name: Optional[str] = Field(nullable=True)
    resource_api_id: Optional[int] = Field(default=None, foreign_key='parsingresourceapi.id')
    meta: dict = Field(default={}, sa_column=Column(JSON))
    active: bool = Field(default=True)
    engaged: bool = Field(default=False)


class ParsingAccountApiCredentials(TimeStampMixin, ParsingAccountApiCredentialsBase, table=True):
    id: int = Field(primary_key=True, default=None)
    resource_api: Optional["ParsingResourceApi"] = Relationship(back_populates='credentials')


class ParsingAccountApiCredentialsRead(ParsingAccountApiCredentialsBase):
    id: int


class ParsingAccountApiCredentialsUpdate(ParsingAccountApiCredentialsBase):
    pass


class ParsingAccountApiCredentialsCreate(ParsingAccountApiCredentialsBase):
    pass
