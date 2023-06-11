import pytest
from weesl.modules.rsync.cmd import RsyncCommandBuilder

@pytest.mark.parametrize("kwargs,expected", [
    ({"dir": "/home/user/test", "target": "/home/user/target"}, "rsync -av /home/user/test /home/user/target"),
    ])
def test_rsnyc_command_builder(kwargs, expected):
    cmd = RsyncCommandBuilder(**kwargs)
    assert str(cmd) == expected
