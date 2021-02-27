from domain.models.internal.movie_model import Genre
from infra.repository.input.genre_repository import GenreRepository
from sqlalchemy.engine.base import Connection, Engine


def test_fetch_all_genres(conn: Connection):

    # テストデータ
    genre = Genre(genre_id=0, name="name", japanese_name="japanese_name")
    conn.execute("INSERT INTO genres VALUES (?, ?, ?)",
        genre.genre_id,
        genre.name,
        genre.japanese_name
    )

    # テスト用のリポジトリを初期化
    genre_repository = GenreRepository(conn)

    assert genre_repository.fetch_all() == [genre]
