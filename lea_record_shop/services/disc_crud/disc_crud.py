from copy import copy
from typing import Optional
from uuid import uuid4

import lea_record_shop.services.disc_crud.disc_crud_exceptions as disc_crud_exceptions
from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto, GetDiscsResponseDto, UpdateDiscRequestDto
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository
from lea_record_shop.services.disc_crud.dto import CreateDiscRequestDto, DiscDto

QUERY_HARD_LIMIT = 100


def _serialize_disc_to_dto(disc: Disc) -> DiscDto:
    return DiscDto(_id=disc.id, name=disc.name, artist=disc.artist, year_of_release=disc.year_of_release,
                   genre=disc.genre, quantity=disc.quantity)


class DiscCrud:
    """
    Encapsulates the CRUD operations for the Disc model, as simple as possible.
    Performs validation of DTOs, instantiates the model and delegates the
    persistence operations to repository (or whatever name you want to call it).
    """

    disc_crud_repository: IDiscCrudRepository

    def __init__(self, disc_crud_repository: IDiscCrudRepository):
        self.disc_crud_repository = disc_crud_repository

    async def create_disc(self, data: CreateDiscRequestDto) -> DiscDto:
        # Do validation
        # ...

        # Instantiate
        disc = Disc(_id=str(uuid4()), name=data.name, artist=data.artist, year_of_release=data.year_of_release,
                    genre=data.genre, quantity=data.quantity)
        # ...

        # Persist
        # yeah, a lot of try/excepts, the reason for this
        # is to properly report when an error happens outside
        # the application layer (e.g. one of it's providers/deps)
        # and type them properly, maybe there's a better way to do this (?)
        try:
            await self.disc_crud_repository.save(disc)
        except Exception as e:
            raise disc_crud_exceptions.ProviderException(e)
        # ...

        return _serialize_disc_to_dto(disc)

    async def get_disc(self, _id: str) -> Optional[DiscDto]:
        try:
            disc = await self.disc_crud_repository.get_by_id(_id)
        except Exception as e:
            raise disc_crud_exceptions.ProviderException(e)

        if disc is None:
            return None
        return _serialize_disc_to_dto(disc)

    async def get_discs(self, _params: GetDiscsRequestDto = GetDiscsRequestDto()) -> GetDiscsResponseDto:
        params = copy(_params)
        params.limit = min(params.limit, QUERY_HARD_LIMIT)

        try:
            data = await self.disc_crud_repository.get(params)
        except Exception as e:
            raise disc_crud_exceptions.ProviderException(e)

        response = GetDiscsResponseDto()
        response.params = params
        response.limit = params.limit
        response.offset = params.offset
        response.data = data

        return response

    async def update_disc(self, data: UpdateDiscRequestDto) -> DiscDto:
        # Check if disc exists
        try:
            disc = await self.disc_crud_repository.get_by_id(data.id)
        except Exception as e:
            raise disc_crud_exceptions.ProviderException(e)
        if disc is None:
            raise disc_crud_exceptions.RequestedDiscNotFound(data.id)

        # Validation...
        # ...

        # Update
        disc.name = data.name if data.name is not None else disc.name
        disc.artist = data.artist if data.artist is not None else disc.artist
        disc.year_of_release = data.year_of_release if data.year_of_release is not None else disc.year_of_release
        disc.genre = data.genre if data.genre is not None else disc.genre
        disc.quantity = data.quantity if data.quantity is not None else disc.quantity
        # ...

        # Persist
        await self.disc_crud_repository.update(disc)
        # ...

        return _serialize_disc_to_dto(disc)

    async def delete_disc(self, _id: str) -> None:
        try:
            deleted = await self.disc_crud_repository.delete(_id)
        except Exception as e:
            raise disc_crud_exceptions.ProviderException(e)

        if not deleted:
            raise disc_crud_exceptions.RequestedDiscNotFound(_id)
        return None
