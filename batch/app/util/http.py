import time
from functools import wraps
from typing import Union

import requests
from requests.exceptions import Timeout
from pydantic import BaseModel

from domain.exceptions.http_exception import ServerSideError, ClientSideError


WAIT_TIME_BASE = 5
TIMEOUT = 2


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
    __check_status_code(response.status_code)

    return response


def call_post_api(url: str, data: Union[str, BaseModel]):

    # POSTデータを文字列に変換
    data_str = data.json() if isinstance(data, BaseModel) else data
    assert type(data_str) == str

    # API実行
    try:
        response = requests.post(url=url, data=data, timeout=TIMEOUT)
    except Timeout:
        raise ServerSideError()
    
    # ステータスコードをチェック
    __check_status_code(response)

    return response


def __check_status_code(response) -> None:
    # ステータスコードをチェック
    if response.status_code >= 500:
        raise ServerSideError()
    elif response.status_code >= 400:
        print(response.json())
        raise ClientSideError()
    