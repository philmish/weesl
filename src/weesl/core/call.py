from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Any

from weesl.core.interpolate import interpolate_env, interpolate_placeholder_str

@dataclass
class Call:
    mod: str
    fn: str
    args: Tuple[str]
    kwargs: Dict[str, str]
    receiver: Optional[str] = None

    @property
    def is_builtin(self) -> bool:
        return self.mod.startswith(".")

    def interpolate_args(self, prefix: str, kv: Dict[str, Any]):
        self.args = tuple([interpolate_placeholder_str(i, prefix, kv) for i in self.args])
        self.args = tuple([interpolate_env(i) for i in self.args])

    def interpolate_kwargs(self, prefix: str, kv: Dict[str, Any]):
        self.kwargs = {k: interpolate_placeholder_str(v, prefix, kv) for k, v in self.kwargs.items()}
        self.kwargs = {k: interpolate_env(v) for k, v in self.kwargs.items()}

    @classmethod
    def from_weesl(cls, call: str):
        parts = call.split("|")
        funcparts = parts[0].split("::")
        mod, fn = funcparts[0], funcparts[1]
        args: Tuple[str] = tuple()
        kwargs: Dict[str, str] = dict()
        recv = None
        for arg in parts[1].split(","):
            if "=" in arg:
                kv = arg.split("=")
                kwargs[kv[0]] = kv[1]
            else:
                args = (*args, arg)
        if len(parts) > 2:
            recv = parts[2]
        return cls(mod, fn, args, kwargs, recv)

