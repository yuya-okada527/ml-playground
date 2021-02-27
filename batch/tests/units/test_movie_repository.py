from datetime import date

from domain.models.internal.movie_model import Genre, Movie
from infra.repository.input.movie_repository import MovieRepository
from sqlalchemy.engine.base import Connection


def test_fetch_all_movie_id(conn: Connection):

    # テストデータ
    movie = Movie(movie_id=0)
    conn.execute("INSERT INTO movies (movie_id) VALUES (?)", movie.movie_id)

    # テスト用のリポジトリを初期化
    movie_repository = MovieRepository(conn)

    assert movie_repository.fetch_all_movie_id() == [int(movie.movie_id)]


def test_fetch_all_similar_movies(conn: Connection):

    # テストデータ
    movie_id = 0
    similar_movie_list = [1, 2]
    conn.execute("INSERT INTO movies (movie_id) VALUES (?)", movie_id)
    for similar_movie_id in similar_movie_list:
        conn.execute("INSERT INTO similar_movies VALUES (?, ?)",
            movie_id,
            similar_movie_id
        )

    # テスト用のリポジトリを初期化
    movie_repository = MovieRepository(conn)

    # 検証
    actual = movie_repository.fetch_all_similar_movie()
    expected = {
        movie_id: similar_movie_list
    }

    assert actual == expected


def test_fetch_all_movies(conn: Connection):

    # テストデータ
    movie = Movie(
        movie_id=0,
        imdb_id="imdb_id",
        original_title="original_title",
        japanese_title="japanese_title",
        overview="overview",
        tagline="tagline",
        poster_path="poster_path",
        backdrop_path="backdrop_path",
        popularity=0.1,
        vote_average=1,
        vote_count=0,
        release_date=date(2020, 1, 1),
        genres=[Genre(genre_id=0, name="name", japanese_name="japanese_name")],
        similar_movies=[1, 2]
    )
    INSERT_MOVIE_STATEMENT = """\
    INSERT INTO
        movies
    VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
    """
    conn.execute(INSERT_MOVIE_STATEMENT,
        movie.movie_id,
        movie.imdb_id,
        movie.original_title,
        movie.japanese_title,
        movie.overview,
        movie.tagline,
        movie.poster_path,
        movie.backdrop_path,
        movie.popularity,
        movie.vote_average,
        movie.vote_count,
        movie.release_date_str
    )
    for genre in movie.genres:
        conn.execute("INSERT INTO genres VALUES (?, ?, ?)",
            genre.genre_id,
            genre.name,
            genre.japanese_name
        )
        conn.execute("INSERT INTO movie_genres VALUES (?, ?)",
            movie.movie_id,
            genre.genre_id
        )
    for similar_movie_id in movie.similar_movies:
        conn.execute("INSERT INTO similar_movies VALUES (?, ?)",
            movie.movie_id,
            similar_movie_id
        )

    # テスト用のリポジトリを初期化
    movie_repository = MovieRepository(conn)

    # 検証
    actual = movie_repository.fetch_all()

    assert len(actual[0].genres) == 1
    assert actual == [movie]
