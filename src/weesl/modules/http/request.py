from requests import Request
from abc import ABC, abstractmethod
from typing import Callable, Dict, Literal, Any, Self, TypedDict


class RequestHooks(TypedDict):
    response: Callable


class RequestBuilder(ABC):

    def __init__(self) -> None:
        self.request = Request()

    def setMethod(self, method: Literal["GET", "POST", "PUT", "DEL"]) -> Self:
        self.request.method = method
        return self

    def setHeaders(self, headers: Dict[str, Any]) -> Self:
        self.request.headers = headers
        return self

    def setUrl(self, url: str) -> Self:
        self.request.url = url
        return self

    def setHooks(self, hooks: RequestHooks) -> Self:
        self.request.hooks = hooks
        return self

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> Request:
        raise NotImplemented

