import pytest
from collections.abc import Callable
from typing import Dict, Mapping, TypedDict
from requests.adapters import BaseAdapter
from requests import Response, PreparedRequest, Session


ResponseMockHook = Callable[[PreparedRequest], Response] 


def method_not_supported_hook(request: PreparedRequest) -> Response:
    response = Response()
    response.status_code = 405
    response.request = request
    return response
    

def not_found_hook(request: PreparedRequest) -> Response:
    response = Response()
    response.status_code = 404
    response.request = request
    return response


class MockedRoute(TypedDict):
    GET: ResponseMockHook 
    POST: ResponseMockHook
    PUT: ResponseMockHook
    DELETE: ResponseMockHook


def new_mocked_route(
        get: ResponseMockHook,
        post: ResponseMockHook,
        put: ResponseMockHook,
        delete: ResponseMockHook
        ) -> MockedRoute:
    return MockedRoute(
            GET=get,
            POST=post,
            PUT=put,
            DELETE=delete
    )


class MockAdapter(BaseAdapter):

    def __init__(self) -> None:
        super().__init__()
        self.uri_register: Dict[str, MockedRoute] = {}
        self.not_found_mock: ResponseMockHook = not_found_hook

    def add_route(
            self, 
            uri: str, 
            route: MockedRoute
            ):
        self.uri_register[uri] = route

    def send(
            self, 
            request: PreparedRequest, 
            stream: bool = False, 
            timeout: None | float | tuple[float, float] | tuple[float, None] = None, 
            verify: bool | str = True, 
            cert: None | bytes | str | tuple[bytes | str, bytes | str] = None, 
            proxies: Mapping[str, str] | None = None
            ) -> Response:

        if request.url in self.uri_register:
            route = self.uri_register[request.url]
            method = request.method
            if method is None:
                return method_not_supported_hook(request)
            handler = route.get(method)
            if handler is None:
                return method_not_supported_hook(request)
            return handler(request)

        return self.not_found_mock(request)


@pytest.mark.parametrize("route_map,url,expected_code", [
    ({}, "mock://test.org/hello", 404)
    ])
def test_adapter_mock(route_map: Dict[str, MockedRoute], url: str, expected_code: int):
    session = Session()
    adapter = MockAdapter()
    for uri, route in route_map.items():
        adapter.add_route(uri, route)
    session.mount("mock://", MockAdapter())
    assert session.get(url).status_code == expected_code
