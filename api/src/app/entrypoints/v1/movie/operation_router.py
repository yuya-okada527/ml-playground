"""運用APIルーターモジュール

運用で使用するAPIのルーター定義を記述するモジュール
"""
from fastapi import APIRouter

# ルーター作成
router = APIRouter(
    prefix="/v1/operation",
    tags=["operation"],
    # TODO 共通レスポンス
    responses={}
)


@router.get(
    "/health",
    summary="ヘルスチェック",
    description="ヘルスチェック機能を提供するAPI."
)
async def ping() -> dict[str, str]:
    return {
        "health": "ok"
    }
