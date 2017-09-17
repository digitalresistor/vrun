import os
import itertools

from .compat import ConfigParser

def find_config(path=os.getcwd()):
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

