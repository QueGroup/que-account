from typing import (
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
    Request,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import (
    JWTError,
)

from src.application import (
    dto,
)
from src.application.service import (
    UserService,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.services.security import (
    SignatureService,
)
from src.presentation.api.providers.di_containers import (
    Container,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@inject
async def get_current_user(
        request: Request,
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> models.UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    authorization = request.headers.get("Authorization")
    token = request.cookies.get("access_token") or (authorization and authorization.split()[1])
    if token is None:
        raise credentials_exception
    try:
        payload = SignatureService.decode_token(token=token)
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = dto.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_id(user_id=token_data.user_id)

    if user is None:
        raise credentials_exception
    return user


@inject
def require_role() -> Callable[[models.UserModel], Coroutine[Any, Any, models.UserModel]]:
    async def check_user_roles(user: models.UserModel = Depends(get_current_user)) -> models.UserModel:
        if user.is_superuser:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this operation",
            )

    return check_user_roles
