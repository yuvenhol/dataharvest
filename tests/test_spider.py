import pytest

from dataharvest.spider.common_spider import CommonSpider
from dataharvest.spider import AutoSpider
from dataharvest.spider import XiaoHongShuSpider


def test_common_spider():
    spider = CommonSpider()
    doc = spider.crawl(
        "https://baike.baidu.com/item/%E9%87%91%E7%BC%95%E7%8E%89%E8%A1%A3/617831?fr=ge_ala"
    )
    print(doc)


def test_auto_spider():
    spider = AutoSpider()
    doc = spider.crawl(
        "https://baike.baidu.com/item/%E9%87%91%E7%BC%95%E7%8E%89%E8%A1%A3/617831?fr=ge_ala"
    )
    print(doc)


@pytest.mark.asyncio
async def test_async_common_spider():
    spider = AutoSpider()
    doc = await spider.a_crawl(
        "http://www.360doc.com/content/24/0102/21/9087553_1109645045.shtml"
    )
    print(doc)
    print(doc.page_content)


def test_xhs_spider():
    spider = XiaoHongShuSpider()
    doc = spider.crawl(
        "https://www.xiaohongshu.com/discovery/item/645da5ac0000000013031f93"
    )
    print(doc)
