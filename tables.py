# -*- coding: utf-8 -*-
# TODO remove utf8 requirement for this file

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
    W_ROOTLETTERS[0],  W_ROOTLETTERS[1],  W_ROOTLETTERS[2],  'gh',
    'ṅ',               W_ROOTLETTERS[4],  W_ROOTLETTERS[5],  W_ROOTLETTERS[6],
    'jh',              'ñ',               'ṭ',               'ṭh',
    'ḍ',               'ḍh',              'ṇ',               W_ROOTLETTERS[8],
    W_ROOTLETTERS[9],  W_ROOTLETTERS[10], 'dh',              W_ROOTLETTERS[11],
    W_ROOTLETTERS[12], W_ROOTLETTERS[13], W_ROOTLETTERS[14], 'bh',
    W_ROOTLETTERS[15], W_ROOTLETTERS[23], W_ROOTLETTERS[24], W_ROOTLETTERS[25],
    'v',               'ś',               'ṣ',               W_ROOTLETTERS[27],
    W_ROOTLETTERS[28], 'kṣ', )

# Tibetan Unicode consonants for Tibetan transliteration of Sanskrit
SU_ROOTLETTERS = (
    U_ROOTLETTERS[0],  U_ROOTLETTERS[1],  U_ROOTLETTERS[2],  '\u0f43',
    U_ROOTLETTERS[3],  U_ROOTLETTERS[4],  U_ROOTLETTERS[5],  U_ROOTLETTERS[6],
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

S_TSHEG = '\u0f0b'
S_SPACE = '\u00a0'
S_SHAD = '\u0f0d'
S_NYIS_SHAD = '\u0f0e'
S_SNA_LDAN = '\u0f83'
S_OM = '\u0f00'

W_SYMBOLS = ('/', '//', )

U_SYMBOLS = (S_SHAD, S_NYIS_SHAD, )

# Valid characters for superjoined wylie
# ['r', 'l', 's']
SUPER = (W_ROOTLETTERS[24], W_ROOTLETTERS[25], W_ROOTLETTERS[27], )

# Valid characters for subjoined wylie
# ['w', 'y', 'r', 'l']
SUB = (W_ROOTLETTERS[19], W_ROOTLETTERS[23], W_ROOTLETTERS[24],
       W_ROOTLETTERS[25], )

# Valid characters for wylie prefixes
# ['g', 'd', 'b', 'm', '\'']
PREFIXES = (W_ROOTLETTERS[2],  W_ROOTLETTERS[10], W_ROOTLETTERS[14],
            W_ROOTLETTERS[15], W_ROOTLETTERS[22], )

# Valid characters for wylie suffixes
# ['g', 'ng', 'd', 'n', 'b', 'm', '\'', 'r', 'l', 's']
SUFFIXES = (W_ROOTLETTERS[2],  W_ROOTLETTERS[3],  W_ROOTLETTERS[10],
            W_ROOTLETTERS[11], W_ROOTLETTERS[14], W_ROOTLETTERS[15],
            W_ROOTLETTERS[22], W_ROOTLETTERS[24], W_ROOTLETTERS[25],
            W_ROOTLETTERS[27], )

# Valid characters for wylie second suffixes
# ['s' 'd']
SUFFIX2S = (W_ROOTLETTERS[27], W_ROOTLETTERS[10], )

# Wylie characters that take the 'ra' character as its superjoined letter.
#  ['k', 'g', 'ng', 'j', 'ny', 't', 'd', 'n', 'b',  'm', 'ts', 'dz']
RAGO_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[2],  W_ROOTLETTERS[3],
                    W_ROOTLETTERS[6],  W_ROOTLETTERS[7],  W_ROOTLETTERS[8],
                    W_ROOTLETTERS[10], W_ROOTLETTERS[11], W_ROOTLETTERS[14],
                    W_ROOTLETTERS[15], W_ROOTLETTERS[16], W_ROOTLETTERS[18], )

# Wylie characters that take the 'la' character as its superjoined letter.
#  ['k', 'g', 'ng', 'c', 'j', 't', 'd', 'p',  'b', 'h']
LAGO_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[2],  W_ROOTLETTERS[3],
                    W_ROOTLETTERS[4],  W_ROOTLETTERS[6],  W_ROOTLETTERS[8],
                    W_ROOTLETTERS[10], W_ROOTLETTERS[12], W_ROOTLETTERS[14],
                    W_ROOTLETTERS[28], )

# Wylie characters that take the 'sa' character as its superjoined letter.
#  ['k', 'g', 'ng', 'ny', 't', 'd', 'n', 'p',  'b',  'm', 'ts']
SAGO_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[2],  W_ROOTLETTERS[3],
                    W_ROOTLETTERS[7],  W_ROOTLETTERS[8],  W_ROOTLETTERS[10],
                    W_ROOTLETTERS[11], W_ROOTLETTERS[12], W_ROOTLETTERS[14],
                    W_ROOTLETTERS[15], W_ROOTLETTERS[16], )

# Wylie characters that take the 'ya' character as its subjoined letter.
#  ['k', 'kh', 'g', 'p', 'ph', 'b', 'm', 'h']
YATA_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[1],  W_ROOTLETTERS[2],
                    W_ROOTLETTERS[12], W_ROOTLETTERS[13], W_ROOTLETTERS[14],
                    W_ROOTLETTERS[15], W_ROOTLETTERS[28], )

# Wylie characters that take the 'ra' character as its subjoined letter.
#  ['k', 'kh', 'g', 't', 'th', 'd', 'n', 'p', 'ph', 'b', 'm',  's', 'h']
RATA_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[1],  W_ROOTLETTERS[2],
                    W_ROOTLETTERS[8],  W_ROOTLETTERS[9],  W_ROOTLETTERS[10],
                    W_ROOTLETTERS[11], W_ROOTLETTERS[12], W_ROOTLETTERS[13],
                    W_ROOTLETTERS[14], W_ROOTLETTERS[15], W_ROOTLETTERS[27],
                    W_ROOTLETTERS[28], )

# Wylie characters that take the 'la' character as its subjoined letter.
#  ['k', 'g', 'b', 'r', 's', 'z']
LATA_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[2],  W_ROOTLETTERS[14],
                    W_ROOTLETTERS[24], W_ROOTLETTERS[27], W_ROOTLETTERS[21], )

# Wylie characters that take the 'wa' character as its subjoined letter.
# ['k', 'kh', 'g', 'c', 'ny', 't', 'd', 'ts', 'tsh', 'zh', 'z', 'r', 'l', 'sh',
#  's', 'h']
WAZUR_ROOTLETTERS = (W_ROOTLETTERS[0],  W_ROOTLETTERS[1],  W_ROOTLETTERS[2],
                     W_ROOTLETTERS[4],  W_ROOTLETTERS[7],  W_ROOTLETTERS[8],
                     W_ROOTLETTERS[10], W_ROOTLETTERS[16], W_ROOTLETTERS[17],
                     W_ROOTLETTERS[20], W_ROOTLETTERS[21], W_ROOTLETTERS[24],
                     W_ROOTLETTERS[25], W_ROOTLETTERS[26], W_ROOTLETTERS[27],
                     W_ROOTLETTERS[28], )

# 'g.' to define a W_ROOTLETTERS[2] prefix with a 'ya' root letter.
PREFIX_GA = ''.join([W_ROOTLETTERS[2], '.'])

SUPER_RULES = (RAGO_ROOTLETTERS, LAGO_ROOTLETTERS, SAGO_ROOTLETTERS, )

SUB_RULES = (YATA_ROOTLETTERS, RATA_ROOTLETTERS,
             LATA_ROOTLETTERS, WAZUR_ROOTLETTERS, )


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
STACK = {
    'v': '\u0fba',
    'y': '\u0fbb',
    'r': '\u0fbc'}

# The SHAD or NYIS SHAD are not to be drawn if followed by these letters
SHAD_IRREGULAR = [U_ROOTLETTERS[0], U_ROOTLETTERS[2]]

# TODO improve rule string litterals system agnostic, by referrencing to
#      main rootletters or vowels
S_RULES_4 = ('phyw', )

# TODO: n.y case needed??
S_RULES_3 = ('ghr', 'hra', 'hwa', 'tsy', 'trw', 'rdh', 'sye', 'n.y', )

S_RULES_2 = ('gh', 'dh', 'cy', 'jh', 'nn', 'mm', 'ww', 'yy', 'rr', 'hy', 'ty',
             'tv', 'tw', 'tz', 'bh', 'ss', )

S_BASIC_RULES = S_RULES_4 + S_RULES_3 + S_RULES_2

S_DOUBLE_CONSONANTS = ('gg', 'dd', 'bb', )

S_DONT_STACK = ('phaṭ', )

SNA_LDAN_CASES = ('hūṃ', 'hkṣmlvryaṃ', )

SW_YATA_CASES = (
    ('k', 'y'),
    ('d', 'y'),
    ('b', 'y'),
    ('m', 'y'),
    ('k', 'y', 'ai'),
    ('c', 'y', 'ai'),
    ('ph', 'y', 'v'),
    ('t', 'y', '$'),
    ('ś', 'y', '$'),
    ('h', 'y', '$'),
    ('kṣ', 'y', '$'),
    ('s', 'y', '$'), )

SW_RATA_CASES = (
    ('k', 'r'),
    ('g', 'r'),
    ('d', 'r'),
    ('n', 'r'),
    ('p', 'r'),
    ('ph', 'r'),
    ('b', 'r'),
    ('m', 'r'),
    ('dz', 'r'),
    ('k', 'r', 'i'),
    ('kh', 'r'),
    ('t', 'r', '$'),
    ('th', 'r', '$'),
    ('bh', 'r', '$'),
    ('s', 'r', '$'), )

SW_WAZUR_CASES = (
    ('j', 'v'),
    ('ph', 'y', 'v'),
    ('y', 'v'),
    ('ṭ', 'v', '$'),
    ('ḍ', 'v', '$'),
    ('t', 'v', '$'),
    ('l', 'v'),
    ('h', 'v'),
    ('d', 'v', '$'),
    ('dh', 'v', '$'),
    ('ś', 'v', '$'),
    ('s', 'v', '$'),
    ('t', 'r', 'v', '$'), )

SW_AMBIGOUS = ('ts', 'tsh', 'dz', 'w', 'ny', 'ng', 'sh', )

SW_UNIQUE = (3, 4, 8, 9, 10, 11, 12, 13, 14, 18, 23, 28, 29, 30, 33, )

# TODO: find solution for the ww/wv ambiguity
