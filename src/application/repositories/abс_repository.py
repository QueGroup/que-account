import abc
import dataclasses
import logging
from typing import (
    Any,
    Callable,
    Generic,
    Sequence,
    Type,
    TypeVar,
)

from jose import (
    jwt,
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
from src.infrastructure.database.models import (
    Base,
)
from src.infrastructure.services.security import (
    HashService,
    SignatureService,
)
from src.presentation.api.exceptions import (
    InvalidTokenError,
    PasswordIncorrectError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=Any)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class QueryMixin(abc.ABC):
    @abc.abstractmethod
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        """
        :example: return select(self.model).filter(*args).filter_by(**filters)
        :param args:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _get_all_query(
            self,
            skip: int = 0,
            limit: int = 10,
            *args: Any,
            **kwargs: Any
    ) -> Select[tuple[Any]]:
        """
        :example: return select(self.model).order_by(order).limit(limit).offset(offset)
        :param skip:
        :param limit:
        :param args:
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _update_query(self, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        raise NotImplementedError()

    @abc.abstractmethod
    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        raise NotImplementedError()


class CRUDMixin(
    QueryMixin,
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

    async def partial_update(self, data_in: UpdateSchemaT, **kwargs: Any) -> ModelT:
        async with self._session_factory() as session:
            # stmt = (
            #     update(
            #         self.model
            #     ).values(
            #         **data_in.model_dump(
            #             exclude_unset=True
            #         )
            #     ).filter_by(
            #         **kwargs
            #     ).returning(
            #         self.model
            #     )
            # )
            stmt = self._update_query(data_in=data_in, **kwargs)
            result: Result = await session.execute(stmt)
            # await session.commit()
            return result.scalar_one()

    async def destroy(self, *args: Any, **kwargs: Any) -> None:
        async with self._session_factory() as session:
            await session.execute(self._delete_query(*args, **kwargs))
            await session.commit()


class AuthMixin(QueryMixin, abc.ABC, Generic[ModelT, CreateSchemaT]):
    def __init__(
            self, session: Callable[[], AsyncSession], model: Type[ModelT]
    ):
        self._session_factory = session
        self.model = model

    async def singup(self, user_in: CreateSchemaT, *args: Any, **kwargs: Any) -> ModelT:
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

    async def signin(self, user_in: SchemaT, *args: Any, **kwargs: Any) -> JWTokensSchema:
        async with self._session_factory() as session:
            stmt = self._get_query(*args, **kwargs)
            result: Result = await session.execute(stmt)
            user: ModelT = result.scalar_one_or_none()
            print(user)
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

    async def signout(self):
        # TODO: Реализуйте логику выхода из системы, например, добавление токена в черный список
        pass


# TODO: [WIP]
class AbstractRefreshTokenRepository(
    QueryMixin,
    abc.ABC,
    Generic[ModelT],
):
    def __init__(self, session: Callable[[], AsyncSession], model: Type[ModelT]) -> None:
        self._session_factory = session
        self.model = model

    async def create(self, refresh_token: str, user_id: int) -> ModelT:
        # token_headers = jwt.get_unverified_header(refresh_token)
        try:
            pass
        except jwt.JWTError as e:
            logging.info(e)
            raise InvalidTokenError()

    @staticmethod
    def _verify_refresh_token(token_payload: dict):
        if len(token_payload.values()) > 1:
            raise jwt.JWTError()
