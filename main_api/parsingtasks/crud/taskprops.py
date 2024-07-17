from main_api.async_crud_base import CRUDBase
from main_api.parsingtasks.models import TaskProps, TaskPropsRead, TaskPropsCreate

class CRUDTask(CRUDBase[TaskProps, TaskPropsRead, TaskPropsCreate]):
    pass


taskprops_crud = CRUDTask(TaskProps)