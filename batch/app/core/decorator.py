import time
from functools import wraps

from core.logging import create_logger


log = create_logger(__file__)


def service(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            log.exception(f"{wrapper.__name__}の実行に失敗しました.")
            raise e
        end = time.time()
        log.info(f"{wrapper.__name__}の実行完了. 経過時間={end - start:.3f} sec")
        return result
    return wrapper
