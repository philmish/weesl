from requests import Request
from typing import Callable, Dict, List, Literal, Any, Tuple, TypedDict, Union, IO, TypeVar


class RequestHooks(TypedDict):
    response: Callable


HttpRequestBuilder = TypeVar("HttpRequestBuilder", bound="RequestBuilder")

class RequestBuilder:

    def __init__(self) -> None:
        self.request = Request()

    def setMethod(self, method: Literal["GET", "POST", "PUT", "DELET"]):
        self.request.method = method
        return self

    def setHeaders(self, headers: Dict[str, Any]):
        self.request.headers = headers
        return self

    def setUrl(self, url: str):
        self.request.url = url
        return self

    def setParams(self, params: Union[Dict[str, Any], List[Tuple[str, Any]]]):
        self.request.params = params
        return self

    def setHooks(self, hooks: RequestHooks):
        self.request.hooks = hooks
        return self

    def setJson(self, json: Dict[str,Any]):
        self.request.json = json
        return self

    def setFiles(self, files: Dict[str, IO]):
        self.request.files = files
        return self

    def setAuth(self, data: Tuple[str, str]):
        self.request.auth = data
        return self

    def reset(self):
        self.request = Request()

    def get_request(self, reset: bool = True) -> Request:
        req = self.request
        if reset: self.reset()
        return req

