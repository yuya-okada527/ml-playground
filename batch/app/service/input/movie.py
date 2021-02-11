from core.logging import create_logger
from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie import Genre, Movie
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.input.genre import AbstractGenreRepository
from infra.repository.input.movie import AbstractMovieRepository


log = create_logger(__file__)


def update_genre_master(
    genre_repository: AbstractGenreRepository, 
    tmdb_client: AbstractTmdbClient
) -> None:

    log.info("ジャンルマスタ更新バッチ実行開始")

    # 登録済のジャンルIDを全て取得
    genre_id_set = {genre.genre_id for genre in genre_repository.fetch_all()}
    
    # 英語表記のジャンルを取得
    english_genres = tmdb_client.fetch_genres(MovieLanguage.EN)

    # ジャンルIDで集計
    genre_id_dict = {genre.id : genre for genre in english_genres.genres}

    # 日本語表記のジャンルを取得
    japanese_genres = tmdb_client.fetch_genres(MovieLanguage.JP)

    # ジャンルモデルに詰め替える
    genre_list = []
    for jp_genre in japanese_genres.genres:

        # 登録済のジャンルはスキップ
        if jp_genre.id in genre_id_set:
            continue

        # 日本語表記と英語表記が一致しない場合はスキップ
        en_genre = genre_id_dict.get(jp_genre.id)
        if not en_genre:
            print(jp_genre)
            continue

        genre_list.append(Genre(
            genre_id=en_genre.id, 
            name=en_genre.name, 
            japanese_name=jp_genre.name)
        )

    # モデルの永続化
    count = genre_repository.save(genre_list)

    log.info(f"ジャンルマスタ更新バッチ実行完了. 更新数={count}")


def update_movies(
    page: int, 
    tmdb_client: AbstractTmdbClient, 
    movie_repository: AbstractMovieRepository
):

    log.info(f"人気映画情報取得バッチ実行開始. page={page}")

    # 登録済の映画IDを取得
    registered_movies = set(movie_repository.fetch_all_movie_id())
    
    # 人気映画のリストを取得
    popular_movies = tmdb_client.fetch_popular_movies(page)

    # 映画IDリストを取得
    movie_id_list = [movie.id for movie in popular_movies.results if not movie.id in registered_movies]

    # 映画詳細リストを取得
    movie_detail_list = tmdb_client.fetch_movie_detail_list(
        movie_id_list=movie_id_list,
        language=MovieLanguage.JP
    )

    # 映画モデルリストに変換
    movie_list = [movie.to_internal_movie() for movie in movie_detail_list]

    # モデルの永続化
    movie_repository.save_movie_list(movie_list)

    log.info(f"人気映画情報取得バッチ実行完了. 更新数={len(movie_list)}")
