from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from dataharvest.base import Document
from dataharvest.spider import BaseSpider


class ZhihuSpider(BaseSpider):
    index = 100

    def match(self, url: str) -> bool:
        if url.startswith("https://zhuanlan.zhihu.com/p/"):
            return True
        return False

    def crawl(self, url: str):
        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state(state='networkidle', timeout=3000)
            html = page.content()
            return Document(url=url, metadata={}, page_content=html)

    async def a_crawl(self, url: str):
        async with async_playwright() as p:
            browser = await p.webkit.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state(state='networkidle', timeout=3000)
            html = await page.content()
            return Document(url=url, metadata={}, page_content=html)
