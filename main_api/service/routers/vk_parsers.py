from fastapi import APIRouter, BackgroundTasks, Depends

from main_api.db.db import get_db
from main_api.service.pydantic_serializers import ParseVkGroupsData
from main_api.service.vk_parsing.get_groups_users import get_groups_users

vk_parsers_router = APIRouter()

@vk_parsers_router.post('/get_users_from_groups')
async def get_users_from_groups(
    background_tasks: BackgroundTasks,
    data: ParseVkGroupsData,
    db = Depends(get_db),
):
    # background_tasks.add_task(
    #     get_groups_users,
    #     db,
    #     data.parsing_task_name,
    #     data.groups_screennames,
    #     data.fields
    # )

    await get_groups_users(
        db,
        data.parsing_task_name,
        data.groups_screennames,
        data.fields
    )