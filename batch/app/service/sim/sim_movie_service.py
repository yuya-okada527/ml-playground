from infra.client.tmdb.api import AbstractTmdbClient
from infra.repository.sim.redis_repository import AbstarctRedisRepository
from infra.repository.input.movie import AbstractMovieRepository


def exec_constrcut_tmdb_similarity(
    tmdb_client: AbstractTmdbClient,
    redis_repository: AbstarctRedisRepository,
    movie_repository: AbstractMovieRepository
):
    ...
