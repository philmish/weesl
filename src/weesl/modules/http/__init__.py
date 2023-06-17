from typing import Dict, Callable
from weesl.lib.modules import WeeslModule

class Module(WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {}

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)
