from typing import List


def make_url(path: str, queries: List[str] = None):
    # クエリがあれば、クエリつきでURL作成
    if queries:
        return path + "?" + "&".join(queries)

    # クエリがない場合、パスのみ
    return path
