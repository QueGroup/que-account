from fastapi import (
    HTTPException,
    status,
)

from src.application.dto import (
    JWTokensSchema,
    UserLoginSchema,
    UserRegistrationSchema,
)
from src.domain.user.entity import (
    UserEntity,
)
from src.infrastructure.database.models import (
    UserModel,
)
from src.infrastructure.database.repositories import (
    AuthRepository,
)


class AuthService:
    def __init__(self, auth_repository: AuthRepository) -> None:
        self.repository: AuthRepository = auth_repository

    async def signup(self, user_in: UserRegistrationSchema) -> UserModel:
        if user_in.password is None and user_in.telegram_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must specify one of the fields. Either telegram_id or password"
            )
        else:
            user_entity = UserEntity.create(
                **user_in.model_dump()
            )
            return await self.repository.singup(
                user_entity,
                username=user_in.username,
                telegram_id=user_in.telegram_id
            )

    async def signin(self, user_in: UserLoginSchema) -> JWTokensSchema:
        return await self.repository.signin(user_in=user_in)
