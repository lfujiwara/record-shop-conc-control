from json import dumps
from typing import Awaitable

from aiopg import connection as pg_connection

from lea_record_shop.entities import PurchaseOrder
from lea_record_shop.services.purchase_order_service import IPurchaseOrderRepository


class PurchaseOrderRepositoryPostgresql(IPurchaseOrderRepository):
    _connection: pg_connection

    def __init__(self, _connection: pg_connection):
        self._connection = _connection

    async def save(self, purchase_order: PurchaseOrder) -> Awaitable[None]:
        async with self._connection.cursor() as cursor:
            await cursor.execute(
                """INSERT INTO purchase_orders 
                (id, disc_id, customer_id, quantity, timestamp, customer_json, disc_json)
                VALUES 
                (%(id)s, %(disc_id)s, %(customer_id)s, %(quantity)s, %(timestamp)s, %(customer_json)s, %(disc_json)s)""",
                {
                    "id": purchase_order.id,
                    "disc_id": purchase_order.disc.id,
                    "customer_id": purchase_order.customer.id,
                    "quantity": purchase_order.quantity,
                    "timestamp": purchase_order.timestamp.isoformat(),
                    "customer_json": dumps(purchase_order.customer.to_json()),
                    "disc_json": dumps(purchase_order.disc.to_json()),
                }
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()