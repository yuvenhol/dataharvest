import random

from dataharvest.proxy.base import BaseProxy
from dataharvest.spider import AutoSpider
from dataharvest.spider.base import SpiderConfig


class MyProxy(BaseProxy):
    def __init__(self):
        self.proxies = ["http://127.0.0.1:53380"]

    def __call__(self) -> str:
        return random.choice(self.proxies)


def test_proxy_constructor():
    proxy_gene_func = MyProxy()
    auto_spider = AutoSpider(config=SpiderConfig(proxy_gene_func=proxy_gene_func))
    url = "https://baike.baidu.com/item/%E6%98%8E%E5%94%90%E5%AF%85%E3%80%8A%E7%81%8C%E6%9C%A8%E4%B8%9B%E7%AF%A0%E5%9B%BE%E8%BD%B4%E3%80%8B?fromModule=lemma_search-box"

    doc = auto_spider.crawl(url)
    print(doc)


def test_proxy_call():
    proxy_gene_func = MyProxy()
    auto_spider = AutoSpider()
    config = SpiderConfig(proxy_gene_func=proxy_gene_func)
    url = "https://baike.baidu.com/item/%E6%98%8E%E5%94%90%E5%AF%85%E3%80%8A%E7%81%8C%E6%9C%A8%E4%B8%9B%E7%AF%A0%E5%9B%BE%E8%BD%B4%E3%80%8B?fromModule=lemma_search-box"
    doc = auto_spider.crawl(url, config=config)
    print(doc)
