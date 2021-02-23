from app.domain.models.internal.movie_model import Movie


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


def test_can_output_movie():
    """条件に合う映画はインデックス構築可能"""

    # テストデータ
    movie = _make_movie_model()

    assert movie.can_output() == True


def _make_movie_model():

    return Movie(
        movie_id="test",
        original_title="test title",
        japanese_title="日本語タイトル",
        overview="overview",
        tagline="tagline",
        poster_path="poster_path",
        popularity=0,
        vote_average=0,
        vote_count=0
    )
