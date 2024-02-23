from typing import (
    Awaitable,
    Callable,
)

from fastapi import (
    Request,
    Response,
)
import structlog


async def logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    req_id = request.headers.get("request-id")

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=req_id,
    )

    response: Response = await call_next(request)

    return response
