from typing import (
    Annotated,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)

from src.application.dto import (
    RoleCreateSchema,
    RoleResponseSchema, RoleUpdateSchema,
)
from src.application.service import (
    RoleService,
)
from src.infrastructure.database.models import (
    RoleModel,
)
from src.presentation.api.providers import (
    Container,
    require_role,
)

role_router = APIRouter()


@role_router.post(
    "/",
    response_model=RoleResponseSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role())],
)
@inject
async def create_role(
        role_in: RoleCreateSchema,
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> RoleModel:
    return await role_service.create_role(role_in=role_in)


@role_router.get(
    "/",
    response_model=list[RoleResponseSchema],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_roles(
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> list[RoleModel]:
    return await role_service.get_all_roles()


@role_router.get(
    "/title/{title}/",
    response_model=RoleResponseSchema,
    summary="Get the single role by title",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_role_by_title(
        title: Annotated[str, Path],
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> RoleModel | None:
    role = await role_service.get_role_by_title(title=title)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@role_router.get(
    "/{role_id}/",
    response_model=RoleResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get the single role by role id"
)
@inject
async def get_role_by_id(
        role_id: Annotated[int, Path],
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> RoleModel | None:
    role = await role_service.get_role_by_id(role_id=role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@role_router.patch(
    "/{role_id}/",
    response_model=RoleResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role())],
)
@inject
async def update_role(
        role_id: Annotated[int, Path],
        role_in: RoleUpdateSchema,
        role_service: RoleService = Depends(Provide[Container.role_service])
):
    return await role_service.update_role(pk=role_id, role_in=role_in)


@role_router.delete(
    "/{role_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role())],
)
@inject
async def delete_role(
        role_id: Annotated[int, Path],
        role_service: RoleService = Depends(Provide[Container.role_service])
) -> None:
    return await role_service.delete_role(role_id=role_id)
