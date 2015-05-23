# -*- coding: utf-8 -*-
# TODO remove utf8 requirement for this file

# # Schol/latin consonants
# W_ROOTLETTERS = (
#     'k',  'kh',  'g',  'ṅ',
#     'c',  'ch',  'j',  'ñ',
#     't',  'th',  'd',  'n',
#     'p',  'ph',  'b',  'm',
#     'ts', 'tsh', 'dz', 'v',
#     'ź',  'z',   '’', 'y',
#     'r',  'l',   'ś',  's',
#     'h',  'a', )

# Wylie/latin consonants
W_ROOTLETTERS = (
    'k',  'kh',  'g',  'ng',
    'c',  'ch',  'j',  'ny',
    't',  'th',  'd',  'n',
    'p',  'ph',  'b',  'm',
    'ts', 'tsh', 'dz', 'w',
    'zh', 'z',   '\'', 'y',
    'r',  'l',   'sh', 's',
    'h',  'a', )

# Tibetan Unicode consonants
U_ROOTLETTERS = (
    '\u0f40', '\u0f41', '\u0f42', '\u0f44',
    '\u0f45', '\u0f46', '\u0f47', '\u0f49',
    '\u0f4f', '\u0f50', '\u0f51', '\u0f53',
    '\u0f54', '\u0f55', '\u0f56', '\u0f58',
    '\u0f59', '\u0f5a', '\u0f5b', '\u0f5d',
    '\u0f5e', '\u0f5f', '\u0f60', '\u0f61',
    '\u0f62', '\u0f63', '\u0f64', '\u0f66',
    '\u0f67', '\u0f68', )

# Latin consonants for transliteration of sanskrit (IAST)
# TODO: replace char litterals with codepoints.
SW_ROOTLETTERS = (
    'k',  'kh', 'g',  'gh',
    'ṅ',  'c',  'ch', 'j',
    'jh', 'ñ',  'ṭ',  'ṭh',
    'ḍ',  'ḍh', 'ṇ',  't',
    'th', 'd',  'dh', 'n',
    'p',  'ph', 'b',  'bh',
    'm',  'y',  'r',  'l',
    'v',  'ś',  'ṣ',  's',
    'h', 'kṣ', )

# Tibetan Unicode consonants for Tibetan transliteration of Sanskrit
SU_ROOTLETTERS = (
    U_ROOTLETTERS[0],  U_ROOTLETTERS[1],  U_ROOTLETTERS[2],  '\u0f43',
    U_ROOTLETTERS[3],  U_ROOTLETTERS[4],  U_ROOTLETTERS[5],  U_ROOTLETTERS[18],
    '\u0f5c',          U_ROOTLETTERS[7],  '\u0f4a',          '\u0f4b',
    '\u0f4c',          '\u0f4d',          '\u0f4e',          U_ROOTLETTERS[8],
    U_ROOTLETTERS[9],  U_ROOTLETTERS[10], '\u0f52',          U_ROOTLETTERS[11],
    U_ROOTLETTERS[12], U_ROOTLETTERS[13], U_ROOTLETTERS[14], '\u0f57',
    U_ROOTLETTERS[15], U_ROOTLETTERS[23], U_ROOTLETTERS[24], U_ROOTLETTERS[25],
    U_ROOTLETTERS[19], U_ROOTLETTERS[26], '\u0f65',          U_ROOTLETTERS[27],
    U_ROOTLETTERS[28], '\u0f69', )

# Wylie/latin vowels
W_VOWELS = ('i', 'u', 'e', 'o', )

# Tibetan Unicode vowels
U_VOWELS = ('\u0f72', '\u0f74', '\u0f7a', '\u0f7c', )

# Latin vowels for transliteration of sanskrit (IAST)
# TODO: replace char litterals with codepoints.
SW_VOWELS = (
    'a',         'ā',  W_VOWELS[0], 'ī',
    W_VOWELS[1], 'ū',  W_VOWELS[2], 'ai',
    W_VOWELS[3], 'au', 'ṛ',         'ṝ',
    'ḷ',         'ḹ',  'ṃ',         'ḥ', )

# Tibetan Unicode vowels for Tibetan transliteration of Sanskrit
SU_VOWELS = (
    '\u0f68',    '\u0f71', U_VOWELS[0], '\u0f73',
    U_VOWELS[1], '\u0f75', U_VOWELS[2], '\u0f7b',
    U_VOWELS[3], '\u0f7d', '\u0f76',    '\u0f77',
    '\u0f78',    '\u0f79', '\u0f7e',    '\u0f7f', )

# TODO: replace char litterals with codepoints.
U_OM = 'oṃ'
U_STACKED_YA = '\u0fbb'
U_STACKED_RA = '\u0fbc'

TSHEG = '\u0f0b'
S_SPACE = '\u00a0'
S_SHAD = '\u0f0d'
S_NYIS_SHAD = '\u0f0e'
S_SNA_LDAN = '\u0f83'
S_OM = '\u0f00'

W_SYMBOLS = ('/', '//', )

U_SYMBOLS = (S_SHAD, S_NYIS_SHAD, )

def get_chars(indices, alphabet):
    return tuple([alphabet[index] for index in indices])

def defs(index_groups, char_indices, rootletters):
    group = get_chars(char_indices, rootletters)
    rules = tuple([get_chars(indices, rootletters) for indices in index_groups])
    valid_list = dict(zip(group, rules))
    return (group, valid_list,)

def suffix_rules(rootletters):
    suffixes = get_chars(SUFFIXES_I, rootletters)
    sec_suffixes = get_chars(SUFFIX2S_I, rootletters)
    return dict(zip(POSTVOWEL, (suffixes, sec_suffixes)))

# Valid characters for superjoined wylie
# ['r', 'l', 's']
SUPER_INDICES = (24, 25, 27, )

# Valid characters for subjoined wylie
# ['w', 'y', 'r', 'l']
SUB_INDICES = (19, 23, 24, 25, )

# Valid characters for wylie prefixes
# ['g', 'd', 'b', 'm', '\'']
PREFIXES_I = (2,  10, 14, 15, 22, )

# Valid characters for wylie suffixes
# ['g', 'ng', 'd', 'n', 'b', 'm', '\'', 'r', 'l', 's']
SUFFIXES_I = (2,  3,  10, 11, 14, 15, 22, 24, 25, 27, )

# Valid characters for wylie second suffixes
# ['s' 'd']
SUFFIX2S_I = (27, 10, )

# Wylie characters that take the 'ra' character as its superjoined letter.
#  ['k', 'g', 'ng', 'j', 'ny', 't', 'd', 'n', 'b',  'm', 'ts', 'dz']
RAGO_INDICES = (0,  2,  3, 6,  7,  8, 10, 11, 14, 15, 16, 18, )

# Wylie characters that take the 'la' character as its superjoined letter.
#  ['k', 'g', 'ng', 'c', 'j', 't', 'd', 'p',  'b', 'h']
LAGO_INDICES = (0,  2,  3, 4,  6,  8, 10, 12, 14, 28, )

# Wylie characters that take the 'sa' character as its superjoined letter.
#  ['k', 'g', 'ng', 'ny', 't', 'd', 'n', 'p',  'b',  'm', 'ts']
SAGO_INDICES = (0,  2,  3, 7,  8,  10, 11, 12, 14, 15, 16, )

# Wylie characters that take the 'ya' character as its subjoined letter.
#  ['k', 'kh', 'g', 'p', 'ph', 'b', 'm', 'h']
YATA_INDICES = (0,  1,  2, 12, 13, 14, 15, 28, )

# Wylie characters that take the 'ra' character as its subjoined letter.
#  ['k', 'kh', 'g', 't', 'th', 'd', 'n', 'p', 'ph', 'b', 'm',  's', 'h']
RATA_INDICES = (0,  1,  2, 8,  9,  10, 11, 12, 13, 14, 15, 27, 28, )

# Wylie characters that take the 'la' character as its subjoined letter.
#  ['k', 'g', 'b', 'r', 's', 'z']
LATA_INDICES = (0,  2,  14, 24, 27, 21, )

# Wylie characters that take the 'wa' character as its subjoined letter.
# ['k', 'kh', 'g', 'c', 'ny', 't', 'd', 'ts', 'tsh', 'zh', 'z', 'r', 'l', 'sh',
#  's', 'h']
WAZUR_INDICES = (0,  1,  2, 4,  7,  8, 10, 16, 17, 20, 21, 24, 25, 26, 27, 28, )

# Syllable objects have the following structure. The individual elements are
# referred to as 'components', or 'syllable components'.

PREVOWEL = ('prefix',
            'super',
            'root',
            'subjoined',
            'secondsub',
            'vowel', )

POSTVOWEL = ('suffix',
             'suffix2',
             'genitive',
             'genvowel', )

SYLLSTRUCT = PREVOWEL + POSTVOWEL

SUBOFFSET = 0x50

# Normal stacking without subjoining for: 'va', 'ya', 'ra'
STACK = {
    SW_ROOTLETTERS[28]: '\u0fba',
    SW_ROOTLETTERS[25]: '\u0fbb',
    SW_ROOTLETTERS[26]: '\u0fbc'}

# The SHAD or NYIS SHAD are not to be drawn if followed by these letters
SHAD_IRREGULAR = [U_ROOTLETTERS[0], U_ROOTLETTERS[2]]

S_DONT_STACK = ('phaṭ', )

SNA_LDAN_CASES = ('hūṃ', 'hkṣmlvryaṃ', 'ddhaṃ', )

SW_YATA_REGEX = (
    # ya followed by one or two vowels and preceded by kṣ, t, ś, s, h
    ('(kṣ|t|ś|s|h)y({}){{1,2}}$'.format('|'.join(SW_VOWELS))),
    ('(k|c)yai'),
    ('phyv'),
    # TODO: handle n.y
    ('(k|d|b|m|n)y'), )

SW_RATA_REGEX = (
    # ra followed by one or two vowels and preceded by t, th, bh, s
    ('(t|th|bh|s)r({}){{1,2}}$'.format('|'.join(SW_VOWELS))),
    ('kri'),
    ('(kh|k|d|b|m|g|n|p|ph|j)r'), )

SW_WAZUR_REGEX = (
    # va followed by one or two vowels and preceded by t, ḍ, d, dh, ś, s, tr
    ('(t|ḍ|d|dh|ś|s|tr)v({}){{1,2}}$'.format('|'.join(SW_VOWELS))),
    ('phyv'),
    ('(y|j|l|h)v'), )

SW_REGEX = {
    SW_ROOTLETTERS[28]: SW_WAZUR_REGEX,
    SW_ROOTLETTERS[25]: SW_YATA_REGEX,
    SW_ROOTLETTERS[26]: SW_RATA_REGEX}

S_ACHUNG = W_ROOTLETTERS[22]
U_ACHUNG = U_ROOTLETTERS[22]

SW_AMBIGOUS = ('ts', 'tsh', 'dz', 'w', 'ny', 'ng', 'sh', )

SW_UNIQUE = (3, 4, 8, 9, 10, 11, 12, 13, 14, 18, 23, 28, 29, 30, 33, )

# TODO: find solution for the ww/wv ambiguity
