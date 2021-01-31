from pydantic import BaseModel


class Genre(BaseModel):
    genre_id: int
    name: str
    japanese_name: str