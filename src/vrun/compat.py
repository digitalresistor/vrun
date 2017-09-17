# flake8: noqa

import sys

PY2 = sys.version_info[0] == 2

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

if not hasattr(ConfigParser, 'read_dict'):
    def read_dict(self, dictionary, source='<dict>'):
        for (section, options) in dictionary.items():
            if (
                section
                not in {
                    self.default_section if hasattr(self, 'default_section') 
                    else 'DEFAULT' 
                }
            ):
                self.add_section(section)

            for (option, value) in options.items():
                self.set(section, option, value)

    ConfigParser.read_dict = read_dict
