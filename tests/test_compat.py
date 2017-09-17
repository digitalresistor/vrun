from vrun import compat

def test_ConfigParser_read_dict():
    cp = compat.ConfigParser()

    cp.read_dict(
        {
            'test': {
                'test': 'value',
                'another': 'test',
            },
            'DEFAULT': {
                'test': 'defaults',
            }
        }
    )

    assert cp.has_section('test')
    assert cp.defaults() == {'test': 'defaults'}
    assert cp.items('test') == [('test', 'value'), ('another', 'test')]
