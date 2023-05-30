from typing import Any, Dict, List
from weesl.core.call import Call


"""
Task defined in a weesl setup yaml file.
Contains all variables specific to the tasks scope and the
List of calls run during the task.
The calls will be run in the sequence defined by the order in your yaml
file.
"""
class Task:

    def __init__(self, name: str, vars: Dict[str, Any] , calls: List[Call]) -> None:
        self.name = name
        self.vars = vars
        self.calls = calls

    def set_var(self, key: str, val: Any):
        self.vars[key] = val

    @classmethod
    def setup(cls, name: str, vars: Dict[str, Any],  calls: List[str]):
        return cls(name, vars, [Call.from_shaper(i) for i in calls])

"""
Iterator implementation for a list of Tasks.
"""
class TaskList:

    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks
        self.position = -1

    def __iter__(self):
        return self

    def __next__(self) -> Task:
        self.position += 1
        if self.position < len(self.tasks):
            return self.tasks[self.position]
        raise StopIteration

