from typing import Any, Dict
import pytest
from weesl.modules.git.cmd import StatusCommand

@pytest.mark.parametrize("args,expected", [
    ({"short": False, "branch": False, "show_stash": False}, "git status"),
    ({"short": True, "branch": False, "show_stash": False}, "git status --short"),
    ({"short": False, "branch": True, "show_stash": False}, "git status --branch"),
    ({"short": False, "branch": False, "show_stash": True}, "git status --show-stash"),
    ({"short": False, "branch": True, "show_stash": True}, "git status --branch --show-stash"),
    ])
def test_git_status_command_builder(args: Dict[str, Any], expected:str):
    cmd = StatusCommand(**args)
    assert str(cmd) == expected
