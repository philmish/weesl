from typing import Dict, Callable, Any
from abc import ABC, abstractmethod, abstractproperty



"""
Base Class for all WeeslModules
"""
class WeeslModule(ABC):

    @abstractproperty
    def calls(self) -> Dict[str, Callable]:
        raise NotImplemented

    @abstractmethod
    def execute(self, name: str, *args, **kwargs) -> Any:
        raise NotImplemented
