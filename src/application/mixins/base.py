import abc
import dataclasses
from typing import (
    Any,
    Callable,
    Generic,
    Sequence,
    Type,
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
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.dto import (
    JWTokensSchema,
)
from src.application.strategies import (
    AuthStrategy,
)
from src.infrastructure.database.models import (
    Base,
)
from src.presentation.api.exceptions import (
    UserAlreadyExistsError,
)

ModelT = TypeVar("ModelT", bound=Base)
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
            **kwargs: Any
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


class RUDQueryMixin(
    abc.ABC,
    RetrieveQueryMixin,
    ListQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin
):
    pass


class CRUDMixin(
    RUDQueryMixin,
    Generic[ModelT, CreateSchemaT, UpdateSchemaT],
    abc.ABC,
):
    def __init__(
            self, session: Callable[[], AsyncSession], model: Type[ModelT]
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
    Generic[ModelT, CreateSchemaT]
):
    def __init__(
            self, session: Callable[[], AsyncSession], model: Type[ModelT]
    ):
        self._session_factory = session
        self.model = model

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
                raise UserAlreadyExistsError()
            user = self.model(
                **user_in.__dict__
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def signin(
            self,
            strategy: AuthStrategy,
            user_in: SchemaT
    ) -> JWTokensSchema:
        async with self._session_factory() as session:
            return await strategy.authenticate(user_in=user_in, session=session)

    async def signout(self) -> None:
        # TODO: Реализуйте логику выхода из системы, например, добавление токена в черный список
        pass
