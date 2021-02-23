from domain.exceptions.service_exception import BaseAppException


class ClientSideError(BaseAppException):
    pass


class ServerSideError(BaseAppException):
    pass
