from dataharvest.spider.base import SpiderConfig
from dataharvest.spider.common_spider import CommonSpider
from dataharvest.spider.mafengwo_spider import MaFengWoSpider
from dataharvest.spider.spider import AutoSpider, BaseSpider
from dataharvest.spider.toutiao_spider import ToutiaoSpider

__all__ = [
    "AutoSpider",
    "CommonSpider",
    "BaseSpider",
    "ToutiaoSpider",
    "MaFengWoSpider",
    "SpiderConfig",
]
