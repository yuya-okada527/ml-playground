from typing import List

from domain.models.solr.movies import SolrResultModel
from entrypoints.v1.movie.messages.search_messages import MovieResponse, SearchMovieResponse
from domain.enums.movies import MovieField
from infra.client.solr.api import AbstractSolrClient
from infra.client.solr.query import SolrFilterQuery, SolrQuery, SolrSortQuery, SortDirection


DEFAULT_MOVIE_FLS = [
    MovieField.MOVIE_ID,
    MovieField.ORIGINAL_TITLE,
    MovieField.JAPANESE_TITLE,
    MovieField.OVERVIEW,
    MovieField.TAGLINE,
    MovieField.POSTER_PATH,
    MovieField.BACKDROP_PATH,
    MovieField.POPULARITY,
    MovieField.VOTE_AVERAGE,
    MovieField.GENRES,
    MovieField.GENRE_LABELS,
    MovieField.KEYWORDS,
    MovieField.KEYWORD_LABELS
]

DEFAULT_SORT = [
    SolrSortQuery(field=MovieField.POPULARITY, direction=SortDirection.DESC)
]

def exec_search_service(
    q: List[str],
    start: int,
    rows: int,
    solr_client: AbstractSolrClient
) -> SearchMovieResponse:
    
    # クエリの構築
    solr_query = _build_query(q=q, start=start, rows=rows)

    # 検索実行
    search_result = solr_client.search_movies(solr_query)

    return _map_response(search_result)


def _build_query(
    q: List[str],
    start: int,
    rows: int
) -> SolrQuery:
    return SolrQuery(
        fq=_build_free_word_query(q),
        fl=DEFAULT_MOVIE_FLS,
        start=start,
        rows=rows,
        sort=DEFAULT_SORT
    )


def _build_free_word_query(q: List[str]) -> List[SolrFilterQuery]:
    if not q:
        return []

    return [SolrFilterQuery.exact_condition(
        field=MovieField.FREE_WORD, 
        value=value
        ) for value in q
    ]


def _map_response(search_result: SolrResultModel) -> SearchMovieResponse:
    return SearchMovieResponse(
        start=search_result.response.start,
        returned_num=len(search_result.response.docs),
        available_num=search_result.response.numFound,
        results=[MovieResponse(**movie.dict()) for movie in search_result.response.docs]
    )
