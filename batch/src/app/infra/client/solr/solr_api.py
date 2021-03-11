"""Solr APIクライアントモジュール

Solrに対するHTTP通信を抽象化するモジュール
"""
import json
from typing import Protocol

from core.config import SolrSettings
from domain.models.solr.solr_movie_model import MovieSolrModel
from domain.models.solr.solr_schema_model import SolrSchemaResponseModel
from util.http_util import (APPLICATION_JSON, CONTENT_TYPE, call_get_api,
                            call_post_api)

# APIパス
SCHEMA_PATH = "/solr/{collection}/schema"
UPDATE_PATH = "/solr/{collection}/update"


class AbstractSolrClient(Protocol):
    """Solrクライアントインターフェース"""

    def update_schema(self, schema_data: str) -> None:
        """スキーマ更新関数

        Solrのスキーマを更新する.

        Args:
            schema_data: SolrのSchema APIでPOSTするJSONデータ
        """
        ...

    def index_movies(self, movies: list[MovieSolrModel]) -> None:
        """映画インデックス更新関数

        Solrの映画インデックスと更新する.

        Args:
            movies: 映画モデルリスト
        """
        ...

    def delete_old(self, exec_time: int) -> None:
        """データ削除関数

        Solrの古い映画インデックスを削除する.

        Args:
            exce_time: 実行日付(これ以前のデータを削除します)
        """
        ...

    def commit(self) -> None:
        """コミット関数

        Solrに対する更新をコミットする.
        """
        ...

    def get_schema(self) -> SolrSchemaResponseModel:
        """スキーマ取得関数

        Solrのスキーマを取得する.
        """
        ...


class SolrClient:

    def __init__(self, settings: SolrSettings) -> None:
        self.url = settings.get_url()
        self.collection = settings.solr_collection

    def update_schema(self, schema_data: str) -> None:

        # リクエスト条件を構築
        url = self.url + SCHEMA_PATH.format(collection=self.collection)

        # POSTメソッドでAPIを実行
        call_post_api(url=url, data=schema_data, timeout=60)

    def index_movies(self, movies: list[MovieSolrModel]) -> None:

        # リクエスト条件を構築
        url = self.url + UPDATE_PATH.format(collection=self.collection)
        data = json.dumps([movie.dict() for movie in movies])
        headers = {CONTENT_TYPE: APPLICATION_JSON}

        # POSTメソッドでAPIを実行
        call_post_api(url=url, data=data, headers=headers)

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
        call_post_api(url=url, data=data, headers=headers)

    def commit(self) -> None:

        # リクエスト条件を構築
        url = self.url + UPDATE_PATH.format(collection=self.collection)
        data = json.dumps({
            "commit": {}
        })
        headers = {CONTENT_TYPE: APPLICATION_JSON}

        # POSTメソッドでAPIを実行
        call_post_api(url=url, data=data, headers=headers)

    def get_schema(self) -> SolrSchemaResponseModel:

        # リクエスト条件を構築
        url = self.url + SCHEMA_PATH.format(collection=self.collection)

        # API実行
        response = call_get_api(url=url, query=None)

        return SolrSchemaResponseModel(**response.json())
