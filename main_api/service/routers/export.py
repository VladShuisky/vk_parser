from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select

from main_api.db.db import get_db
from main_api.parsingtasks.models import Task
from main_api.parsingtasks.models.taskresults import TaskResults
from main_api.service.export.saver_for_promo import StringIOSaverForPromoCsv


export_router = APIRouter()

@export_router.get('/csv/for_promo')
async def export_csv_for_promo(
    task_name: str,
    tags_to_add: str,
    comment_to_add: str,
    db = Depends(get_db)
):
    """
    create a special csv file with clients with columns: 
    vk_id, vk_profile_url, tags, comment, json_data_dict 
    """
    stmt = select(Task).where(Task.unique_name == task_name)
    res = await db.execute(stmt)
    task: Optional[Task] = res.scalars().first()
    if not task:
        raise HTTPException(404, 'no task with this unique name!')
    
    results_stmt = select(TaskResults).where(TaskResults.task == task)
    res = await db.execute(results_stmt)
    results = res.scalars().first()
    
    # results: Optional[TaskResults] = task.results
    if not results:
        raise HTTPException(404, 'no task result for this... probably this task is process now')
    
    data: dict = results.body.get('result')
    if not data:
        raise HTTPException(404, 'no one user item in task results, nothing to export!')

    to_return = StringIOSaverForPromoCsv().save_to_csv(
        items_to_save=data,
        tags=tags_to_add,
        comment=comment_to_add,
        separator=','
    )

    response = Response(content=to_return)
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
