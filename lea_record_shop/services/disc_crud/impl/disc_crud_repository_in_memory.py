from typing import Awaitable, List

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository


class DiscCrudRepositoryInMemory(IDiscCrudRepository):
    discs = {}

    async def save(self, disc: Disc) -> Awaitable[None]:
        self.discs[disc.id] = disc

    async def get_by_id(self, id: str) -> Awaitable[Disc]:
        return self.discs.get(id, None)

    async def get(self, params: GetDiscsRequestDto) -> Awaitable[List[Disc]]:
        response = []

        print(params.offset, params.limit)
        for disc in list(self.discs.values())[params.offset:(params.offset + params.limit)]:
            if params.name_exact and disc.name != params.name_exact:
                continue
            if params.name and disc.name.find(params.name) == -1:
                continue
            if params.artist_exact and disc.artist != params.artist_exact:
                continue
            if params.artist and disc.artist.find(params.artist) == -1:
                continue
            if params.genre_exact and disc.genre != params.genre_exact:
                continue
            if params.genre and disc.genre.find(params.genre) == -1:
                continue
            if params.year_of_release_min and disc.price < params.year_of_release_min:
                continue
            if params.year_of_release_max and disc.price > params.year_of_release_max:
                continue

            response.append(disc)
        return response
