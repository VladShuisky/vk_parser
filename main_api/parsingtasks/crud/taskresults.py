from main_api.async_crud_base import CRUDBase
from main_api.parsingtasks.models import TaskResults, TaskResultsCreate, TaskResultsUpdate

class CRUDTask(CRUDBase[TaskResults, TaskResultsCreate, TaskResultsUpdate]):
    pass


taskresults_crud = CRUDTask(TaskResults)