import importlib
from yaml import load
from typing import Callable, List, Dict, Any
from weesl.lib.data_container import WeeslDataContainer
from weesl.lib.modules import WeeslModule
from weesl.core.call import Call
from weesl.core.task import Task, TaskList

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Weesl:

    mod_map: Dict[str, WeeslModule] = dict()
    var_pre: str = ".$"
    gloabal_pre: str = "$"

    def __init__(self, data, title, mods, tasks, settings) -> None:
        self.title = title
        self.data = data
        self.settings = settings
        self.mods = mods
        self.tasks = tasks

    def builtins(self) -> Dict[str, Callable]:
        return {
            "set": self._set,
            "print": lambda s: print(f"{s}"),
        }

    def _set(self, k: str ,v: Any):
        self.globals[k] = v

    @property
    def meta_keys(self) -> List[str]:
        return ["title", "author", "mods"]

    @property
    def settings_keys(self) -> List[str]:
        return ["debug", "log"]

    @property
    def globals(self) -> Dict[str, Any]:
        if "global" in self.data:
            return self.data["global"]
        return {}

    @staticmethod
    def required_keys() -> List[str]:
        return ["data", "tasks", "title", "mods", "settings"]

    @staticmethod
    def load_modules(mods: List[str]) -> Dict[str, WeeslModule]:
        modules: Dict[str, WeeslModule] = dict()
        for name in mods:
            mod = importlib.import_module(f"weesl.modules.{name}")
            modules[name] = getattr(mod, "Module")()
        return modules

    @staticmethod
    def parse_tasks(tasks: List[Dict[str, Dict[str, Any]]]) -> TaskList:
        parsed: List[Task] = list()
        for task in tasks:
            for k, v in task.items():
                data = {"name": k, **v}
                parsed.append(Task.setup(**data))
        return TaskList(parsed)

    def interpolate_call(self, call: Call, vars: Dict[str, Any]) -> Call:
        call.interpolate_args(self.var_pre, vars)
        call.interpolate_kwargs(self.var_pre, vars)
        call.interpolate_args(self.gloabal_pre, self.globals)
        call.interpolate_kwargs(self.gloabal_pre, self.globals)
        return call

    def execute_call(self, call: Call, vars: Dict[str, Any]):
        call = self.interpolate_call(call, vars)
        fn = call.fn
        args = call.args
        kwargs = call.kwargs
        recv = call.receiver

        if call.is_builtin:
            res = self.builtins()[fn](*args, **kwargs)
            return res, recv
        else:
            mod = call.mod
            if mod not in self.mod_map:
                raise Exception(f"Unknown Module {mod}")
            loaded_mod = self.mod_map[mod]
            res = loaded_mod.execute(fn, *args, **kwargs)
            return res, recv

    def run(self):
        for task in self.tasks:
            print(f"Executing task {task.name}")
            for call in task.calls:
                res, recv = self.execute_call(call, task.vars)
                if recv is not None and res is not None:
                    if isinstance(res, WeeslDataContainer):
                        res = res.get_value()
                    if recv.startswith(self.gloabal_pre):
                        self._set(recv.replace(self.gloabal_pre, ""), res)
                    elif recv.startswith(self.var_pre):
                        task.set_var(recv.replace(self.var_pre, ""), res)

        print("Weesl finished execution.")
            
    @classmethod
    def setup(cls, filepath: str):
        with open(filepath, "r") as config:
            data = load(config, Loader)
            for k in cls.required_keys():
                if not k in data:
                    raise Exception(f"Missing key {k}")
            weesl = cls(**{i: [data[i]] for i in cls.required_keys()})
            weesl.title = weesl.title[0]
            weesl.data = weesl.data[0]
            weesl.mods = weesl.mods[0]
            weesl.mod_map = cls.load_modules(weesl.mods)
            weesl.tasks = cls.parse_tasks(weesl.tasks[0])
            return weesl

