# DataHarvest

DataHarvest 是一个用于数据搜索🔍、爬取🕷、清洗🧽的工具。

AI时代，数据是一切的基石，DataHarvest 能够帮助获取干净有效的数据。

![DataHarvest](https://yuvenhol-1255563050.cos.ap-beijing.myqcloud.com/img/202407022046608.png)

## 搜索

| 搜索引擎   | 官网                       | 支持          |
|--------|--------------------------|-------------|
| tavily | https://docs.tavily.com/ | ✅           |
| 天工     | https://www.tiangong.cn/ | coming soon |

## 数据爬取&清洗

| 网站       | 内容 | url pattern                | 爬取          | 清洗 |
|----------|----|----------------------------|-------------|----|
| 百度百科     | 词条 | baike.baidu.com/item/      | ✅           | ✅  |
| 百度百家号    | 文章 | baijiahao.baidu.com/s/     | ✅           | ✅  |
| B站       | 文章 | www.bilibili.com/read/     | ✅           | ✅  |
| 腾讯网      | 文章 | new.qq.com/rain/a/         | ✅           | ✅  |
| 360个人图书馆 | 文章 | www.360doc.com/content/    | ✅           | ✅  |
| 360百科    | 词条 | baike.so.com/doc/          | ✅           | ✅  |
| 搜狗百科     | 词条 | baike.sogou.com/v/         | ✅           | ✅  |
| 搜狐       | 文章 | www.sohu.com/a/            | ✅           | ✅  |
| 头条       | 文章 | www.toutiao.com/article/   | ✅           | ✅  |
| 网易       | 文章 | www.163.com/\w+/article/.+ | ✅           | ✅  |
| 微信公众号    | 文章 | weixin.qq.com/s/           | ✅           | ✅  |
| 马蜂窝      | 文章 | www.mafengwo.cn/i/                  | ✅ |    |
| 小红书      |    |                            | coming soon |    |

其他情况使用基础playwright数据爬取和html2text数据清洗，但并未做特殊适配。

## 安装与使用

```shell
pip install dataharvest
playwright install
```

## 最佳实践

### 搜索

```python
from dataharvest.searcher import TavilySearcher

api_key = "xxx"  # 或者设置环境变量 TAVILY_API_KEY

searcher = TavilySearcher(api_key)
searcher.search("战国水晶杯")
```

```
SearchResult(keyword='战国水晶杯', answer=None, images=None, items=[
    SearchResultItem(title='战国水晶杯_百度百科', url='https://baike.baidu.com/item/战国水晶杯/7041521', score=0.98661,
                     description='战国水晶杯为战国晚期水晶器皿，于1990年出土于浙江省杭州市半山镇石塘村，现藏于杭州博物馆。战国水晶杯高15.4厘米、口径7.8厘米、底径5.4厘米，整器略带淡琥珀色，局部可见絮状包裹体；器身为敞口，平唇，斜直壁，圆底，圈足外撇；光素无纹，造型简洁。',
                     content='')])
```

### 爬虫

```python
from dataharvest.spider import AutoSpider

url = "https://baike.so.com/doc/5579340-5792710.html?src=index#entry_concern"
auto_spider = AutoSpider()
doc = auto_spider.crawl(url)
print(doc)
```

### 清洗

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

效果：
![](https://yuvenhol-1255563050.cos.ap-beijing.myqcloud.com/img/202407052255246.png)

### 整合

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

## 鸣谢

伙伴们如果觉着这个项目对你有帮助，那么请帮助点一个star✨。如果觉着存在问题或者有其他需求，那么欢迎在issue提出。当然，我们非常欢迎您加入帮忙完善。