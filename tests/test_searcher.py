import logging


def test_tavily_searcher():
    from dataharvest.searcher.tavily_searcher import TavilySearcher
    searcher = TavilySearcher()
    logging.info(searcher.search("战国水晶杯"))
