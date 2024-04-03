from pathlib import (
    Path,
)

from httpx import (
    AsyncClient,
)
import pytest
from sqlalchemy import (
    NullPool,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.database import (
    models,
)
from src.main import (
    init_api,
)
from src.presentation import (
    Container,
)

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db.sqlite3"

DB_URI = f"sqlite+aiosqlite:///{DB_PATH}"
engine_test = create_async_engine(
    DB_URI,
    poolclass=NullPool
)

async_session_maker = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)

models.Base.metadata.bind = engine_test
app = init_api()


async def override_get_db():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def setup_db() -> None:
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac():
    # noinspection PyUnresolvedReferences
    app.dependency_overrides[Container.db.provided.get_db_session] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
