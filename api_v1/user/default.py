from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import (
    RedirectResponse,
)

default_router = APIRouter(tags=["default"], include_in_schema=False)


@default_router.get("/", response_class=RedirectResponse)
async def home() -> RedirectResponse:
    return RedirectResponse("/docs", status_code=status.HTTP_302_FOUND)
