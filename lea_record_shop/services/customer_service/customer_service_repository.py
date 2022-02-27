from abc import ABC, abstractmethod
from typing import Awaitable

from lea_record_shop.entities import Customer


class ICustomerServiceRepository(ABC):

    @abstractmethod
    def save(self, customer: Customer) -> Awaitable[None]:
        pass

    @abstractmethod
    def get_by_id(self, _id: str) -> Awaitable[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Awaitable[bool]:
        pass
