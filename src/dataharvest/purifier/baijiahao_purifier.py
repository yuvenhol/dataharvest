import re

from dataharvest.base import Document
from dataharvest.purifier.purifier import BasePurifier
import html2text
from parsel import Selector


class BaiJiaHaoPurifier(BasePurifier):

    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "baijiahao.baidu.com/s" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗无用标签
        selector.xpath("//span[@data-testid='report-btn']").drop()

        title_text = selector.xpath("//div[@id='header']/div/text()").get()
        title = f"# {title_text}\n\n"

        content_label = selector.xpath("//div[@data-testid='article']").get()
        content_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", content_label)

        content = self.convertor.handle(content_label_replaced)

        clean_data = title + content

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
