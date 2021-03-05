from domain.enums.movie_enums import MovieLanguage
from domain.enums.similarity_enums import SimilarityModelType
from domain.models.internal.movie_model import Review
from domain.models.rest.tmdb_model import (TmdbMovie, TmdbMovieReview,
                                           TmdbMovieReviewList,
                                           TmdbReviewAuthorDetail,
                                           TmdbSimilarMovieList)


class FakeTmdbClient:

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


class FakeMoviewRepository:

    def save_similar_movie_list(
        self,
        movie_id: int,
        similar_movie_list: list[int]
    ) -> int:
        return len(similar_movie_list)

class FakeRedisRepository:

    def save_movie_similarity(
        self,
        movie_id: int,
        similar_movies: list[int],
        model_type: SimilarityModelType
    ) -> int:
        return len(similar_movies)
