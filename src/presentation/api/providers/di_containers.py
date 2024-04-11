from dependency_injector import (
    containers,
    providers,
)

from src.application.services import (
    AuthService,
    RoleService,
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
    AuthRepository,
    UserRepository,
)
from src.infrastructure.database.repositories.role import (
    RoleRepository,
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
    redis = providers.Singleton(RedisUserSignatureBlacklist, url=config().db.construct_redis_dsn())

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.get_db_session,
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    auth_repository = providers.Factory(
        AuthRepository,
        session_factory=db.provided.get_db_session,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session_factory=db.provided.get_db_session,
    )
    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        role_service=role_service,
    )
