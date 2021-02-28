"""コア区分値モジュール

ドメインに依存しない区分値を定義するモジュール
"""
from enum import Enum


class LogLevel(Enum):
    """ログレベルEnumクラス

    ログレベルを定義するenumクラス
    """
    INFO = "info"
    DEBUG = "debug"
