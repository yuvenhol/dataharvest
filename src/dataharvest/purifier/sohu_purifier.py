import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class SohuPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()

    def match(self, url: str) -> bool:
        return "www.sohu.com/a/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗无用的标签
        selector.xpath("//a[@id='backsohucom']").drop()
        selector.xpath("//p[@data-role='editor-name']").drop()

        # 标题
        title_label = selector.xpath("//div[@class='text-title']/h1").get()
        title = self.convertor.handle(title_label)

        # 正文
        article_label = selector.xpath("//article[@id='mp-editor']").get()

        article_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", article_label)

        article = self.convertor.handle(article_label_replaced)

        clean_data = title + article

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
