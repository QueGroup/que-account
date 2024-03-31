from datetime import (
    datetime,
    timedelta,
)
import hashlib
import hmac
from typing import (
    Any,
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

config = load_config().security


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

    @staticmethod
    def verify_signature(
            telegram_id: int,
            signature: str,
            timestamp: int,
            nonce: int,
    ) -> bool:
        data_to_verify = f"{telegram_id}{timestamp}{nonce}"
        expected_signature = hmac.new(
            config.signature_secret_key.encode(),
            data_to_verify.encode(),
            hashlib.sha256
        ).hexdigest()

        return expected_signature == signature


class SignatureService:

    @staticmethod
    def create_access_token(
            data: dict[str, Any],
            expires_delta: timedelta = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=config.access_expire_time_in_seconds)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(
            data: dict[str, Any],
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=config.refresh_expire_time_in_seconds)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
        return encoded_jwt
