from sqlalchemy import create_engine

from core.config import InputDbSettings


def create_input_engine(settings: InputDbSettings):
    return create_engine(
        f"{settings.engine}://{settings.db_user}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
    )


ENGINE = create_input_engine(InputDbSettings())
