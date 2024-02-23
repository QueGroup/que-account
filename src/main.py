import asyncio

from fastapi import (
    FastAPI,
)
import structlog
import uvicorn

from src.app.middlewares import (
    setup_middlewares,
)
from src.infrastructure.log import (
    configure_logging,
)

logger = structlog.stdlib.get_logger()


async def init_api() -> FastAPI:
    app = FastAPI(
        title="Que Account",
        version="0.1.0",
    )
    configure_logging()
    setup_middlewares(app)
    await logger.info("Initializing API")
    return app


async def run_server(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8080,
        reload=True,
        use_colors=True,
        log_level="debug"
    )
    server = uvicorn.Server(config)
    await logger.info("Starting server")
    await server.serve()


async def main() -> None:
    app = await init_api()
    await run_server(app)


if __name__ == "__main__":
    asyncio.run(main())
