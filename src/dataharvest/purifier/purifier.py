from abc import ABC, abstractmethod

from dataharvest.base import Document


class BasePurifier(ABC):
    index = 0

    @abstractmethod
    def match(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def purify(self, doc: Document) -> Document:
        raise NotImplementedError


class AutoPurifier:
    _purifiers = []

    def __init__(self):
        AutoPurifier._purifiers = [cls() for cls in BasePurifier.__subclasses__()]
        AutoPurifier._purifiers.sort(key=lambda purifier: purifier.index)

    def _route(self, url: str) -> BasePurifier:
        for purifier in self._purifiers:
            if purifier.match(url):
                return purifier
        raise Exception(f"Cannot find purifier for url: {url}")

    def purify(self, doc: Document) -> Document:
        purifier = self._route(doc.url)
        return purifier.purify(doc)
