from typing import Any, Dict, Union, TypedDict
import pytest
from weesl.modules.git.cmd import InitCommand, StatusCommand


class StatusArgs(TypedDict):
    short: bool
    branch: bool
    show_stash: bool

@pytest.mark.parametrize("args,expected", [
    ({"short": False, "branch": False, "show_stash": False}, "git status"),
    ({"short": True, "branch": False, "show_stash": False}, "git status --short"),
    ({"short": False, "branch": True, "show_stash": False}, "git status --branch"),
    ({"short": False, "branch": False, "show_stash": True}, "git status --show-stash"),
    ({"short": False, "branch": True, "show_stash": True}, "git status --branch --show-stash"),
    ])
def test_git_status_command_builder(args: StatusArgs, expected:str):
    cmd = StatusCommand(**args)
    assert str(cmd) == expected

class InitArgs(TypedDict, total=False):
    bare: bool
    quite: bool
    branch: str

@pytest.mark.parametrize("args,expected", [
    ({"bare": False, "quite": False}, "git init"),
    ])
def test_git_init_command_builder(args: InitArgs, expected: str):
    cmd = InitCommand(**args)
    assert str(cmd) == expected
