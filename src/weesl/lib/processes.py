from subprocess import Popen, PIPE
from typing import Optional
from dataclasses import dataclass
from weesl.lib.data_container import WeeslDataContainer

@dataclass
class CommandOutputContainer(WeeslDataContainer):
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

def run_process(cmd: str) -> CommandOutputContainer:
    p = Popen(cmd, stdout=PIPE, shell=True)
    (out, err) = p.communicate()
    p_status = p.wait()
    res = CommandOutputContainer(
            raw_value=p_status, 
            status=p_status, 
            err=err.decode(), 
            out=out.decode()
    )
    return res
