from unittest.mock import (
    AsyncMock,
)

import pytest

from src.application.services import (
    UserService,
)
from src.infrastructure.database.repositories import (
    UserRepository,
)


@pytest.fixture()
def mock_user_repository():
    mock_repo = AsyncMock(spec=UserRepository)
    yield mock_repo


@pytest.fixture()
def user_service(mock_user_repository):
    return UserService(user_repository=mock_user_repository)
