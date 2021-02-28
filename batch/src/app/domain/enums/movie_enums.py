"""映画区分値モジュール

映画ドメインに関するモジュール
"""
from enum import Enum


class MovieLanguage(Enum):
    """言語enum

    言語enum
    """
    JP = "ja"
    EN = "en-US"
