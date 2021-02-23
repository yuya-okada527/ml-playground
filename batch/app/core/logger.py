"""ロギングモジュール

アプリケーション内のログ設定を定義するモジュール
アプリケーションのログは必ずこのログを通してロギングする必要がある
"""
import logging

from domain.enums.core_enums import LogLevel

from core.config import CoreSettings

settings = CoreSettings()


def create_logger(log_name: str) -> logging.Logger:
    """ロガー作成関数

    ロガーを作成する

    Args:
        log_name: ロガー名
    """

    # ロガーの作成
    log = logging.getLogger(log_name)

    # ログレベルの設定
    if settings.batch_log_level == LogLevel.INFO:
        log.setLevel(logging.INFO)
    elif settings.batch_log_level == LogLevel.DEBUG:
        log.setLevel(logging.DEBUG)

    # 標準出力に出力
    handler = logging.StreamHandler()
    # LTSV形式で出力
    formatter = logging.Formatter("Level:%(levelname)s\tTime:%(asctime)s\tFile:%(pathname)s\tMessage:%(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
