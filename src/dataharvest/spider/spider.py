from dataharvest.schema import Document
from dataharvest.spider.base import BaseSpider


class AutoSpider:
    _spiders = []

    def __init__(self):
        AutoSpider._spiders = [cls() for cls in BaseSpider.__subclasses__()]
        AutoSpider._spiders.sort(key=lambda spider: spider.index)

    def _route(self, url: str) -> BaseSpider:
        for spider in self._spiders:
            if spider.match(url=url):
                return spider
        raise Exception(f"Cannot find spider for url: {url}")

    def crawl(self, url: str) -> Document:
        spider = self._route(url)
        return spider.crawl(url)

    async def a_crawl(self, url: str) -> Document:
        spider = self._route(url)
        return await spider.a_crawl(url)
