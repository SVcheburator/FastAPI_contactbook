import unittest
import sys
from datetime import date
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

sys.path.append('../')
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_user(self):
        body = UserModel(username="test_name",
                         email="test_email@gmail.com",
                         password="password")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)

    async def test_get_user_by_email(self):
        user = User(email="test_email@gmail.com")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test_email@gmail.com", db=self.session)
        self.assertEqual(result, user)

    async def test_update_avatar(self):
        user = User(email="test_email@gmail.com")
        self.session.query().filter().first.return_value = user
        test_url = "Test_url"
        result = await update_avatar(email=user.email, url=test_url, db=self.session)
        self.assertEqual(user, result)


if __name__ == '__main__':
    unittest.main()