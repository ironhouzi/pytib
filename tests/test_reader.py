import pytest

from pytib import read
from pytib.tables import generate_tables, U_TSHEG


@pytest.fixture
def table():
    return generate_tables({})


def test_unsplit_curly(table):
    assert ''.join(read('{sangs', table)).rstrip() == '{སངས'
    assert ''.join(read('sangs}', table)).rstrip() == 'སངས}'
    assert ''.join(read('{sangs sangs}', table)).rstrip() == (
        f'{{སངས{U_TSHEG}སངས}}'
    )
