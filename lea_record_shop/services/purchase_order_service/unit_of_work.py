from abc import ABC, abstractmethod
from typing import Awaitable


class IUnitOfWork(ABC):

    @abstractmethod
    def begin(self) -> Awaitable[None]:
        pass

    @abstractmethod
    def complete(self) -> Awaitable[None]:
        pass

    @abstractmethod
    def reset(self) -> Awaitable[None]:
        pass
