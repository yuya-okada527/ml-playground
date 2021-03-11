"""HTTPユーティリティモジュール

HTTP通信に関するユーティリティを記述するモジュール
"""
import json
import time
from functools import wraps
from typing import Any, Optional, Union

import requests
from core.logger import create_logger
from domain.exceptions.http_exception import ClientSideError, ServerSideError
from pydantic import BaseModel
from requests.exceptions import Timeout
from requests.models import Response

# リトライ待機時間ベース時間 (sec)
WAIT_TIME_BASE = 5
# タイムアウト時間 (sec)
TIMEOUT = 3
# MAXリトライ回数
MAX_RETRY_NUM = 3

# ヘッダー関連定数
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"

log = create_logger(__file__)


def retry_exec(max_retry_num: int, wait_time_base: int):
    """リトライ実行デコレータ

    Args:
        max_retry_num (int): 最大リトライ回数
    """
    def _retry_exec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, max_retry_num + 1):
                try:
                    return func(*args, **kwargs)
                except ServerSideError as e:
                    if i == max_retry_num:
                        log.exception("最大リトライ回数を超えました.")
                        raise e
                    log.warning(f"HTTP通信でリトライが発生しました. スリープ後、リトライ実行します.  リトライ回数={i}")
                    time.sleep(wait_time_base * (i + 1))
        return wrapper
    return _retry_exec


@retry_exec(max_retry_num=MAX_RETRY_NUM, wait_time_base=WAIT_TIME_BASE)
def call_get_api(
    url: str,
    query: Optional[BaseModel]
) -> Response:
    """GETメソッドでAPIを実行する.

    Args:
        url (str): URL
        query (Optional[BaseModel]): クエリ

    Raises:
        ServerSideError:
            - 500系のエラーが発生した場合に発生します.
            - タイムアウトした際に発生します.

    Returns:
        Response: レスポンス
    """

    query_dict = query.dict() if query is not None else {}

    # API実行
    try:
        response = requests.get(url, query_dict, timeout=TIMEOUT)
    except Timeout:
        log.warning(f"HTTP通信でタイムアウトが発生しました. url={url}")
        raise ServerSideError()

    # ステータスコードをチェック
    _check_status_code(response)

    return response


@retry_exec(max_retry_num=MAX_RETRY_NUM, wait_time_base=WAIT_TIME_BASE)
def call_post_api(
    url: str,
    data: Union[str, dict[str, Any], BaseModel] = "",
    headers: Optional[dict[str, str]] = None,
    timeout: int = TIMEOUT
) -> Response:
    """POSTメソッドでAPIを実行する.

    Args:
        url (str): URL
        data (Union[str, dict[str, Any], BaseModel], optional): POSTデータ. Defaults to "".
        headers (Optional[dict[str, str]], optional): HTTPヘッダー. Defaults to None.
        timeout (int): タイムアウト時間(sec). Defaults to 3.

    Raises:
        ServerSideError:
            - 500系のエラーが発生した場合に発生します.
            - タイムアウトした際に発生します.

    Returns:
        Response: レスポンス
    """

    # POSTデータを文字列に変換
    data_str = _data_to_string(data)
    assert type(data_str) == str

    # API実行
    try:
        response = requests.post(url=url, data=data_str, timeout=timeout, headers=headers)
    except Timeout:
        log.warning(f"HTTP通信でタイムアウトが発生しました. url={url}")
        raise ServerSideError()

    # ステータスコードをチェック
    _check_status_code(response)

    return response


def _data_to_string(data: Union[str, dict[str, Any], BaseModel]) -> str:
    """POSTデータを文字列に変換する.

    Args:
        data (Union[str, dict[str, Any], BaseModel]): POSTデータ

    Returns:
        str: POSTデータ文字列
    """
    if isinstance(data, str):
        return data
    elif isinstance(data, dict):
        return json.dumps(data)
    elif isinstance(data, BaseModel):
        return data.json()

    # TODO 例外
    return None


def _check_status_code(response: Response) -> None:
    """ステータスコードをチェックする.

    Args:
        response (Response): レスポンス

    Raises:
        ServerSideError: 5xx系のステータスコードの場合
        ClientSideError: 4xx系のステータスコードの場合
    """
    # ステータスコードをチェック
    if response.status_code >= 500:
        raise ServerSideError()
    elif response.status_code >= 400:
        log.error(f"クライアントサイドのエラーが発生しました. ステータスコード={response.status_code}, レスポンス={response.json()}")
        raise ClientSideError()
