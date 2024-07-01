from dataharvest.purifier.purifier import AutoPurifier
from dataharvest.spider.spider import AutoSpider


def test_auto_purifier():
    url = "https://zhuanlan.zhihu.com/p/369984873"
    auto_spider = AutoSpider()
    auto_purifier = AutoPurifier()
    doc = auto_spider.crawl(url)
    doc = auto_purifier.purify(doc)
    print(doc)
