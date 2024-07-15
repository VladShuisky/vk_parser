from main_api.async_crud_base import CRUDBase
from main_api.parsingtasks.models import Task, TaskCreate
from main_api.parsingtasks.models.task import TaskRead


class CRUDTask(CRUDBase[Task, TaskRead, TaskCreate]):
    pass


task_crud = CRUDTask(Task)