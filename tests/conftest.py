import pytest

from pytib.tables import generate_tables


@pytest.fixture
def table():
    return generate_tables({})
