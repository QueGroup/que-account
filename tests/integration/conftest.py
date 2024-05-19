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
from src.infrastructure.services.security import (
    HashService,
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


@pytest.fixture(scope="session")
async def data_roles() -> list[models.Role]:
    async with async_session_maker() as session:
        roles = [models.Role(id=i, title=f"Role{i}") for i in range(1, 3)]
        session.add_all(roles)
        await session.commit()
        yield roles


@pytest.fixture(scope="session")
async def admin_user() -> models.User:
    async with async_session_maker() as session:
        hashed_password = HashService.hash_password("admin_password")
        user = models.User(username="admin", password=hashed_password, is_superuser=True)
        session.add(user)
        await session.commit()
    yield user


@pytest.fixture(scope="session")
async def users() -> list[models.User]:
    async with async_session_maker() as session:
        users = [
            models.User(username="user1", password=HashService.hash_password("user1"), is_active=True),
            models.User(username="user2", password=HashService.hash_password("admin_password"), is_superuser=True),
            models.User(username="user3", password=HashService.hash_password("user3"), is_active=False),
            models.User(username="user4", password=HashService.hash_password("user4"), is_active=True),
        ]
        session.add_all(users)
        await session.commit()
        yield users


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
