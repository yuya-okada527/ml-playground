from typing import Protocol

from core.config import SolrSettings
from util.http import call_post_api
from 

# APIパス
SCHEMA_PATH = "/solr/{collection}/schema"


class AbstractSolrClient(Protocol):
    
    def update_schema(self, schema_data: str) -> None:
        ...


class SolrClient:

    def __init__(self, settings: SolrSettings) -> None:
        self.url = settings.get_url()
        self.collection = settings.collection
    
    def update_schema(self, schema_data: str) -> None:
        
        # リクエスト条件を構築
        url = self.url + SCHEMA_PATH.format(collection=self.collection)

        # POSTメソッドでAPIを実行
        response = call_post_api(url=url, data=schema_data)

        print(response)


