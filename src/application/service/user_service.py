from src.application.dto import (
    UserUpdateSchema,
)
from src.infrastructure.database.models import (
    UserModel,
)
from src.infrastructure.database.repositories import (
    SQLAlchemyUserRepository,
)


class UserService:
    def __init__(self, user_repository: SQLAlchemyUserRepository) -> None:
        self.repository: SQLAlchemyUserRepository = user_repository

    # async def create_user(self, user_in: UserRegistrationSchema) -> None:
    #     if user_in.password is None and user_in.telegram_id is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="You must specify one of the fields. Either telegram_id or password"
    #         )
    #     else:
    #         user_entity = UserEntity.create(
    #             **user_in.model_dump()
    #         )
    #         await self.repository.create(user_entity)

    async def get_users(self) -> list[UserModel]:
        return await self.repository.get_multi(is_active=True)

    async def get_user(self, user_id: int) -> UserModel | None:
        return await self.repository.get_single(user_id=user_id)

    async def update_user(self, user: UserUpdateSchema) -> UserModel:
        return await self.repository.partial_update(data_in=user)

    async def delete_user(self, user_id: int) -> None:
        return await self.repository.destroy(user_id=user_id, is_active=False)
