"""ミドルウェア定義モジュール

APIの実行前後で実行される処理を定義する
"""
from fastapi.middleware.cors import CORSMiddleware

# CORSミドルウェア
CORS = {
    "middleware_class": CORSMiddleware,
    "allow_origins": [
        # ローカルフロントAPP
        "http://localhost:3000",
    ],
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "expose_headers": []
}
