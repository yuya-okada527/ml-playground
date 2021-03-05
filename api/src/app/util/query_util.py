"""クエリユーティリティモジュール

HTTPクエリに関するユーティリティを提供するモジュール
"""
import re
from typing import Any, Callable, List, Optional

# クエリパラメータ分割パターン(半角・全角スペース・カンマ)
SPLIT_PATTERN = re.compile(r"[ 　,]")


def split_query_params(
    value: Optional[str],
    type_func: Callable[[str], Any] = str
) -> List[Any]:
    """クエリを分割する

    Args:
        value (Optional[str]): 値
        type_func (Callable[[str], Any], optional): 型変換関数. Defaults to str.

    Returns:
        List[Any]: 分割済リスト
    """

    # 空の値は空リストで返す
    if not value:
        return []

    # パラメータを分割
    return [type_func(v) for v in re.split(SPLIT_PATTERN, value)]
