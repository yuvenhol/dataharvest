from typing import Optional

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async, stealth_sync

from dataharvest.schema import Document
from dataharvest.spider import BaseSpider, SpiderConfig
from dataharvest.spider.utils import random_user_agent


class XiaoHongShuSpider(BaseSpider):

    def __init__(self, config: Optional[SpiderConfig] = None):
        self._config = self._merge_config(config)
        self._cookies = [{
            'name': "webId",
            'value': "xxx123",
            'domain': ".xiaohongshu.com",
            'path': "/"
        }]

    def match(self, url: str) -> bool:
        return "/www.xiaohongshu.com/explore/" in url or "/xhslink.com/" in url

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        config = self._merge_config(config)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            browser_context = browser.new_context(
                user_agent=random_user_agent()
            )

            browser_context.add_cookies(self._cookies)

            context_page = browser_context.new_page()

            stealth_sync(context_page)
            context_page.goto(url)
            context_page.wait_for_load_state(state="load")
            html = context_page.content()
            document = Document(url=url, metadata={}, page_content=html)
            return document

    async def a_crawl(
            self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        config = self._merge_config(config)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            browser_context = await browser.new_context(
                user_agent=random_user_agent()
            )

            await browser_context.add_cookies(self._cookies)

            context_page = await browser_context.new_page()
            await stealth_async(context_page)
            await context_page.goto(url)
            await context_page.wait_for_load_state(state="load")
            html = await context_page.content()
            document = Document(url=url, metadata={}, page_content=html)
            return document
