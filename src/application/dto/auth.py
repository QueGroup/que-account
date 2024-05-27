from fastapi.security import (
    HTTPBasicCredentials,
)
from pydantic import (
    BaseModel,
)


class JWTokens(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: int
    jti: str


class UserRegistration(BaseModel):
    username: str
    telegram_id: int | None = None
    password: str | None = None


class UserLogin(HTTPBasicCredentials):
    """
    Attributes
    ----------
    username : str
    password : str
    telegram_id : Optional[int]
        Used only in telegram bot, when user has telegram_id, and we are using it for only saving
    """
    telegram_id: int | None = None


class UserTMELogin(BaseModel):
    telegram_id: int
    signature: str
    nonce: int
    timestamp: int


class UserLoginWithOTP(BaseModel):
    telegram_id: str


class ConfirmOtp(BaseModel):
    code: int


class ResetPassword(BaseModel):
    old_password: str
    new_password: str
    repeat_password: str
