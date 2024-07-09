import random

from dataharvest.proxy.base import BaseProxy


class MyProxy(BaseProxy):
    def __init__(self):
        self.proxies = ["http://127.0.0.1:7890"]

    def __call__(self) -> str:
        return random.choice(self.proxies)


def test_proxy():
    proxy = MyProxy()
    assert proxy() == "http://127.0.0.1:7890"
