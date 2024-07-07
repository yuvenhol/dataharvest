import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class WangYiPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return re.match(r"^.+?www.163.com/\w+/article/.+", url) is not None

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗无用标签
        selector.xpath(
            "//div[@class='post_body']/div[@style='height: 0px;overflow:hidden;']"
        ).drop()

        # 标题
        title_label = selector.xpath("//h1[@class='post_title']").get()
        title = self.convertor.handle(title_label)

        # 内容
        content_label = selector.xpath("//div[@class='post_body']").get()
        content_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", content_label)

        content = self.convertor.handle(content_label_replaced)

        clean_data = title + content

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
