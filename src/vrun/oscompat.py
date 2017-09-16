import os
import sys

WIN = sys.platform == 'win32' or os.name == 'nt'

if not WIN:
    def get_binpath(prefix):
        return os.path.join(prefix, 'bin')

    def get_exec_path(binpath, execbin):
        return os.path.join(binpath, execbin)

    def exec_bin(execbin, argv, env):
        os.execve(execbin, argv, env)

else:  # pragma: nocover
    import subprocess

    def get_binpath(prefix):
        return os.path.join(prefix, 'Scripts')

    def get_exec_path(binpath, execbin):
        if '.exe' not in execbin:
            return os.path.join(binpath, '{}.exe'.format(execbin))
        else:
            return os.path.join(binpath, execbin)

    def exec_bin(execbin, argv, env):
        exe = subprocess.Popen(
            [execbin] + argv[1:],
            env=env,
            universal_newlines=True
        )
        exe.communicate()
        sys.exit(exe.returncode)
