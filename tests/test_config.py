import os

import pytest

from vrun import config
from vrun.compat import ConfigParser


@pytest.mark.parametrize('parts, result', [
    (
        ['simple'],
        ['simple']
    ),
    (
        ['multiple', 'simple'],
        ['multiple', 'simple']
    ),
    (
        ['with', '"quotes"'],
        ['with', '"quotes"']
    ),
    (
        ['"testing', 'quote', 'support"'],
        ['testing quote support']
    ),
    (
        ["'testing", 'quote', "support'"],
        ['testing quote support']
    ),
    (
        ['"testing', '\'quote', 'support"'],
        ['testing \'quote support']
    ),
    (
        ['"testing', '\'quote\'', 'support"'],
        ['testing \'quote\' support']
    ),
    (
        ['"testing', '\'quote', '\'support"'],
        ['testing \'quote \'support']
    ),
    (
        ['""'],
        ['""']
    ),
    (
        ['" ', ' "'],
        ['   ']
    ),
    (
        ['one', 'two', '"three', 'four"'],
        ['one', 'two', 'three four']
    ),
])
def test_quoted_combine(parts, result):
    assert list(config.quoted_combine(parts)) == result


@pytest.mark.parametrize('parts', [
    ['"testing', '\'quote', '"support"'],
    ['" ', '""'],
    ['"test', '"ing'],
])
def test_quoted_combine_invalid(parts):
    with pytest.raises(ValueError):
        assert list(config.quoted_combine(parts))


@pytest.mark.parametrize('folder, result', [
    ('configtest', 'vrun.cfg'),
    (os.path.join('configtest', 'vrun_ini'), 'vrun.ini'),
    (os.path.join('configtest', 'setup_cfg'), 'setup.cfg'),
    (os.path.join('configtest', 'setup_cfg_no_section'), None),
    (os.path.join('configtest', 'empty'), None),
])
def test_find_config(folder, result):
    curpath = os.path.dirname(os.path.realpath(__file__))

    cwd = os.path.join(curpath, folder)

    if result:
        assert config.find_config(cwd).endswith(result)
    else:
        assert config.find_config(cwd) == result


@pytest.mark.parametrize('folder', [
    'configtest',
    os.path.join('configtest', 'vrun_ini'),
    os.path.join('configtest', 'setup_cfg'),
])
def test_config_from_file(folder):
    curpath = os.path.dirname(os.path.realpath(__file__))
    cwd = os.path.join(curpath, folder)

    config_file = config.find_config(cwd)
    assert isinstance(config.config_from_file(config_file), ConfigParser)


def test_Config_has_command():
    config_dict = {
        'vrun':
            {
                'singlecommand': '/bin/bash',
                'interpolate': '/bin/bash {posargs} testing',
            }
        }
    cp = ConfigParser()
    cp.read_dict(config_dict)

    cfg = config.Config(cp)

    assert cfg.has_command('singlecommand') is True
    assert cfg.has_command('interpolate') is True
    assert cfg.has_command('nonexistent') is False


_config_dict = {
    'vrun':
        {
            'singlecommand': '/bin/bash',
            'simple': 'bash',
            'interpolate': '/bin/bash {posargs} testing',
            'ip': 'bash "quoted string" {posargs} testing',
            'python.version': 'python --version',
        }
    }


@pytest.mark.parametrize('config_dict, command, posargs, result', [
    (_config_dict, 'singlecommand', [], ['/bin/bash']),
    (_config_dict, 'interpolate', ['test'], ['/bin/bash', 'test', 'testing']),
    (_config_dict, 'simple', ['implicit', 'args'], ['bash', 'implicit', 'args']),
    (
        _config_dict,
        'ip',
        ['test', 'ing'],
        ['bash', 'quoted string', 'test', 'ing', 'testing']
    ),
    (
        _config_dict,
        'ip',
        ['test ing'],
        ['bash', 'quoted string', 'test ing', 'testing']
    ),
    (
        _config_dict,
        'python.version',
        [],
        ['python', '--version']
    ),
])
def test_Config_interpolate_command(config_dict, command, posargs, result):
    cp = ConfigParser()
    cp.read_dict(config_dict)
    cfg = config.Config(cp)

    assert cfg.interpolate_command(command, posargs) == result


def test_config_interpolate_command_not_found():
    cp = ConfigParser()
    cp.read_dict(_config_dict)
    cfg = config.Config(cp)

    with pytest.raises(KeyError) as e:
        cfg.interpolate_command('nonexistent', [])

    assert 'Command does not exist' in e.value.args[0]
