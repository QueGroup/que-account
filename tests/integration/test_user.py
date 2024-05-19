from typing import (
    Final,
)

import pytest
from starlette import (
    status,
)

URL_PATH: Final[str] = "/api/v1/users"


@pytest.fixture(scope="session")
async def active_user(ac) -> dict[str, str]:
    response = await ac.post("/api/v1/auth/login/",
                             json={"username": "user1", "password": "user1"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.fixture(scope="session")
async def inactive_user(ac) -> dict[str, str]:
    response = await ac.post("/api/v1/auth/login/",
                             json={"username": "user3", "password": "user3"})
    assert response.status_code == status.HTTP_200_OK
    ac_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {ac_token}"}
    return headers


@pytest.mark.asyncio
async def test_get_users(ac, users):
    response = await ac.get(f"{URL_PATH}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user(ac, users, active_user):
    get_user_response = await ac.get(f"{URL_PATH}/me/", headers=active_user)
    excepted_len = 1
    assert get_user_response.status_code == status.HTTP_200_OK
    assert len([get_user_response.json()]) == excepted_len


@pytest.mark.asyncio
async def test_get_deactivate_user(ac, users, inactive_user):
    response = await ac.get(f"{URL_PATH}/me/", headers=inactive_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["message"] == "Your account is deactivated"


@pytest.mark.asyncio
async def test_reactivate_user(ac, users, inactive_user):
    response = await ac.post(f"{URL_PATH}/me/reactivate/", headers=inactive_user)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    me_response = await ac.get(f"{URL_PATH}/me/", headers=inactive_user)
    assert me_response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_deactivate_user(ac, users, active_user):
    response = await ac.delete(f"{URL_PATH}/me/", headers=active_user)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    me_response = await ac.get(f"{URL_PATH}/me/", headers=active_user)
    assert me_response.status_code == status.HTTP_400_BAD_REQUEST
    assert me_response.json()["detail"]["message"] == "Your account is deactivated"


@pytest.mark.asyncio
async def test_update_user(ac, users):
    response = await ac.post("/api/v1/auth/login/",
                             json={"username": "user4", "password": "user4"})
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {
        "language": "en"
    }
    response = await ac.patch(f"{URL_PATH}/me/", json=update_data, headers=headers)
    data = response.json()

    assert data["language"] == "en"
    assert response.status_code == status.HTTP_200_OK
