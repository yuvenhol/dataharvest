import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class QQNewPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "new.qq.com/rain/a/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗标签
        selector.xpath("//div[@class='videoPlayer']").drop()
        selector.xpath("//div[@class='qnt-link-list']").drop()

        # 标题
        title_label = selector.xpath("//div[@class='content-article']/h1").get()
        title = self.convertor.handle(title_label)

        # 内容
        content_label = selector.xpath(
            "//div[starts-with(@class, 'article-content-wrap')]"
        ).get()
        content_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", content_label)

        content = self.convertor.handle(content_label_replaced)

        return Document(
            url=doc.url, metadata={**doc.metadata}, page_content=title + content
        )
