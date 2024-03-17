from dependency_injector import (
    containers,
    providers,
)

from src.application.service import (
    AuthService,
    UserService,
)
from src.infrastructure import (
    load_config,
)
from src.infrastructure.database import (
    DBConnector,
    RedisUserSignatureBlacklist,
)
from src.infrastructure.database.repositories import (
    SQLAlchemyAuthRepository,
    SQLAlchemyUserRepository,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.api.controllers.users",
            "src.presentation.api.controllers.auth",
            "src.presentation.api.controllers.healthcheck",
        ]
    )

    config = providers.Singleton(load_config)

    db = providers.Singleton(DBConnector, db_url=config().db.construct_sqlalchemy_url())
    redis = providers.Singleton(RedisUserSignatureBlacklist, url=config().db.construct_redis_dsn())

    user_repository = providers.Factory(
        SQLAlchemyUserRepository,
        session_factory=db.provided.get_db_session,
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    auth_repository = providers.Factory(
        SQLAlchemyAuthRepository,
        session_factory=db.provided.get_db_session,
    )
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
    )
