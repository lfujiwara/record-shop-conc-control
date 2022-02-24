from typing import Awaitable
from uuid import uuid4

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto, GetDiscsResponseDto
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository
from lea_record_shop.services.disc_crud.dto import CreateDiscRequestDto, DiscDto

QUERY_HARD_LIMIT = 100


def _serialize_disc_to_dto(disc: Disc) -> DiscDto:
    return DiscDto(id=disc.id, name=disc.name, artist=disc.artist, year_of_release=disc.year_of_release,
                   genre=disc.genre, quantity=disc.quantity)


class DiscCrud():
    """
    Encapsulates the CRUD operations for the Disc model, as simple as possible.
    Performs validation of DTOs, instantiates the model and delegates the
    persistence operations to repository (or whatever name you want to call it).
    """

    disc_crud_repository: IDiscCrudRepository

    def __init__(self, disc_crud_repository: IDiscCrudRepository):
        self.disc_crud_repository = disc_crud_repository

    async def create_disc(self, data: CreateDiscRequestDto) -> Awaitable[DiscDto]:
        # Do validation
        # ...

        # Instantiate
        disc = Disc(id=str(uuid4()), name=data.name, artist=data.name, year_of_release=data.year_of_release,
                    genre=data.genre, quantity=data.quantity)
        # ...

        # Persist
        await self.disc_crud_repository.save(disc)
        # ...

        return _serialize_disc_to_dto(disc)

    async def get_disc(self, _id: str) -> DiscDto:
        disc = await self.disc_crud_repository.get_by_id(_id)
        if disc is None:
            return None
        return _serialize_disc_to_dto(disc)

    async def get_discs(self, params: GetDiscsRequestDto = GetDiscsRequestDto()) -> Awaitable[GetDiscsResponseDto]:
        params.limit = min(params.limit, QUERY_HARD_LIMIT)

        data = await self.disc_crud_repository.get(params)

        response = GetDiscsResponseDto()
        response.params = params
        response.limit = params.limit
        response.offset = params.offset
        response.data = data

        return response
