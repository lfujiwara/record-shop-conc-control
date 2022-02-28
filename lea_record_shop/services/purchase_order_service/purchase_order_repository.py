from abc import ABC, abstractmethod
from typing import Awaitable

from lea_record_shop.entities import PurchaseOrder


class IPurchaseOrderRepository(ABC):

    @abstractmethod
    def save(self, purchase_order: PurchaseOrder) -> Awaitable[None]:
        pass
