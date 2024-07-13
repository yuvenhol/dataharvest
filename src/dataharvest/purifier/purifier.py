from dataharvest.purifier.base import BasePurifier
from dataharvest.schema import Document


class AutoPurifier:
    _purifiers = []

    def __init__(self):
        AutoPurifier._purifiers = [cls() for cls in BasePurifier.__subclasses__()]
        AutoPurifier._purifiers.sort(key=lambda purifier: purifier.index)

    @classmethod
    def register(cls, purifier: BasePurifier):
        AutoPurifier._purifiers.append(purifier)
        AutoPurifier._purifiers.sort(key=lambda purifier: purifier.index)

    def _route(self, url: str) -> BasePurifier:
        for purifier in self._purifiers:
            if purifier.match(url):
                return purifier
        raise Exception(f"Cannot find purifier for url: {url}")

    def purify(self, doc: Document) -> Document:
        purifier = self._route(doc.url)
        return purifier.purify(doc)
