# test/unit/app/models/employee/test_employee_model.py

from collections import namedtuple
from unittest.mock import MagicMock

from app.models.employee.employee import Employee
from app.schemas.pagination import PaginationParams


def test_list_employees():
    db_mock = MagicMock()

    FakeRow = namedtuple('FakeRow', ['id', 'username', 'name', 'password'])
    fake_row = FakeRow(1, 'Carlos', 'Silva', '1234')

    db_mock.execute.return_value.fetchall.return_value = [fake_row]
    db_mock.execute.return_value.scalar.return_value = 1

    pagination = PaginationParams(
        current_page=1, rows_per_page=10, order_by='id', sort_by='asc'
    )

    employees, metadata = Employee.list_employees(pagination, db_mock)
    assert employees[0]['col_1'] == 'Carlos'
