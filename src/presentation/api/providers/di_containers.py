from dependency_injector import (
    containers,
    providers,
)

from src.application.services import (
    AuthService,
    CompositeNotifier,
    RoleService,
    UserService,
)
from src.application.services.profile import (
    ProfileService,
)
from src.infrastructure.database import (
    DBConnector,
    JTIRedisStorage,
    RedisConnector,
)
from src.infrastructure.database.repositories import (
    AuthRepository,
    ProfileRepository,
    UserRepository,
)
from src.infrastructure.database.repositories.role import (
    RoleRepository,
)
from src.core import (
    load_config,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.presentation.api.controllers.user",
            "src.presentation.api.controllers.auth",
            "src.presentation.api.controllers.healthcheck",
            "src.presentation.api.controllers.role",
            "src.presentation.api.controllers.profile"
        ]
    )

    config = providers.Singleton(load_config)
    db = providers.Singleton(DBConnector, db_url=config().db.construct_sqlalchemy_url())
    session = db.provided.get_db_session
    redis = providers.Singleton(RedisConnector, url=config().db.construct_redis_dsn())

    blacklist_service = providers.Factory(
        JTIRedisStorage,
        redis_connector=redis,
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=session,
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    role_repository = providers.Factory(
        RoleRepository,
        session_factory=session,
    )
    role_service = providers.Factory(
        RoleService,
        role_repository=role_repository,
    )
    notifier = providers.Factory(
        CompositeNotifier,
    )
    auth_repository = providers.Factory(
        AuthRepository,
        session_factory=session,
    )
    auth_service = providers.Factory(
        AuthService,
        auth_repository=auth_repository,
        role_service=role_service,
        notifier=notifier
    )
    profile_repository = providers.Factory(
        ProfileRepository,
        session_factory=session
    )
    profile_service = providers.Factory(
        ProfileService,
        profile_repository=profile_repository,
    )
