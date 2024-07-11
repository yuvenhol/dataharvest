import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class XiaoHongShuPurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        # self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "www.xiaohongshu.com/explore/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 标题
        title_label = selector.xpath("//div[@id='detail-title']/text()").get()
        title = f"# {self.convertor.handle(title_label)}"

        # 文字
        desc_label = selector.xpath("//div[@id='detail-desc']").get()
        desc = self.convertor.handle(desc_label)

        # 图片
        img_label = selector.xpath("//div[@class='swiper-wrapper']")
        img_label.xpath("./div[@class='swiper-slide swiper-slide-duplicate swiper-slide-prev']").drop()
        img_label.xpath("./div[@class='swiper-slide swiper-slide-duplicate swiper-slide-duplicate-active']").drop()
        img = self.convertor.handle(img_label.get())

        return Document(
            url=doc.url, metadata={**doc.metadata}, page_content=title + desc + img
        )
