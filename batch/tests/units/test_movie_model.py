from app.domain.models.internal.movie_model import Movie


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


def _make_movie_model():
    """出稿対象となる最低限のフィールドを追加した映画モデル"""

    return Movie(
        movie_id="test",
        original_title="test title",
        overview="overview",
        poster_path="poster_path",
        similar_movies=[1, 2, 3, 4, 5]
    )
