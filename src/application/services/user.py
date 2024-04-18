from src.application import (
    dto,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.database.repositories import (
    UserRepository,
)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository: UserRepository = user_repository

    async def get_users(self, skip: int, limit: int) -> list[models.User]:
        return await self.repository.get_multi(is_active=True, skip=skip, limit=limit)

    async def get_user_by_id(self, user_id: int) -> models.User | None:
        return await self.repository.get_single(id=user_id)

    async def get_user_by_telegram_id(self, telegram_id: int) -> models.User | None:
        return await self.repository.get_single(telegram_id=telegram_id)

    async def get_user_by_username(self, username: str) -> models.User | None:
        return await self.repository.get_single(username=username)

    # FIXME: В параметрах передается pk, но в других методах стоит id. Нужно переименовать на id
    async def update_user(self, pk: int, user_in: dto.UserUpdate) -> models.User:
        return await self.repository.partial_update(data_in=user_in, pk=pk)

    async def deactivate_user(self, user_id: int) -> None:
        return await self.repository.destroy(id=user_id, is_active=False)

    async def reactivate_user(self, user_id: int) -> None:
        return await self.repository.destroy(id=user_id, is_active=True)
