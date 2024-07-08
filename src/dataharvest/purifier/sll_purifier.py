import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class SllPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.single_line_break = True

    def match(self, url: str) -> bool:
        return "www.360doc.com/content/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗无用标签
        selector.xpath("//i[@id='ArticleReadingBtn']").drop()

        h1_title_label = selector.xpath("//h1[@id='titiletext']").get()
        h1_title = self.convertor.handle(h1_title_label)

        art_content_str = ""

        art_content_list = selector.xpath("//td[@id='artContent']/*").getall()
        for content_item in art_content_list:
            print(content_item)
            art_content_str += content_item

        content_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", art_content_str)
        content = self.convertor.handle(content_label_replaced)

        clean_data = h1_title + content

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
