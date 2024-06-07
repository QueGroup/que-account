import abc
import asyncio
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
    func,
    select,
)
from sqlalchemy.exc import (
    IntegrityError,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.core.types import (
    CreateSchemaT,
    ModelT,
    UpdateSchemaT,
)

from .interfaces import (
    IRetrieveQuery,
    IRLUDQuery,
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

    async def __generate_new_id(self) -> int:
        async with self._session_factory() as session:
            max_id_instance = await session.execute(select(func.max(self.model.id)))
            max_id = max_id_instance.scalar() or 0
            new_id = max_id + 1
            existing_instance = await session.get(self.model, new_id)
            while existing_instance:
                new_id += 1
                existing_instance = await session.get(self.model, new_id)
            return new_id

    async def generate_new_id(self) -> int:
        try:
            return await asyncio.wait_for(self.__generate_new_id(), timeout=5)
        except asyncio.TimeoutError:
            raise TimeoutError("Timeout occurred while generating new id.")

    async def create(self, data_in: CreateSchemaT) -> ModelT:
        async with self._session_factory() as session:
            if dataclasses.is_dataclass(data_in):
                instance = self.model(**data_in.__dict__)
            elif issubclass(type(data_in), BaseModel):
                instance = self.model(**data_in.model_dump())
            session.add(instance)
            try:
                await session.commit()
                await session.refresh(instance)
            except IntegrityError as e:
                if "duplicate key value violates unique constraint" in str(e.orig):
                    await session.rollback()
                    new_id = await self.generate_new_id()
                    instance.id = new_id
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
