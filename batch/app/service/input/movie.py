from core.decorator import service
from core.logging import create_logger
from domain.enums.movie_enums import MovieLanguage
from domain.models.internal.movie import Genre, Movie, Review
from domain.models.rest.tmdb import TmdbMovieReview
from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.input.genre import AbstractGenreRepository
from infra.repository.input.movie import AbstractMovieRepository
from infra.repository.input.review_repository import AbstractReviewRepository


MAX_SIMILAR_MOVIES = 5


log = create_logger(__file__)


@service
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
    # TODO APIだと日本語データを取得できない... (翻訳API?)
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


@service
def update_movies(
    page: int,
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository
) -> None:

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


@service
def collect_reviews(
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository,
    review_repository: AbstractReviewRepository
) -> None:

    log.info("レビューデータ収集バッチ実行開始.")

    # 登録済の映画IDを全て取得
    registered_movie_ids = movie_repository.fetch_all_movie_id()

    # 登録済のレビューIDを全て取得
    registered_review_ids = review_repository.fetch_all_review_id()

    # 映画IDごとにレビューデータを取得・登録していく
    count = 0
    for movie_id in registered_movie_ids:
        # ページは1固定とする
        movie_review_response = tmdb_client.fetch_movie_reviews(movie_id=movie_id, page=1)
        # 内部モデルに変換
        movie_review_list = [_map_review_model(review, movie_id)
            for review in movie_review_response.results
            if review.id not in registered_review_ids   # 登録済の物はスキップする
        ]

        # 登録
        count += review_repository.save_review_list(movie_review_list)

    log.info(f"レビューデータ収集バッチ実行終了.  登録数={count}")


@service
def collect_similar_movies(
    tmdb_client: AbstractTmdbClient,
    movie_repository: AbstractMovieRepository
) -> None:

    log.info("類似映画収集バッチ実行開始.")

    # 登録済の映画IDを全て取得
    registered_movies_id_set = set(movie_repository.fetch_all_movie_id())

    # 登録済の類似映画IDを全て取得 (key: movie_id, value: set(similar_movie_id))
    registered_similar_movie_map = movie_repository.fetch_all_similar_movie()

    # 映画IDごとに全ての類似映画を取得
    count = 0
    for i, movie_id in enumerate(registered_movies_id_set, start=1):

        # 登録している映画はスキップする
        if movie_id in registered_similar_movie_map:
            continue

        # 最終ページまで全ての類似映画を取得する
        similar_movie_list = []
        current_page = 1
        while True:
            # 類似映画IDリストを更新
            similar_movies_response = tmdb_client.fetch_similar_movie_list(
                movie_id=movie_id,
                page=current_page
            )
            similar_movie_list.extend(
                [movie.id for movie in similar_movies_response.results if movie.id in registered_movies_id_set]
            )

            # 最終ページなら終了
            if current_page == similar_movies_response.total_pages:
                break

            # 類似映画の数が閾値を超えたら打ち切り
            if len(similar_movie_list) >= MAX_SIMILAR_MOVIES:
                break

            # ページを更新し、再度API実行
            current_page += 1

        # 登録できる映画IDがない場合、スキップ
        if not similar_movie_list:
            continue

        # UPSERT処理で登録
        count += movie_repository.save_similar_movie_list(
            movie_id=movie_id,
            similar_movie_list=similar_movie_list
        )

        if i % 20 == 0:
            log.info(f"{i}件目の処理が完了しました.")

    log.info(f"類似映画収集バッチ実行終了.  登録数={count}")


def _map_review_model(movie_review: TmdbMovieReview, movie_id: int) -> Review:
    return Review(
        review_id=movie_review.id,
        movie_id=movie_id,
        review=movie_review.content
    )
