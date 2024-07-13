from dataharvest.purifier import AutoPurifier
from dataharvest.spider import AutoSpider


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
    print(doc)
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


def test_auto_purifier_bilibili():
    url = "https://www.bilibili.com/read/cv35655718/?from=category_0&jump_opus=1"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_qqnew():
    url = "https://new.qq.com/rain/a/20240703A09D9300"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_sobaike():
    url = "https://baike.so.com/doc/5579340-5792710.html?src=index#entry_concern"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    print(doc)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_toutiao():
    url = "https://www.toutiao.com/article/7386866265849168419/?log_from=e75b95143ac23_1720001882524"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_wechat():
    url = "https://mp.weixin.qq.com/s/g7WfEc5UxAi3aMyDmwQnow"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)


def test_auto_purifier_xiaohongshu():
    url = "https://www.xiaohongshu.com/explore/64ca1b73000000000b028dd2"
    auto_spider = AutoSpider()
    doc = auto_spider.crawl(url)
    auto_purifier = AutoPurifier()
    doc = auto_purifier.purify(doc)
    print(doc)
