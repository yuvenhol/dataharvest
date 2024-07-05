from abc import ABC, abstractmethod

from dataharvest.schema import Document


class BaseSpider(ABC):
    index = 0

    @abstractmethod
    def match(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def crawl(self, url: str) -> Document:
        raise NotImplementedError

    @abstractmethod
    async def a_crawl(self, url: str) -> Document:
        raise NotImplementedError
