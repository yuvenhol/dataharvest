import hashlib
import json
import time
from typing import Optional

import httpx

from dataharvest.schema import SearchResult
from dataharvest.schema import SearchResultItem
from dataharvest.searcher.base import BaseSearcher


class SkySearcher(BaseSearcher):
    """
    天工搜索
    Reference: https://model-platform.tiangong.cn/api-reference
    """

    def __init__(self, app_key: str, app_secret: str, base_url: Optional[str] = None):
        self.url = base_url or "https://api.singularity-ai.com/sky-saas-search/api/v1/search"
        self.app_key = app_key
        self.app_secret = app_secret

    def _get_headers(self):
        timestamp = str(int(time.time()))
        sign_content = self.app_key + self.app_secret + timestamp
        sign_result = hashlib.md5(sign_content.encode("utf-8")).hexdigest()

        return {
            "app_key": self.app_key,
            "timestamp": timestamp,
            "sign": sign_result,
            "Content-Type": "application/json",
        }

    @staticmethod
    def parse_response(keyword, response) -> SearchResult:
        items = []
        answer = ""
        for line in response.iter_lines():
            if line.startswith('{"code":400007,"code_msg":"服务器忙，请稍后再试"}'):
                raise Exception("服务器忙，请稍后再试")
            elif line.startswith(
                    """data: {"type":1,"card_type":"search_result","target":"finish"""
            ):
                search_result_json = json.loads(line[line.index("{"):])
                search_result = search_result_json["arguments"][0]["messages"][0][
                    "sourceAttributions"
                ]
                items = [
                    SearchResultItem(url=i["seeMoreUrl"],
                                     title=i["title"],
                                     description=i["snippet"])
                    for i in search_result]
            elif line.startswith(
                    """data: {"type":1,"card_type":"markdown","target":"finish"""
            ):
                markdown_json = json.loads(line[line.index("{"):])
                answer += markdown_json["arguments"][0]["messages"][0]["text"]

        return SearchResult(keyword=keyword, answer=answer, items=items)

    def search(self, keyword: str, **kwargs) -> SearchResult:
        data = {
            "content": keyword,
            "stream_resp_type": kwargs.get("stream_resp_type", "all"),
        }

        response = httpx.post(self.url, headers=self._get_headers(), json=data)
        response.raise_for_status()
        return self.parse_response(keyword, response)
