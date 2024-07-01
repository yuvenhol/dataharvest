import html2text

from dataharvest.base import Document
from dataharvest.purifier.purifier import BasePurifier


class CommonPurifier(BasePurifier):
    index = 2 ** 16

    def __init__(self):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        self.converter = h

    def match(self, url: str) -> bool:
        return True

    def purify(self, doc: Document, converter=None, **kwargs) -> Document:
        if not converter:
            converter = self.converter

        page_content = converter.handle(doc.page_content)

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=page_content)