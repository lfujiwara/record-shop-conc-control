from os import environ
from typing import Awaitable

import aiopg

from lea_record_shop.services.customer_service import CustomerService
from lea_record_shop.services.disc_crud import DiscCrud
from lea_record_shop.services.purchase_order_service import PurchaseOrderService
from lea_record_shop_extensions.deps.customer_service_repository_postgresql import CustomerServiceRepositoryPostgresql
from lea_record_shop_extensions.deps.disc_crud_repository_postgresql import DiscCrudRepositoryPostgresql
from lea_record_shop_extensions.deps.purchase_order_repository_postgresql import PurchaseOrderRepositoryPostgresql
from lea_record_shop_extensions.deps.unit_of_work_optimistic_postgresql import UnitOfWorkOptimisticPostgresql

DB_CONFIG = {'host': environ.get('POSTGRES_HOST', 'localhost'), 'port': int(environ.get('POSTGRES_PORT', 5432)),
             'user': environ.get('POSTGRES_USER', 'postgres'), 'password': environ.get('POSTGRES_PASSWORD', 'postgres'),
             'database': environ.get('POSTGRES_DB', 'postgres'), 'schema': environ.get('POSTGRES_SCHEMA', 'public')}


async def _pool_gen():
    """
    Returns the latest pool created, if there is one,
    otherwise creates a new one.
    """
    pool = None
    while True:
        if pool is None:
            pool = await aiopg.create_pool(host=DB_CONFIG['host'], port=DB_CONFIG['port'], user=DB_CONFIG['user'],
                                           password=DB_CONFIG['password'], dbname=DB_CONFIG['database'],
                                           options=f'-c search_path={DB_CONFIG["schema"]}')
        yield pool


_get_pool = _pool_gen()


async def inject_disc_crud() -> Awaitable[DiscCrud]:
    # any alternatives to this? (anext)
    pool = await _get_pool.__anext__()
    conn = await pool.acquire()
    return DiscCrud(DiscCrudRepositoryPostgresql(conn))


async def inject_customer_service() -> Awaitable[CustomerService]:
    pool = await _get_pool.__anext__()
    conn = await pool.acquire()
    return CustomerService(CustomerServiceRepositoryPostgresql(conn))


async def inject_purchase_order_service() -> Awaitable[PurchaseOrderService]:
    pool = await _get_pool.__anext__()
    conn = await pool.acquire()

    uow = UnitOfWorkOptimisticPostgresql(conn, lambda _: pool.release(conn))
    purchase_order_repository = PurchaseOrderRepositoryPostgresql(conn)
    customer_repository = CustomerServiceRepositoryPostgresql(conn)
    disc_repository = DiscCrudRepositoryPostgresql(conn)

    return PurchaseOrderService(
        uow, purchase_order_repository, customer_repository, disc_repository
    )
