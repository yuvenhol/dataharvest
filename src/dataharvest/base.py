from dataharvest.purifier import AutoPurifier
from dataharvest.schema import Document
from dataharvest.spider import AutoSpider


class DataHarvest:
    def __init__(self):
        self.spider = AutoSpider()
        self.purifier = AutoPurifier()

    async def a_crawl_and_purify(self, url) -> Document:
        doc = await self.spider.a_crawl(url)
        return self.purifier.purify(doc)

    def crawl_and_purify(self, url) -> Document:
        doc = self.spider.crawl(url)
        return self.purifier.purify(doc)
