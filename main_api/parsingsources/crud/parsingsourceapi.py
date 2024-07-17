from main_api.async_crud_base import CRUDBase
from main_api.parsingsources.models import ParsingResourceApi, ParsingResouceApiRead, ParsingResourseApiCreate


class CRUDTask(CRUDBase[ParsingResourceApi, ParsingResourseApiCreate, ParsingResouceApiRead]):
    pass


parsingaccountcreds_crud = CRUDTask(ParsingResourceApi)