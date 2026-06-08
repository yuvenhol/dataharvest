# DataHarvest

DataHarvest is a tool for data search 🔍, crawling 🕷, and cleaning 🧽.

In the AI era, data is the foundation of everything. DataHarvest helps you quickly obtain clean, usable data—ready to use out of the box with flexible configuration.

Beyond the tool itself, we also collect and organize technical solutions in our [wiki](https://github.com/yuvenhol/dataharvest/wiki).

![DataHarvest](https://yuvenhol-1255563050.cos.ap-beijing.myqcloud.com/img/202407022046608.png)


## Search Support

| Search Engine | Website                    | Supported |
|---------------|----------------------------|-----------|
| Tavily        | https://docs.tavily.com/   | ✅        |
| TianGong      | https://www.tiangong.cn/   | ✅        |

## Crawling & Cleaning Support

| Website              | Content Type | URL Pattern                | Crawl | Clean |
|----------------------|--------------|----------------------------|-------|-------|
| Baidu Baike          | Entry        | baike.baidu.com/item/      | ✅    | ✅    |
| Baidu Baijiahao      | Article      | baijiahao.baidu.com/s/     | ✅    | ✅    |
| Bilibili             | Article      | www.bilibili.com/read/     | ✅    | ✅    |
| Tencent News         | Article      | new.qq.com/rain/a/         | ✅    | ✅    |
| 360doc               | Article      | www.360doc.com/content/    | ✅    | ✅    |
| 360 Baike            | Entry        | baike.so.com/doc/          | ✅    | ✅    |
| Sogou Baike          | Entry        | baike.sogou.com/v/         | ✅    | ✅    |
| Sohu                 | Article      | www.sohu.com/a/            | ✅    | ✅    |
| Toutiao              | Article      | www.toutiao.com/article/   | ✅    | ✅    |
| NetEase              | Article      | www.163.com/\w+/article/.+ | ✅    | ✅    |
| WeChat Official Account | Article   | weixin.qq.com/s/           | ✅    | ✅    |
| Mafengwo             | Article      | www.mafengwo.cn/i/         | ✅    |       |
| Xiaohongshu (RED)    | Short-link post | /xhslink.com/           | ✅    | ✅    |

For other cases, basic Playwright crawling and html2text cleaning are used, but no special site-specific adaptation is provided.

## Installation

```shell
pip install dataharvest
playwright install
```

## Usage

**Note: It is recommended to use a virtual environment to avoid unnecessary issues.**

The project is divided into three main modules—search, spider, and data cleaning—which are independent of each other. You can use each module as needed.

Crawling and cleaning support automatic strategy matching based on URL. You only need to use `AutoSpider` and `AutoPurifier`.

## Best Practices

### Integration

Search + auto crawl + auto clean

```python
import asyncio

from dataharvest.base import DataHarvest
from dataharvest.searcher import TavilySearcher

searcher = TavilySearcher()
dh = DataHarvest()
r = searcher.search("战国水晶杯")
tasks = [dh.a_crawl_and_purify(item.url) for item in r.items]
loop = asyncio.get_event_loop()
docs = loop.run_until_complete(asyncio.gather(*tasks))
```

### Search

```python
from dataharvest.searcher import TavilySearcher

api_key = "xxx"  # or set the environment variable TAVILY_API_KEY

searcher = TavilySearcher(api_key)
searcher.search("战国水晶杯")
```

```
SearchResult(keyword='战国水晶杯', answer=None, images=None, items=[
    SearchResultItem(title='战国水晶杯_百度百科', url='https://baike.baidu.com/item/战国水晶杯/7041521', score=0.98661,
                     description='战国水晶杯为战国晚期水晶器皿，于1990年出土于浙江省杭州市半山镇石塘村，现藏于杭州博物馆。战国水晶杯高15.4厘米、口径7.8厘米、底径5.4厘米，整器略带淡琥珀色，局部可见絮状包裹体；器身为敞口，平唇，斜直壁，圆底，圈足外撇；光素无纹，造型简洁。',
                     content='')])
```

### Crawling

```python
from dataharvest.spider import AutoSpider

url = "https://baike.so.com/doc/5579340-5792710.html?src=index#entry_concern"
auto_spider = AutoSpider()
doc = auto_spider.crawl(url)
print(doc)
```

### Proxy

In many cases, you need to configure a proxy—for example, for Xiaohongshu and Mafengwo.
You need to implement a proxy generator class and define its `__call__` method.

You can pass the configuration when initializing the spider, or provide it at call time.

```python
from dataharvest.proxy.base import BaseProxy, Proxy
from dataharvest.spider import AutoSpider
from dataharvest.spider.base import SpiderConfig


class MyProxy(BaseProxy):

    def __call__(self) -> Proxy:
        return Proxy(protocol="http", host="127.0.0.1", port="53380", username="username", password="password")


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


```

### Cleaning

```python
from dataharvest.purifier import AutoPurifier
from dataharvest.spider import AutoSpider

url = "https://baike.so.com/doc/5579340-5792710.html?src=index#entry_concern"
auto_spider = AutoSpider()
doc = auto_spider.crawl(url)
print(doc)
auto_purifier = AutoPurifier()
doc = auto_purifier.purify(doc)
print(doc)
```

Example output:
![](https://yuvenhol-1255563050.cos.ap-beijing.myqcloud.com/img/202407052255246.png)

## Acknowledgments

If you find this project helpful, please give it a star ✨. If you encounter any issues or have other requirements, feel free to open an issue. We also welcome contributions to help improve the project. Contact: WeChat `yuvenhol02`

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=yuvenhol/dataharvest&type=Date)
