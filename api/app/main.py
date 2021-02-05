from fastapi import FastAPI

from entrypoints.v1.movie import search as v1_search


app = FastAPI(
    title="Movie Recommender Core API",
    description="Movie Recommenderに対するコア機能を提供するAPI.",
    version="0.1.0"
)

# ルート定義
app.include_router(v1_search.router)
