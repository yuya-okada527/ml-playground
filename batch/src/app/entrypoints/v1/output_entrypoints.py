"""出稿エントリポイントモジュール

全文検索エンジンにインデックスを構築する際に使用するバッチのエントリポイントを記述するモジュール
"""
import typer
from core.config import SolrSettings
from infra.client.solr.solr_api import SolrClient
from infra.repository.input.movie_repository import MovieRepository
from service.output_service import exec_build_index, exec_update_solr_schema

app = typer.Typer()


@app.command("schema")
def update_solr_schema_batch() -> None:
    """Solrスキーマ更新バッチ

    Solrのスキーマを更新します.
    """

    # クライアントの初期化
    solr_client = SolrClient(SolrSettings())

    # サービスの実行
    exec_update_solr_schema(solr_client=solr_client)


@app.command("index")
def build_index_batch() -> None:
    """インデックス構築バッチ

    検索インデックスを構築します.
    """

    # クライアントの初期化
    solr_client = SolrClient(SolrSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()

    # サービス実行
    exec_build_index(solr_client=solr_client, movie_repository=movie_repository)
