from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie_model import Genre, Review
from domain.models.rest.tmdb_model import (TmdbMovie, TmdbMovieGenre,
                                           TmdbMovieReview,
                                           TmdbMovieReviewList,
                                           TmdbReviewAuthorDetail,
                                           TmdbSimilarMovieList)
from service.logic.input_logic import (map_genre_list, update_review_data,
                                       update_similar_movies_data)


def test_map_genre_list_registered_id_is_not_target():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=0, name="名前")]
    force_update = False

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = []

    assert actual == expected


def test_map_genre_list_registered_id_is_target_if_force_update():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=0, name="名前")]
    force_update = True

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = [Genre(genre_id=0, name="name", japanese_name="名前")]

    assert actual == expected


def test_map_genre_list_mismatched_genre_is_not_target():

    # テストデータ
    registered_genre_id_set = {0, 1}
    english_genres = [TmdbMovieGenre(id=0, name="name")]
    japanese_genres = [TmdbMovieGenre(id=1, name="名前")]
    force_update = False

    # 検証
    actual = map_genre_list(
        registered_genre_id_set,
        english_genres,
        japanese_genres,
        force_update
    )
    expected = []

    assert actual == expected


def test_update_review_data():

    # テストデータ
    registered_movie_ids = [0]
    registered_review_ids = []
    tmdb_client = FakeTmdbClient()
    review_repository = FakeReviewRepositry()

    # 検証
    actual = update_review_data(
        registered_movie_ids=registered_movie_ids,
        registered_review_ids=registered_review_ids,
        tmdb_client=tmdb_client,
        review_repository=review_repository
    )

    assert actual == 2


def test_update_review_data_registered_review_id_is_not_target():

    # テストデータ
    registered_movie_ids = [0]
    registered_review_ids = ["review1"]
    tmdb_client = FakeTmdbClient()
    review_repository = FakeReviewRepositry()

    # 検証
    actual = update_review_data(
        registered_movie_ids=registered_movie_ids,
        registered_review_ids=registered_review_ids,
        tmdb_client=tmdb_client,
        review_repository=review_repository
    )

    assert actual == 1


def test_update_similar_movies_data():

    # テストデータ
    registered_movies_id_set = {0, 2, 3}
    registered_similar_movie_map = {}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 2


def test_update_similar_movies_data_registered_movie_is_not_target():

    # テストデータ
    registered_movies_id_set = {0, 2, 3}
    registered_similar_movie_map = {0: []}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 0


def test_update_similar_movies_data_registered_movie_is_not_target_similar_movie():

    # テストデータ
    registered_movies_id_set = {0, 3}
    registered_similar_movie_map = {}
    tmdb_client = FakeTmdbClient()
    movie_repository = FakeMoviewRepository()

    # 検証
    actual = update_similar_movies_data(
        registered_movies_id_set=registered_movies_id_set,
        registered_similar_movie_map=registered_similar_movie_map,
        tmdb_client=tmdb_client,
        movie_repository=movie_repository
    )

    assert actual == 1


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
