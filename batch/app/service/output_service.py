import json
from time import time_ns

from core.constants import HALF_SPACE
from core.decorator import batch_service
from core.logging import create_logger
from domain.models.internal.movie import Movie
from domain.models.solr.movie import MovieSolrModel
from domain.models.solr.schema import SolrSchemaModel
from infra.client.solr.api import AbstractSolrClient
from infra.repository.input.movie import AbstractMovieRepository
from util.resource import get_resource


log = create_logger(__file__)


SOLR_CONFIG_PATH = "solr/schema.json"


@batch_service
def update_schema(solr_client: AbstractSolrClient) -> None:

    log.info("検索スキーマ更新バッチ実行開始.")

    # 現時点のスキーマを取得
    current_schema = solr_client.get_schema()

    # 追加スキーマを取得
    update_schema = get_resource(SOLR_CONFIG_PATH)

    # スキーマの差分を計算
    schema = _calculate_difference(
        current_schema=current_schema.schema_,
        update_schema=json.loads(update_schema)
    )

    # スキーマをアップデート
    solr_client.update_schema(schema)

    log.info("検索スキーマ更新バッチ実行終了.")


@batch_service
def build_index(
    solr_client: AbstractSolrClient,
    movie_repository: AbstractMovieRepository
) -> None:

    # 実行時間
    exec_time = time_ns()
    log.info(f"検索インデックス構築バッチ実行開始. 実行開始時間={exec_time}")

    # 映画リストを取得
    # TODO チャンクに分ける
    # TODO 並列化
    movies = movie_repository.fetch_all()

    # Solr用のモデルに変換
    movie_solr_model_list = [_map_to_solr_model(movie, exec_time) for movie in movies if movie.can_output()]

    # 映画リストのインデックスを構築
    solr_client.index_movies(movie_solr_model_list)

    # 古いデータを削除
    solr_client.delete_old(exec_time)

    # コミット
    solr_client.commit()

    log.info(f"検索インデックス構築バッチ実行終了. データ数={len(movie_solr_model_list)}")


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
        release_date=movie.release_date_str,
        release_year=movie.release_year,
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


def _calculate_difference(
    current_schema: SolrSchemaModel,
    update_schema: dict
) -> dict:
    """差分スキーマ計算関数

    現在のschemaと更新対象のスキーマの差分を計算する
    """

    # 現在のスキーマのフィールドタイプ名をセットに変換
    current_field_type_set = {field_type["name"] for field_type in current_schema.fieldTypes}

    # フィールドタイプの差分を検知
    add_field_type = []
    replace_field_type = []
    for field_type in update_schema.get("fieldTypes", []):
        # 同名のフィールドタイプがある場合、replace
        if field_type["name"] in current_field_type_set:
            replace_field_type.append(field_type)
        # 新規のフィールドタイプの場合、add
        else:
            add_field_type.append(field_type)

    # 現在のスキーマのフィールド名をセットに変換
    current_field_set = {field["name"] for field in current_schema.fields_}

    # フィールドの差分を検知
    add_field = []
    replace_field = []
    for field in update_schema.get("fields", []):
        # 同名のフィールドタイプがある場合、replace
        if field["name"] in current_field_set:
            replace_field.append(field)
        # 新規のフィールドタイプの場合、add
        else:
            add_field.append(field)

    # TODO スキーマクラスを実装
    return {
        "add-field-type": add_field_type,
        "replace-field-type": replace_field_type,
        "add-field": add_field,
        "replace-field": replace_field
    }
