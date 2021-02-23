import time
from enum import Enum
from functools import wraps
from typing import Any, Callable, Dict, TypeVar, cast

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
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            log.exception(f"{wrapper.__name__}の実行に失敗しました.")
            raise e
        end = time.time()
        log.info(f"{wrapper.__name__}の実行完了. パラメータ={_filter_params(kwargs)}.  経過時間={end - start:.3f} sec")
        return result
    return cast(ServiceFunction, wrapper)


def _filter_params(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    params = {}
    for key, value in kwargs.items():
        if _is_basic_type(value):
            params[key] = value

    return params


def _is_basic_type(value: Any) -> bool:
    for basic_type in BASIC_TYPES:
        if isinstance(value, basic_type):
            return True

    return False
