from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from dataharvest.base import Document
from dataharvest.spider.spider import BaseSpider


class CommonSpider(BaseSpider):
    index = 2 ** 16

    def match(self, url: str) -> bool:
        return True

    def crawl(self, url: str):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()
            js = """
                    Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
                    """
            page.add_init_script(js)
            page.goto(url)
            page.wait_for_load_state('load')
            html = page.content()
            document = Document(url=page.url, metadata={}, page_content=html)
            return document

    async def a_crawl(self, url: str):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            js = """
                    Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
                    """
            await page.add_init_script(js)
            await page.goto(url)
            await page.wait_for_load_state('load')
            html = await page.content()
            await browser.close()
            return Document(url=url, metadata={}, page_content=html)
