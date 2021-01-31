from tortoise import fields
from tortoise.models import Model


class GenreRdbModel(Model):
    genre_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    japanese_name = fields.CharField(max_length=64)

    class Meta:
        table = "genres"
    
    def __str__(self) -> str:
        return f"[{self.genre_id=}, {self.name=}, {self.japanse_name=}]"

