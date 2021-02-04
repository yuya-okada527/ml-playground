from infra.client.solr.api import AbstractSolrClient
from infra.repository.input.genre import AbstractGenreRepository
from util.resource import get_resource


SOLR_CONFIG_PATH = "solr/schema.json"


def update_schema(solr_client: AbstractSolrClient):

    # 追加スキーマを取得
    schema = get_resource(SOLR_CONFIG_PATH)

    # スキーマをアップデート
    solr_client.update_schema(schema)


def build_index(solr_client: AbstractSolrClient, genre_repository: AbstractGenreRepository):

    # ジャンルマスタを取得
    ...

    # 