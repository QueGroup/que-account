import abc
from typing import (
    Any,
    TypeVar,
)

from pydantic import (
    BaseModel,
)
from sqlalchemy import (
    Result,
    Select,
    or_,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application import (
    dto,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.services.security import (
    HashService,
    SignatureService,
)
from src.presentation.api.exceptions import (
    InvalidSignatureError,
    PasswordIncorrectError,
    UserNotFoundError,
)

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class AuthStrategy(abc.ABC):
    @abc.abstractmethod
    async def authenticate(
            self,
            session: AsyncSession,
            user_in: SchemaT,
    ) -> SchemaT:
        pass


class DefaultAuthStrategy(AuthStrategy):

    @staticmethod
    def _get_query(*args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        username_f = models.UserModel.username == kwargs.get("username")
        telegram_id_f = models.UserModel.telegram_id == kwargs.get("telegram_id")

        combined_filter = or_(username_f, telegram_id_f)

        return select(models.UserModel).filter(combined_filter)

    async def authenticate(
            self,
            session: AsyncSession,
            user_in: SchemaT,
    ) -> SchemaT:
        stmt = self._get_query(**user_in.model_dump())
        result: Result = await session.execute(stmt)
        user: models.UserModel = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError()
        if user_in.password and not HashService.verify_password(user.password, user_in.password):
            raise PasswordIncorrectError()
        access_token = SignatureService.create_access_token(uid=str(user.user_id), fresh=True)
        refresh_token = SignatureService.create_refresh_token(uid=str(user.user_id))
        return dto.JWTokens(access_token=access_token, refresh_token=refresh_token)


class TelegramAuthStrategy(AuthStrategy):
    @staticmethod
    def _get_query(**kwargs: Any) -> Select[tuple[Any]]:
        telegram_id = kwargs.get("telegram_id")
        return select(models.UserModel).where(models.UserModel.telegram_id == telegram_id)

    async def authenticate(
            self,
            session: AsyncSession,
            user_in: SchemaT,
            *args: Any,
            **kwargs: Any,
    ) -> dto.JWTokens:
        stmt = self._get_query(telegram_id=user_in.telegram_id)
        result: Result = await session.execute(stmt)
        user: models.UserModel = result.scalar_one_or_none()

        if HashService.verify_signature(**user_in.model_dump()):
            if not user:
                raise UserNotFoundError()
            else:
                access_token = SignatureService.create_access_token(
                    uid=str(user.user_id), fresh=True
                )
                refresh_token = SignatureService.create_refresh_token(uid=str(user.user_id))
                return dto.JWTokens(access_token=access_token, refresh_token=refresh_token)
        else:
            raise InvalidSignatureError()
