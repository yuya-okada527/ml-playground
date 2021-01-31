import time
from functools import wraps

import requests
from requests.exceptions import Timeout
from pydantic import BaseModel

from domain.exceptions.http_exception import ServerSideError, ClientSideError


WAIT_TIME_BASE = 10
TIMEOUT = 1


def retry_exec(max_retry_num: int):
    def _retry_exec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retry_num):
                try:
                    return func(*args, **kwargs)
                except ServerSideError as e:
                    # TODO ログ
                    time.sleep(WAIT_TIME_BASE * (i + 1))
        return wrapper
    return _retry_exec


@retry_exec(max_retry_num=3)
def call_get_api(url: str, query: BaseModel):
    # API実行
    try:
        response = requests.get(url, query.dict(), timeout=TIMEOUT)
    except Timeout:
        raise ServerSideError()

    # ステータスコードをチェック
    if response.status_code >= 500:
        raise ServerSideError()
    elif response.status_code >= 400:
        raise ClientSideError()

    return response






