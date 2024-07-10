from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Union as Uni

from dataharvest.proxy.base import BaseProxy
from dataharvest.schema import Document


@dataclass
class SpiderConfig:
    proxy_gene_func: Optional[BaseProxy] = None
    headers: Uni[Dict[str, str], None] = None


class BaseSpider(ABC):
    _index = 0
    _config: SpiderConfig = None

    def _merge_config(self, config: SpiderConfig) -> SpiderConfig:
        if self._config is None and config is None:
            return SpiderConfig()

        if config is None:
            return self._config

        if self._config is None:
            return config

        return SpiderConfig(
            proxy_gene_func=config.proxy_gene_func or self._config.proxy_gene_func,
            headers=config.headers or self._config.headers,
        )

    @staticmethod
    def convert_2_playwright_lunch_arg(config: SpiderConfig):
        proxy_obj = None
        if config.proxy_gene_func:
            proxy_obj = config.proxy_gene_func()

        return {
            "proxy": None if not proxy_obj else {"server": proxy_obj.server_url, "username": proxy_obj.username,
                                                 "password": proxy_obj.password}
        }

    @abstractmethod
    def match(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def crawl(self, url: str, config: Optional[SpiderConfig] = None) -> Document:
        raise NotImplementedError

    @abstractmethod
    async def a_crawl(
            self, url: str, config: Optional[SpiderConfig] = None
    ) -> Document:
        raise NotImplementedError
