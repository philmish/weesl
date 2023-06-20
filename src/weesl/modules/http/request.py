from requests import Request
from typing import Callable, Dict, List, Literal, Any, Self, Tuple, TypedDict, Union, IO


class RequestHooks(TypedDict):
    response: Callable


class RequestBuilder:

    def __init__(self) -> None:
        self.request = Request()

    def setMethod(self, method: Literal["GET", "POST", "PUT", "DELET"]) -> Self:
        self.request.method = method
        return self

    def setHeaders(self, headers: Dict[str, Any]) -> Self:
        self.request.headers = headers
        return self

    def setUrl(self, url: str) -> Self:
        self.request.url = url
        return self

    def setParams(self, params: Union[Dict[str, Any], List[Tuple[str, Any]]]) -> Self:
        self.request.params = params
        return self

    def setHooks(self, hooks: RequestHooks) -> Self:
        self.request.hooks = hooks
        return self

    def setJson(self, json: Dict[str,Any]) -> Self:
        self.request.json = json
        return self

    def setFiles(self, files: Dict[str, IO]) -> Self:
        self.request.files = files
        return self

    def setAuth(self, data: Tuple[str, str]) -> Self:
        self.request.auth = data
        return self

    def reset(self):
        self.request = Request()

    def get_request(self, reset: bool = True) -> Request:
        req = self.request
        if reset: self.reset()
        return req

