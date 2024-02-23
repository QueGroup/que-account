from typing import (
    AsyncGenerator,
)

from mypy.typeshed.stdlib.contextlib import (
    asynccontextmanager,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.config import (
    DbConfig,
)


class DBConnector:
    def __init__(self, db: DbConfig):
        self.engine = create_async_engine(
            url=db.construct_sqlalchemy_url(),
            echo=False,
            max_overflow=200,
            pool_size=20,
            query_cache_size=1200,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        from sqlalchemy import (
            exc,
        )

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        from sqlalchemy import (
            exc,
        )

        session: AsyncSession = self.session_factory()

        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
