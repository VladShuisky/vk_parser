from typing import List
from pydantic import BaseModel


class ParseVkGroupsData(BaseModel):
    parsing_task_name: str
    groups_screennames: List[str]
    fields: List[str]