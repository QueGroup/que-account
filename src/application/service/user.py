from src.application.dto import (
    UserUpdateSchema,
)
from src.infrastructure.database.models import (
    UserModel,
)
from src.infrastructure.database.repositories import (
    UserRepository,
)


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.repository: UserRepository = user_repository

    async def get_users(self) -> list[UserModel]:
        return await self.repository.get_multi(is_active=True)

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        return await self.repository.get_single(user_id=user_id)

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserModel | None:
        return await self.repository.get_single(telegram_id=telegram_id)

    async def get_user_by_username(self, username: str) -> UserModel | None:
        return await self.repository.get_single(username=username)

    async def update_user(self, pk: int, user_in: UserUpdateSchema) -> UserModel:
        return await self.repository.partial_update(data_in=user_in, pk=pk)

    async def deactivate_user(self, user_id: int) -> None:
        return await self.repository.destroy(user_id=user_id, is_active=False)
