W_ROOTLETTERS = [
    'k',  'kh',  'g',  'ng',
    'c',  'ch',  'j',  'ny',
    't',  'th',  'd',  'n',
    'p',  'ph',  'b',  'm',
    'ts', 'tsh', 'dz', 'w',
    'zh', 'z',   '\'', 'y',
    'r',  'l',   'sh', 's',
    'h',  'a']

U_ROOTLETTERS = [
    u'\u0f40', u'\u0f41', u'\u0f42', u'\u0f44',
    u'\u0f45', u'\u0f46', u'\u0f47', u'\u0f49',
    u'\u0f4f', u'\u0f50', u'\u0f51', u'\u0f53',
    u'\u0f54', u'\u0f55', u'\u0f56', u'\u0f58',
    u'\u0f59', u'\u0f5a', u'\u0f5b', u'\u0f5d',
    u'\u0f5e', u'\u0f5f', u'\u0f60', u'\u0f61',
    u'\u0f62', u'\u0f63', u'\u0f64', u'\u0f66',
    u'\u0f67', u'\u0f68']

W_VOWELS = ['i', 'u', 'e', 'o', 'a']

U_VOWELS = [u'\u0f72', u'\u0f74', u'\u0f7a', u'\u0f7c']

SUPER = ['r', 'l', 's']

SUB = ['y', 'r', 'l', 'w']

PREFIXES = ['g', 'd', 'b', 'm', '\'']

SUFFIXES = ['g', 'ng', 'd', 'n', 'b',
            'm', '\'', 'r', 'l', 's']

SUFFIX2S = ['s' 'd']

RA_GO = ['k', 'g', 'ng', 'j', 'ny', 't',
         'd', 'n', 'b',  'm', 'ts', 'dz']

LA_GO = ['k', 'g', 'ng', 'ch', 'j',
         't', 'd', 'p',  'b',  'h']

SA_GO = ['k', 'g', 'ng', 'ny', 't',
         'd', 'n', 'p',  'b',  'm', 'ts']

YA_TA = ['k', 'kh', 'g', 'p', 'ph', 'b', 'm', 'h']

RA_TA = ['k', 'kh', 'g', 't', 'th', 'd',
         'n', 'p', 'ph', 'b', 'm',  's', 'h']

LA_TA = ['k', 'g', 'b', 'r', 's', 'z']

WA_ZUR = ['k',   'kh', 'g', 'ny', 'd', 'ts',
          'tsh', 'zh', 'z', 'r',  'l', 'sh', 'h']

SUPER_RULES = [RA_GO, LA_GO, SA_GO]

SUB_RULES = [YA_TA, RA_TA, LA_TA, WA_ZUR]

SYLLSTRUCT = ['prefix',
              'super',
              'root',
              'subjoined',
              'vowel',
              'suffix',
              'suffix2']
