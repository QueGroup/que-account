from dataclasses import (
    dataclass,
)
from typing import (
    Literal,
)

from environs import (
    Env,
)
from sqlalchemy import (
    URL,
)


# TODO: Разделить DBConfig на PSQLConfig и RedisConfig
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
    port: int

    redis_host: str
    redis_database: str
    redis_port: int
    redis_password: str | None = None

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
        redis_host = env.str("REDIS_HOST")
        redis_port = env.int("REDIS_PORT")
        redis_database = env.str("REDIS_DB")
        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
            redis_host=redis_host,
            redis_port=redis_port,
            redis_database=redis_database
        )


@dataclass(slots=True, frozen=True)
class S3Config:
    service_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str
    region_name: str
    bucket_name: str

    @staticmethod
    def from_env(env: Env) -> "S3Config":
        service_name = env.str("SERVICE_NAME", "s3")
        aws_access_key_id = env.str("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = env.str("AWS_SECRET_ACCESS_KEY")
        endpoint_url = env.str("ENDPOINT_URL", "https://storage.yandexcloud.net")
        region_name = env.str("REGION_NAME")
        bucket_name = env.str("BUCKET_NAME")

        return S3Config(
            service_name=service_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            region_name=region_name,
            bucket_name=bucket_name,
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
    access_token_cookie_httponly: bool
    access_token_cookie_secure: bool
    sessions_cookie_name: str
    access_token_cookie_samesite: Literal["lax", "strict", "none"] = "lax"
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
class Settings:
    """
    Application settings class.

    This class holds the settings specific to the application.

    Attributes
    ----------
    app_host : str
        The host address of the application (default is '127.0.0.1').
    app_port : int
        The port number of the application (default is 8080).
    """
    app_host: str = "127.0.0.1"
    app_port: int = 8080
    logfire: bool = True

    @staticmethod
    def from_env(env: Env) -> "Settings":
        return Settings(
            app_host=env.str("APP_HOST"),
            app_port=env.int("APP_PORT"),
            logfire=env.bool("LOGFIRE")
        )


@dataclass(slots=True, frozen=True)
class Miscellaneous:
    """
    Miscellaneous settings class.

    This class holds settings that don't fit into other categories.

    Attributes
    ----------
    bot_token : str
        API token for the telegram bot
    """
    bot_token: str

    @staticmethod
    def from_env(env: Env) -> "Miscellaneous":
        return Miscellaneous(
            bot_token=env.str("BOT_TOKEN"),
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
    settings: Settings
    misc: Miscellaneous
    s3: S3Config


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
        settings=Settings.from_env(env),
        misc=Miscellaneous.from_env(env),
        s3=S3Config.from_env(env),
    )
