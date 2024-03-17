import re

from fastapi import (
    HTTPException,
)
from pydantic import (
    BaseModel,
    field_validator,
)


class UserBaseSchema(BaseModel):
    telegram_id: int | None = None
    username: str


class UserUpdateSchema(UserBaseSchema):
    telegram_id: int | None = None
    username: str | None = None
    is_active: bool | None = None
    language: str | None = None

    @field_validator("username")
    def validate_name(cls, value) -> str:
        match_pattern = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
        if not match_pattern.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value


class UserResponseSchema(UserBaseSchema):
    user_id: int
