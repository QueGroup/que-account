import re

from fastapi import (
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBasicCredentials,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)
from pydantic_core.core_schema import (
    ValidationInfo,
)


class JWTokens(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "access_token":
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikp"
                    "vaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                "refresh_token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l"
                                 "IiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.bQTnz6AuMJvmXXQsVPrxeQNvzDkimo7VNXxHeSBfC"
                                 "lLufmCVZRUuyTwJF311JHuh",
            }
        }
    )


class TokenData(BaseModel):
    id: int | None = None


class UserRegistration(BaseModel):
    username: str
    telegram_id: int | None = None
    password: str | None = None
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "username": "John Doe",
                "telegram_id": 1234567890,
            }
        }
    )

    @field_validator("username")
    def validate_name(cls, value: str) -> str | None:
        match_pattern = re.compile(r"^[a-zA-Z0-9\-]+$")
        if not match_pattern.match(value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Name should contains only letters"
            )
        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str | None:
        if value is None:
            return value
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should be at least 8 characters long"
            )
        if value.islower() or value.isupper():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should contain both uppercase and lowercase letters"
            )
        if value.isalnum():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should contain at least one special character"
            )
        return value


class UserLogin(HTTPBasicCredentials):
    pass


class UserTMELogin(BaseModel):
    telegram_id: int
    signature: str
    nonce: int
    timestamp: int

    model_config = ConfigDict(from_attributes=True)


class UserLoginWithOTP(BaseModel):
    telegram_id: str


class TelegramUserLogin(BaseModel):
    telegram_id: str
    username: str
    signature: str


class ConfirmOtp(BaseModel):
    code: int


class UserLogout(BaseModel):
    refresh_token: str


class ResetPassword(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str | None:
        if value is None:
            return value
        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should be at least 8 characters long"
            )
        if value.islower() or value.isupper():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should contain both uppercase and lowercase letters"
            )
        if value.isalnum():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password should contain at least one special character"
            )
        return value

    @field_validator('repeat_password')
    def repeat_password_must_match_new_password(cls, value: str, values: ValidationInfo) -> str | None:
        if value != values.data.get("new_password"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='New password and repeat password must match'
            )
        return value
