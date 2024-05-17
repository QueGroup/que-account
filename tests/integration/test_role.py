from typing import (
    Final,
)

import pytest
from starlette import (
    status,
)

URL_PATH: Final[str] = "/api/v1/roles/single"


@pytest.mark.asyncio
async def test_get_role_by_id(ac, data_roles):
    role_id = data_roles[0].id
    response = await ac.get(f"{URL_PATH}/?role_id={role_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data_roles[0].to_dict()


@pytest.mark.asyncio
async def test_get_role_by_title(ac, data_roles):
    title = data_roles[0].title
    response = await ac.get(f"{URL_PATH}/?title={title}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data_roles[0].to_dict()


@pytest.mark.asyncio
async def test_get_roles(ac, data_roles):
    response = await ac.get(f"{URL_PATH}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [i.to_dict() for i in data_roles]


@pytest.mark.asyncio
async def test_get_role_not_exists(ac, data_roles):
    role_id = 3
    title = "Test Title"
    id_response = await ac.get(f"{URL_PATH}/?role_id={role_id}")
    title_response = await ac.get(f"{URL_PATH}/?title={title}")
    assert id_response.status_code == status.HTTP_404_NOT_FOUND
    assert title_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_role(ac):
    pass


@pytest.mark.asyncio
async def test_update_role(ac):
    pass


@pytest.mark.asyncio
async def test_delete_role(ac):
    pass
