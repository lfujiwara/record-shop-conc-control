from os import environ

import aiopg

from lea_record_shop.services.customer_service import CustomerService
from lea_record_shop.services.disc_crud import DiscCrud
from lea_record_shop_extensions.deps.customer_service_repository_postgresql import CustomerServiceRepositoryPostgresql
from lea_record_shop_extensions.deps.disc_crud_repository_postgresql import DiscCrudRepositoryPostgresql

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


async def inject_disc_crud() -> DiscCrud:
    print('injecting disc crud')
    # any alternatives to this? (anext)
    pool = await _get_pool.__anext__()
    conn = await pool.acquire()
    return DiscCrud(DiscCrudRepositoryPostgresql(conn))


async def inject_customer_service() -> CustomerService:
    print('injecting customer service')
    pool = await _get_pool.__anext__()
    conn = await pool.acquire()
    return CustomerService(CustomerServiceRepositoryPostgresql(conn))
