from tortoise import fields
from tortoise.models import Model


class GenreRdbModel(Model):
    genre_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    japanese_name = fields.CharField(max_length=64, null=True)

    class Meta:
        table = "genres"


class MovieGenreRdbModel(Model):
    movie_genre_id = fields.IntField(pk=True, generated=True)
    movie_id = fields.IntField(index=True)
    genre_id = fields.IntField()

    class Meta:
        table = "movie_genres"


class MovieRdbModel(Model):
    movie_id = fields.IntField(pk=True, generated=True)
    tmdb_id = fields.CharField(max_length=64, unique=True)
    imdb_id = fields.CharField(max_length=64, null=True)
    original_title = fields.CharField(max_length=256, null=True)
    japanese_title = fields.CharField(max_length=256, null=True)
    overview = fields.TextField()
    tagline = fields.TextField()
    poster_path = fields.CharField(max_length=256)
    backdrop_path = fields.CharField(max_length=256, null=True)
    popularity = fields.FloatField(null=True)
    vote_average = fields.FloatField(null=True)
    vote_count = fields.IntField(null=True)

    class Meta:
        table = "movies"
    
