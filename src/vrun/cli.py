from __future__ import print_function
import os
import sys

def get_binpath(prefix):
    if os.name == 'nt':
        return os.path.join(prefix, 'Scripts')
    else:
        return os.path.join(prefix, 'bin')

def get_exec(binpath, execbin):
    if os.name == 'nt' and '.exe' not in execbin:
        return os.path.join(binpath, '{}.exe'.format(execbin))
    else:
        return os.path.join(binpath, execbin)

def main():
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
        execbin = get_exec(binpath, execbin)

    if not os.path.exists(execbin):
        print('vrun requires that the target executable exists.', file=sys.stderr)
        print('Unable to find: {}'.format(execbin), file=sys.stderr)
        sys.exit(-1)

    try:
        # Windows has to be special...
        if os.name == 'nt':
            import subprocess
            exe = subprocess.Popen(
                [execbin] + newargv[1:],
                env=newenv,
                universal_newlines=True
            )
            exe.communicate()
            sys.exit(exe.returncode)
        else:
            # Sane OS's let you just execute a new binary that takes the place
            # of the old:
            os.execve(execbin, newargv, newenv)

    except Exception as e:
        print('vrun was unable to execute the target executable.', file=sys.stderr)
        print('Executable: {}'.format(execbin), file=sys.stderr)
        print('Exception as follows: {}'.format(e), file=sys.stderr)
