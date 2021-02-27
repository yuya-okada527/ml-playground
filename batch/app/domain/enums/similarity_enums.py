"""類似性モジュール

類似性モジュール
"""
from enum import Enum


class SimilarityModelType(Enum):
    """類似性モデルタイプ

    類似性モデル区分値
    """
    TMDB_SIM = "tmdb-sim"
    GLOVE_SIM = "glove-sim"
