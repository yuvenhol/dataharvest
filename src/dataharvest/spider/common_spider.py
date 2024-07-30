from typing import Optional

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async, stealth_sync

from dataharvest.schema import Document
from dataharvest.spider.base import SpiderConfig
from dataharvest.spider.spider import BaseSpider


class CommonSpider(BaseSpider):
    _index = 2 ** 16

    def __init__(self, config: Optional[SpiderConfig] = None):
        self._config = self._merge_config(config)

    def match(self, url: str) -> bool:
        return True

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        config = self._merge_config(config)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            page = browser.new_page()
            if config.headers:
                page.set_extra_http_headers(config.headers)
            stealth_sync(page)
            page.goto(url)
            page.wait_for_load_state(state="load")
            html = page.content()
            document = Document(url=page.url, metadata={}, page_content=html)
            return document

    async def a_crawl(
            self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        config = self._merge_config(config)
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            page = await browser.new_page()
            if config.headers:
                await page.set_extra_http_headers(config.headers)
            await stealth_async(page)
            await page.goto(url)
            await page.wait_for_load_state("load")
            html = await page.content()
            await browser.close()
            return Document(url=url, metadata={}, page_content=html)
