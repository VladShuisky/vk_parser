from fastapi import APIRouter

from main_api.parsingtasks.routers import task

app_router = APIRouter()

app_router.include_router(task.router, prefix='/tasks', tags=['tasks'])
