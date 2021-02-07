from time import time_ns
from core.constants import HALF_SPACE

from domain.models.internal.movie import Movie
from domain.models.solr.movie import MovieSolrModel
from infra.client.solr.api import AbstractSolrClient
from infra.repository.input.movie import AbstractMovieRepository
from util.resource import get_resource


SOLR_CONFIG_PATH = "solr/schema.json"


def update_schema(solr_client: AbstractSolrClient):

    # 現時点のスキーマを取得
    old_schema = solr_client.get_schema()

    # 追加スキーマを取得
    new_schema = get_resource(SOLR_CONFIG_PATH)

    if True:
        return None

    # スキーマの差分を計算
    schema = ...

    # スキーマをアップデート
    solr_client.update_schema(schema)


def build_index(
    solr_client: AbstractSolrClient, 
    movie_repository: AbstractMovieRepository
) -> None:

    # 実行時間
    exec_time = time_ns()
    print(f"実行時間={exec_time}")

    # 映画リストを取得
    # TODO チャンクに分ける
    # TODO 並列化
    movies = movie_repository.fetch_all()

    # Solr用のモデルに変換
    movie_solr_model_list = [_map_to_solr_model(movie, exec_time) for movie in movies]

    # 映画リストのインデックスを構築
    solr_client.index_movies(movie_solr_model_list)

    # 古いデータを削除
    solr_client.delete_old(exec_time)

    # コミット
    solr_client.commit()



def _map_to_solr_model(movie: Movie, exec_time: int) -> MovieSolrModel:
    return MovieSolrModel(
        movie_id=movie.movie_id,
        free_word=_make_freeword(movie),
        original_title=movie.original_title,
        japanese_title=movie.japanese_title,
        overview=movie.overview,
        tagline=movie.tagline,
        poster_path=movie.poster_path,
        backdrop_path=movie.backdrop_path,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        genres=[genre.genre_id for genre in movie.genres],
        genre_labels=[genre.japanese_name for genre in movie.genres],
        index_time=exec_time
    )


def _make_freeword(movie: Movie):
    
    # フリーワードの要素を保持
    free_word_list = []

    # タイトル
    free_word_list.append(movie.original_title)
    free_word_list.append(movie.japanese_title)

    # ジャンル
    free_word_list.extend([genre.japanese_name for genre in movie.genres])

    # 半角スペース区切りで返す
    return HALF_SPACE.join(free_word_list)
