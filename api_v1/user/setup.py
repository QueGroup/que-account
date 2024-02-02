from fastapi import (
    FastAPI,
)

from .default import (
    default_router,
)
from .endpoints import (
    user_router,
)


def setup_endpoints(app: FastAPI) -> None:
    app.include_router(router=default_router)
    app.include_router(router=user_router)
