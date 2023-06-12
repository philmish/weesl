import os
from typing import Any, Dict
import pytest
from weesl.core.interpolate import interpolate_env, interpolate_placeholder_str

@pytest.mark.parametrize("setup,target,expected", [
    ({"HOMEDIR": "/home/user"}, "ENV:HOMEDIR;/not/home:/testing", "/home/user/testing"),
    ({}, "ENV:HOMEDIR;/not/home:/testing", "/not/home/testing"),
    ({"HOMEDIR": "/home/user", "TESTDIR": "/testing"}, "ENV:HOMEDIR;/not/home:ENV:TESTDIR;/testing:", "/home/user/testing"),
    ])
def test_interpolate_env(setup: Dict[str, str], target: str, expected: str):
    for k, v in setup.items():
        os.environ[k] = v
    result = interpolate_env(target)
    assert result == expected
    for k, _ in setup.items():
        del os.environ[k]

@pytest.mark.parametrize("prefix,target,vars,expected", [
    ("$", "$test", {"test": 1234}, 1234),
    ])
def test_interpolate_placeholder_str(prefix: str, target: str, vars: Dict[str, Any], expected: Any):
    assert interpolate_placeholder_str(target, prefix, vars) == expected
