from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any


"""
Base for data objects, which might also be used for data filtering/mutation
like type casting.
"""
@dataclass
class WeeslDataContainer(ABC):
    raw_value: Any

    def get_raw(self) -> Any:
        return self.raw_value

    @abstractmethod
    def get_value(self) -> Any:
        raise NotImplemented
