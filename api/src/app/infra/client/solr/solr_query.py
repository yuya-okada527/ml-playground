"""Solrクエリモジュール

Solrに対するクエリを記述するモジュール
"""
from enum import Enum
from typing import List, Optional

from domain.enums.movie_enums import MovieField
from pydantic import BaseModel

# 全検索クエリ
SEARCH_ALL = "*:*"


class SortDirection(Enum):
    """ソート方向Enum"""
    # 昇順
    ASC = "asc"
    # 降順
    DESC = "desc"


class QueryParserType(Enum):
    """クエリパーサのタイプ"""
    # Standardパーサ
    STANDARD = "lucene"
    # DisMaxパーサ
    DISMAX = "dismax"
    # Extended DisMaxパーサ
    EXTENDED_DISMAX = "edismax"


class SolrFilterQuery(BaseModel):
    """Solrのフィルタクエリ(fl)を表す"""
    field: MovieField
    condition: str

    @classmethod
    def exact_condition(cls, field: MovieField, value: str):
        """完全一致フィルタクエリを構築する

        Args:
            field (MovieField): Solrフィールド
            value (str): 検索値

        Returns:
            SolrFilterQuery: フィルタクエリ
        """
        assert field is not None

        if not value:
            return None

        return cls(field=field, condition=value)

    def get_query_string(self) -> Optional[str]:
        """クエリ文字列を取得する

        Returns:
            str: クエリ文字列
        """
        if self:
            return f"{self.field.value}:{self.condition}"

        return None

    def __bool__(self) -> bool:
        """真偽値判定

        Returns:
            bool: フィールドと条件の両方が揃っていればTrue, 揃っていなければFalse
        """
        # フィールドと条件の両方が揃っていればTrue
        if self.field and self.condition:
            return True

        return False


class SolrSortQuery(BaseModel):
    """Solrのソートクエリ(sort)を表す"""
    field: MovieField
    direction: SortDirection

    def get_query_string(self) -> str:
        """クエリ文字列を取得する

        Returns:
            str: クエリ文字列
        """
        return f"{self.field.value} {self.direction.value}"


class SolrQuery(BaseModel):
    """Solrクエリ"""
    q: str = SEARCH_ALL
    fq: List[SolrFilterQuery] = []
    fl: List[MovieField] = []
    start: int
    rows: int
    sort: List[SolrSortQuery] = []
    defType: Optional[QueryParserType] = None
    boost: Optional[str] = None

    def get_query_string(self) -> str:
        """クエリ文字列を取得する

        Returns:
            str: クエリ文字列
        """
        # クエリパラメータをリストで保持
        params = []

        # qパラメータを設定
        if self.q:
            params.append(f"q={self.q}")
        else:
            params.append(f"q={SEARCH_ALL}")
        # 必須要素をセット
        params.append(f"start={self.start}")
        params.append(f"rows={self.rows}")

        # 任意要素をセット
        if self.fq:
            params.extend([f"fq={fq.get_query_string()}" for fq in self.fq if fq])
        if self.fl:
            params.append(f"fl={','.join([fl.value for fl in self.fl if fl])}")
        if self.sort:
            params.append(f"sort={','.join([sort.get_query_string() for sort in self.sort if sort])}")
        if self.defType:
            params.append(f"defType={self.defType.value}")
        if self.defType == QueryParserType.EXTENDED_DISMAX and self.boost:
            params.append(f"boost={self.boost}")

        return "&".join(params)
