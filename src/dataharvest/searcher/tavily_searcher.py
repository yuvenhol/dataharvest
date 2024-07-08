import os
from typing import Optional

import httpx

from dataharvest.schema import SearchResult, SearchResultItem
from dataharvest.searcher.base import BaseSearcher


class TavilySearcher(BaseSearcher):
    """
    Reference: https://docs.tavily.com/docs/tavily-api/rest_api
    """

    def __init__(self, api_key: Optional[str] = None, max_results: int = 5, **kwargs):
        """
        :param api_key:  Your Tavily API key.
        :param keyword:  The search query string.
        :param search_depth:  The depth of the search.
        It can be basic or advanced.
        Default is basic for quick results and advanced for indepth high quality results but longer response time.
        Advanced calls equals 2 requests.
        :param include_images:  Include a list of query related images in the response.
        Default is False.
        :param include_answer:  Include answers in the search results.
        Default is False.
        :param include_raw_content:  Include raw content in the search results.
        Default is False.
        :param max_results:  The number of maximum search results to return.
        Default is 5.
        :param include_domains:  A list of domains to specifically include in the search results.
        Default is None, which includes all domains.
        :param exclude_domains:  A list of domains to specifically exclude from the search results.
        Default is None, which doesn't exclude any domains.
        :param api_key:
        :param max_results:
        :param kwargs:
        """
        tavily_api_key = api_key or os.getenv("TAVILY_API_KEY")

        if not tavily_api_key:
            raise ValueError("Tavily API key is required.")

        self.api_key = tavily_api_key
        self.max_results = max_results
        self.search_depth = kwargs.get("search_depth", "basic")
        self.include_answer = kwargs.get("include_answer", False)
        self.include_images = kwargs.get("include_images", False)
        self.include_raw_content = kwargs.get("include_raw_content", False)
        self.include_domains = kwargs.get("include_domains", [])
        self.exclude_domains = kwargs.get("exclude_domains", [])

        self.client = httpx.Client()

    def search(self, keyword: str, **kwargs) -> SearchResult:
        """
        search a keyword,you can customize parameters in kwargs

        :return:  A SearchResult object.
        """
        req = {
            "api_key": self.api_key,
            "query": keyword,
            "search_depth": kwargs.get("search_depth", self.search_depth),
            "include_answer": kwargs.get("include_answer", self.include_answer),
            "include_images": kwargs.get("include_images", self.include_images),
            "include_raw_content": kwargs.get(
                "include_raw_content", self.include_raw_content
            ),
            "max_results": kwargs.get("max_results", self.max_results),
            "include_domains": kwargs.get("include_domains", self.include_domains),
            "exclude_domains": kwargs.get("exclude_domains", self.exclude_domains),
        }

        res = self.client.post("https://api.tavily.com/search", json=req)
        res.raise_for_status()
        res_json = res.json()
        images = res_json.get("images", [])
        answer = res_json.get("answer", "")
        items = [
            SearchResultItem(
                title=item["title"],
                url=item["url"],
                score=item["score"],
                description=item["content"],
            )
            for item in res_json["results"]
        ]
        return SearchResult(keyword, answer, images, items)
