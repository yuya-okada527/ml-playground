from domain.models.internal.movie_model import (Genre, Movie, Review,
                                                _remove_emoji)


def test_cannot_output_if_both_original_and_japanese_title_is_empty():
    """タイトルが存在しない場合インデックス構築対象外"""

    # テストデータ
    movie = _make_movie_model()
    movie.original_title = ""
    movie.japanese_title = None

    assert not movie.can_output()


def test_cannot_output_if_overview_is_none():
    """シナリオがNoneの場合インデックス構築対象外"""

    # テストデータ
    movie = _make_movie_model()
    movie.overview = None

    assert movie.can_output() == False


def test_cannot_output_if_overview_is_empty():
    """シナリオが空文字の場合インデックス構築対象外"""

    # テストデータ
    movie = _make_movie_model()
    movie.overview = ""

    assert movie.can_output() == False


def test_cannot_output_if_both_poster_path_and_backdrop_path_is_empty():
    """ポスタと背景の両方が存在しない場合インデックス構築対象外"""

    # テストデータ
    movie = _make_movie_model()
    movie.poster_path = ""
    movie.backdrop_path = ""

    assert movie.can_output() == False


def test_cannot_output_if_num_similar_movies_is_less_than_5():
    """類似映画の件数が5件未満の場合インデックス構築対象外"""

    # テストデータ
    movie = _make_movie_model()
    movie.similar_movies = [1, 2, 3, 4]

    assert movie.can_output() == False


def test_can_output_movie():
    """条件に合う映画はインデックス構築可能"""

    # テストデータ
    movie = _make_movie_model()

    assert movie.can_output()


def test_remove_emoji_src_is_none():
    """ソース文字列がNoneの場合"""

    # テストデータ
    src = None

    assert _remove_emoji(src) == ""


def test_remove_emoji_src_is_empty():
    """ソース文字列が空文字の場合"""

    # テストデータ
    src = ""

    assert _remove_emoji(src) == ""


def test_remove_emoji_src_includes_emoji():
    """ソース文字列に絵文字を含む場合"""

    # テストデータ
    src = "before🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩after"

    assert _remove_emoji(src) == "beforeafter"


def test_remove_emoji_src_not_includes_emoji():
    """ソース文字列に絵文字を含まない場合"""

    # テストデータ
    src = "beforeafter"

    assert _remove_emoji(src) == "beforeafter"


def test_review_includes_emoji():
    """レビューデータに絵文字を含む場合"""

    # テストデータ
    review = Review(
        review_id="review",
        movie_id=0,
        review="before🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩after"
    )

    assert review.review_without_emoji == "beforeafter"


def test_genre_equal_if_genre_id_is_same():
    """ジャンルIDが同じなら同じジャンル"""

    # テストデータ
    genre1 = Genre(
        genre_id=0,
        name="name",
        japanese_name="japanese_name"
    )
    genre2 = Genre(
        genre_id=0,
        name="different name",
        japanese_name="different japanese_name"
    )

    assert genre1 == genre2


def test_genre_not_equal_if_genre_id_is_different():
    """ジャンルIDが同じなら同じジャンル"""

    # テストデータ
    genre1 = Genre(
        genre_id=0,
        name="name",
        japanese_name="japanese_name"
    )
    genre2 = Genre(
        genre_id=1,
        name="name",
        japanese_name="japanese_name"
    )

    assert genre1 != genre2


def test_genre_can_manage_same_genres():

    # テストデータ
    genre1 = Genre(
        genre_id=0,
        name="name",
        japanese_name="japanese_name"
    )
    genre2 = Genre(
        genre_id=0,
        name="different name",
        japanese_name="different japanese_name"
    )
    genre_set = set([genre1, genre2])

    assert len(genre_set) == 1


def _make_movie_model():
    """出稿対象となる最低限のフィールドを追加した映画モデル"""

    return Movie(
        movie_id=0,
        original_title="test title",
        overview="overview",
        poster_path="poster_path",
        similar_movies=[1, 2, 3, 4, 5]
    )
