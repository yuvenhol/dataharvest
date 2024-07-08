import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class WechatPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "weixin.qq.com/s/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清洗无用标签
        selector.xpath("//section[@class='mp_profile_iframe_wrp']").drop()

        # 标题
        title_label = selector.xpath("//h1[@id='activity-name']").get()
        title = self.convertor.handle(title_label)

        # 内容
        content_label = selector.xpath("//div[@id='js_content']").get()
        content_label_replaced = re.sub(r"<img\b[^>]*?>", "[图片]", content_label)

        content = self.convertor.handle(content_label_replaced)

        return Document(
            url=doc.url, metadata={**doc.metadata}, page_content=title + content
        )
