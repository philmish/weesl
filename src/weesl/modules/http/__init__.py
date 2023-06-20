from typing import Dict, Callable
from weesl.lib.modules import WeeslModule
from weesl.modules.http.request import RequestBuilder
from weesl.modules.http.session import SessionHandler

class Module(WeeslModule):

    def __init__(self) -> None:
        super().__init__()
        self.request_builder = RequestBuilder
        self.session_handler = SessionHandler()

    @property
    def calls(self) -> Dict[str, Callable]:
        return {}

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)
