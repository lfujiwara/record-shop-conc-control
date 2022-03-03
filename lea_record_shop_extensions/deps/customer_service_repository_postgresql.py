from typing import Optional

from asyncpg import Connection

from lea_record_shop.entities import Customer
from lea_record_shop.services.customer_service.customer_service_repository import ICustomerServiceRepository


class CustomerServiceRepositoryPostgresql(ICustomerServiceRepository):
    _connection: Connection

    def __init__(self, _connection: Connection):
        self._connection = _connection

    async def save(self, customer: Customer):
        query = """
                INSERT INTO customers (
                    id, document, name, birth_date, email, phone, is_active)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """
        await self._connection.execute(query, customer.id, customer.document, customer.name, customer.birth_date,
                                       customer.email, customer.phone, customer.is_active)

    async def get_by_id(self, _id: str) -> Optional[Customer]:
        query = """
                SELECT id as _id, document, name, birth_date, email, phone, is_active
                FROM customers
                WHERE id = $1
                """
        result = await self._connection.fetchrow(query, _id)
        if not result:
            return None  # Union type not supported yet
        return Customer(*result)

    async def update(self, customer: Customer) -> bool:
        query = """
                UPDATE customers
                SET document = $1, name = $2, birth_date = $3, email = $4, phone = $5, is_active = $6
                WHERE id = $7
                RETURNING id
                """
        result = await self._connection.fetch(query, customer.document, customer.name, customer.birth_date,
                                              customer.email, customer.phone, customer.is_active, customer.id)

        return len(result) > 0
