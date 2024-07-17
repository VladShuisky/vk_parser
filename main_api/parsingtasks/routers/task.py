# from fastapi_crudrouter import SQLAlchemyCRUDRouter
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from main_api.db.db import get_db
from main_api.parsingtasks.models import Task, TaskCreate, TaskPropsUpdate
from main_api.parsingtasks.models.task import TaskBase, TaskRead, TaskUpdate
from main_api.parsingtasks.crud import task_crud


# router = SQLAlchemyCRUDRouter(
#     db=get_db,
#     delete_all_route=False,
#     db_model=Task,
#     schema=TaskBase,
#     create_schema=TaskCreate,
#     update_schema=TaskPropsUpdate
# ) # sqlalchemycrudrouter не поддерживает асинхронную работу

router = APIRouter()

@router.get('/', response_model=List[TaskRead])
async def get_tasks(
    db = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    return await task_crud.get_multi(db, skip=skip, limit=limit)

@router.get('/{task_id}', response_model=TaskRead)
async def get_task_by_id(
    task_id: int,
    db = Depends(get_db),
):
    return await task_crud.get_or_raise_404(db, id=task_id)

@router.post('/{task_id}', response_model=TaskRead)
async def create_task(
    data: TaskCreate,
    db = Depends(get_db),
):
    return await task_crud.create(db, obj_in=data)

@router.put('/', response_model=TaskRead)
async def update_task(
    data: TaskUpdate,
    id: int,
    db = Depends(get_db),
):
    task = await task_crud.get(db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Item not found")
    task = await task_crud.update(db=db, db_obj=task, obj_in=data)  #TODO ПРОВЕРИТЬ ПОЗЖЕ