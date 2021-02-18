from domain.exceptions.service_exception import BaseException


class ClientSideError(BaseException):
    pass


class ServerSideError(BaseException):
    pass
