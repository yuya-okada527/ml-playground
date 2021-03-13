"""ミドルウェア定義モジュール

APIの実行前後で実行される処理を定義する
"""
from fastapi.middleware.cors import CORSMiddleware

from core.config import CoreSettings

core_settings = CoreSettings()

# CORSミドルウェア
CORS = {
    "middleware_class": CORSMiddleware,
    "allow_origins": core_settings.fe_domain.split(","),
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "expose_headers": []
}
