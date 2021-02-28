"""Solr APIクライアントモジュール

Solr APIのクライアントを記述するモジュール
"""
from typing import Protocol

from core.config import SolrSettings
from domain.models.solr.movies import SolrResultModel
from infra.client.solr.solr_query import SolrQuery
from util.http_util import call_get_api

SELECT_PATH = "/{collection}/select"


class AbstractSolrClient(Protocol):

    def search_movies(self, query: SolrQuery) -> SolrResultModel:
        """映画を検索する.

        Args:
            query (SolrQuery): Solrクエリ

        Returns:
            SolrResultModel: Solr検索結果
        """
        ...


class SolrClient:

    def __init__(self, settings: SolrSettings) -> None:
        self.url = settings.get_url()
        self.collection = settings.solr_collection

    def search_movies(self, query: SolrQuery) -> SolrResultModel:

        # リクエスト条件を構築
        url = self.url + SELECT_PATH.format(collection=self.collection)
        query_string = query.get_query_string()

        # API実行
        response = call_get_api(url=url, query_string=query_string)

        return SolrResultModel(**response.json())


async def get_solr_client() -> SolrClient:
    """Solrクライアントを取得します.

    Returns:
        SolrClient: Solrクライアント
    """
    return SolrClient(SolrSettings())
