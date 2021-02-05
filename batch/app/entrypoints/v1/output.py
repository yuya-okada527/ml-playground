import typer
from core.config import SolrSettings

from infra.client.solr.api import SolrClient
from infra.repository.input.movie import MovieRepository
from service.output.movie import build_index, update_schema


app = typer.Typer()


@app.command("schema")
def output_schema():

    # クライアントの初期化
    solr_client = SolrClient(SolrSettings())

    # サービスの実行
    update_schema(solr_client)


@app.command("index")
def output_index():

    # クライアントの初期化
    solr_client = SolrClient(SolrSettings())

    # リポジトリの初期化
    movie_repository = MovieRepository()

    # サービス実行
    build_index(solr_client=solr_client, movie_repository=movie_repository)
