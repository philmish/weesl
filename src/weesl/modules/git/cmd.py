from dataclasses import dataclass


@dataclass
class StatusCommand:
    short: bool
    branch: bool
    show_stash: bool

    def __str__(self) -> str:
        cmd = "git status "
        if self.short:
            cmd += "--short "
        if self.branch:
            cmd += "--branch "
        if self.show_stash:
            cmd += "--show-stash "
        return cmd

@dataclass
class InitCommand:
    bare: bool
    quite: bool
    branch: str

    @staticmethod
    def default_branch() -> str:
        return "master"

    def __str__(self) -> str:
        cmd = "git init "
        if self.bare:
            cmd += "--bare "
        if self.quite:
            cmd += "--quite "
        if self.branch != InitCommand.default_branch:
            cmd += f"--initial-branch={self.branch} "
        return cmd

