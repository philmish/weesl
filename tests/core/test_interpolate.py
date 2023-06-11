import os
from typing import Dict
import pytest
from weesl.core.interpolate import interpolate_env

@pytest.mark.parametrize("setup,target,expected", [
    ({"HOMEDIR": "/home/user"}, "ENV:HOMEDIR;/not/home:/testing", "/home/user/testing"),
    ({}, "ENV:HOMEDIR;/not/home:/testing", "/not/home/testing"),
    ])
def test_interpolate_env(setup: Dict[str, str], target: str, expected: str):
    for k, v in setup.items():
        os.environ[k] = v
    result = interpolate_env(target)
    assert result == expected
    for k, _ in setup.items():
        del os.environ[k]
