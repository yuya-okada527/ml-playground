from core.config import InputDbSettings
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


def create_input_engine(settings: InputDbSettings) -> Engine:
    return create_engine(
        f"{settings.input_db_engine}://{settings.input_db_user}:{settings.input_db_password}@{settings.input_db_host}:{settings.input_db_port}/{settings.input_db_database}"
    )


ENGINE = create_input_engine(InputDbSettings())
