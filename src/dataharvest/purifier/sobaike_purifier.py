import cssutils
import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class SoBaikePurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "baike.so.com/doc/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清理无用标签
        selector.xpath("//div[@id='main-content-text']//a[@class='conArrow']").drop()
        selector.xpath(
            "//div[@id='main-content-text']//a[@class='reference_sup']"
        ).drop()
        selector.xpath(
            "//div[@id='main-content-text']//span[@class='opt js-edittext']"
        ).drop()
        selector.xpath("//a[@class='show-img layoutright']").drop()

        # 标题
        title = selector.xpath(
            "//div[@id='baike-title']/h1/span[@class='title']/text()"
        ).get()
        clean_data = f"# {title}\r\n"

        # 所属类别
        classify_key = selector.xpath(
            "//div[@class='entry-classify-down js-classify-list']/span/text()"
        ).get()
        classify_val = selector.xpath(
            "//div[@class='classify-txt js-classify-txt short']/text()"
        ).get()

        clean_data += classify_key
        clean_data += classify_val + "\r\n\r\n"

        # 描述
        description_label = selector.xpath("//div[@id='js-card-content']").get()
        clean_data += self.convertor.handle(description_label)
        clean_data += "\r\n\r\n"

        # 基本信息
        base_info_dict = {}
        base_info_ul_list = selector.xpath(
            "//div[@id='basic-info']/div[@class='card-list-box']/ul"
        )

        for base_info_ul_item in base_info_ul_list:
            cur_li_list = base_info_ul_item.xpath("./li")

            for li_item in cur_li_list:
                key = li_item.xpath(
                    "./div/p[starts-with(@class,'cardlist-name')]/@title"
                ).get()
                value = li_item.xpath(
                    "./div/p[starts-with(@class,'cardlist-value')]/@title"
                ).get()

                base_info_dict[key] = value

        clean_data += "## 基本信息\r\n"
        clean_data += "\n".join([f"* {k}: {v}" for k, v in base_info_dict.items()])
        clean_data += "\r\n\r\n"

        # 正文
        content_label = selector.xpath("//div[@id='main-content-text']")

        style_tags = selector.xpath("//style/text()").getall()

        sheet = cssutils.parseString("\n".join([t for t in style_tags]))

        not_visible_elements = set()
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                selectors = rule.selectorText.split(", ")
                styles = rule.style.cssText
                if "visibility: hidden" in styles or "display: none" in styles:
                    not_visible_elements.update(selectors)

        for not_visible_item in not_visible_elements:
            content_label.xpath(
                ".//*[@class='" + str(not_visible_item)[1:] + "']"
            ).drop()

        print(content_label.get())
        clean_data += self.convertor.handle(content_label.get())

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
