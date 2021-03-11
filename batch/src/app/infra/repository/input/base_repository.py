"""ベースリポジトリモジュール

リポジトリの共通機能を提供するモジュール
"""
import base64

from core.config import InputDbSettings
from core.logger import create_logger
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

log = create_logger(__file__)


def create_input_engine(settings: InputDbSettings) -> Engine:
    """入稿DBエンジン作成関数

    入稿DBエンジンを作成する
    """
    url = f"{settings.input_db_engine}://{settings.input_db_user}:{settings.input_db_password}@{settings.input_db_host}:{settings.input_db_port}/{settings.input_db_database}"
    log.error(base64.b64encode(url.encode()).decode())
    return create_engine(url)


ENGINE = create_input_engine(InputDbSettings())
