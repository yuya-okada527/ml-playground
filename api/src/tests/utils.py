from typing import List, Optional

from domain.enums.similarity_enums import SimilarityModelType
from domain.models.solr.movies import (MovieSolrModel, SolrResponseModel,
                                       SolrResultModel)
from infra.client.solr.solr_query import SolrQuery


def make_url(path: str, queries: Optional[List[str]] = None):
    assert isinstance(queries, list) or queries is None

    # クエリがあれば、クエリつきでURL作成
    if queries:
        return path + "?" + "&".join(queries)

    # クエリがない場合、パスのみ
    return path


async def get_fake_solr_client():
    return FakeSolrClient()

class FakeSolrClient:

    def search_movies(self, query: SolrQuery) -> SolrResultModel:
        return SolrResultModel(
            responseHeader=None,
            response=SolrResponseModel(
                numFound=1,
                start=0,
                numFoundExact=True,
                docs=[
                    MovieSolrModel(
                        movie_id=0,
                        original_title="original_title",
                        japanese_title="japanese_title",
                        poster_path="poster_path",
                        popularity=0,
                        vote_average=0
                    )
                ]
            )
        )


async def get_fake_kvs_repository():
    return FakeKvsRepository()


class FakeKvsRepository:

    def get_similar_movie_id_list(
        self,
        movie_id: int,
        model_type: SimilarityModelType
    ) -> List[int]:
        return [0]
