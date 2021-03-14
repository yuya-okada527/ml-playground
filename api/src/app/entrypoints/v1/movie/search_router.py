"""検索APIルーターモジュール

検索APIのルーター定義を記述するモジュール
"""
from typing import Optional

from entrypoints.v1.movie.messages.movie_messages import (MovieIdResponse,
                                                          MovieResponse,
                                                          SearchMovieResponse)
from fastapi import APIRouter, Depends, Path, Query
from infra.client.solr.solr_api import AbstractSolrClient, get_solr_client
from service.search_service import (exec_search_by_id_service,
                                    exec_search_movie_ids, exec_search_service)
from util.query_util import split_query_params

# ルーター作成
router = APIRouter(
    prefix="/v1/movie/search",
    tags=["search"],
    # TODO 共通レスポンス
    responses={}
)


@router.get(
    "",
    summary="映画検索API",
    description="映画情報をフリーワードで検索する機能を提供するAPI.",
    response_model=SearchMovieResponse,
    response_description="検索結果"
)
async def search(
    query: Optional[str] = Query(
        None,
        max_length=100,
        title="検索クエリ",
        description="フリーワードの検索キーワードを指定してください。半角スペース/全角スペース区切りでAND検索を実行します."
    ),
    start: int = Query(
        0,
        ge=0,
        le=1000,
        title="取得開始位置",
        description="指定した位置でレスポンスを返します(0始まり)."
    ),
    rows: int = Query(
        10,
        ge=1,
        le=50,
        title="取得件数",
        description="指定した件数を最大取得件数としてレスポンスを返します."
    ),
    solr_client: AbstractSolrClient = Depends(get_solr_client)
) -> SearchMovieResponse:

    # サービス実行
    return exec_search_service(
        q=split_query_params(query),
        start=start,
        rows=rows,
        solr_client=solr_client
    )


@router.get(
    "/{movie_id}",
    summary="映画取得API",
    description="映画IDに紐づく映画情報を取得するAPI.",
    response_model=MovieResponse,
    response_description="検索結果"
)
async def search_by_id(
    movie_id: int = Path(
        ...,
        ge=0,
        title="映画ID",
        description="検索対象映画ID"
    ),
    solr_client: AbstractSolrClient = Depends(get_solr_client)
) -> MovieResponse:

    # サービス実行
    return exec_search_by_id_service(
        movie_id=movie_id,
        solr_client=solr_client
    )


@router.get(
    "/id/all",
    summary="全映画ID取得API",
    description="全映画IDを取得するAPI",
    response_model=MovieIdResponse,
    response_description="全映画IDリスト"
)
async def search_movie_ids(
    solr_client: AbstractSolrClient = Depends(get_solr_client)
) -> MovieIdResponse:

    # サービス実行
    return exec_search_movie_ids(solr_client=solr_client)
