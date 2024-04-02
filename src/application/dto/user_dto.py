import re

from fastapi import (
    HTTPException,
)
from pycountry import (
    languages,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)

from .role_dto import (
    RoleResponse,
)


class UserBase(BaseModel):
    telegram_id: int | None = None
    username: str
    language: str | None = None


# TODO: Написать валидатор для языка
class UserUpdate(UserBase):
    username: str | None = None
    language: str | None = None

    @field_validator("username")
    def validate_name(cls, value: str) -> str:
        match_pattern = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")
        if not match_pattern.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @field_validator("language")
    def validate_language(cls, value: str) -> str:
        if not languages.get(alpha_2=value):
            raise HTTPException(status_code=422, detail="Invalid language code")
        return value


class UserResponse(UserBase):
    user_id: int
    roles: list["RoleResponse"] = []
    model_config = ConfigDict(
        from_attributes=True,
    )
