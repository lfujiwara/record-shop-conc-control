from typing import Awaitable

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository


class DiscCrudRepositoryInMemory(IDiscCrudRepository):
    discs = {}

    async def save(self, disc: Disc) -> Awaitable[None]:
        self.discs[disc.id] = disc

    async def get_by_id(self, id: str) -> Awaitable[Disc]:
        return self.discs.get(id, None)
