from typing import List

from domain.enums.movie_enums import MovieField
from domain.models.solr.movies import MovieSolrModel, SolrResultModel
from entrypoints.v1.movie.messages.movie_messages import (MovieResponse,
                                                          SearchMovieResponse)
from infra.client.solr.solr_query import (SolrFilterQuery, SolrQuery,
                                          SolrSortQuery, SortDirection)

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
    MovieField.RELEASE_DATE,
    MovieField.RELEASE_YEAR,
    MovieField.GENRES,
    MovieField.GENRE_LABELS,
    MovieField.KEYWORDS,
    MovieField.KEYWORD_LABELS
]

DEFAULT_SORT = [
    SolrSortQuery(field=MovieField.POPULARITY, direction=SortDirection.DESC)
]

IMAGE_URL_BASE = "https://image.tmdb.org/t/p/w500"


def build_search_query(
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


def build_search_by_id_query(movie_id: int) -> SolrQuery:
    return SolrQuery(
        q=SolrFilterQuery.exact_condition(
            field=MovieField.MOVIE_ID,
            value=str(movie_id)
        ).get_query_string(),
        fl=DEFAULT_MOVIE_FLS,
        start=0,
        rows=1,
    )


def map_movie(movie: MovieSolrModel) -> MovieResponse:
    return MovieResponse(
        movie_id=movie.movie_id,
        original_title=movie.original_title,
        japanese_title=movie.japanese_title,
        overview=movie.overview,
        tagline=movie.tagline,
        poster_url=IMAGE_URL_BASE + movie.poster_path if movie.poster_path else None,
        backdrop_url=IMAGE_URL_BASE + movie.backdrop_path if movie.backdrop_path else None,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        release_date=movie.release_date,
        release_year=movie.release_year,
        genre_labels=movie.genre_labels,
        genres=movie.genres
    )


def map_movie_response(search_result: SolrResultModel) -> SearchMovieResponse:
    return SearchMovieResponse(
        start=search_result.response.start,
        returned_num=len(search_result.response.docs),
        available_num=search_result.response.numFound,
        results=[map_movie(movie) for movie in search_result.response.docs]
    )


def _build_free_word_query(q: List[str]) -> List[SolrFilterQuery]:
    if not q:
        return []

    return [SolrFilterQuery.exact_condition(
        field=MovieField.FREE_WORD,
        value=value)
        for value in q
    ]
