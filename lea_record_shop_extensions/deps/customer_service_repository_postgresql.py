from typing import Awaitable

from aiopg import connection as pg_connection

from lea_record_shop.entities import Customer
from lea_record_shop.services.customer_service.customer_service_repository import ICustomerServiceRepository


class CustomerServiceRepositoryPostgresql(ICustomerServiceRepository):
    _connection: pg_connection

    def __init__(self, _connection: pg_connection):
        self._connection = _connection

    async def save(self, customer: Customer) -> Awaitable[None]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute(
                """
                INSERT INTO customers (
                    id, document, name, birth_date, email, phone, is_active)
                VALUES (
                    %(id)s, %(document)s, %(name)s, %(birth_date)s, %(email)s, %(phone)s, %(is_active)s)
                """,
                customer.__dict__)

    async def get_by_id(self, _id: str) -> Awaitable[Customer]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute(
                """
                SELECT id as _id, document, name, birth_date, email, phone, is_active
                FROM customers
                WHERE id = %(id)s
                """,
                {'id': _id})

            # get column names
            column_names = [desc[0] for desc in _cursor.description]
            # get row data
            row = await _cursor.fetchone()

        if not row:
            return None
        # transform row data to dict
        row_dict = dict(zip(column_names, row))
        return Customer(**row_dict)

    async def update(self, customer: Customer) -> Awaitable[bool]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute(
                """
                UPDATE customers
                SET document = %(document)s, name = %(name)s, birth_date = %(birth_date)s, email = %(email)s, phone = %(phone)s, is_active = %(is_active)s
                WHERE id = %(id)s
                RETURNING id
                """,
                customer.__dict__)

            row_count = _cursor.rowcount

        return row_count > 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
