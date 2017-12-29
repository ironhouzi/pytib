# -*- coding: utf-8 -*-
import re
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
    'h',  'a'
)

# Tibetan Unicode consonants
U_ROOTLETTERS = (
    '\u0f40', '\u0f41', '\u0f42', '\u0f44',
    '\u0f45', '\u0f46', '\u0f47', '\u0f49',
    '\u0f4f', '\u0f50', '\u0f51', '\u0f53',
    '\u0f54', '\u0f55', '\u0f56', '\u0f58',
    '\u0f59', '\u0f5a', '\u0f5b', '\u0f5d',
    '\u0f5e', '\u0f5f', '\u0f60', '\u0f61',
    '\u0f62', '\u0f63', '\u0f64', '\u0f66',
    '\u0f67', '\u0f68'
)

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
    'h', 'kṣ'
)

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
    U_ROOTLETTERS[28], '\u0f69'
)

# Wylie/latin vowels
W_VOWELS = ('i', 'u', 'e', 'o')

# Tibetan Unicode vowels
U_VOWELS = ('\u0f72', '\u0f74', '\u0f7a', '\u0f7c')

# Latin vowels for transliteration of sanskrit (IAST)
# TODO: replace char litterals with codepoints.
SW_VOWELS = (
    'a',         'ā',  W_VOWELS[0], 'ī',
    W_VOWELS[1], 'ū',  W_VOWELS[2], 'ai',
    W_VOWELS[3], 'au', 'ṛ',         'ṝ',
    'ḷ',         'ḹ',  'ṃ',         'ḥ'
)

# Tibetan Unicode vowels for Tibetan transliteration of Sanskrit
SU_VOWELS = (
    '\u0f68',    '\u0f71', U_VOWELS[0], '\u0f73',
    U_VOWELS[1], '\u0f75', U_VOWELS[2], '\u0f7b',
    U_VOWELS[3], '\u0f7d', '\u0f76',    '\u0f77',
    '\u0f78',    '\u0f79', '\u0f7e',    '\u0f7f'
)

SW_OM = SW_VOWELS[8] + SW_VOWELS[14]

U_TSHEG = '\u0f0b'
U_SHAD = '\u0f0d'
U_NYIS_SHAD = '\u0f0e'
U_SNA_LDAN = '\u0f83'
U_OM = '\u0f00'

SPECIAL_CASE = {
    'oṃ': '\u0f00',
    'tsandan': '\u0f59' + '\u0f53' + '\u0fa1' + '\u0f53'
}

W_SYMBOLS = ('/', '//')
U_SYMBOLS = (U_SHAD, U_NYIS_SHAD)


def get_chars(indices, alphabet):
    return tuple(alphabet[index] for index in indices)


def defs(index_groups, char_indices, rootletters):
    group = get_chars(char_indices, rootletters)
    rules = tuple(get_chars(indices, rootletters) for indices in index_groups)
    valid_list = dict(zip(group, rules))
    return group, valid_list


def suffix_rules(rootletters):
    suffixes = get_chars(SUFFIXES_I, rootletters)
    sec_suffixes = get_chars(SUFFIX2S_I, rootletters)
    return dict(zip(POSTVOWEL, (suffixes, sec_suffixes)))


# Valid characters for superjoined wylie
# ['r', 'l', 's']
SUPER_INDICES = (24, 25, 27)

# Valid characters for subjoined wylie
# ['w', 'y', 'r', 'l']
SUB_INDICES = (19, 23, 24, 25)

# Valid characters for wylie prefixes
# ['g', 'd', 'b', 'm', '\'']
PREFIXES_I = (2,  10, 14, 15, 22)

# Valid characters for wylie suffixes
# ['g', 'ng', 'd', 'n', 'b', 'm', '\'', 'r', 'l', 's']
SUFFIXES_I = (2,  3,  10, 11, 14, 15, 22, 24, 25, 27)

# Valid characters for wylie second suffixes
# ['s' 'd']
SUFFIX2S_I = (27, 10)

# Wylie characters that take the 'ra' character as its superjoined letter.
#  ['k', 'g', 'ng', 'j', 'ny', 't', 'd', 'n', 'b',  'm', 'ts', 'dz']
RAGO_INDICES = (0,  2,  3, 6,  7,  8, 10, 11, 14, 15, 16, 18)

# Wylie characters that take the 'la' character as its superjoined letter.
#  ['k', 'g', 'ng', 'c', 'j', 't', 'd', 'p',  'b', 'h']
LAGO_INDICES = (0,  2,  3, 4,  6,  8, 10, 12, 14, 28)

# Wylie characters that take the 'sa' character as its superjoined letter.
#  ['k', 'g', 'ng', 'ny', 't', 'd', 'n', 'p',  'b',  'm', 'ts']
SAGO_INDICES = (0,  2,  3, 7,  8,  10, 11, 12, 14, 15, 16)

# Wylie characters that take the 'ya' character as its subjoined letter.
#  ['k', 'kh', 'g', 'p', 'ph', 'b', 'm', 'h']
YATA_INDICES = (0,  1,  2, 12, 13, 14, 15, 28)

# Wylie characters that take the 'ra' character as its subjoined letter.
#  ['k', 'kh', 'g', 't', 'th', 'd', 'n', 'p', 'ph', 'b', 'm',  's', 'h']
RATA_INDICES = (0,  1,  2, 8,  9,  10, 11, 12, 13, 14, 15, 27, 28)

# Wylie characters that take the 'la' character as its subjoined letter.
#  ['k', 'g', 'b', 'r', 's', 'z']
LATA_INDICES = (0,  2,  14, 24, 27, 21)

# Wylie characters that take the 'wa' character as its subjoined letter.
# ['k', 'kh', 'g', 'c', 'ny', 't', 'd', 'ts', 'tsh', 'zh', 'z', 'r', 'l', 'sh',
#  's', 'h']
WAZUR_INDICES = (0,  1,  2, 4,  7,  8, 10, 16, 17, 20, 21, 24, 25, 26, 27, 28)

# Syllable objects have the following structure. The individual elements are
# referred to as 'components', or 'syllable components'.

POSTVOWEL = (
    'suffix',
    'suffix2',
    'genitive',
    'genvowel'
)

SUBOFFSET = 0x50

# Normal stacking without subjoining for: 'va', 'ya', 'ra'
STACK = {
    SW_ROOTLETTERS[28]: '\u0fba',
    SW_ROOTLETTERS[25]: '\u0fbb',
    SW_ROOTLETTERS[26]: '\u0fbc'
}

# The SHAD or NYIS SHAD are not to be drawn if followed by these letters
SHAD_IRREGULAR = (U_ROOTLETTERS[0], U_ROOTLETTERS[2])

ACHUNG_INDEX = 22
U_ACHUNG = U_ROOTLETTERS[22]

# TODO: find solution for the ww/wv ambiguity


def create_lookup(cfg={}):
    c = tuple(cfg.get('consonants', W_ROOTLETTERS))
    ga_prefixer = cfg.get('ga_prefixer', '.')
    latin_shads = cfg.get('shads', W_SYMBOLS)
    latin_vowel_a = c[-1]
    latin_tibetan_alphabet = c + W_VOWELS
    latin_indic_alphabet = (
        SW_ROOTLETTERS + SW_VOWELS + (c[ACHUNG_INDEX],)
    )

    # TODO: n.y case needed??
    S_BASIC_RULES = (
        SW_ROOTLETTERS[21] + SW_ROOTLETTERS[25] + W_ROOTLETTERS[19],    # phyw
        SW_ROOTLETTERS[3] + SW_ROOTLETTERS[26],     # ghr
        SW_ROOTLETTERS[32] + SW_ROOTLETTERS[26] + SW_VOWELS[0],     # hra
        SW_ROOTLETTERS[32] + W_ROOTLETTERS[19] + SW_VOWELS[0],      # hwa
        W_ROOTLETTERS[16] + SW_ROOTLETTERS[25],     # tsy
        SW_ROOTLETTERS[15] + SW_ROOTLETTERS[26] + W_ROOTLETTERS[19],    # trw
        SW_ROOTLETTERS[26] + SW_ROOTLETTERS[18],    # rdh
        SW_ROOTLETTERS[31] + SW_ROOTLETTERS[25] + SW_VOWELS[6],    # sye
        SW_ROOTLETTERS[31] + ga_prefixer + SW_ROOTLETTERS[25],    # n.y
        SW_ROOTLETTERS[3],  # gh
        SW_ROOTLETTERS[18],  # dh
        SW_ROOTLETTERS[5] + SW_ROOTLETTERS[25],  # cy
        SW_ROOTLETTERS[8],  # jh
        SW_ROOTLETTERS[19] + SW_ROOTLETTERS[19],  # nn
        SW_ROOTLETTERS[24] + SW_ROOTLETTERS[24],  # mm
        W_ROOTLETTERS[19] + W_ROOTLETTERS[19],  # ww
        SW_ROOTLETTERS[25] + SW_ROOTLETTERS[25],  # yy
        SW_ROOTLETTERS[26] + SW_ROOTLETTERS[26],  # rr
        SW_ROOTLETTERS[32] + SW_ROOTLETTERS[25],  # hy
        SW_ROOTLETTERS[15] + SW_ROOTLETTERS[25],  # ty
        SW_ROOTLETTERS[15] + SW_ROOTLETTERS[28],  # tv
        SW_ROOTLETTERS[15] + W_ROOTLETTERS[19],  # tw
        SW_ROOTLETTERS[15] + W_ROOTLETTERS[21],  # tz
        SW_ROOTLETTERS[23],  # bh
        SW_ROOTLETTERS[31] + SW_ROOTLETTERS[31]   # ss
    )

    S_DOUBLE_CONSONANTS = (
        SW_ROOTLETTERS[2] + SW_ROOTLETTERS[2],      # gg
        SW_ROOTLETTERS[17] + SW_ROOTLETTERS[17],    # dd
        SW_ROOTLETTERS[22] + SW_ROOTLETTERS[22]     # bb
    )

    SNA_LDAN_CASES = (
        SW_ROOTLETTERS[32] + SW_VOWELS[5] + SW_VOWELS[14],     # hūṃ
        (SW_ROOTLETTERS[32] + SW_ROOTLETTERS[33] + SW_ROOTLETTERS[24]
         + SW_ROOTLETTERS[27] + SW_ROOTLETTERS[28] + SW_ROOTLETTERS[26]
         + SW_ROOTLETTERS[25] + SW_VOWELS[0] + SW_VOWELS[14]),     # hkṣmlvryaṃ
        SW_ROOTLETTERS[17] + SW_ROOTLETTERS[18] + SW_VOWELS[0]    # 'ddhaṃ'
    )

    re_vow = '|'.join(SW_VOWELS)
    phyv = SW_ROOTLETTERS[21] + SW_ROOTLETTERS[25] + SW_ROOTLETTERS[28]
    kri = SW_ROOTLETTERS[0] + SW_ROOTLETTERS[26] + SW_VOWELS[2]

    SW_YATA_REGEX = (
        # ya followed by one or two vowels and preceded by kṣ, t, ś, s, h
        re.compile(
            f'({SW_ROOTLETTERS[33]}|{SW_ROOTLETTERS[15]}|{SW_ROOTLETTERS[29]}|'
            f'{SW_ROOTLETTERS[31]}|{SW_ROOTLETTERS[32]}){SW_ROOTLETTERS[25]}'
            f'({re_vow}){{1,2}}$'),
        re.compile(
            f'({SW_ROOTLETTERS[0]}|{SW_ROOTLETTERS[5]})'
            f'{SW_ROOTLETTERS[25]}{SW_VOWELS[7]}'),  # (k|c)yai
        re.compile(phyv),
        # TODO: handle n.y
        re.compile(  # (k|d|b|m|n)y
            f'({SW_ROOTLETTERS[0]}|{SW_ROOTLETTERS[17]}|{SW_ROOTLETTERS[22]}|'
            f'{SW_ROOTLETTERS[24]}|{SW_ROOTLETTERS[19]}){SW_ROOTLETTERS[25]}'
        )
    )

    SW_RATA_REGEX = (
        # ra followed by one or two vowels and preceded by t, th, bh, s
        re.compile(
            f'({SW_ROOTLETTERS[15]}|{SW_ROOTLETTERS[16]}|{SW_ROOTLETTERS[23]}|'
            f'{SW_ROOTLETTERS[31]}){SW_ROOTLETTERS[26]}({re_vow}){{1,2}}$'),
        re.compile(kri),
        re.compile(  # (kh|k|d|b|m|g|n|p|ph|j)r
            f'({SW_ROOTLETTERS[1]}|{SW_ROOTLETTERS[0]}|{SW_ROOTLETTERS[17]}|'
            f'{SW_ROOTLETTERS[22]}|{SW_ROOTLETTERS[24]}|{SW_ROOTLETTERS[2]}|'
            f'{SW_ROOTLETTERS[19]}|{SW_ROOTLETTERS[20]}|{SW_ROOTLETTERS[21]}|'
            f'{SW_ROOTLETTERS[7]}){SW_ROOTLETTERS[26]}')
    )

    SW_WAZUR_REGEX = (
        # va followed by one or two vowels and preceded by t, ḍ, d, dh, ś, s, tr
        re.compile(
            f'({SW_ROOTLETTERS[15]}|{SW_ROOTLETTERS[12]}|{SW_ROOTLETTERS[17]}|'
            f'{SW_ROOTLETTERS[18]}|{SW_ROOTLETTERS[29]}|{SW_ROOTLETTERS[31]}|'
            f'{SW_ROOTLETTERS[15]}{SW_ROOTLETTERS[26]}){SW_ROOTLETTERS[28]}'
            f'({re_vow}){{1,2}}$'),
        re.compile(phyv),
        re.compile(
            f'({SW_ROOTLETTERS[25]}|{SW_ROOTLETTERS[7]}|{SW_ROOTLETTERS[27]}'
            f'|{SW_ROOTLETTERS[32]}){SW_ROOTLETTERS[28]}')
    )

    SW_REGEX = {
        SW_ROOTLETTERS[28]: SW_WAZUR_REGEX,
        SW_ROOTLETTERS[25]: SW_YATA_REGEX,
        SW_ROOTLETTERS[26]: SW_RATA_REGEX
    }

    lookup = {
        'CONSONANTS': c,
        'LATIN_VOWEL_A': latin_vowel_a,
        'LATIN_A_CHUNG': c[ACHUNG_INDEX],
        'TIBETAN_VOWELS': W_VOWELS + (latin_vowel_a,),
        'LATIN_TIBETAN_ALPHABET': latin_tibetan_alphabet,
        'LATIN_TIBETAN_ALPHABET_SET': set(latin_tibetan_alphabet),
        'LATIN_INDIC_ALPHABET_SET': set(latin_indic_alphabet),
        'GA_PREFIX': ''.join([c[2], ga_prefixer]),
        'PREFIXES': get_chars(PREFIXES_I, c),
        'VALID_SUFFIX': suffix_rules(c),
        'TIBETAN_UNICODE': dict(
            zip(latin_tibetan_alphabet, U_ROOTLETTERS + U_VOWELS)
        ),
        'TIBINDIC_UNICODE': dict(zip(
            latin_indic_alphabet,
            SU_ROOTLETTERS + SU_VOWELS + (U_ACHUNG,)
        )),
        'MAX_TIB_CHAR_LEN': max(len(char) for char in latin_tibetan_alphabet),
        'MAX_INDIC_CHAR_LEN': max(len(char) for char in latin_indic_alphabet),
        'S_BASIC_RULES': S_BASIC_RULES,
        'SW_VOWELS': SW_VOWELS,
        'W_VOWELS': W_VOWELS,
        'SW_ROOTLETTERS': SW_ROOTLETTERS,
        'SW_REGEX': SW_REGEX,
        'STACK': STACK,
        'SNA_LDAN_CASES': SNA_LDAN_CASES,
        'S_DOUBLE_CONSONANTS': S_DOUBLE_CONSONANTS,
        'LATIN_SHADS': latin_shads,
        'SYMBOL_LOOKUP': dict(zip(latin_shads, U_SYMBOLS)),
        'SPECIAL_CASE': {
            SW_OM: U_OM,             # oṃ
            c[16] + c[29] + c[11] + c[10] + c[29] + c[11]: (    # tsandan
                '\u0f59' + '\u0f53' + '\u0fa1' + '\u0f53')
        }

    }

    lookup['SUPERJOIN'], lookup['VALID_SUPERJOIN'] = defs(
        (RAGO_INDICES, LAGO_INDICES, SAGO_INDICES),
        SUPER_INDICES,
        c
    )

    lookup['SUB'], lookup['VALID_SUBJOINED_LIST'] = defs(
        (WAZUR_INDICES, YATA_INDICES, RATA_INDICES, LATA_INDICES),
        SUB_INDICES,
        c
    )

    return lookup
