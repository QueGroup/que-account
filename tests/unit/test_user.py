from typing import (
    Any,
)
import unittest

import pytest

from src.core import (
    ex,
)
from src.domain.user import (
    entity,
)
from src.infrastructure.database import (
    models,
)
from tests.misc import (
    fake,
)


class TestUserEntity(unittest.TestCase):

    def setUp(self):
        self.user = entity.User(
            username=fake.username(),
            password=fake.password(),
            telegram_id=fake.telegram_id(),
            is_active=fake.bool(),
            is_superuser=fake.bool(),
            language=fake.language_code()
        )

    def test_create_user_without_password_and_telegram_id(self):
        with self.assertRaises(ex.MissingFieldsError):
            entity.User.create(password=None, telegram_id=None, username=fake.username())

    def test_create_user_with_password(self):
        password = fake.password()

        user = entity.User.create(password=password, telegram_id=None, username=fake.username())

        self.assertTrue(user.check_password(password_in=password, password=user.password))
        self.assertIsNone(user.telegram_id)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.deleted_at)
        self.assertEqual(user.language, "ru")

    def test_create_user_with_telegram_id(self):
        telegram_id = fake.telegram_id()
        user = entity.User.create(telegram_id=telegram_id, password=None, username=fake.username())

        self.assertIsNone(user.password)
        self.assertEqual(user.telegram_id, telegram_id)

    def test_set_password(self):
        new_password = fake.password()
        self.user.set_password(new_password)

        self.assertTrue(self.user.check_password(new_password))
        self.assertFalse(self.user.check_password(self.user.password))


@pytest.mark.asyncio
class TestUserService:

    async def test_get_users(self, mock_user_repository: Any, user_service: Any):
        expected_users = [
            models.User(id=1, username='user1', telegram_id=123),
            models.User(id=2, username='user2', telegram_id=456),
        ]
        mock_user_repository.get_multi.return_value = expected_users

        users = await user_service.get_users(skip=0, limit=10)

        mock_user_repository.get_multi.assert_called_once_with(is_active=True, skip=0, limit=10)
        assert len(users) == 2
        assert users[0].id == 1
        assert users[0].username == 'user1'
        assert users[0].telegram_id == 123
        assert users[1].id == 2
        assert users[1].username == 'user2'
        assert users[1].telegram_id == 456

    @pytest.mark.parametrize(
        "user_id, expected_user",
        [
            (1, models.User(id=1, username='user1', telegram_id=123)),
            (2, models.User(id=2, username='user2', telegram_id=456)),
            (3, None),
        ]
    )
    async def test_get_user_by_id(self, mock_user_repository: Any, user_service: Any, user_id, expected_user):
        if expected_user is not None:
            mock_user_repository.get_single.return_value = expected_user
        else:
            mock_user_repository.get_single.return_value = None

        user = await user_service.get_user_by_id(user_id=user_id)

        mock_user_repository.get_single.assert_called_once_with(id=user_id)
        assert user == expected_user

    @pytest.mark.asyncio
    async def test_update_user(self, mock_user_repository: Any, user_service: Any):
        user_in = {'username': 'new_username'}
        expected_user = models.User(id=1, username='new_username')
        mock_user_repository.partial_update.return_value = expected_user

        user = await user_service.update_user(pk=1, user_in=user_in)

        mock_user_repository.partial_update.assert_called_once_with(data_in=user_in, pk=1)
        assert user == expected_user

    async def test_deactivate_user(self, mock_user_repository: Any, user_service: Any):
        expected_user = models.User(id=1, is_active=False)
        mock_user_repository.destroy.return_value = expected_user

        await user_service.deactivate_user(user_id=1)

        mock_user_repository.destroy.assert_called_once_with(id=1, is_active=False)

    async def test_reactivate_user(self, mock_user_repository: Any, user_service: Any):
        expected_user = models.User(id=1, is_active=True)
        mock_user_repository.destroy.return_value = expected_user

        await user_service.reactivate_user(user_id=1)

        mock_user_repository.destroy.assert_called_once_with(id=1, is_active=True)
