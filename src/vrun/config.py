import os
import itertools

from .compat import ConfigParser


def find_config(path=None):
    if path is None:
        path = os.getcwd()

    check_files = [
        # config file, check for vrun section
        ('vrun.cfg', False),
        ('vrun.ini', False),
        ('setup.cfg', True)
    ]

    for filename, section_check in check_files:
        p = os.path.join(path, filename)
        if os.path.exists(p):
            if section_check:
                # Verify we have a vrun section before turning the path as being found
                cp = ConfigParser()
                cp.read(p)
                if cp.has_section('vrun'):
                    return p
            else:
                return p
    else:
        return None


def config_from_file(path):
    cp = ConfigParser(
        defaults={
            'here': os.path.dirname(path),
        }
    )
    cp.read(path)
    return cp


def quoted_combine(parts):
    quoted = None
    next_arg = None

    for part in parts:
        if (
            part.startswith(('\'', '"')) and
            not part.endswith(('\'', '"'))
        ):
            if quoted and quoted == part[0]:
                raise ValueError(
                    "Invalid quoting in command. "
                    "Opening quote found twice without closing quote."
                )
            elif not quoted:
                next_arg = part[1:]
                quoted = part[0]
                continue

        if (
            quoted and
            part.endswith(quoted) and
            not part.startswith(quoted)
        ):
            next_arg = "{} {}".format(next_arg, part[:-1])
            yield next_arg
            quoted = None
            continue

        if (
            quoted and
            part.endswith(quoted) and
            part.startswith(quoted)
        ):
            raise ValueError(
                "Invalid quoting in command. "
                "Found closing quote without opening quote."
            )

        if quoted:
            next_arg = "{} {}".format(next_arg, part)
            continue

        yield part


class Config(object):
    """
    Configuration object that takes a ConfigParser
    """
    def __init__(self, config):
        self.config = config

    def has_command(self, command):
        return (
            self.config.has_section('vrun') and
            self.config.has_option('vrun', command)
        )

    def interpolate_command(self, command, posargs):
        if self.has_command(command):
            command = self.config.get('vrun', command)
            parts = itertools.chain.from_iterable(
                filter(
                    None,
                    [
                        x.strip().split(' ') for x
                        in command.splitlines()
                    ]
                )
            )

            argv = quoted_combine(parts)

            if posargs:
                def interpolate():
                    pos_args_found = False

                    for arg in argv:
                        if arg == '{posargs}':
                            pos_args_found = True
                            for posarg in posargs:
                                yield posarg
                        else:
                            yield arg

                    if pos_args_found is False:
                        for posarg in posargs:
                            yield posarg

                argv = list(interpolate())
            else:
                argv = list(argv)

            return argv
        else:
            raise KeyError("Command does not exist in the configuration file")
