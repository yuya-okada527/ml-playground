"""リソースユーティリティモジュール

リソースに関するユーティリティを記述するモジュール
"""
import os
from pathlib import Path

# リソースのパス
RESOURCES_PATH = os.path.join(
    Path(__file__).resolve().parents[2],
    "resources"
)


def get_resource(path: str, encoding: str = "utf8") -> str:
    """リソースを取得する

    Args:
        path (str): パス
        encoding (str, optional): 文字コード. Defaults to "utf8".

    Returns:
        str: リソース文字列
    """
    with open(os.path.join(RESOURCES_PATH, path), encoding=encoding) as f:
        return f.read()
