import pytest

from pytib.core import parse
from pytib.tables import create_lookup


@pytest.fixture
def defs():
    return (
        ('sangs', 'སངས'),
        ('bre', 'བྲེ'),
        ('rta', 'རྟ'),
        ('mgo', 'མགོ'),
        ('gya', 'གྱ'),
        ('g.yag', 'གཡག'),
        ("'rba", 'འརྦ'),
        ('tshos', 'ཚོས'),
        ('lhongs', 'ལྷོངས'),
        ('mngar', 'མངར'),
        ('sngas', 'སྔས'),
        ('rnyongs', 'རྙོངས'),
        ('brnyes', 'བརྙེས'),
        ('rgyas', 'རྒྱས'),
        ('skyongs', 'སྐྱོངས'),
        ('bskyongs', 'བསྐྱོངས'),
        ('grwa', 'གྲྭ'),
        ("spre'u", 'སྤྲེའུ'),
        ("spre'u'i", 'སྤྲེའུའི'),
        ("'dra", 'འདྲ'),
        ("'bya", 'འབྱ'),
        ("'gra", 'འགྲ'),
        ("'gyang", 'འགྱང'),
        ("'khra", 'འཁྲ'),
        ("'khyig", 'འཁྱིག'),
        ("'kyags", 'འཀྱགས'),
        ("'phre", 'འཕྲེ'),
        ("'phyags", 'འཕྱགས'),
        ('a', 'ཨ'),
        ('o', 'ཨོ'),
        ("a'am", 'ཨའམ'),
        ('ab', 'ཨབ'),
        ('bswa', 'བསྭ'),
        ('grwa', 'གྲྭ'),
        ("dbu'i", 'དབུའི'),
    )


@pytest.fixture
def latin_sanskrit_quick_checks():
    return ('sarva', 'ai', 'au', 'akṣye', 'vajra', 'kyai')


@pytest.fixture
def table():
    return create_lookup()
    # return Table()


@pytest.fixture
def polyglotta_table():
    consonants = (
        'k',  'kh',  'g',  'ṅ',
        'c',  'ch',  'j',  'ñ',
        't',  'th',  'd',  'n',
        'p',  'ph',  'b',  'm',
        'ts', 'tsh', 'dz', 'v',
        'ź',  'z',   '’',  'y',
        'r',  'l',   'ś',  's',
        'h',  'a'
    )

    return create_lookup(consonants, '-')
    # return Table(consonants, '-')


def test_wylie(defs, table):
    for wylie, u_tibetan in defs:
        syllable = parse(wylie, table)
        assert (
            tuple((f, f'U+0{ord(f):X}') for f in syllable)
            == tuple((f, f'U+0{ord(f):X}') for f in u_tibetan)
        )


def test_sna_ldan(table):
    uni = '\u0f67' + '\u0f75' + '\u0f83'
    latin = 'hūṃ'
    result = parse(latin, table)
    assert result == uni


def test_om(table):
    uni = '\u0f00'
    latin = 'oṃ'
    result = parse(latin, table)
    assert result == uni


# TODO: find counter case
def test_phat(table):
    uni = '\u0f55' + '\u0f4a'
    latin = 'phaṭ'
    assert parse(latin, table) == uni


def test_bighnan(table):
    uni = '\u0f56' + '\u0f72' + '\u0f43' + '\u0fa3' + '\u0f71' + '\u0f53'
    latin = 'bighnān'
    assert parse(latin, table) == uni


def test_ah(table):
    uni = '\u0f68' + '\u0f71' + '\u0f7f'
    latin = 'āḥ'
    assert parse(latin, table) == uni


def test_mandal(table):
    uni = '\u0f58' + '\u0f53' + '\u0f9c' + '\u0f63'
    latin = 'manḍal'
    assert parse(latin, table) == uni


def test_sanskrit_tib_genitive(table):
    uni = '\u0F64' + '\u0F71' + '\u0F40' + '\u0FB1' + '\u0F60' + '\u0F72'
    latin = "śākya'i"
    result = parse(latin, table)
    assert result == uni


# # TODO: find counter case
def test_sarva(table):
    uni = '\u0F66' + '\u0F62' + '\u0FA6'
    latin = 'sarva'
    assert parse(latin, table) == uni


# # TODO: find counter case
def test_vajra(table):
    uni = '\u0F56' + '\u0F5B' + '\u0FB2'
    latin = 'vajra'
    assert parse(latin, table) == uni


# # TODO: find counter case
def test_badzra(table):
    uni = '\u0F56' + '\u0F5B' + '\u0FB2'
    latin = 'badzra'
    assert parse(latin, table) != uni


# TODO: find counter case
def test_hksmlvryam(table):
    uni = '\u0f67' + '\u0fb9' + '\u0fa8' + '\u0fb3' + '\u0fba' + \
        '\u0fbc' + '\u0fbb' + '\u0f83'
    latin = 'hkṣmlvryaṃ'
    assert parse(latin, table) == uni


# TODO: find counter case
def test_tthddhnaa(table):
    uni = '\u0f4a' + '\u0f9b' + '\u0f9c' + '\u0f9d' + '\u0f9e' + '\u0f71'
    latin = 'ṭṭhḍḍhṇā'
    assert parse(latin, table) == uni


# TODO: find counter case
def test_shunyata(table):
    uni = '\u0f64' + '\u0f75' + '\u0f53' + '\u0fb1' + '\u0f4f' + '\u0f71'
    latin = 'śūnyatā'
    assert parse(latin, table) == uni


# TODO: find counter case
def test_kyai(table):
    uni = '\u0f40' + '\u0fb1' + '\u0f7b'
    latin = 'kyai'
    result = parse(latin, table)
    assert result == uni


# TODO: find counter case
def test_lakshmyai(table):
    uni = '\u0f63' + '\u0f69' + '\u0fa8' + '\u0fb1' + '\u0f7b'
    latin = 'lakṣmyai'
    assert parse(latin, table) == uni


# TODO: find counter case
def test_akshye(table):
    uni = '\u0f68' + '\u0f69' + '\u0fb1' + '\u0f7a'
    latin = 'akṣye'
    assert parse(latin, table) == uni


def test_ai(table):
    uni = '\u0F68' + '\u0F7B'
    latin = 'ai'
    assert parse(latin, table) == uni


def test_au(table):
    uni = '\u0F68' + '\u0F7D'
    latin = 'au'
    assert parse(latin, table) == uni


def test_matu(table):
    uni = '\u0F58' + '\u0F4F' + '\u0F74'
    latin = 'matu'
    assert parse(latin, table) == uni


def test_dha(table):
    uni = '\u0F52'
    latin = 'dha'
    assert parse(latin, table) == uni


def test_dpei(polyglotta_table):
    uni = '\u0F51' + '\u0F54' + '\u0F60' + '\u0F72'
    latin = 'dpa’i'
    assert parse(latin, polyglotta_table) == uni


def test_tsandan(table):
    uni = '\u0f59' + '\u0f53' + '\u0fa1' + '\u0f53'
    latin = 'tsandan'
    assert parse(latin, table) == uni
