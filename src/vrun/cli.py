from __future__ import print_function
import os
import sys

from .config import (
    Config,
    config_from_file,
    find_config,
)

from .oscompat import (
    get_binpath,
    get_exec_path,
    exec_bin,
)


def main():
    cfg = None
    config_file = find_config()

    if config_file:
        try:
            cfg = Config(config_from_file(config_file))
        except:
            print('Configuration file: {} found, '
                  'but may be malformed, continuing without'.format(config_file),
                  file=sys.stderr
                  )
            cfg = None

    prefix = sys.prefix
    binpath = get_binpath(prefix)

    PATH = os.environ.get('PATH', '')
    if PATH:
        PATH = binpath + os.pathsep + PATH
    else:
        PATH = binpath

    newenv = os.environ

    newenv['PATH'] = PATH
    newenv['VRUN_ACTIVATED'] = '1'
    newenv['VIRTUAL_ENV'] = sys.prefix

    newargv = sys.argv[1:]

    if not newargv:
        print('vrun requires the program to execute as an argument.', file=sys.stderr)
        print('Example: ./venv/bin/vrun /bin/bash', file=sys.stderr)
        sys.exit(-1)

    execbin = newargv[0]

    if os.sep not in execbin:
        if cfg:
            if cfg.has_command(execbin):
                newargv = cfg.interpolate_command(execbin, newargv[1:])
                execbin = newargv[0]

        if os.sep not in execbin:
            execbin = get_exec_path(binpath, execbin)

    if not os.path.exists(execbin):
        print('vrun requires that the target executable exists.', file=sys.stderr)
        print('Unable to find: {}'.format(execbin), file=sys.stderr)
        sys.exit(-1)

    try:
        exec_bin(execbin, newargv, newenv)
    except Exception as e:
        print('vrun was unable to execute the target executable.', file=sys.stderr)
        print('Executable: {}'.format(execbin), file=sys.stderr)
        print('Exception as follows: {}'.format(e), file=sys.stderr)
