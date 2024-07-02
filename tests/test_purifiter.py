from dataharvest.purifier.purifier import AutoPurifier
from dataharvest.spider.spider import AutoSpider


def test_auto_purifier():
    url = "https://zhuanlan.zhihu.com/p/369984873"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_sohu():
    url = "https://www.sohu.com/a/325718406_120013344"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_sll():
    url = "http://www.360doc.com/content/23/0613/11/72042116_1084562587.shtml"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_baijiahao():
    url = "https://baijiahao.baidu.com/s?id=1800439094856373024"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_wangyi():
    url = "https://www.163.com/auto/article/J6361L350008856R.html?clickfrom=w_lb_4_big"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_sogoubaike():
    url = "https://baike.sogou.com/v63038718.htm"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)