import re

import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class BaiduBaikePurifier(BasePurifier):
    index = 100

    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0
        self.convertor.single_line_break = True
        self.convertor.ignore_images = True

    def match(self, url: str) -> bool:
        return "/baike.baidu.com/item/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 小标签清洗
        selector.xpath('//div[starts-with(@class, "editLemma")]').drop()
        selector.xpath('//div[starts-with(@class, "lemmaPicture")]').drop()
        selector.xpath('//span[starts-with(@class,"ttsBtn")]').drop()
        selector.xpath('//span[starts-with(@class,"supWrap")]').drop()

        # 内容拼装
        title = selector.xpath('//h1[contains(@class, "J-lemma-title")]/text()')[
            0
        ].get()
        clean_data = f"# {title}\n\n"
        # 描述
        if desc := selector.xpath(
            '//div[starts-with(@class, "lemmaDescText")]/text()'
        ).get():
            clean_data += f"{desc}\n\n"
        # 简介
        lemma_summary_e = selector.xpath(
            '//div[starts-with(@class, "lemmaSummary") and contains(@class, "J-summary")]'
        ).get()
        summary = self.convertor.handle(lemma_summary_e)
        clean_data += f"## 简介\n\n{summary}"
        # 基本信息
        if item_elements := selector.xpath("//div[starts-with(@class, 'itemWrapper')]"):
            item_dict = {
                item.xpath("./dt/text()").get(): item.xpath("./dd/span/text()").get()
                for item in item_elements
            }
            clean_data += "## 基本信息\n\n"
            clean_data += "\n".join([f"* {k}: {v}" for k, v in item_dict.items()])
        # 正文
        clean_data += "\n\n"
        if content_e := selector.xpath('//div[@class="J-lemma-content"]'):
            clean_data += self.convertor.handle(content_e[0].get())

        # 最终杂质字符
        clean_data = clean_data.replace("\u00a0", "")
        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)


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
