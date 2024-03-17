from redis.asyncio import (
    Redis,
    from_url,
)


class RedisUserSignatureBlacklist:
    def __init__(self, url: str) -> None:
        self.protocol: Redis = from_url(
            url=url,
            decode_responses=True,
        )
        self.namespace: str = "auth_service"

    async def add(self, user_id: int, signature: str) -> None:
        signature_key = f"{self.namespace}:{user_id}"
        async with self.protocol.client() as session:
            await session.set(signature_key, signature)

    async def get(self, user_id: int) -> str:
        signature_key = f"{self.namespace}:{user_id}"
        async with self.protocol.client() as session:
            return await session.get(signature_key)

    async def remove(self, user_id: int):
        signature_key = f"{self.namespace}:{user_id}"
        async with self.protocol.client() as session:
            return await session.delete(signature_key)

    async def clear(self, user_id: int, count_size: int = 10) -> int:
        pattern = f"{self.namespace}:{user_id}:*"
        cursor = b"0"
        deleted_count = 0

        async with self.protocol.client() as session:
            while cursor:
                cursor, keys = await session.scan(cursor, match=pattern, count=count_size)
                deleted_count += await session.unlink(*keys)
        return deleted_count
