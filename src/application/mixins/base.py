import abc
import dataclasses
from typing import (
    Any,
    Callable,
    Generic,
    Sequence,
    TypeVar,
)

from pydantic import (
    BaseModel,
)
from sqlalchemy import (
    Delete,
    Result,
    Select,
    Update,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application import (
    dto,
)
from src.application.dto import (
    ResetPassword,
)
from src.application.strategies import (
    AuthStrategy,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.services.security import (
    HashService,
)
from src.shared import (
    ex,
)

ModelT = TypeVar("ModelT", bound=models.Model)
CreateSchemaT = TypeVar("CreateSchemaT", bound=Any)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class RetrieveQueryMixin:
    @abc.abstractmethod
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        raise NotImplementedError()


class ListQueryMixin:
    @abc.abstractmethod
    def _get_all_query(
            self,
            skip: int = 0,
            limit: int = 10,
            *args: Any,
            **kwargs: Any,
    ) -> Select[tuple[Any]]:
        raise NotImplementedError()


class UpdateQueryMixin:
    @abc.abstractmethod
    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        raise NotImplementedError()


class DeleteQueryMixin:
    @abc.abstractmethod
    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        raise NotImplementedError()


class RLUDQueryMixin(
    abc.ABC,
    RetrieveQueryMixin,
    ListQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
):
    pass


class RUQueryMixin(
    abc.ABC,
    RetrieveQueryMixin,
    UpdateQueryMixin,
):
    pass


class CRUDMixin(
    RLUDQueryMixin,
    Generic[ModelT, CreateSchemaT, UpdateSchemaT],
    abc.ABC,
):
    def __init__(
            self,
            session: Callable[[], AsyncSession],
            model: type[ModelT],
    ):
        self._session_factory = session
        self.model = model

    async def create(self, data_in: CreateSchemaT) -> ModelT:
        async with self._session_factory() as session:
            if dataclasses.is_dataclass(data_in):
                instance = self.model(**data_in.__dict__)
            elif issubclass(type(data_in), BaseModel):
                instance = self.model(**data_in.model_dump())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def get_single(self, *args: Any, **kwargs: Any) -> ModelT | None:
        async with self._session_factory() as session:
            row = await session.execute(self._get_query(*args, **kwargs))
            return row.scalar_one_or_none()

    async def get_multi(self, *args: Any, **kwargs: Any) -> list[ModelT]:
        async with self._session_factory() as session:
            row = await session.execute(self._get_all_query(*args, **kwargs))
            entity: Sequence[ModelT] = row.scalars().all()
            return list(entity)

    async def partial_update(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> ModelT:
        async with self._session_factory() as session:
            stmt = self._update_query(pk=pk, data_in=data_in, **kwargs)
            result: Result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def destroy(self, *args: Any, **kwargs: Any) -> None:
        async with self._session_factory() as session:
            await session.execute(self._delete_query(*args, **kwargs))
            await session.commit()


class AuthMixin(
    RetrieveQueryMixin,
    abc.ABC,
    Generic[ModelT, CreateSchemaT, UpdateSchemaT]
):
    def __init__(
            self,
            session: Callable[[], AsyncSession],
            model: type[ModelT],
    ):
        self._session_factory = session
        self.model = model

    def _get_user(self, *args: Any, **kwargs: Any) -> Select[tuple]:
        return select(self.model).filter(*args).filter_by(**kwargs)

    async def signup(
            self,
            user_in: CreateSchemaT,
            *args: Any,
            **kwargs: Any
    ) -> ModelT:
        async with self._session_factory() as session:
            stmt = self._get_query(*args, **kwargs)
            result: Result = await session.execute(stmt)
            if result.scalar() is not None:
                raise ex.UserAlreadyExists()
            user = self.model(**user_in.__dict__)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def signin(
            self,
            strategy: AuthStrategy,
            user_in: SchemaT
    ) -> dto.JWTokens:
        async with self._session_factory() as session:
            return await strategy.authenticate(user_in=user_in, session=session)

    # TODO: Когда пользователь сбрасывает пароль, то старые токены остаются активными
    async def reset_password(self, pk: int, password_in: ResetPassword) -> None:
        async with self._session_factory() as session:
            stmt = self._get_user(user_id=pk)
            result: Result = await session.execute(stmt)
            user: models.User = result.scalar_one_or_none()
            if not user:
                raise ex.UserNotFound(user_id=pk)
            if not HashService.verify_password(password=user.password, hashed_password=password_in.old_password):
                raise ex.IncorrectPassword()
            new_hashed_password = HashService.hash_password(password=password_in.new_password)
            user.password = new_hashed_password
            await session.execute(stmt)
            await session.commit()

    # TODO: Реализуйте логику выхода из системы, например, добавление токена в черный список
    async def signout(self) -> None:
        pass
