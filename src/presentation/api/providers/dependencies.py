from typing import (
    Annotated,
    Any,
    Callable,
    Coroutine,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import (
    jwt,
)

from src.application.dto import (
    TokenData,
)
from src.application.service import (
    UserService,
)
from src.infrastructure import (
    Config,
)
from src.infrastructure.database.models import (
    UserModel,
)
from src.presentation.api.providers.di_containers import (
    Container,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@inject
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        config: Config = Depends(Provide[Container.config]),
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.security.secret_key, algorithms=[config.security.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_id(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


@inject
def require_role() -> Callable[[UserModel], Coroutine[Any, Any, UserModel]]:
    async def check_user_roles(user: UserModel = Depends(get_current_user)) -> UserModel:
        if user.is_superuser:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this operation",
            )

    return check_user_roles
