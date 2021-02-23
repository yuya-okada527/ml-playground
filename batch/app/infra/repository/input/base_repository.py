from core.config import InputDbSettings
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def create_input_engine(settings: InputDbSettings) -> Engine:
    return create_engine(
        f"{settings.engine}://{settings.db_user}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
    )


ENGINE = create_input_engine(InputDbSettings())
