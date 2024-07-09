from abc import ABC, abstractmethod


class BaseProxy(ABC):
    @abstractmethod
    def __call__(self) -> str:
        raise NotImplementedError
