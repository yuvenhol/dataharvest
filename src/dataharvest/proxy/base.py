from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class Proxy:
    server_url: str
    username: Optional[str] = None
    password: Optional[str] = None


class BaseProxy(ABC):
    @abstractmethod
    def __call__(self) -> Proxy:
        raise NotImplementedError
