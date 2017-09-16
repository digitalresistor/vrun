# pragma: nocover

import subprocess
import sys

import pytest

from vrun import oscompat

pytestmark = [pytest.mark.skipif(not oscompat.WIN, reason="Tests are Windows only")]

def test_get_binpath():
    assert oscompat.get_binpath('test') == 'test\\Scripts'

def test_get_exec_path():
    assert oscompat.get_exec_path('bin', 'cmd') == 'bin\\cmd.exe'

def test_get_exec_path_exe():
    assert oscompat.get_exec_path('bin', 'cmd.exe') == 'bin\\cmd.exe'

def test_exec_bin(monkeypatch):
    class Popen(object):
        def __init__(self, *args, **kw):
            self.communicate_called = False
            self.returncode = -1

        def __call__(self, *args, **kw):
            self.args = args
            self.kw = kw
            self.returncode = 0

            return self

        def communicate(self):
            self.communicate_called = True

    popen_monkey = Popen()
    monkeypatch.setattr(subprocess, 'Popen', popen_monkey)

    def exit(retcode):
        assert retcode == 0

    monkeypatch.setattr(sys, 'exit', exit)

    oscompat.exec_bin('bin\\bash.exe', ['bin\\bash', 'test'], [])

    assert popen_monkey.communicate_called is True
    assert len(popen_monkey.args) == 1
    assert len(popen_monkey.args[0]) == 2
    assert popen_monkey.args[0] == ['bin\\bash.exe', 'test']
    assert popen_monkey.kw['env'] == []
    assert popen_monkey.kw['universal_newlines'] is True
