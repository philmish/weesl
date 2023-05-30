import os
import subprocess
from typing import Callable, Dict, Optional, List
from dataclasses import dataclass
from weesl.lib import modules, data_container
from weesl.modules.sys import rsync

@dataclass
class CommandOutputContainer(data_container.WeeslDataContainer):
    status: int
    err: Optional[str]
    out: str

    @property
    def has_err(self) -> bool:
        return self.status != 0

    def get_value(self):
        if self.has_err and self.err is not None:
            return self.out
        return f"Status: {self.status}\n{self.out}\nerr: {self.err}"

class Module(modules.WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "exec": self._exec,
            "env_set": self._env_set,
            "rsync": self._rsync
        }

    def _exec(self, cmd: str) -> CommandOutputContainer:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = p.communicate()
        p_status = p.wait()
        if err is not None:
            err = err.decode()
        out = out.decode()
        res = CommandOutputContainer(
                raw_value=p_status, 
                status=p_status, 
                err=err, 
                out=out
        )
        return res

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
