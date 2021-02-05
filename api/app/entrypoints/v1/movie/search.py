from fastapi import APIRouter


router = APIRouter(
    prefix="/v1/movie/search",
    tags=["search"],
    # TODO 共通レスポンス
    responses={}
)

@router.get("")
async def search():
    return {}