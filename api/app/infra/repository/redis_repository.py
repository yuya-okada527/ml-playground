from typing import Protocol


class AbstractKvsRepository(Protocol):
    ...


class RedisRepository:
    ...


async def get_kvs_repository() -> AbstractKvsRepository:
    return RedisRepository()