from abc import ABC, abstractmethod

from dataharvest.schema import Document


class BasePurifier(ABC):
    index = 0

    @abstractmethod
    def match(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def purify(self, doc: Document) -> Document:
        raise NotImplementedError
