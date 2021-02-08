from typing import Protocol
import json

from core.config import SolrSettings
from domain.models.solr.movie import MovieSolrModel
from domain.models.solr.schema import SolrSchemaResponseModel
from util.http import APPLICATION_JSON, CONTENT_TYPE, call_get_api, call_post_api


# APIパス
SCHEMA_PATH = "/solr/{collection}/schema"
UPDATE_PATH = "/solr/{collection}/update"


class AbstractSolrClient(Protocol):
    
    def update_schema(self, schema_data: str) -> None:
        ...
    
    def index_movies(self, movies: list[MovieSolrModel]) -> None:
        ...

    def delete_old(self, exec_time) -> None:
        ...
    
    def commit(self) -> None:
        ...
    
    def get_schema(self) -> SolrSchemaResponseModel:
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

    def index_movies(self, movies: list[MovieSolrModel]) -> None:
        
        # リクエスト条件を構築
        url = self.url + UPDATE_PATH.format(collection=self.collection)
        data = json.dumps([movie.dict() for movie in movies])
        headers = {CONTENT_TYPE: APPLICATION_JSON}

        # POSTメソッドでAPIを実行
        response = call_post_api(url=url, data=data, headers=headers)

    def delete_old(self, exec_time: int) -> None:
        
        # リクエスト条件を構築
        url = self.url + UPDATE_PATH.format(collection=self.collection)
        data = json.dumps({
            "delete": {
                "query": f"index_time:[0 TO {exec_time-1}]"
            }
        })
        headers = {CONTENT_TYPE: APPLICATION_JSON}

        # POSTメソッドでAPIを実行
        response = call_post_api(url=url, data=data, headers=headers)

    def commit(self) -> None:

        # リクエスト条件を構築
        url = self.url + UPDATE_PATH.format(collection=self.collection)
        data = json.dumps({
            "commit": {}
        })
        headers = {CONTENT_TYPE: APPLICATION_JSON}

        # POSTメソッドでAPIを実行
        response = call_post_api(url=url, data=data, headers=headers)

    def get_schema(self) -> SolrSchemaResponseModel:
        
        # リクエスト条件を構築
        url = self.url + SCHEMA_PATH.format(collection=self.collection)

        # API実行
        response = call_get_api(url=url, query=None)

        print(response.json())

        return SolrSchemaResponseModel(**response.json())

