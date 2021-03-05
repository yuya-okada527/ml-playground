"""メインモジュール

APIの基本機能を定義するモジュール
"""
from fastapi import FastAPI

from core.middleware import CORS
from entrypoints.v1.movie import operation_router as v1_operation
from entrypoints.v1.movie import search_router as v1_search
from entrypoints.v1.movie import similar_router as v1_similar

# APP定義
app = FastAPI(
    title="ML Playground Core API",
    description="ML Playgroundに対するコア機能を提供するAPI.",
    version="0.1.0"
)

# ルート定義
app.include_router(v1_search.router)
app.include_router(v1_similar.router)
app.include_router(v1_operation.router)

# ミドルウェア定義
app.add_middleware(**CORS)
