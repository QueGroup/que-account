from fastapi import (
    APIRouter,
)

user_router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@user_router.get("/hello/{name}")
async def say_hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}
