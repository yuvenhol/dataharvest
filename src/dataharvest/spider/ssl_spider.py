from typing import Optional

import httpx

from dataharvest.schema import Document
from dataharvest.spider.base import SpiderConfig
from dataharvest.spider.spider import BaseSpider


class SslSpider(BaseSpider):
    def __init__(self, config: Optional[SpiderConfig] = None):
        self.client = httpx.Client(**BaseSpider.convert_2_httpx_client_arg(config))
        self.a_client = httpx.AsyncClient(
            **BaseSpider.convert_2_httpx_client_arg(config)
        )
        self._config = self._merge_config(config)

        if not self._config.headers:
            self._config.headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            }

    def match(self, url: str) -> bool:
        return "/www.360doc.com/content/" in url

    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        res = self.client.get(url, headers=self._config.headers, follow_redirects=True)
        res.raise_for_status()
        document = Document(
            url=str(res.request.url),
            metadata={},
            page_content=res.content.decode("utf-8"),
        )
        return document

    async def a_crawl(
        self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        res = await self.a_client.get(
            url, headers=self._config.headers, follow_redirects=True
        )
        res.raise_for_status()
        document = Document(
            url=str(res.request.url),
            metadata={},
            page_content=res.content.decode("utf-8"),
        )
        return document
