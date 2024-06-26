from fastapi import (
    Request,
)

from src.application import (
    dto,
)
from src.domain.user import (
    entity,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.database.repositories import (
    AuthRepository,
    IAuthStrategy,
)

from .notification import (
    Notifier,
)
from .role import (
    RoleService,
)


class AuthService:
    def __init__(
            self,
            auth_repository: AuthRepository,
            role_service: RoleService,
            notifier: Notifier,
    ) -> None:
        self.repository: AuthRepository = auth_repository
        self.service: RoleService = role_service
        self.notifier: Notifier = notifier

    async def signup(self, user_in: dto.UserRegistration) -> models.User:
        user_entity = entity.User.create(
            **user_in.model_dump(),
        )
        return await self.repository.signup(
            user_in=user_entity,
            username=user_in.username,
            telegram_id=user_in.telegram_id,
        )

    async def signin(
            self,
            *,
            user_in: dto.UserTMELogin | dto.UserLogin,
            strategy: IAuthStrategy,
            request: Request | None = None
    ) -> dto.JWTokens:
        data = await self.repository.signin(user_in=user_in, strategy=strategy)
        text = self._get_device_info(request)
        if isinstance(data, tuple) and text is not None:
            telegram_id, jwt_tokens = data
            await self.notifier.send_message(chat_id=telegram_id, text=text)
            return jwt_tokens
        return data  # type: ignore

    async def reset_password(self, pk: int, password_in: dto.ResetPassword) -> None:
        return await self.repository.reset_password(pk=pk, password_in=password_in)

    @staticmethod
    def _get_device_info(request: Request) -> str | None:
        try:
            user_agent, host = request.headers.get("user-agent"), request.client.host
            return (
                "Logged in to your account. With device:\n"
                f"Browser: {user_agent}\n"
                f"IP: {host}\n"
            )
        except AttributeError:
            return None
