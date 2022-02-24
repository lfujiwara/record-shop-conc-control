from lea_record_shop.services.disc_crud.impl import DiscCrudRepositoryInMemory
from lea_record_shop.services.disc_crud import DiscCrud


async def deps() -> DiscCrud:
    return DiscCrud(DiscCrudRepositoryInMemory())