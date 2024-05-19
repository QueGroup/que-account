from typing import (
    Final,
)

import pytest
from starlette import (
    status,
)

URL_PATH: Final[str] = "/api/v1/roles"


@pytest.fixture(scope="session")
async def admin_token(ac, admin_user):
    response = await ac.post("/api/v1/auth/login/",
                             json={"username": admin_user.username, "password": "admin_password"})
    token = response.json()["access_token"]
    return token


@pytest.mark.asyncio
async def test_get_role_by_id(ac, data_roles):
    role_id = data_roles[0].id
    response = await ac.get(f"{URL_PATH}/single/?role_id={role_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data_roles[0].to_dict()


@pytest.mark.asyncio
async def test_get_role_by_title(ac, data_roles):
    title = data_roles[0].title
    response = await ac.get(f"{URL_PATH}/single/?title={title}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data_roles[0].to_dict()


@pytest.mark.asyncio
async def test_get_roles(ac, data_roles):
    response = await ac.get(f"{URL_PATH}/single/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [i.to_dict() for i in data_roles]


@pytest.mark.asyncio
async def test_get_role_not_exists(ac, data_roles):
    role_id = 3
    title = "Test Title"
    id_response = await ac.get(f"{URL_PATH}/single/?role_id={role_id}")
    title_response = await ac.get(f"{URL_PATH}/single/?title={title}")
    assert id_response.status_code == status.HTTP_404_NOT_FOUND
    assert title_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_role(ac, admin_token):
    role_data = {
        "title": "new_role"
    }
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    response = await ac.post(f"{URL_PATH}/", json=role_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "new_role"


@pytest.mark.asyncio
async def test_update_role(ac, data_roles, admin_token):
    role_id = data_roles[0].id
    data = {"title": "New Title"}
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    response = await ac.patch(f"{URL_PATH}/{role_id}/", json=data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "New Title"
    assert response.json()["id"] == role_id


@pytest.mark.asyncio
async def test_delete_role(ac, data_roles, admin_token):
    role_id = data_roles[0].id
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }
    response = await ac.delete(f"{URL_PATH}/{role_id}/", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    get_response = await ac.get(f"{URL_PATH}/single/")
    assert get_response.status_code == status.HTTP_200_OK
