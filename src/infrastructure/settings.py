from dataclasses import (
    dataclass,
)

from environs import (
    Env,
)
from sqlalchemy import (
    URL,
)


@dataclass(frozen=True, slots=True)
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    redis_host: str = ""
    redis_password: str = ""
    redis_database: str = ""
    redis_port: int = 0

    def construct_sqlalchemy_url(
            self,
            driver: str = "asyncpg",
            host: str | None = None,
            port: int | None = None,
    ) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """

        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    def construct_psql_dns(self) -> str:
        uri = URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    def construct_redis_dsn(self) -> str:
        uri = URL.create(
            drivername="redis",
            username=None,
            password=self.redis_password,
            host=self.redis_host,
            port=self.redis_port,
            database=self.redis_database,
        )
        return uri.render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str("DB_HOST")
        password = env.str("POSTGRES_PASSWORD")
        user = env.str("POSTGRES_USER")
        database = env.str("POSTGRES_DB")
        port = env.int("DB_PORT", 5432)
        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
        )


@dataclass(slots=True, frozen=True)
class Security:
    """
    Security configuration class.
    This class holds the settings related to the security of the application,
     such as JWT keys, token expiration times, and cookie settings.
    Attributes
    ----------
    secret_key : str
        The secret key used to sign JWT tokens.
    signature_secret_key : str
        The ...
    algorithm : str
        The algorithm used for signing and verifying JWT tokens.
    access_expire_time_in_seconds : int
        The lifetime of access tokens in seconds.
    refresh_expire_time_in_seconds : int
        The lifetime of refresh tokens in seconds.
    access_token_cookie_samesite : str
        The 'SameSite' attribute for access token cookies.
    access_token_cookie_httponly : bool
        Flag indicating whether access token cookies are accessible only via HTTP(S) requests.
    access_token_cookie_secure : bool
        Flag indicating whether access token cookies should only be sent over secure connections (HTTPS).
    sessions_cookie_name : str
        The name of the cookie used for storing access tokens.
    """
    secret_key: str
    signature_secret_key: str
    algorithm: str
    access_token_cookie_samesite: str
    access_token_cookie_httponly: bool
    access_token_cookie_secure: bool
    sessions_cookie_name: str
    access_expire_time_in_seconds: int = 60 * 60 * 24
    refresh_expire_time_in_seconds: int = 60 * 60 * 24 * 30

    @staticmethod
    def from_env(env: Env) -> "Security":
        secret_key = env.str("SECRET_JWT_KEY")
        signature_secret_key = env.str("SIGNATURE_SECRET_KEY")
        algorithm = env.str("ALGORITHM")
        access_token_cookie_samesite = env.str("ACCESS_TOKEN_COOKIE_SAMESITE")
        access_token_cookie_httponly = env.bool("ACCESS_TOKEN_COOKIE_HTTPONLY")
        access_token_cookie_secure = env.bool("ACCESS_TOKEN_SECURE")
        sessions_cookie_name = env.str("SESSION_COOKIE_NAME")

        return Security(
            secret_key=secret_key,
            algorithm=algorithm,
            access_token_cookie_samesite=access_token_cookie_samesite,
            access_token_cookie_httponly=access_token_cookie_httponly,
            access_token_cookie_secure=access_token_cookie_secure,
            sessions_cookie_name=sessions_cookie_name,
            signature_secret_key=signature_secret_key,
        )


@dataclass(slots=True, frozen=True)
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes,
    providing a centralized point of access for all settings.

    Attributes
    ----------
    db: Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    security: Optional[Security]
        Holds the settings specific to the jwt
    """

    db: DbConfig
    security: Security


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig.from_env(env),
        security=Security.from_env(env),
    )
