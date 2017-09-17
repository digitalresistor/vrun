import os
import re
import sys

import pytest

from vrun import cli
from vrun.oscompat import WIN

@pytest.fixture()
def cwd_is_empty(monkeypatch):
    curpath = os.path.dirname(os.path.realpath(__file__))
    cwd = os.path.join(curpath, 'configtest', 'empty')

    monkeypatch.setattr(os, 'getcwd', lambda: cwd)

@pytest.fixture()
def disable_exec_bin(monkeypatch):
    class DummyExecBin(object):
        def __init__(self):
            self.called = False
            self.execbin = None
            self.argv = None
            self.env = None
            self.raise_exception = False

        def __call__(self, execbin, argv, env):
            self.called = True
            self.execbin = execbin
            self.argv = argv
            self.env = env

            if self.raise_exception is True:
                raise DummyExit(-99)

    dummy_exec_bin = DummyExecBin()
    monkeypatch.setattr(cli, 'exec_bin', dummy_exec_bin)

    def exit(code):
        raise DummyExit(code)

    monkeypatch.setattr(sys, 'exit', exit)
    yield dummy_exec_bin

@pytest.fixture()
def update_sys_argv(monkeypatch):
    def do_update(argv):
        assert isinstance(argv, list)

        if len(argv) == 0:
            argv.append('vrun')

        monkeypatch.setattr(sys, 'argv', argv)

    return do_update

@pytest.fixture()
def update_os_environ(monkeypatch):
    def do_update(environ):
        assert isinstance(environ, dict)

        monkeypatch.setattr(os, 'environ', environ)

    return do_update

def test_main(disable_exec_bin, capsys, update_sys_argv, cwd_is_empty):
    update_sys_argv([])

    with pytest.raises(DummyExit) as e:
        cli.main()

    assert e.value.code == -1
    out, err = capsys.readouterr()
    assert 'vrun requires the program to execute as an argument.' in err


def test_main_exists(disable_exec_bin, update_sys_argv, update_os_environ, cwd_is_empty):
    update_sys_argv(['vrun', 'python'])
    update_os_environ({})

    cli.main()

    assert disable_exec_bin.called is True

    if WIN:  # pragma: nocover
        assert disable_exec_bin.execbin.endswith('python.exe')
    else:
        assert disable_exec_bin.execbin.endswith('python')

    assert disable_exec_bin.argv == ['python']
    assert 'VRUN_ACTIVATED' in disable_exec_bin.env
    assert 'VIRTUAL_ENV' in disable_exec_bin.env
    assert 'PATH' in disable_exec_bin.env


def test_main_not_exists(
    disable_exec_bin,
    capsys,
    update_sys_argv,
    update_os_environ,
    cwd_is_empty
):
    update_sys_argv(['vrun', 'this_should_not_exist'])
    update_os_environ({})

    with pytest.raises(DummyExit) as e:
        cli.main()

    assert e.value.code == -1
    out, err = capsys.readouterr()
    assert 'vrun requires that the target executable exists.' in err

def test_main_execve_failed(
    disable_exec_bin,
    capsys,
    update_sys_argv,
    update_os_environ,
    cwd_is_empty
):
    update_sys_argv(['vrun', 'python'])
    update_os_environ({})
    disable_exec_bin.raise_exception = True

    cli.main()

    out, err = capsys.readouterr()
    assert 'vrun was unable to execute the target executable.' in err
    assert re.search('Executable: .*python', err)


@pytest.mark.parametrize('folder, argv, argv_result', [
    (
        'configtest',
        ['print_testing'],
        ['python', '-c', 'print("testing")']
    ),
    (
        'configtest',
        ['posargs_testing', 'some', 'sample', 'posargs'],
        ['python', 'some', 'sample', 'posargs', 'testing']
    ),
    (
        'configtest',
        ['python.version'],
        ['python', '--version']
    ),
    (
        os.path.join('configtest', 'vrun_ini'),
        ['print_testing'],
        ['python', '-c', 'print("testing")']
    ),
    (
        os.path.join('configtest', 'vrun_ini'),
        ['posargs_testing', 'some', 'sample', 'posargs'],
        ['python', 'some', 'sample', 'posargs', 'testing']
    ),
    (
        os.path.join('configtest', 'setup_cfg'),
        ['print_testing'],
        ['python', '-c', 'print("testing")']
    ),
    (
        os.path.join('configtest', 'setup_cfg'),
        ['posargs_testing', 'some', 'sample', 'posargs'],
        ['python', 'some', 'sample', 'posargs', 'testing']
    ),
    (
        os.path.join('configtest', 'setup_cfg_no_section'),
        ['python'],
        ['python']
    ),
    (
        os.path.join('configtest', 'empty'),
        ['python'],
        ['python']
    ),
    (
        os.path.join('configtest', 'bad'),
        ['python'],
        ['python']
    ),
])
def test_main_with_config(
    folder,
    argv,
    argv_result,
    monkeypatch,
    disable_exec_bin,
    update_sys_argv,
    update_os_environ
):
    curpath = os.path.dirname(os.path.realpath(__file__))
    cwd = os.path.join(curpath, folder)

    monkeypatch.setattr(os, 'getcwd', lambda: cwd)

    update_sys_argv(['vrun'] + argv)
    update_os_environ({})

    cli.main()

    assert disable_exec_bin.called is True
    assert disable_exec_bin.argv == argv_result


def test_main_with_bad_config(
    monkeypatch,
    disable_exec_bin,
    update_sys_argv,
    update_os_environ,
    capsys
):
    curpath = os.path.dirname(os.path.realpath(__file__))
    cwd = os.path.join(curpath, 'configtest', 'bad')

    monkeypatch.setattr(os, 'getcwd', lambda: cwd)
    update_sys_argv(['vrun'] + ['python'])
    update_os_environ({})

    cli.main()

    assert disable_exec_bin.called is True
    assert disable_exec_bin.argv == ['python']

    out, err = capsys.readouterr()
    assert 'may be malformed' in err


class DummyExit(Exception):
    def __init__(self, code, *args, **kw):
        self.code = code
        super(DummyExit, self).__init__(*args, **kw)
