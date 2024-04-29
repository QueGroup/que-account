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

from .role import (
    RoleResponse,
)


class UserBase(BaseModel):
    username: str
    language: str


class UserUpdate(UserBase):
    username: str | None = None
    language: str | None = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "dryhence",
                "language": "ru",
            }
        }
    )

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
    id: int
    telegram_id: int | None = None
    roles: list["RoleResponse"] = []
    days_since_created: int
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 76564380,
                "telegram_id": 8056567643,
                "username": "hencedry",
                "language": "en",
                "roles": [{"id": 1, "title": "admin"}],
                "days_since_created": 347
            }
        }
    )
