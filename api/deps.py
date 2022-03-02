from os import environ
from typing import Awaitable, AsyncGenerator

import asyncpg
from asyncpg import Pool
from fastapi import Depends

from lea_record_shop.services.customer_service import CustomerService
from lea_record_shop.services.disc_crud import DiscCrud
from lea_record_shop.services.purchase_order_service import PurchaseOrderService
from lea_record_shop_extensions.deps.customer_service_repository_postgresql import CustomerServiceRepositoryPostgresql
from lea_record_shop_extensions.deps.disc_crud_repository_postgresql import DiscCrudRepositoryPostgresql
from lea_record_shop_extensions.deps.purchase_order_repository_postgresql import PurchaseOrderRepositoryPostgresql
from lea_record_shop_extensions.deps.unit_of_work_optimistic_postgresql import UnitOfWorkOptimisticPostgresql
from lea_record_shop_extensions.deps.unit_of_work_pessimistic_postgresql import UnitOfWorkPessimisticPostgresql

DB_CONFIG = {'host': environ.get('POSTGRES_HOST', 'localhost'), 'port': int(environ.get('POSTGRES_PORT', 5432)),
             'user': environ.get('POSTGRES_USER', 'postgres'), 'password': environ.get('POSTGRES_PASSWORD', 'postgres'),
             'database': environ.get('POSTGRES_DB', 'postgres'), 'schema': environ.get('POSTGRES_SCHEMA', 'public')}

USE_OPTIMISTIC_CC = environ.get('USE_OPTIMISTIC_CC', 'false') == 'true'


async def get_pool() -> AsyncGenerator:
    async with asyncpg.create_pool(host=DB_CONFIG['host'], port=DB_CONFIG['port'], user=DB_CONFIG['user'],
                                   password=DB_CONFIG['password'], database=DB_CONFIG['database'],
                                   server_settings={'search_path': DB_CONFIG['schema']}, min_size=1,
                                   max_size=5) as pool:
        try:
            yield pool
        finally:
            await pool.close()


async def inject_disc_crud(pool: Pool = Depends(get_pool)) -> Awaitable[DiscCrud]:
    try:
        conn = await pool.acquire(timeout=30)
        return DiscCrud(DiscCrudRepositoryPostgresql(conn))
    finally:
        await pool.release(conn)


async def inject_customer_service(pool: Pool = Depends(get_pool)) -> Awaitable[CustomerService]:
    try:
        conn = await pool.acquire(timeout=30)
        return CustomerService(CustomerServiceRepositoryPostgresql(conn))
    finally:
        await pool.release(conn)


async def inject_purchase_order_service(pool: Pool = Depends(get_pool)) -> Awaitable[PurchaseOrderService]:
    conn = await pool.acquire(timeout=30)

    try:
        purchase_order_repository = PurchaseOrderRepositoryPostgresql(conn)
        customer_repository = CustomerServiceRepositoryPostgresql(conn)
        disc_repository = DiscCrudRepositoryPostgresql(conn, not USE_OPTIMISTIC_CC)
        uow = UnitOfWorkPessimisticPostgresql(conn) if not USE_OPTIMISTIC_CC else UnitOfWorkOptimisticPostgresql(conn)

        yield PurchaseOrderService(
            uow, purchase_order_repository, customer_repository, disc_repository
        )
    finally:
        await pool.release(conn)
