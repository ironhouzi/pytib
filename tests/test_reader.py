import pytest

from pytib.read import read, _partition_word
from pytib.tables import generate_tables


@pytest.fixture
def table():
    return generate_tables({})


def test_classify_valid_word(table):
    assert tuple(_partition_word('sangs', table)) == ('sangs',)
    assert tuple(_partition_word('sangs/', table)) == ('sangs', '/')
    assert tuple(_partition_word('/sangs', table)) == ('/', 'sangs')
    assert tuple(_partition_word('sangs/foo', table)) == ('sangs', '/', 'foo')
    assert tuple(_partition_word('sangs//foo', table)) == ('sangs', '//', 'foo')


def test_bka(table):
    uni = '\u0f56' + '\u0f40' + '\u0F60'
    latin = "bka'"
    assert ''.join(read(latin, table)).rstrip() == uni


def test_unsplit_heading_curly(table):
    assert ''.join(read('{sangs', table)).rstrip() == '{ སངས'


def test_unsplit_trailing_curly(table):
    assert ''.join(read('sangs}', table)).rstrip() == 'སངས }'


def test_unsplit_curly(table):
    assert ''.join(read('{sangs sangs}', table)).rstrip() == '{ སངས་སངས }'


def test_joined_shad_after_nga(table):
    assert ''.join(read('dang/', table)).rstrip() == 'དང་།'


def test_spaced_shad_after_nga(table):
    assert ''.join(read('dang /', table)).rstrip() == 'དང་།'


def test_double_joined_shad_after_nga(table):
    assert ''.join(read('sang/ dang/', table)).rstrip() == 'སང་། དང་།'


def test_double_joined_shad_after_nga_w_ws(table):
    assert ''.join(read('sang/dang/', table)).rstrip() == 'སང་། དང་།'


def test_double_joined_shad_after_nga_w_nl(table):
    assert ''.join(read('sang\n/dang/', table)).rstrip() == 'སང\n། དང་།'


def test_double_spaced_shad_after_nga(table):
    assert ''.join(read('sang / dang /', table)).rstrip() == 'སང་། དང་།'


def test_double_spaced_shad_after_nga_w_leading_shad(table):
    assert ''.join(read('/ sang / dang /', table)).rstrip() == '། སང་། དང་།'


def test_two_trailing_shad_in_word(table):
    assert ''.join(read('sang/dang/', table)).rstrip() == 'སང་། དང་།'


def test_two_leading_shad_in_word(table):
    assert ''.join(read('/sang/dang', table)).rstrip() == '། སང་། དང'


def test_three_shad_in_word(table):
    assert ''.join(read('/sang/dang/', table)).rstrip() == '། སང་། དང་།'


def test_multiple_invalid_in_word(table):
    assert ''.join(read('/foo/fofo/', table)).rstrip() == '། foo ། fofo །'


def test_double_shad_for_kha(table):
    assert ''.join(read('ka/', table)).rstrip() == 'ཀ །'


def test_invalid_double_shad_for_kha(table):
    assert ''.join(read('ka//', table)).rstrip() == 'ཀ །'


def test_double_shad_for_ga(table):
    assert ''.join(read('ga/', table)).rstrip() == 'ག །'


def test_invalid_double_shad_for_ga(table):
    assert ''.join(read('ga//', table)).rstrip() == 'ག །'


# def test_no_double_shad_for_ga(table):
#     assert ''.join(read('ga/', table)).rstrip() == 'ག'
