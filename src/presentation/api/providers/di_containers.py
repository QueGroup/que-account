from dependency_injector import (
    containers,
    providers,
)

from src.application.services import (
    AuthService,
    RoleService,
    TelegramNotifierService,
    UserService,
)
from src.infrastructure.database import (
    DBConnector,
    JTIRedisStorage,
    RedisConnector,
)
from src.infrastructure.database.repositories import (
    AuthRepository,
    UserRepository,
)
from src.infrastructure.database.repositories.role import (
    RoleRepository,
)
from src.shared import (
    load_config,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.api.controllers.user",
            "src.presentation.api.controllers.auth",
            "src.presentation.api.controllers.healthcheck",
            "src.presentation.api.controllers.role",
        ]
    )

    config = providers.Singleton(load_config)

    db = providers.Singleton(DBConnector, db_url=config().db.construct_sqlalchemy_url())
    redis = providers.Singleton(RedisConnector, url=config().db.construct_redis_dsn())

    blacklist_service = providers.Factory(
        JTIRedisStorage,
        redis_connector=redis,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.get_db_session,
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session_factory=db.provided.get_db_session,
    )
    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository,
    )
    telegram_notifier = providers.Factory(
        TelegramNotifierService,
        bot_token=config().misc.bot_token,
    )
    auth_repository = providers.Factory(
        AuthRepository,
        session_factory=db.provided.get_db_session,
    )
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        role_service=role_service,
        telegram_notifier=telegram_notifier
    )
