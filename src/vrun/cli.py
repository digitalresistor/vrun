from __future__ import print_function
import os
import sys

def main():
    prefix = sys.prefix
    binpath = os.path.join(prefix, 'bin')

    PATH = os.environ.get('PATH', [])
    PATH = binpath + os.pathsep + PATH

    os.putenv('PATH', PATH)
    os.putenv('VRUN_ACTIVATED', '1')
    os.putenv('VIRTUAL_ENV', sys.prefix)
    newargv = sys.argv[1:]

    if not newargv:
        print('vrun requires the program to execute as an argument.', file=sys.stderr)
        print('Example: ./venv/bin/vrun /bin/bash', file=sys.stderr)
        sys.exit(-1)

    execbin = newargv[0]

    if os.sep not in execbin:
        execbin = os.path.join(binpath, execbin)

    if not os.path.exists(execbin):
        print('vrun requires that the target executable exists.', file=sys.stderr)
        print('Unable to find: {}'.format(execbin), file=sys.stderr)
        sys.exit(-1)

    try:
        # Execute the actual executable...
        os.execv(execbin, newargv)
    except Exception as e:
        print('vrun was unable to execute the target executable.', file=sys.stderr)
        print('Executable: {}'.format(execbin), file=sys.stderr)
        print('Exception as follows: {}'.format(e), file=sys.stderr)
