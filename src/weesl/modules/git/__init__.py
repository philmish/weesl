from typing import Dict, Callable
from weesl.lib.modules import WeeslModule
from weesl.lib.processes import CommandOutputContainer, run_process
from weesl.modules.git.cmd import InitCommand, StatusCommand


class Module(WeeslModule):

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
                "status": self._status
        }

    def _status(
            self, 
            short: bool = False, 
            branch: bool = False, 
            show_stash: bool = False
            ) -> CommandOutputContainer:
        cmd = str(StatusCommand(short=short, branch=branch, show_stash=show_stash))
        return run_process(cmd)

    def _init(
            self, 
            bare: bool = False, 
            quite: bool = False, 
            branch: str = InitCommand.default_branch()
            ) -> CommandOutputContainer:
        cmd = str(InitCommand(bare=bare, quite=quite, branch=branch))
        return run_process(cmd)

