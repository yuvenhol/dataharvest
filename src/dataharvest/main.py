import asyncio

from dataharvest.base import DataHarvest
from dataharvest.searcher import TavilySearcher

searcher = TavilySearcher()
dh = DataHarvest()
r = searcher.search("战国水晶杯")
tasks = [dh.a_crawl_and_purify(item.url) for item in r.items]
loop = asyncio.get_event_loop()
docs = loop.run_until_complete(asyncio.gather(*tasks))
print(docs)
