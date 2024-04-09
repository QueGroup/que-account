import abc


class PasswordEncoder(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def hash_password(password: str) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        pass
