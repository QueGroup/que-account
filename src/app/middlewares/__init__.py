from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .logging import logging_middleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        BaseHTTPMiddleware, dispatch=logging_middleware
    )


__all__ = (
    "setup_middlewares",
)
