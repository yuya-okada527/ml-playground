from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie_model import Genre, Review
from domain.models.rest.tmdb_model import (TmdbMovieGenre, TmdbMovieReview,
                                           TmdbMovieReviewList,
                                           TmdbReviewAuthorDetail)
from service.logic.input_logic import map_genre_list, update_review_data


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


class FakeReviewRepositry:

    def save_review_list(self, review_list: list[Review]) -> int:
        return len(review_list)
