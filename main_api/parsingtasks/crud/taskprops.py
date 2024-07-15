from main_api.async_crud_base import CRUDBase
from main_api.parsingtasks.models import TaskProps, TaskPropsRead, TaskPropsCreate
from main_api.parsingtasks.models.taskprops import TaskRead

class CRUDTask(CRUDBase[TaskProps, TaskPropsRead, TaskPropsCreate]):
    pass


taskprops_crud = CRUDTask(TaskProps)