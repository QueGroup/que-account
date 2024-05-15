import abc
import dataclasses
from typing import (
    Any,
    Callable,
    Generic,
    Sequence,
)

from pydantic import (
    BaseModel,
)
from sqlalchemy import (
    Result,
    Select,
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
    IAuthStrategy,
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

from .interfaces import (
    IRetrieveQuery,
    IRLUDQuery,
)
from .types import (
    CreateSchemaT,
    ModelT,
    SchemaT,
    UpdateSchemaT,
)


class CRUDMixin(
    IRLUDQuery,
    Generic[ModelT, CreateSchemaT, UpdateSchemaT],
    abc.ABC,
):
    """
    An abstract class providing methods for creating, retrieving, updating, and deleting data.
    """

    def __init__(
            self,
            session: Callable[[], AsyncSession],
            model: type[ModelT],
    ):
        """
        :param session: a callable that returns an async SQLAlchemy session
        :param model: a SQLAlchemy model class
        """
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
    IRetrieveQuery,
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
            strategy: IAuthStrategy,
            user_in: SchemaT
    ) -> tuple[int, dto.JWTokens] | dto.JWTokens:
        async with self._session_factory() as session:
            return await strategy.authenticate(user_in=user_in, session=session)

    async def reset_password(self, pk: int, password_in: ResetPassword) -> None:
        async with self._session_factory() as session:
            stmt = self._get_user(id=pk)
            result: Result = await session.execute(stmt)
            user: models.User = result.scalar_one_or_none()
            if not user:
                raise ex.UserNotFound()
            if not HashService.verify_password(password=user.password, hashed_password=password_in.old_password):
                raise ex.IncorrectPassword()
            new_hashed_password = HashService.hash_password(password=password_in.new_password)
            user.password = new_hashed_password
            await session.execute(stmt)
            await session.commit()
