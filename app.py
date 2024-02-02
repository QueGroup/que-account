import asyncio

from fastapi import (
    FastAPI,
)
import uvicorn

from api_v1.user import (
    setup_endpoints,
)


def init_api() -> FastAPI:
    app = FastAPI(
        title="Que Account",
        version="0.1.0",
    )
    setup_endpoints(app)
    return app


async def run_server(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8080,
        reload=True,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    app = init_api()
    await run_server(app)


if __name__ == "__main__":
    asyncio.run(main())
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)
