from domain.models.internal.movie import Genre, Movie
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.input.genre import AbstractGenreRepository
from infra.repository.input.movie import AbstractMovieRepository


def update_genre_master(genre_repository: AbstractGenreRepository, tmdb_client: AbstractTmdbClient):
    
    # 英語表記のジャンルを取得
    english_genres = tmdb_client.fetch_genres("en-US")

    # ジャンルIDで集計
    genre_id_dict = {genre.id : genre for genre in english_genres.genres}

    # 日本語表記のジャンルを取得
    # TODO languageをenumを切る
    japanese_genres = tmdb_client.fetch_genres("ja")

    # RDBモデルに詰め替える
    genre_list = []
    for jp_genre in japanese_genres.genres:
        en_genre = genre_id_dict.get(jp_genre.id)

        # 日本語表記と英語表記が一致しない場合はスキップ
        if not en_genre:
            print(jp_genre)
            continue

        genre_list.append(Genre(
            genre_id=en_genre.id, 
            name=en_genre.name, 
            japanese_name=jp_genre.name)
        )

    # モデルの永続化
    genre_repository.save(genre_list)


def update_movies(
    page: int, 
    tmdb_client: AbstractTmdbClient, 
    movie_repository: AbstractMovieRepository
):
    
    # 人気映画のリストを取得
    popular_movies = tmdb_client.fetch_popular_movies(page)

    # 映画IDリストを取得
    movie_id_list = [movie.id for movie in popular_movies.results]

    # 映画詳細リストを取得
    movie_detail_list = tmdb_client.fetch_movie_detail_list(
        movie_id_list=movie_id_list,
        language="ja"
    )

    # 映画モデルリストに変換
    movie_list = [
        Movie(
            tmdb_id=movie.id,
            imdb_id=movie.imdb_id,
            original_title=movie.original_title,
            japanese_title=movie.title,
            overview=movie.overview,
            tagline=movie.tagline,
            poster_path=movie.poster_path,
            backdrop_path=movie.backdrop_path,
            popularity=movie.popularity,
            vote_average=movie.vote_average,
            vote_count=movie.vote_count,
            genres=[Genre(genre_id=genre.id) for genre in movie.genres]
        )
        for movie in movie_detail_list
    ]

    # モデルの永続化
    movie_repository.save_movie_list(movie_list)
