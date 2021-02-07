from fastapi import APIRouter, Path, Query, Depends

from entrypoints.v1.movie.messages.movie_messages import SimilarMovieResponse
from domain.enums.similarity_enums import SimilarityModelType
from infra.client.solr.api import AbstractSolrClient, get_solr_client
from infra.repository.redis_repository import AbstractKvsRepository, get_kvs_repository


router = APIRouter(
    prefix="/v1/movie/similar",
    tags=["similar"],
    # TODO 共通レスポンス
    responses={}
)


@router.get(
    "/{movie_id}",
    summary="類似映画取得API",
    description="類似映画情報を提供するAPI.",
    response_model=SimilarMovieResponse,
    response_description="類似映画結果"
)
async def search_similar(
    movie_id: int = Path(
        ...,
        ge=0,
        title="映画ID",
        description="指定映画と類似した映画情報を返します."
    ),
    model_type: SimilarityModelType = Query(
        ...,
        title="類似性判定モデルタイプ",
        description="類似性判定に使用するモデルのタイプ"
    ),
    kvs_repository: AbstractKvsRepository = Depends(get_kvs_repository),
    solr_client: AbstractSolrClient = Depends(get_solr_client)
) -> SimilarMovieResponse:
    return None