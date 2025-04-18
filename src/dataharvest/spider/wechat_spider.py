import re
from typing import Optional

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async, stealth_sync

from dataharvest.schema import Document
from dataharvest.spider import BaseSpider, SpiderConfig
from dataharvest.spider.utils import random_user_agent


class WechatSpider(BaseSpider):
    """微信公众号爬虫，使用Playwright实现，确保获取完整内容"""

    def __init__(self, config: Optional[SpiderConfig] = None):
        super().__init__(config)
        self._cookies = []

    def match(self, url: str) -> bool:
        """匹配微信公众号链接"""
        return "mp.weixin.qq.com/s" in url

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        """同步爬取微信公众号文章内容"""
        config = self._merge_config(config)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            browser_context = browser.new_context(
                user_agent=random_user_agent()
            )

            # 添加cookies
            if self._cookies:
                browser_context.add_cookies(self._cookies)

            # 创建新页面
            page = browser_context.new_page()
            stealth_sync(page)
            
            # 访问URL并等待加载
            page.goto(url)
            page.wait_for_load_state("load")
            
            # 向下滚动页面以加载所有内容
            page.evaluate("""
                () => {
                    window.scrollTo(0, document.body.scrollHeight);
                    return new Promise(resolve => setTimeout(resolve, 1000));
                }
            """)
            
            # 获取文章元数据
            metadata = {}
            
            title_element = page.query_selector("#activity-name")
            if title_element:
                metadata["title"] = title_element.inner_text().strip()
            
            publish_time = page.query_selector("#publish_time")
            if publish_time:
                metadata["publish_time"] = publish_time.inner_text().strip()
            
            author = page.query_selector("#js_name")
            if author:
                metadata["author"] = author.inner_text().strip()
            
            # 提取 og:description 元标签内容
            description_meta = page.query_selector("meta[property='og:description']")
            if description_meta:
                metadata["description"] = description_meta.get_attribute("content")
            
            # 获取页面内容
            html = page.content()
            
            return Document(url=page.url, metadata=metadata, page_content=html)

    async def a_crawl(
            self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        """异步爬取微信公众号文章内容"""
        config = self._merge_config(config)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                **self.convert_2_playwright_lunch_arg(config))
            browser_context = await browser.new_context(
                user_agent=random_user_agent()
            )

            # 添加cookies
            if self._cookies:
                await browser_context.add_cookies(self._cookies)

            # 创建新页面
            page = await browser_context.new_page()
            await stealth_async(page)
            
            # 访问URL并等待加载
            await page.goto(url)
            await page.wait_for_load_state("load")
            
            # 向下滚动页面以加载所有内容
            await page.evaluate("""
                () => {
                    window.scrollTo(0, document.body.scrollHeight);
                    return new Promise(resolve => setTimeout(resolve, 1000));
                }
            """)
            
            # 获取文章元数据
            metadata = {}
            
            title_element = await page.query_selector("#activity-name")
            if title_element:
                metadata["title"] = await title_element.inner_text()
                metadata["title"] = metadata["title"].strip()
            
            publish_time = await page.query_selector("#publish_time")
            if publish_time:
                metadata["publish_time"] = await publish_time.inner_text()
                metadata["publish_time"] = metadata["publish_time"].strip()
            
            author = await page.query_selector("#js_name")
            if author:
                metadata["author"] = await author.inner_text()
                metadata["author"] = metadata["author"].strip()
            
            # 提取 og:description 元标签内容
            description_meta = await page.query_selector("meta[property='og:description']")
            if description_meta:
                metadata["description"] = await description_meta.get_attribute("content")
            
            # 获取页面内容
            html = await page.content()
            
            await browser.close()
            
            return Document(url=await page.url, metadata=metadata, page_content=html) 