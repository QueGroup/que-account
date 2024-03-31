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

from src.application.dto import (
    JWTokensSchema,
)
from src.infrastructure.database.models import (
    UserModel,
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
        username_f = UserModel.username == kwargs.get("username")
        telegram_id_f = UserModel.telegram_id == kwargs.get("telegram_id")

        combined_filter = or_(username_f, telegram_id_f)

        return select(UserModel).filter(combined_filter)

    async def authenticate(
            self,
            session: AsyncSession,
            user_in: SchemaT,
    ) -> SchemaT:
        stmt = self._get_query(**user_in.model_dump())
        result: Result = await session.execute(stmt)
        user: UserModel = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError()
        if user_in.password and not HashService.verify_password(user.password, user_in.password):
            raise PasswordIncorrectError()
        access_token = SignatureService.create_access_token(data={"user_id": user.user_id})
        refresh_token = SignatureService.create_refresh_token(data={"user_id": user.user_id})
        return JWTokensSchema(
            access_token=access_token,
            refresh_token=refresh_token
        )


class TelegramAuthStrategy(AuthStrategy):
    @staticmethod
    def _get_query(**kwargs: Any) -> Select[tuple[Any]]:
        telegram_id = kwargs.get("telegram_id")
        return select(UserModel).where(UserModel.telegram_id == telegram_id)

    async def authenticate(
            self,
            session: AsyncSession,
            user_in: SchemaT,
            *args: Any,
            **kwargs: Any,
    ) -> JWTokensSchema:
        stmt = self._get_query(telegram_id=user_in.telegram_id)
        result: Result = await session.execute(stmt)
        user: UserModel = result.scalar_one_or_none()

        if HashService.verify_signature(
                **user_in.model_dump()
        ):
            if not user:
                raise UserNotFoundError()
            else:
                access_token = SignatureService.create_access_token(data={"user_id": user.user_id})
                refresh_token = SignatureService.create_refresh_token(data={"user_id": user.user_id})
                return JWTokensSchema(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
        else:
            raise InvalidSignatureError()
