from domain.models.internal.movie_model import Genre
from infra.repository.input.genre_repository import GenreRepository
from sqlalchemy.engine.base import Engine


def test_fetch_all_genres(test_engine: Engine):

    # テストデータ
    genre = Genre(genre_id=0, name="name", japanese_name="japanese_name")
    test_engine.execute("INSERT INTO genres VALUES (?, ?, ?)",
        genre.genre_id,
        genre.name,
        genre.japanese_name
    )

    # テスト用のリポジトリを初期化
    genre_repository = GenreRepository(test_engine)

    assert genre_repository.fetch_all() == [genre]
