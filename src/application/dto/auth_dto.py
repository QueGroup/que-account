import re

from fastapi import (
    HTTPException,
)
from fastapi.security import (
    HTTPBasicCredentials,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class JWTokens(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    user_id: int | None = None


class UserRegistration(BaseModel):
    username: str
    telegram_id: int | None = None
    password: str | None = None

    @field_validator("username")
    def validate_name(cls, value: str) -> str:
        match_pattern = re.compile(r"^[a-zA-Z0-9\-]+$")
        if not match_pattern.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str | None:
        if value is None:
            return value
        if len(value) < 8:
            raise HTTPException(
                status_code=422, detail="Password should be at least 8 characters long"
            )
        if value.islower() or value.isupper():
            raise HTTPException(
                status_code=422, detail="Password should contain both uppercase and lowercase letters"
            )
        if value.isalnum():
            raise HTTPException(
                status_code=422, detail="Password should contain at least one special character"
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


class SetNewPassword(BaseModel):
    new_password: str
    re_new_password: str
    old_password: str


class ConfirmOtp(BaseModel):
    code: int


class UserLogout(BaseModel):
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenVerify(BaseModel):
    access_token: str
