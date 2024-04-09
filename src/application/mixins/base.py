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


# noinspection PyUnresolvedReferences
class RetrieveQueryMixin:
    """
    An abstract class providing a method for retrieving a query for fetching data.
    """

    @abc.abstractmethod
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        """
        Return a SELECT query for retrieving a single row from the database.

        >>> return select(self.model).filter(*args).filter_by(**kwargs)

        :param args: Filter arguments to be passed to the SELECT query
        :param kwargs: Filter keyword arguments to be passed to the SELECT query
        :return: A SELECT query for retrieving a single row from the database
        """
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class ListQueryMixin:
    """
    An abstract class providing a method for retrieving a query for fetching a list of data.
    """

    @abc.abstractmethod
    def _get_all_query(
            self,
            skip: int = 0,
            limit: int = 10,
            *args: Any,
            **kwargs: Any,
    ) -> Select[tuple[Any]]:
        """
        Return a SELECT query for retrieving multiple rows from the database.

        >>> return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

        :param skip: The number of rows to skip (optional, default 0)
        :param limit: The maximum number of rows to retrieve (optional, default 10)
        :param args: Filter arguments to be passed to the SELECT query
        :param kwargs: Filter keyword arguments to be passed to the SELECT query
        :return: A SELECT query for retrieving multiple rows from the database
        """
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class UpdateQueryMixin:
    """
    An abstract class providing a method for retrieving a query for updating data.
    """

    @abc.abstractmethod
    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        """
        Return an UPDATE query for updating a single row in the database.

        >>> return (
        ...     update(self.model)
        ...     .where(self.model.id == pk)
        ...     .values(**data_in.model_dump(exclude_unset=True))
        ...     .filter_by(**kwargs)
        ...     .returning(self.model)
        ...    )

        :param pk: The primary key of the row to be updated
        :param data_in: The updated data to be passed to the UPDATE query
        :param kwargs: Additional keyword arguments to be passed to the UPDATE query
        :return: An UPDATE query for updating a single row in the database
        """
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
class DeleteQueryMixin:
    """
    An abstract class providing a method for retrieving a query for deleting data.
    """

    @abc.abstractmethod
    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        """
        Return a DELETE query for deleting one or more rows from the database.

        >>> return Delete(self.model).filter(*args)

        :param args: Filter arguments to be passed to the DELETE query
        :param kwargs: Filter keyword arguments to be passed to the DELETE query
        :return: A DELETE query for deleting one or more rows from the database
        """
        raise NotImplementedError()


class RLUDQueryMixin(
    abc.ABC,
    RetrieveQueryMixin,
    ListQueryMixin,
    UpdateQueryMixin,
    DeleteQueryMixin,
):
    """
    An abstract class providing methods for retrieving, updating, and deleting data.
    """
    pass


class CRUDMixin(
    RLUDQueryMixin,
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

    async def reset_password(self, pk: int, password_in: ResetPassword) -> None:
        async with self._session_factory() as session:
            stmt = self._get_user(id=pk)
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
