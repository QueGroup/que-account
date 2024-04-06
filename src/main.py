import asyncio

from fastapi import (
    FastAPI,
)
import structlog
import uvicorn

from src.infrastructure.log import (
    configure_logging,
)
from src.presentation import (
    Container,
    setup_middlewares,
    setup_routes,
)

logger = structlog.stdlib.get_logger()


def init_api() -> FastAPI:
    app = FastAPI(
        title="Que Account",
        version="0.1.0",
    )

    return app


def init_services(app: FastAPI) -> None:
    setup_middlewares(app)
    configure_logging()
    container = Container()
    app.container = container
    setup_routes(app)


async def start_server(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8080,
        reload=True,
        use_colors=True,
        log_level="debug"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    app = init_api()
    init_services(app)
    await start_server(app)


if __name__ == "__main__":
    asyncio.run(main())
