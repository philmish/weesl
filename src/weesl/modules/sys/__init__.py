import os
from weesl.lib import modules
from weesl.modules.sys import rsync
from typing import Callable, Dict, Optional, List
from weesl.lib.processes import CommandOutputContainer, run_process

class Module(modules.WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "exec": self._exec,
            "env_set": self._env_set,
            "rsync": self._rsync
        }

    def _exec(self, cmd: str) -> CommandOutputContainer:
        return run_process(cmd)

    def _env_set(self, key: str, val: str):
        os.environ[key] = val

    def _rsync(
            self, 
            local: str, 
            target: str,
            user: Optional[str] = None,
            host: Optional[str] = None,
            key: Optional[str] = None,
            exclude: Optional[List[str]] = None,
            backup: Optional[str] = None,
            verbose: bool = True,
            delete: bool = False,
            from_remote: bool = False,
            ) -> CommandOutputContainer:
        cmd = rsync.RsyncCommandBuilder(
                dir=local,
                target=target,
                user=user,
                host=host,
                key=key,
                exclude=exclude,
                backup=backup,
                verbose=verbose,
                delete=delete,
                from_remote=from_remote
        )
        return self._exec(cmd.build)

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)
