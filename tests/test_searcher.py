import logging


def test_tavily_searcher():
    from dataharvest.searcher.tavily_searcher import TavilySearcher

    searcher = TavilySearcher()
    logging.info(searcher.search("战国水晶杯"))


def test_sky_searcher():
    from dataharvest.searcher.sky_searcher import SkySearcher
    api_key = ""
    app_secret = ""

    searcher = SkySearcher(app_key=api_key,
                           app_secret=app_secret)
    r = searcher.search("苏州博物馆里明唐寅灌木丛绦图轴的资料")
    assert r
