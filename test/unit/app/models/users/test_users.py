# test/unit/app/models/users/test_users.py

from collections import namedtuple
from unittest.mock import MagicMock

from app.models.users.users import User
from app.schemas.pagination import PaginationParams


def test_list_users_mocked():
    db_mock = MagicMock()

    FakeRow = namedtuple("FakeRow", ["id", "username", "name", "password"])
    fake_row = FakeRow(1, "Carlos", "Silva", "1234")

    db_mock.execute.return_value.fetchall.return_value = [fake_row]
    db_mock.execute.return_value.scalar.return_value = 1

    pagination = PaginationParams(
        current_page=1, rows_per_page=10, order_by="id", sort_by="asc"
    )

    users, metadata = User.list_users(pagination, db_mock)
    print(users)
    assert users[0]["col_1"] == "Carlos"
