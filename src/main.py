import asyncio

from fastapi import (
    FastAPI,
)
import logfire
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
from src.core import (
    load_config,
)

logger = structlog.stdlib.get_logger()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Que Account",
        version="0.1.0",
        summary="The service API which provides access to the account",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
    )
    container = Container()
    app.container = container
    setup_routes(app)
    return app


def init_services(app: FastAPI) -> None:
    setup_middlewares(app)
    configure_logging()


async def start_server(app: FastAPI) -> None:
    config = load_config().settings
    app_config = uvicorn.Config(
        app,
        host=config.app_host,
        port=config.app_port,
        reload=True,
        use_colors=True,
        log_level="debug"
    )
    if config.logfire:
        logfire.configure()
        logfire.instrument_fastapi(app)
    server = uvicorn.Server(app_config)
    await server.serve()


async def main() -> None:
    app = create_app()
    init_services(app)

    await start_server(app)


if __name__ == "__main__":
    asyncio.run(main())
