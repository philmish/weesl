from weesl.lib import modules
from weesl.modules.rsync.cmd import RsyncCommandBuilder
from typing import Callable, Dict, Optional, List
from weesl.lib.processes import CommandOutputContainer, run_process


class Module(modules.WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "local": self._local,
            "to_remote": self._to_remote,
            "from_remote": self._from_remote,
        }

    def _local(
            self, 
            dir: str, 
            target: str, 
            exclude: Optional[List[str]] = None,
            backup: Optional[str] = None,
            verbose: bool = True,
            delete: bool = False
            ) -> CommandOutputContainer:
        cmd = RsyncCommandBuilder(
                dir=dir,
                target=target,
                backup=backup,
                verbose=verbose,
                delete=delete,
                exclude=exclude,
                from_remote=False,
        )
        return run_process(str(cmd))

    def _to_remote(
            self, 
            dir: str, 
            target: str, 
            user: str,
            host: str,
            key: Optional[str] = None,
            exclude: Optional[List[str]] = None,
            backup: Optional[str] = None,
            verbose: bool = True,
            delete: bool = False
            ) -> CommandOutputContainer:
        cmd = RsyncCommandBuilder(
                dir=dir,
                target=target,
                user=user,
                host=host,
                key=key,
                backup=backup,
                verbose=verbose,
                delete=delete,
                exclude=exclude,
                from_remote=False,
        )
        return run_process(str(cmd))

    def _from_remote(
            self,
            dir: str, 
            target: str, 
            user: str,
            host: str,
            key: Optional[str] = None,
            exclude: Optional[List[str]] = None,
            backup: Optional[str] = None,
            verbose: bool = True,
            delete: bool = False
            ) -> CommandOutputContainer:
        cmd = RsyncCommandBuilder(
                dir=dir,
                target=target,
                user=user,
                host=host,
                key=key,
                backup=backup,
                verbose=verbose,
                delete=delete,
                exclude=exclude,
                from_remote=True,
        )
        return run_process(str(cmd))


    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)


