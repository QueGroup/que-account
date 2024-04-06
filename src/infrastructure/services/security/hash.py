import hashlib
import hmac

from argon2 import (
    PasswordHasher,
)
from argon2.exceptions import (
    VerifyMismatchError,
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
            config.signature_secret_key.encode(), data_to_verify.encode(), hashlib.sha256
        ).hexdigest()

        return expected_signature == signature
