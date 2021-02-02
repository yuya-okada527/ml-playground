import typer
from core.config import SolrSettings

from infra.client.solr.api import SolrClient
from service.output.movie import update_schema


app = typer.Typer()


@app.command("schema")
def output_schema():

    # クライアントの初期化
    solr_client = SolrClient(SolrSettings())

    # サービスの実行
    update_schema(solr_client)

