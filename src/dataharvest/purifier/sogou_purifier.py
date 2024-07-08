import html2text
from parsel import Selector

from dataharvest.purifier.purifier import BasePurifier
from dataharvest.schema import Document


class SogouBaiKePurifier(BasePurifier):
    def __init__(self):
        self.convertor = html2text.HTML2Text()
        self.convertor.ignore_links = True
        self.convertor.body_width = 0

    def match(self, url: str) -> bool:
        return "baike.sogou.com/v/" in url

    def purify(self, doc: Document) -> Document:
        selector = Selector(doc.page_content)

        # 清理无用标签
        selector.xpath("//sup").drop()
        selector.xpath("//span[@class='base-info-card-value-more']").drop()
        selector.xpath("//a[@class='btn_edit']").drop()
        selector.xpath("//span[starts-with(@id, 'singlePicContainer')]").drop()
        selector.xpath("//span[starts-with(@id, 'commonAlbum')]").drop()

        # 标题
        title_label = selector.xpath("//div[@class='lemma_name']/h1").get()
        clean_data = self.convertor.handle(title_label)

        # 描述
        description_label = selector.xpath("//div[@class='abstract']").get()
        clean_data += self.convertor.handle(description_label)
        clean_data += "\r\n\r\n"

        # 基本信息
        base_info_dict = {}
        base_info_list = selector.xpath("//table[@class='abstract_list']")
        for base_info_item in base_info_list:
            cur_tr_list = base_info_item.xpath("./tbody/tr")

            for tr_item in cur_tr_list:
                key = tr_item.xpath("./th/text()").get()
                value = tr_item.xpath(
                    "./td//div[@class='base-info-card-value']/div/text()"
                ).get()

                base_info_dict[key] = value

        clean_data += "## 基本信息\r\n"
        clean_data += "\n".join([f"* {k}: {v}" for k, v in base_info_dict.items()])
        clean_data += "\r\n\r\n"

        # 正文
        content_label = selector.xpath("//div[@id='j-paragraph-wrap']").get()
        clean_data += self.convertor.handle(content_label)

        return Document(url=doc.url, metadata={**doc.metadata}, page_content=clean_data)
