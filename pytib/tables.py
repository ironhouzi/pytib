# -*- coding: utf-8 -*-
import re

from pytib.exceptions import InvalidConfig

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
SW_VOWELS = (
    'a',         'ā',  W_VOWELS[0], 'ī',
    W_VOWELS[1], 'ū',  W_VOWELS[2], 'ai',
    W_VOWELS[3], 'au', 'ṛ',         'ṝ',
    'ḷ',         'ḹ',  'ṃ',         'ḥ'
)

# TODO: Investigate discouraged unicode chars (F73, F77, F79, F81)
# Tibetan Unicode vowels for Tibetan transliteration of Sanskrit
SU_VOWELS = (
    '\u0f68',    '\u0f71', U_VOWELS[0], '\u0f73',
    U_VOWELS[1], '\u0f75', U_VOWELS[2], '\u0f7b',
    U_VOWELS[3], '\u0f7d', '\u0f76',    '\u0f77',
    '\u0f78',    '\u0f79', '\u0f7e',    '\u0f7f'
)

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


def generate_tables(config):
    ''' Dynamically generate lookup tables '''

    validate(config)

    tc = tuple(config.get('wylie_consonants', W_ROOTLETTERS))
    sc = tuple(config.get('sanskrit_consonants', SW_ROOTLETTERS))
    sv = tuple(config.get('sanskrit_vowels', SW_VOWELS))
    ga_prefixer = config.get('ga_prefixer', '.')
    latin_shads = config.get('shads', W_SYMBOLS)
    latin_vowel_a = tc[-1]
    latin_tibetan_alphabet = tc + W_VOWELS
    latin_indic_alphabet = (
        sc + sv + (tc[ACHUNG_INDEX],)
    )

    # TODO: n.y case needed??
    S_BASIC_RULES = (
        sc[21] + sc[25] + tc[19],       # phyw
        sc[3] + sc[26],                 # ghr
        sc[32] + sc[26] + sv[0],        # hra
        sc[32] + tc[19] + sv[0],        # hwa
        tc[16] + sc[25],                # tsy
        sc[15] + sc[26] + tc[19],       # trw
        sc[26] + sc[18],                # rdh
        sc[31] + sc[25] + sv[6],        # sye
        sc[31] + ga_prefixer + sc[25],  # n.y
        sc[3],              # gh
        sc[18],             # dh
        sc[5] + sc[25],     # cy
        sc[8],              # jh
        sc[19] + sc[19],    # nn
        sc[24] + sc[24],    # mm
        tc[19] + tc[19],    # ww
        sc[25] + sc[25],    # yy
        sc[26] + sc[26],    # rr
        sc[32] + sc[25],    # hy
        sc[15] + sc[25],    # ty
        sc[15] + sc[28],    # tv
        sc[15] + tc[19],    # tw
        sc[15] + tc[21],    # tz
        sc[23],             # bh
        sc[31] + sc[31]     # ss
    )

    S_DOUBLE_CONSONANTS = (
        sc[2] + sc[2],      # gg
        sc[17] + sc[17],    # dd
        sc[22] + sc[22]     # bb
    )

    SNA_LDAN_CASES = (
        sc[32] + sv[5] + sv[14],        # hūṃ
        (sc[32] + sc[33] + sc[24]
         + sc[27] + sc[28] + sc[26]
         + sc[25] + sv[0] + sv[14]),    # hkṣmlvryaṃ
        sc[17] + sc[18] + sv[0]         # 'ddhaṃ'
    )

    re_vow = '|'.join(sv)
    phyv = sc[21] + sc[25] + sc[28]
    kri = sc[0] + sc[26] + sv[2]

    SW_YATA_REGEX = (
        # ya followed by one or two vowels and preceded by kṣ, t, ś, s, h
        re.compile(f'({sc[33]}|{sc[15]}|{sc[29]}|{sc[31]}|{sc[32]})'
                   f'{sc[25]}({re_vow}){{1,2}}$'),
        re.compile(f'({sc[0]}|{sc[5]}){sc[25]}{sv[7]}'),  # (k|c)yai
        re.compile(phyv),
        # TODO: handle n.y
        re.compile(  # (k|d|b|m|n)y
            f'({sc[0]}|{sc[17]}|{sc[22]}|{sc[24]}|{sc[19]}){sc[25]}'
        )
    )

    SW_RATA_REGEX = (
        # ra followed by one or two vowels and preceded by t, th, bh, s
        re.compile(
            f'({sc[15]}|{sc[16]}|{sc[23]}|{sc[31]}){sc[26]}({re_vow}){{1,2}}$'),
        re.compile(kri),
        re.compile(  # (kh|k|d|b|m|g|n|p|ph|j)r
            f'({sc[1]}|{sc[0]}|{sc[17]}|{sc[22]}|{sc[24]}|{sc[2]}|'
            f'{sc[19]}|{sc[20]}|{sc[21]}|{sc[7]}){sc[26]}')
    )

    SW_WAZUR_REGEX = (
        # va followed by one or two vowels and preceded by t, ḍ, d, dh, ś, s, tr
        re.compile(f'({sc[15]}|{sc[12]}|{sc[17]}|{sc[18]}|{sc[29]}|{sc[31]}|'
                   f'{sc[15]}{sc[26]}){sc[28]}({re_vow}){{1,2}}$'),
        re.compile(phyv),
        re.compile(f'({sc[25]}|{sc[7]}|{sc[27]}|{sc[32]}){sc[28]}')
    )

    SW_REGEX = {
        sc[28]: SW_WAZUR_REGEX,
        sc[25]: SW_YATA_REGEX,
        sc[26]: SW_RATA_REGEX
    }

    SW_OM = sv[8] + sv[14]

    tables = {
        'CONSONANTS': tc,
        'LATIN_VOWEL_A': latin_vowel_a,
        'LATIN_A_CHUNG': tc[ACHUNG_INDEX],
        'TIBETAN_VOWELS': W_VOWELS + (latin_vowel_a,),
        'LATIN_TIBETAN_ALPHABET': latin_tibetan_alphabet,
        'LATIN_TIBETAN_ALPHABET_SET': set(latin_tibetan_alphabet),
        'LATIN_INDIC_ALPHABET_SET': set(latin_indic_alphabet),
        'GA_PREFIX': ''.join([tc[2], ga_prefixer]),
        'PREFIXES': get_chars(PREFIXES_I, tc),
        'VALID_SUFFIX': suffix_rules(tc),
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
        'SW_VOWELS': sv,
        'W_VOWELS': W_VOWELS,
        'SW_ROOTLETTERS': sc,
        'SW_REGEX': SW_REGEX,
        'STACK': STACK,
        'SNA_LDAN_CASES': SNA_LDAN_CASES,
        'S_DOUBLE_CONSONANTS': S_DOUBLE_CONSONANTS,
        'LATIN_SHADS': latin_shads,
        'SYMBOL_LOOKUP': dict(zip(latin_shads, U_SYMBOLS)),
        'SPECIAL_CASE': {
            SW_OM: U_OM,             # oṃ
            tc[16] + tc[29] + tc[11] + tc[10] + tc[29] + tc[11]: (    # tsandan
                '\u0f59' + '\u0f53' + '\u0fa1' + '\u0f53')
        }

    }

    tables['SUPERJOIN'], tables['VALID_SUPERJOIN'] = defs(
        (RAGO_INDICES, LAGO_INDICES, SAGO_INDICES),
        SUPER_INDICES,
        tc
    )

    tables['SUB'], tables['VALID_SUBJOINED_LIST'] = defs(
        (WAZUR_INDICES, YATA_INDICES, RATA_INDICES, LATA_INDICES),
        SUB_INDICES,
        tc
    )

    return tables


def validate(config):
    config_types = (
        ('wylie_consonants', W_ROOTLETTERS),
        ('shads', W_SYMBOLS),
        ('ga_prefixer', ('.',)),
        ('sanskrit_consonants', SW_ROOTLETTERS),
        ('sanskrit_vowels', SW_VOWELS)
    )

    for name, default in config_types:
        config_item = config.get(name)

        if config_item:
            missing = len(default) - len(config_item)
            if missing != 0:
                raise InvalidConfig(
                    f'Too few letters - missing: {missing}',
                    config_item
                )
            if not len(set(config_item)) == len(config_item):
                raise InvalidConfig(
                    'Duplicate letters not allowed!',
                    config_item
                )
