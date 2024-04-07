from src.application import (
    dto,
)
from src.application.strategies import (
    AuthStrategy,
)
from src.domain.user import (
    entity,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.database.repositories import (
    AuthRepository,
)

from .role import (
    RoleService,
)


class AuthService:
    def __init__(
            self,
            auth_repository: AuthRepository,
            role_service: RoleService,
    ) -> None:
        self.repository: AuthRepository = auth_repository
        self.service: RoleService = role_service

    async def signup(self, user_in: dto.UserRegistration) -> models.User:
        # FIXME: Необходимо установить роль по умолчанию для пользователя
        # role = await self.service.get_role_by_title(title="default_user")
        user_entity = entity.User.create(
            **user_in.model_dump(),
        )
        return await self.repository.signup(
            user_in=user_entity,
            username=user_in.username,
            telegram_id=user_in.telegram_id,
            # roles=[*{"role_id": role.role_id, "title": role.title}]
        )

    async def signin(
            self,
            user_in: dto.UserTMELogin | dto.UserLogin,
            strategy: AuthStrategy,
    ) -> dto.JWTokens:
        return await self.repository.signin(user_in=user_in, strategy=strategy)

    async def reset_password(self, pk: int, password_in: dto.ResetPassword) -> None:
        return await self.repository.reset_password(pk=pk, password_in=password_in)
