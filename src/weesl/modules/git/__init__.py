from typing import Dict, Callable
from weesl.lib.modules import WeeslModule
from weesl.lib.processes import CommandOutputContainer, run_process


class Module(WeeslModule):

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
                "status": self._status
        }

    def _status(self, *args, **kwargs) -> CommandOutputContainer:
        return run_process("git status")

