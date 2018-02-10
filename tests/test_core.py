from pytib.core import generate_stacks


def test_single_vowel_postitions(table):
    assert list(generate_stacks(['r', 'ny', 'o', 'ng'], table)) \
        == [['r', 'ny', 'o'], ['ng']]


def test_joined_vowel_stac(table):
    assert list(generate_stacks(['h', 'ū', 'ṃ'], table)) \
        == [['h', 'ū', 'ṃ']]


def test_single_vowel_stack(table):
    assert list(generate_stacks(['ai'], table)) == [['ai']]


def test_joined_vowel_postitions(table):
    assert list(generate_stacks(['g', 'a', 'i'], table)) \
        == [['g', 'a', 'i']]
