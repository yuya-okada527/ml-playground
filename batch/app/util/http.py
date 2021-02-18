import time
import json
from functools import wraps
from typing import Optional, Union

import requests
from requests.exceptions import Timeout
from pydantic import BaseModel

from domain.exceptions.http_exception import ServerSideError, ClientSideError


WAIT_TIME_BASE = 5
TIMEOUT = 3

# ヘッダー関連定数
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"


def retry_exec(max_retry_num: int):
    def _retry_exec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retry_num):
                try:
                    return func(*args, **kwargs)
                except ServerSideError:
                    # TODO ログ
                    time.sleep(WAIT_TIME_BASE * (i + 1))
        return wrapper
    return _retry_exec


@retry_exec(max_retry_num=3)
def call_get_api(url: str, query: Optional[BaseModel]):

    query = query.dict() if query is not None else {}

    # API実行
    try:
        response = requests.get(url, query, timeout=TIMEOUT)
    except Timeout:
        raise ServerSideError()

    # ステータスコードをチェック
    __check_status_code(response)

    return response


def call_post_api(url: str, data: Union[str, dict, BaseModel] = "", headers: dict[str, str] = None):

    # POSTデータを文字列に変換
    data_str = _to_string(data)
    assert type(data_str) == str

    # API実行
    try:
        response = requests.post(url=url, data=data_str, timeout=TIMEOUT, headers=headers)
    except Timeout:
        raise ServerSideError()

    # ステータスコードをチェック
    __check_status_code(response)

    return response


def _to_string(data: Union[str, dict, BaseModel]):
    if isinstance(data, str):
        return data
    elif isinstance(data, dict):
        return json.dumps(data)
    elif isinstance(data, BaseModel):
        return data.json()

    # TODO 例外
    return None


def __check_status_code(response) -> None:
    # ステータスコードをチェック
    if response.status_code >= 500:
        raise ServerSideError()
    elif response.status_code >= 400:
        # TODO schema更新エラー
        print(response.json())
        raise ClientSideError()
