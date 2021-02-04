from sqlalchemy import create_engine

from core.config import InputDbSettings


INPUT_APPS = {
    "input": {
        "models": ["domain.models.rdb.input"],
        "default_connection": "default"
    }
}


def create_input_engine(settings: InputDbSettings):
    return create_engine(
        f"{settings.engine}://{settings.db_user}:{settings.password}@{settings.host}:{settings.port}/{settings.database}"
    )
