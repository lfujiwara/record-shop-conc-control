from typing import Optional

from asyncpg import Connection
from asyncpg.transaction import Transaction

from lea_record_shop.services.purchase_order_service import IUnitOfWork


class UnitOfWorkPessimisticPostgresql(IUnitOfWork):
    _connection: Connection
    _tr: Optional[Transaction]

    def __init__(self, _connection: Connection):
        self._connection = _connection
        self._tr = None

    async def begin(self) -> None:
        self._tr = self._connection.transaction(isolation='read_committed')
        await self._tr.start()

    async def complete(self) -> None:
        if self._tr is not None:
            await self._tr.commit()
            self._tr = None

    async def reset(self) -> None:
        if self._tr is not None:
            await self._tr.rollback()
            self._tr = None
