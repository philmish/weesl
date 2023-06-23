from dataclasses import dataclass
from typing import Mapping, Any
from weesl.lib.data_container import WeeslDataContainer

@dataclass
class JsonResultContainer(WeeslDataContainer):
    status: int
    data: Mapping[str, Any]
    
    @property
    def success(self) -> bool:
        return self.status < 300

    def get_value(self) -> Any:
        if not self.success:
            #TODO create custom exception
            raise Exception
        return self.data

