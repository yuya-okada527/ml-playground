from infra.client.solr.api import SolrClient
from util.resource import get_resource


SOLR_CONFIG_PATH = "solr/schema.json"


def update_schema(solr_client: SolrClient):

    # 追加スキーマを取得
    schema = get_resource(SOLR_CONFIG_PATH)

    # スキーマをアップデート
    solr_client.update_schema(schema)

