from fastapi import (
    FastAPI,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from .api import (
    auth_router,
    healthcheck_router,
    user_router,
)
from .api.di_containers import (
    Container,
)
from .api.middlewares import (
    logging_middleware,
)


def setup_routes(app: FastAPI) -> None:
    prefix: str = "/api/v1"
    app.include_router(router=user_router, prefix=f"{prefix}/user", tags=["User"])
    app.include_router(router=healthcheck_router, prefix=f"{prefix}/healthcheck", tags=["Healthcheck"])
    app.include_router(router=auth_router, prefix=f"{prefix}/auth", tags=["Authorization"])


# noinspection PyTypeChecker
def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        BaseHTTPMiddleware, dispatch=logging_middleware
    )


__all__ = (
    "setup_middlewares",
    "setup_routes",
    "Container",
)
