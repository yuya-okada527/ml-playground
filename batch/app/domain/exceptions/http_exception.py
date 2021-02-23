"""HTTP例外モジュール

HTTPプロトコルに関する例外を記述するモジュール
"""
from domain.exceptions.service_exception import BaseAppException


class ClientSideError(BaseAppException):
    """クライアントサイドエラー例外

    外部APIをコールした際、クライアントサイドの問題が発生した場合に投げる例外
    """
    pass


class ServerSideError(BaseAppException):
    """サーバサイドエラー例外

    外部APIをコールした際、サーバサイドの問題が発生した場合に投げる例外
    """
    pass
