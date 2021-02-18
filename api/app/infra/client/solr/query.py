from enum import Enum
from typing import List

from pydantic import BaseModel

from domain.enums.movies import MovieField


SEARCH_ALL = "*:*"


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


class SolrFilterQuery(BaseModel):
    field: MovieField
    condition: str

    @classmethod
    def exact_condition(cls, field: MovieField, value: str):
        assert field is not None

        if not value:
            return None

        return cls(field=field, condition=value)

    def get_query_string(self) -> str:
        return f"{self.field.value}:{self.condition}"


class SolrSortQuery(BaseModel):
    field: MovieField
    direction: SortDirection

    def get_query_string(self) -> str:
        return f"{self.field.value} {self.direction.value}"


class SolrQuery(BaseModel):
    q: str = SEARCH_ALL
    fq: List[SolrFilterQuery] = []
    fl: List[MovieField] = []
    start: int
    rows: int
    sort: List[SolrSortQuery] = []

    def get_query_string(self) -> str:
        # クエリパラメータをリストで保持
        params = []

        # 必須要素をセット
        params.append(f"q={self.q}")
        params.append(f"start={self.start}")
        params.append(f"rows={self.rows}")

        # 任意要素をセット
        if self.fq:
            params.extend([f"fq={fq.get_query_string()}" for fq in self.fq])
        if self.fl:
            params.append(f"fl={','.join([fl.value for fl in self.fl])}")
        if self.sort:
            params.append(f"sort={','.join([sort.get_query_string() for sort in self.sort])}")

        return "&".join(params)
