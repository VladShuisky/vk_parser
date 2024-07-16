from fastapi import APIRouter

from main_api.parsingtasks.routers import task
from main_api.service.routers.vk_parsers import vk_parsers_router

app_router = APIRouter()

app_router.include_router(task.router, prefix='/tasks', tags=['tasks'])

app_router.include_router(vk_parsers_router, prefix='/vk/parsers', tags=['vk_parsers'])
