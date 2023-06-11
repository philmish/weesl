from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RsyncCommandBuilder:
    dir: str
    target: str
    user: Optional[str] = None
    host: Optional[str] = None
    key: Optional[str] = None
    exclude: Optional[List[str]] = None
    backup: Optional[str] = None
    verbose: bool = True
    delete: bool = False
    from_remote: bool = False

    @property
    def authenticatable(self) -> bool:
        return self.user is not None and self.host is not None

    def __str__(self) -> str:
        cmd = "rsync"
        if self.delete: cmd += " --delete"
        flags = "a"
        shell = ""
        target = ""
        src = ""
        if self.verbose is not None: flags += "v"
        if self.key is not None: 
            flags += "e"
            shell += f"'ssh -i {self.key}' "
        if self.authenticatable and not self.from_remote: 
            target += f"{self.user}@{self.host}:{self.target}"
            src += self.dir
        elif self.authenticatable and self.from_remote:
            target += self.target
            src += f"{self.user}@{self.host}:{self.dir}"
        else:
            target += self.target
            src += self.dir
        if self.backup is not None:
            flags += "b"
            target += f" --backup-dir={self.backup}"
        cmd = f"{cmd} -{flags} {shell}{src} {target}"
        return cmd
