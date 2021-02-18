import re
from typing import List, Any, Callable, Optional


# クエリパラメータ分割パターン(半角・全角スペース・カンマ)
SPLIT_PATTERN = re.compile(r"[ 　,]")


def split_query_params(
    value: Optional[str],
    func: Callable[[str], Any] = str
) -> List[Any]:

    # 空の値は空リストで返す
    if not value:
        return []

    # パラメータを分割
    return [func(v) for v in re.split(SPLIT_PATTERN, value)]
