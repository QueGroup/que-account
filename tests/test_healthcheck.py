from unittest.mock import (
    AsyncMock,
    patch,
)

import pytest
from httpx import (
    AsyncClient,
)


@pytest.mark.asyncio
@patch("asyncpg.create_pool", new_callable=AsyncMock)
async def test_healthcheck(mock_create_pool: AsyncMock, ac: AsyncClient):
    mock_create_pool.return_value = AsyncMock()
    mock_create_pool.return_value.__aenter__.return_value = AsyncMock()
    response = await ac.get("/api/v1/healthcheck/")
    assert response.json() == {"status": "ok"}
    assert response.status_code == 200
    mock_create_pool.assert_called_once()
