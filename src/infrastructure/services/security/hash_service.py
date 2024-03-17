from datetime import (
    datetime,
    timedelta,
)

from argon2 import (
    PasswordHasher,
)
from argon2.exceptions import (
    VerifyMismatchError,
)
from jose import (
    jwt,
)

from src.infrastructure import (
    load_config,
)

jwt_config = load_config().security


class HashService:
    _ph = PasswordHasher()

    @staticmethod
    def hash_password(password: str) -> str:
        return HashService._ph.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        try:
            HashService._ph.verify(password, hashed_password)
            return True
        except VerifyMismatchError:
            return False


class SignatureService:

    @staticmethod
    def create_access_token(
            data: dict,
            expires_delta: timedelta = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=jwt_config.access_expire_time_in_seconds)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(
            data: dict,
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=jwt_config.refresh_expire_time_in_seconds)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)
        return encoded_jwt
