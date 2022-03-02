from json import dumps
from typing import Awaitable

from asyncpg import Connection

from lea_record_shop.entities import PurchaseOrder
from lea_record_shop.services.purchase_order_service import IPurchaseOrderRepository


class PurchaseOrderRepositoryPostgresql(IPurchaseOrderRepository):
    _connection: Connection

    def __init__(self, _connection: Connection):
        self._connection = _connection

    async def save(self, purchase_order: PurchaseOrder) -> Awaitable[None]:
        query = """INSERT INTO purchase_orders
                (id, disc_id, customer_id, quantity, timestamp, customer_json, disc_json)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """
        args = (str(purchase_order.id), str(purchase_order.disc.id),
                str(purchase_order.customer.id), purchase_order.quantity,
                purchase_order.timestamp, dumps(purchase_order.customer.to_json()),
                dumps(purchase_order.disc.to_json()))
        await self._connection.execute(query, *args)
