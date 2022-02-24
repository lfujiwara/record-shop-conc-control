from abc import ABC, abstractmethod
from typing import Awaitable

from lea_record_shop.entities import Disc


class IDiscCrudRepository(ABC):

    @abstractmethod
    def save(self, disc: Disc) -> Awaitable[None]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Awaitable[Disc]:
        pass
