# flake8: noqa

import sys

PY2 = sys.version_info[0] == 2

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser
