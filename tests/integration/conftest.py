import asyncio
from contextlib import (
    asynccontextmanager,
)
import os

from httpx import (
    AsyncClient,
)
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.database import (
    models,
)
from src.main import (
    create_app,
)

db_user = os.getenv("TEST_DB_USER")
db_password = os.getenv("TEST_DB_PASSWORD")
db_name = os.getenv("TEST_DB_NAME")
db_host = os.getenv("TEST_DB_HOST")
db_port = os.getenv("TEST_DB_PORT")

DB_URI = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine_test = create_async_engine(
    url=DB_URI,
    echo=False,
    max_overflow=200,
    pool_size=20,
    query_cache_size=1200,
)

async_session_maker = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

models.Model.metadata.bind = engine_test


@pytest.fixture(autouse=True, scope="session")
def app():
    yield create_app()


@asynccontextmanager
async def override_get_db():
    from sqlalchemy import (
        exc,
    )

    session: AsyncSession = async_session_maker()
    try:
        yield session
    except exc.SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


@pytest.fixture(autouse=True, scope="session")
async def setup_db() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Model.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Model.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac(app):
    app.container.session.override(override_get_db)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
