"""類似性Enumモジュール

類似性ドメインに関する区分値を定義するモジュール
"""
from enum import Enum


class SimilarityModelType(Enum):
    """類似性判定モデルタイプ"""
    # TMDB APIを利用して、類似性を判定するモデル
    TMDB_SIM = "tmdb-sim"
    # Gloveのベクトル表現を利用して、類似性を判定するモデル
    GLOVE_SIM = "glove-sim"
