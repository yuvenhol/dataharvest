import hashlib
import json
import re
from typing import Optional

import httpx
from httpx import Response
from parsel import Selector
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from dataharvest.schema import Document
from dataharvest.spider.base import SpiderConfig
from dataharvest.spider.spider import BaseSpider


class MaFengWoSpider(BaseSpider):
    def __init__(self, config: Optional[SpiderConfig] = None):
        self.client = httpx.Client(**BaseSpider.convert_2_httpx_client_arg(config))
        self.a_client = httpx.AsyncClient(**BaseSpider.convert_2_httpx_client_arg(config))
        self._config = self._merge_config(config)

        if not self._config.headers:
            self._config.headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }

    def match(self, url: str) -> bool:
        return "www.mafengwo.cn/i/" in url

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        config = self._merge_config(config)

        # 第一次请求，获取__jsluid_s，并解析__jsl_clearance_s
        first_resp = self.client.get(url, headers=config.headers)

        jsluid_s = first_resp.cookies["__jsluid_s"]

        # 用正则表达式匹配出需要的部分
        first_jsl_clearance_s_raw = re.findall(
            "cookie=(.*?);location", first_resp.text
        )[0]

        # 反混淆、分割出cookie的部分
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            first_jsl_clearance_s = (
                page.evaluate(first_jsl_clearance_s_raw).split(";")[0].split("=")[1]
            )

        # 第二次请求，解析新的__jsl_clearance_s
        second_cookies = {
            "__jsluid_s": jsluid_s,
            "__jsl_clearance_s": first_jsl_clearance_s,
        }
        second_resp = self.client.get(
            url, headers=config.headers, cookies=second_cookies
        )

        second_jsl_clearance_s = handle_go(second_resp.text)

        # 第三次请求，获取真实页面内容
        third_cookies = {
            "__jsluid_s": jsluid_s,
            "__jsl_clearance_s": second_jsl_clearance_s,
        }
        third_resp = self.client.get(url, headers=config.headers, cookies=third_cookies)

        final_content = handle_final_content(third_resp)

        document = Document(url=url, metadata={}, page_content=final_content)
        return document

    async def a_crawl(
        self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        config = self._merge_config(config)

        # 第一次请求，获取__jsluid_s，并解析__jsl_clearance_s
        first_resp = await self.a_client.get(url, headers=config.headers)

        jsluid_s = first_resp.cookies["__jsluid_s"]

        # 用正则表达式匹配出需要的部分
        first_jsl_clearance_s_raw = re.findall(
            "cookie=(.*?);location", first_resp.text
        )[0]

        # 反混淆、分割出cookie的部分
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            first_jsl_clearance_s_js = await page.evaluate(first_jsl_clearance_s_raw)
            first_jsl_clearance_s = first_jsl_clearance_s_js.split(";")[0].split("=")[1]

        # 第二次请求，解析新的__jsl_clearance_s
        second_cookies = {
            "__jsluid_s": jsluid_s,
            "__jsl_clearance_s": first_jsl_clearance_s,
        }

        second_resp = await self.a_client.get(
            url, headers=config.headers, cookies=second_cookies
        )

        second_jsl_clearance_s = handle_go(second_resp.text)

        # 第三次请求，获取真实页面内容
        third_cookies = {
            "__jsluid_s": jsluid_s,
            "__jsl_clearance_s": second_jsl_clearance_s,
        }
        third_resp = await self.a_client.get(
            url, headers=config.headers, cookies=third_cookies
        )

        final_content = handle_final_content(third_resp)

        document = Document(url=url, metadata={}, page_content=final_content)
        return document


def handle_go(second_resp_text: str) -> str:
    """
    处理JS混淆代码逻辑
    :param second_resp_text:
    :return:
    """

    second_jsl_clearance_s = None
    ha = None

    go = json.loads(re.findall(r"};go\((.*?)\)</script>", second_resp_text)[0])
    for i in range(len(go["chars"])):
        for j in range(len(go["chars"])):
            values = go["bts"][0] + go["chars"][i] + go["chars"][j] + go["bts"][1]
            if go["ha"] == "md5":
                ha = hashlib.md5(values.encode()).hexdigest()
            elif go["ha"] == "sha1":
                ha = hashlib.sha1(values.encode()).hexdigest()
            elif go["ha"] == "sha256":
                ha = hashlib.sha256(values.encode()).hexdigest()

            if ha == go["ct"]:
                second_jsl_clearance_s = values

    return second_jsl_clearance_s


def handle_final_content(third_resp: Response) -> str:
    """
    处理最终结果内容
    :param third_resp:
    :return:
    """

    third_resp.raise_for_status()

    selector = Selector(third_resp.text)

    final_content = selector.xpath('//div[@class="_j_content"]').get()

    final_content = (
        final_content or selector.xpath('//div[@class="_j_content_box"]').get()
    )
    final_content = final_content or selector.xpath('//div[@class="post_info"]').get()

    if final_content is None:
        raise Exception("爬取异常,内容为空")

    return final_content
