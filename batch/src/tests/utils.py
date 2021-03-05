from typing import Optional

from domain.enums.movie_enums import MovieLanguage
from domain.enums.similarity_enums import SimilarityModelType
from domain.models.internal.movie_model import Genre, Movie, Review
from domain.models.rest.tmdb_model import (TmdbMovie, TmdbMovieDetail,
                                           TmdbMovieGenre, TmdbMovieGenreList,
                                           TmdbMovieReview,
                                           TmdbMovieReviewList,
                                           TmdbPopularMovieList,
                                           TmdbReviewAuthorDetail,
                                           TmdbSimilarMovieList)
from domain.models.solr.solr_movie_model import MovieSolrModel
from domain.models.solr.solr_schema_model import (SolrResponseHeader,
                                                  SolrSchemaModel,
                                                  SolrSchemaResponseModel)


class FakeTmdbClient:

    def fetch_genres(self, language: MovieLanguage) -> TmdbMovieGenreList:
        if language == MovieLanguage.EN:
            return TmdbMovieGenreList(
                genres=[
                    TmdbMovieGenre(id=0, name="name")
                ]
            )
        elif language == MovieLanguage.JP:
            return TmdbMovieGenreList(
                genres=[
                    TmdbMovieGenre(id=0, name="japanese_name")
                ]
            )

    def fetch_popular_movies(
        self,
        page: int,
        region: Optional[str] = None,
        language: Optional[MovieLanguage] = None
    ) -> TmdbPopularMovieList:
        return TmdbPopularMovieList(
            pages=1,
            results=[
                TmdbMovie(
                        adult=True,
                        overview="overview",
                        id=0,
                        original_title="original_title",
                        original_language="ja",
                        title="title",
                        popularity=0.1,
                        vote_count=0,
                        video=True,
                        vote_average=0.1
                    )
            ],
            total_results=1,
            total_pages=1
        )

    def fetch_movie_detail_list(
        self,
        movie_id_list: list[int],
        language: Optional[MovieLanguage] = None,
        append_to_response: Optional[str] = None
    ) -> list[TmdbMovieDetail]:
        return [TmdbMovieDetail(
            adult=True,
            budget=0,
            id=0,
            original_language="original_language",
            original_title="original_title",
            popularity=0,
            release_date="2020-01-01",
            revenue=0,
            status="status",
            title="title",
            video=True,
            vote_average=0,
            vote_count=0
        )]

    def fetch_movie_reviews(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbMovieReviewList:
        data = {
            0: TmdbMovieReviewList(
                id=0,
                page=page,
                results=[
                    TmdbMovieReview(
                        author="author",
                        author_details=TmdbReviewAuthorDetail(name="name", username="username"),
                        content="content",
                        created_at="2020-01-01",
                        id="review1",
                        updated_at="2020-01-01",
                        url="url"
                    ),
                    TmdbMovieReview(
                        author="author",
                        author_details=TmdbReviewAuthorDetail(name="name", username="username"),
                        content="content",
                        created_at="2020-01-01",
                        id="review2",
                        updated_at="2020-01-01",
                        url="url"
                    )
                ],
                total_pages=1,
                total_results=2
            )
        }

        return data.get(movie_id)

    def fetch_similar_movie_list(
        self,
        movie_id: int,
        language: MovieLanguage = MovieLanguage.EN,
        page: int = 1
    ) -> TmdbSimilarMovieList:
        data = {
            "0_1": TmdbSimilarMovieList(
                page=1,
                results=[
                    TmdbMovie(
                        adult=True,
                        overview="overview",
                        id=2,
                        original_title="original_title",
                        original_language="ja",
                        title="title",
                        popularity=0.1,
                        vote_count=0,
                        video=True,
                        vote_average=0.1
                    )
                ],
                total_pages=2,
                total_results=2
            ),
            "0_2": TmdbSimilarMovieList(
                page=1,
                results=[
                    TmdbMovie(
                        adult=True,
                        overview="overview",
                        id=3,
                        original_title="original_title",
                        original_language="ja",
                        title="title",
                        popularity=0.1,
                        vote_count=0,
                        video=True,
                        vote_average=0.1
                    )
                ],
                total_pages=2,
                total_results=2
            )
        }

        return data.get(f"{movie_id}_{page}",
            TmdbSimilarMovieList(
                page=1,
                results=[],
                total_pages=1,
                total_results=0
            )
        )


class FakeReviewRepositry:

    def save_review_list(self, review_list: list[Review]) -> int:
        return len(review_list)

    def fetch_all_review_id(self) -> list[str]:
        return ["review1"]


class FakeMoviewRepository:

    def save_similar_movie_list(
        self,
        movie_id: int,
        similar_movie_list: list[int]
    ) -> int:
        return len(similar_movie_list)

    def fetch_all_movie_id(self) -> list[int]:
        return [0]

    def save_movie_list(self, movie_list: list[Movie]) -> None:
        return

    def fetch_all_similar_movie(self) -> dict[int, list[int]]:
        return {
            0: [2, 3]
        }

    def fetch_all(self) -> list[Movie]:
        return [
            Movie(
                movie_id=0
            )
        ]


class FakeGenreRepository:

    def fetch_all(self) -> list[Genre]:
        return [Genre(genre_id=0, name="name", japanese_name="japanese_name")]

    def save(self, genre_list: list[Genre]) -> int:
        return len(genre_list)


class FakeRedisRepository:

    def save_movie_similarity(
        self,
        movie_id: int,
        similar_movies: list[int],
        model_type: SimilarityModelType
    ) -> int:
        return len(similar_movies)


class FakeSolrClient:

    def update_schema(self, schema_data: str) -> None:
        return

    def get_schema(self) -> SolrSchemaResponseModel:
        return SolrSchemaResponseModel(
            responseHeader=SolrResponseHeader(status=0, QTime=0),
            schema=SolrSchemaModel(
                name="name",
                version=0,
                uniqueKey="uniqueKey"
            )
        )

    def index_movies(self, movies: list[MovieSolrModel]) -> None:
        return

    def delete_old(self, exec_time: int) -> None:
        return

    def commit(self) -> None:
        return
