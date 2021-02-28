"""AOPモジュール

AOP(Aspect Oriented Programming)を実現するためのデコレータを定義するモジュール
"""
import time
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

from domain.exceptions.service_exception import BaseAppException

from core.logger import create_logger

log = create_logger(__file__)

# パラメータに渡すことのできる基本的な型の一覧
BASIC_TYPES = [
    str,
    int,
    float,
    bool,
    Enum,
    list,
    set,
    dict
]

# 任意のシグネチャに対するデコレータ用の型定義を用意
ServiceFunction = TypeVar("ServiceFunction", bound=Callable[..., Any])


def batch_service(func: ServiceFunction) -> ServiceFunction:
    """バッチサービスアドバイス

    バッチのサービス関数に対するアドバイス
    以下の機能を提供する
    - ロギング
    - 例外処理
    - パフォーマンスログ出力

    Notes:
        このデコレータを使用する関数では、位置引数を利用せず、キーワード引数を使ってください
    """
    @wraps(func)
    def wrapper(**kwargs) -> Any:
        log.info(f"{wrapper.__name__}の実行開始.  パラメータ={_filter_params(kwargs)}.")
        start = time.time()
        try:
            result = func(**kwargs)
        except BaseAppException as e:
            log.exception(f"{wrapper.__name__}の実行に失敗しました.")
            raise e
        except Exception as e:
            log.exception(f"予期せぬ例外で、{wrapper.__name__}の実行に失敗しました.")
            raise e
        end = time.time()
        log.info(f"{wrapper.__name__}の実行完了.  経過時間={end - start:.3f} sec")
        return result
    return cast(ServiceFunction, wrapper)


def _filter_params(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """パラメータ抽出関数

    サービス関数に対する引数から、バッチ引数を抽出する

    Args:
        kwargs: キーワード引数

    Returns:
        バッチ引数として認められた型のみを含むDictを返す
    """
    params = {}
    for key, value in kwargs.items():
        if _is_batch_args(value):
            params[key] = value

    return params


def _is_batch_args(value: Any) -> bool:
    """バッチ引数判定関数

    バッチ引数かどうか判定する

    Args:
        value: 関数の引数の値

    Returns:
        バッチ引数として妥当な場合True, 妥当でない場合False
    """
    for basic_type in BASIC_TYPES:
        if isinstance(value, basic_type):
            return True

    return False
