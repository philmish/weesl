import os
import json
import yaml
from typing import Dict, Callable, Any
from weesl.lib.modules import WeeslModule

class Module(WeeslModule):

    @property
    def calls(self) -> Dict[str, Callable]:
        return {
            "file_exists": self._file_exists,
            "dir_exists": self._dir_exists,
            "mkdir": self._mkdir,
            "join_path": self._join_path,
            "read_json": self._read_json,
            "write_json": self._write_json,
            "read_yaml": self._read_yaml,
            "write_yaml": self._write_yaml,
            "cd": self._cd,
        }

    def _file_exists(self, fpath: str) -> bool:
        return os.path.isfile(fpath)

    def _dir_exists(self, dpath: str) -> bool:
        return os.path.isdir(dpath)

    def _mkdir(self, dpath: str, rec: bool = False):
        if rec:
            os.makedirs(dpath)
        else:
            os.mkdir(dpath)

    def _join_path(self, *args) -> str:
        res = os.path.join(*args)
        return res

    def _cd(self, path: str):
        os.chdir(path)

    def _read_json(self, fpath: str) -> Dict[str, Any]:
        with open(fpath, "r") as f:
            return json.load(f)

    def _write_json(self,fpath: str, data: Dict[str, Any]):
        with open(fpath, "w") as f:
            json.dump(data, f)

    def _read_yaml(self, fpath: str) -> Dict[str, Any]:
        with open(fpath, "r") as f:
            return yaml.safe_load(f)

    def _write_yaml(self, fpath: str, data: Dict[str, Any]):
        with open(fpath, "w") as f:
            yaml.dump(data, f)

    def execute(self, name: str, *args, **kwargs):
        return self.calls[name](*args, **kwargs)

