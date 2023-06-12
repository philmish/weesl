import os
from weesl.lib import modules
from typing import Callable, Dict
from weesl.lib.processes import CommandOutputContainer, run_process

class Module(modules.WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "exec": self._exec,
            "env_set": self._env_set,
        }

    def _exec(self, cmd: str) -> CommandOutputContainer:
        return run_process(cmd)

    def _env_set(self, key: str, val: str):
        os.environ[key] = val

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)
