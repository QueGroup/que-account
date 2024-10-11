from pydantic import (
    BaseModel,
)

__all__ = (
    "UserUpdate",
)


class UserBase(BaseModel):
    username: str
    language: str


class UserUpdate(UserBase):
    username: str | None = None
    language: str | None = None
