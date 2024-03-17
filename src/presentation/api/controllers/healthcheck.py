import asyncpg
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import (
    BaseModel,
)

from src.infrastructure import (
    Config,
)
from src.presentation.api.di_containers import (
    Container,
)

healthcheck_router = APIRouter()


class Healthcheck(BaseModel):
    status: str = "ok"


HEALTHCHECK = Healthcheck()


@healthcheck_router.get(
    "/",
    response_model=Healthcheck,
    status_code=status.HTTP_200_OK,
)
@inject
async def healthcheck(
        config: Config = Depends(Provide[Container.config])
) -> BaseModel:
    try:
        db_conn = await asyncpg.create_pool(dsn=config.db.construct_psql_dns())
        await db_conn.execute("SELECT 1")
        await db_conn.close()
        return HEALTHCHECK
    except OSError:
        raise HTTPException(status_code=500, detail="Database unavailable")
