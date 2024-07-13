import copy
from typing import Optional

from dataharvest.schema import Document
from dataharvest.spider.base import BaseSpider, SpiderConfig


class AutoSpider:
    _spiders = []

    def __init__(self, config: SpiderConfig = SpiderConfig()):
        AutoSpider._spiders = [
            cls(copy.deepcopy(config)) for cls in BaseSpider.__subclasses__()
        ]
        AutoSpider._spiders.sort(key=lambda spider: spider._index)

    @classmethod
    def register(cls, spider: BaseSpider):
        AutoSpider._spiders.append(spider)
        AutoSpider._spiders.sort(key=lambda spider: spider._index)

    def _route(self, url: str) -> BaseSpider:
        for spider in self._spiders:
            if spider.match(url=url):
                return spider
        raise Exception(f"Cannot find spider for url: {url}")

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        spider = self._route(url)
        return spider.crawl(url, config)

    async def a_crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        spider = self._route(url)
        return await spider.a_crawl(url, config)
