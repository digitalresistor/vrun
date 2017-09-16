import os

import pytest

from vrun import oscompat

pytestmark = [pytest.mark.skipif(oscompat.WIN, reason="Tests are Linux only")]

def test_get_binpath():
    assert oscompat.get_binpath('test') == 'test/bin'

def test_get_exec_path():
    assert oscompat.get_exec_path('bin', 'bash') == 'bin/bash'

def test_exec_bin(monkeypatch):
    def execve(execbin, argv, env):
        assert execbin == '/bin/bash'
        assert argv == ['/bin/bash', 'test']
        assert env == []

    monkeypatch.setattr(os, 'execve', execve)

    oscompat.exec_bin('/bin/bash', ['/bin/bash', 'test'], [])
