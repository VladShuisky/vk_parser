from main_api.async_crud_base import CRUDBase
from main_api.parsingsources.models import ParsingAccountApiCredentials, ParsingAccountApiCredentialsCreate, ParsingAccountApiCredentialsRead


class CRUDTask(CRUDBase[ParsingAccountApiCredentials, ParsingAccountApiCredentialsRead, ParsingAccountApiCredentialsCreate]):
    pass


parsingaccountcreds_crud = CRUDTask(ParsingAccountApiCredentials)