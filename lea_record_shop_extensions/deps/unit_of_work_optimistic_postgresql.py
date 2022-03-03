from typing import Optional

from asyncpg import Connection
from asyncpg.transaction import Transaction

from lea_record_shop.services.purchase_order_service import IUnitOfWork


class UnitOfWorkOptimisticPostgresql(IUnitOfWork):
    _connection: Connection
    _tr: Optional[Transaction]

    def __init__(self, _connection: Connection):
        self._connection = _connection
        self._tr = None

    async def begin(self) -> None:
        self._tr = self._connection.transaction(isolation='repeatable_read')
        await self._tr.start()

    async def complete(self) -> None:
        await self._tr.commit()

    async def reset(self) -> None:
        await self._tr.rollback()
