from typing import Awaitable

from aiopg import connection as pg_connection

from lea_record_shop.services.purchase_order_service import IUnitOfWork


class UnitOfWorkOptimisticPostgresql(IUnitOfWork):
    _connection: pg_connection

    def __init__(self, _connection: pg_connection, dispose_conn):
        self._connection = _connection
        self.dispose_conn = dispose_conn

    async def begin(self) -> Awaitable[None]:
        async with self._connection.cursor() as cursor:
            await cursor.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ")

    async def complete(self) -> Awaitable[None]:
        async with self._connection.cursor() as cursor:
            await cursor.execute("COMMIT")

    async def reset(self) -> Awaitable[None]:
        async with self._connection.cursor() as cursor:
            await cursor.execute("ROLLBACK")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose_conn()
