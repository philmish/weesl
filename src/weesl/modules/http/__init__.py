from typing import Dict, Callable
from weesl.lib.modules import WeeslModule
from weesl.modules.http.data import JsonResultContainer
from weesl.modules.http.request import RequestBuilder
from weesl.modules.http.session import SessionHandler

class Module(WeeslModule):

    def __init__(self) -> None:
        super().__init__()
        self.request_builder = RequestBuilder()
        self.session_handler = SessionHandler()

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "get_json": self._get_json,
        }

    def _get_json(self, uri: str) -> JsonResultContainer:
        self.request_builder.setUrl(url=uri).setMethod("GET")
        req = self.request_builder.get_request()
        resp = self.session_handler.run_request(req)
        try:
            data = resp.json()
        except Exception:
            #TODO handle exception explicitly
            data = {}
        return JsonResultContainer(status=resp.status_code, data=data, raw_value=resp)

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)
