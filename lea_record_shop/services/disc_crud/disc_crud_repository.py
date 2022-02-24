from abc import ABC, abstractmethod
from typing import Awaitable, List

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto


class IDiscCrudRepository(ABC):

    @abstractmethod
    def save(self, disc: Disc) -> Awaitable[None]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Awaitable[Disc]:
        pass

    @abstractmethod
    def get(self, params: GetDiscsRequestDto) -> Awaitable[List[Disc]]:
        pass
