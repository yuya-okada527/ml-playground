"""出稿サービスモジュール

出稿バッチに関するサービス関数を提供するモジュール
"""
import json
from time import time_ns

from core.aop import batch_service
from core.logger import create_logger
from infra.client.solr.solr_api import AbstractSolrClient
from infra.repository.input.movie_repository import AbstractMovieRepository
from util.resource_util import get_resource

from service.logic.output_logic import calculate_difference, map_to_solr_model

log = create_logger(__file__)


SOLR_CONFIG_PATH = "solr/schema.json"


@batch_service
def exec_update_solr_schema(solr_client: AbstractSolrClient) -> None:
    """Solrスキーマ更新処理を実行します.

    Args:
        solr_client (AbstractSolrClient): Solrクライアント
    """

    # 現時点のスキーマを取得
    current_schema = solr_client.get_schema()

    # 追加スキーマを取得
    # TODO リソースの取得先をどうする？
    update_schema = get_resource(SOLR_CONFIG_PATH)

    # スキーマの差分を計算
    schema = calculate_difference(
        current_schema=current_schema.schema_,
        update_schema=json.loads(update_schema)
    )

    # スキーマをアップデート
    solr_client.update_schema(schema)


@batch_service
def exec_build_index(
    solr_client: AbstractSolrClient,
    movie_repository: AbstractMovieRepository
) -> None:
    """インデックス構築処理を実行します.

    Args:
        solr_client (AbstractSolrClient): Solrクライアント
        movie_repository (AbstractMovieRepository): 映画リポジトリ
    """

    # 実行時間
    exec_time = time_ns()
    log.info(f"検索インデックス構築バッチ実行開始. 実行開始時間={exec_time}")

    # 映画リストを取得
    # TODO チャンクに分ける
    # TODO 並列化
    movies = movie_repository.fetch_all()

    # Solr用のモデルに変換
    movie_solr_model_list = [map_to_solr_model(movie, exec_time) for movie in movies if movie.can_output()]

    # 映画リストのインデックスを構築
    solr_client.index_movies(movie_solr_model_list)

    # 古いデータを削除
    solr_client.delete_old(exec_time)

    # コミット
    solr_client.commit()

    log.info(f"検索インデックス構築バッチ実行終了. データ数={len(movie_solr_model_list)}")
