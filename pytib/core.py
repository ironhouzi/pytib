import logging
import itertools

from pytib.tables import SUBOFFSET, U_SNA_LDAN, POSTVOWEL
from pytib.exceptions import InvalidTibetan, InvalidSanskrit, ParseError


logger = logging.getLogger('pytib.core')


def valid_superscribe(head_letter, root_letter, table):
    return (
        head_letter in table['SUPERJOIN']
        and root_letter in table['VALID_SUPERJOIN'][head_letter]
    )


def valid_subscribe(root_letter, subjoined_letter, table):
    return (
        subjoined_letter in table['SUB'] and
        root_letter in table['VALID_SUBJOINED_LIST'][subjoined_letter]
    )


def is_superscribed(latin_letters, vowel_position, table):
    if vowel_position == 2:
        return (
            valid_superscribe(latin_letters[0], latin_letters[1], table)
            and not valid_subscribe(latin_letters[0], latin_letters[1], table)
        )
    else:   # vowel_position == 3
        return (
            latin_letters[0] in table['PREFIXES']
            and valid_superscribe(latin_letters[1], latin_letters[2], table)
            and not valid_subscribe(latin_letters[1], latin_letters[2], table)
        )


def is_subscribed(latin_letters, vowel_position, table):
    if vowel_position == 2:
        return (
            not valid_superscribe(latin_letters[0], latin_letters[1], table)
            and valid_subscribe(latin_letters[0], latin_letters[1], table)
        )
    else:   # vowel_position == 3
        return (
            latin_letters[0] in table['PREFIXES']
            and not valid_superscribe(latin_letters[1], latin_letters[2], table)
            and valid_subscribe(latin_letters[1], latin_letters[2], table)
        )


def vowel_pos_0(latin_letters, table):
    if not latin_letters[0] in table['TIBETAN_VOWELS']:
        raise ParseError

    return dict(root=latin_letters[0])


def vowel_pos_1(latin_letters, table):
    if (not latin_letters[0] in table['CONSONANTS']
       and latin_letters[1] in table['TIBETAN_VOWELS']):
        raise ParseError

    return dict(root=latin_letters[0], vowel=latin_letters[1])


def vowel_pos_2(latin_letters, table):
    if is_subscribed(latin_letters, 2, table):
        result = dict(root=latin_letters[0], subjoined=latin_letters[1])
    elif is_superscribed(latin_letters, 2, table):
        result = dict(super=latin_letters[0], root=latin_letters[1])
    # TODO: investigate logical bug!
    elif (latin_letters[0] == table['GA_PREFIX']
          or latin_letters[0] in table['PREFIXES']
          and latin_letters[1] in table['CONSONANTS']):
        result = dict(prefix=latin_letters[0], root=latin_letters[1])
    else:
        raise ParseError

    result['vowel'] = latin_letters[2]

    return result


def vowel_pos_3(latin_letters, table):
    if latin_letters[2] == table['CONSONANTS'][19]\
       and latin_letters[1] == table['CONSONANTS'][24]:
        # syllable has both 'w' and 'r' as subscribed letters
        result = dict(root=latin_letters[0],
                      subjoined=latin_letters[1],
                      secondsub=latin_letters[2])
    elif is_superscribed(latin_letters, 3, table):
        result = dict(prefix=latin_letters[0],
                      super=latin_letters[1],
                      root=latin_letters[2])
    elif is_subscribed(latin_letters, 3, table):
        result = dict(prefix=latin_letters[0],
                      root=latin_letters[1],
                      subjoined=latin_letters[2])
    elif (latin_letters[0] in table['SUPERJOIN']
          and latin_letters[1] in table['CONSONANTS']
          and latin_letters[2] in table['SUB']):
        result = dict(super=latin_letters[0],
                      root=latin_letters[1],
                      subjoined=latin_letters[2])
    else:
        raise ParseError

    result['vowel'] = latin_letters[3]

    return result


def vowel_pos_4(latin_letters, table):
    if not (latin_letters[0] in table['PREFIXES']
            and latin_letters[1] in table['SUPERJOIN']
            and latin_letters[2] in table['CONSONANTS']
            and latin_letters[3] in table['SUB']):
        raise ParseError

    return dict(
        prefix=latin_letters[0],
        super=latin_letters[1],
        root=latin_letters[2],
        subjoined=latin_letters[3],
        vowel=latin_letters[4]
    )


analyze_syllable = (
    vowel_pos_0,
    vowel_pos_1,
    vowel_pos_2,
    vowel_pos_3,
    vowel_pos_4,
)

TIBETAN_VOWEL_LIMIT = len(analyze_syllable)


def find_suffixes(syllable, vowel_position, latin_letters, table):
    '''Identifies the syllable suffixes'''

    post_vowels = iter(POSTVOWEL)

    for latin_suffix in latin_letters[vowel_position+1:]:
        try:
            post_vowel = next(post_vowels)
        except StopIteration:
            break   # Disallow multiple genetive vowels

        invalid_suffix = (
            post_vowel in POSTVOWEL[:2]
            and latin_suffix not in table['TIBETAN_VOWELS']
            and latin_suffix not in table['VALID_SUFFIX'][post_vowel]
        )

        if invalid_suffix:
            raise ParseError

        syllable[post_vowel] = latin_suffix

    return syllable


def letter_partition(string, table, letter_set, char_limit):
    '''
    Checks if the roman character(s) at the end of the wylie/IAST string
    forms a valid wylie letter and continues backwards through the
    wylie/IAST string, until the entire wylie string is partitioned.
    '''

    alphabet = table[letter_set]
    found = False

    while len(string) != 0:
        for i in range(table[char_limit], 0, -1):
            part = string[:i]

            if part == '':
                break

            if part == table['GA_PREFIX'] or part in alphabet:
                found = True
                yield part
                string = string[i:]
            elif i == 1 and part not in alphabet:
                raise ParseError

    if not found:
        raise ParseError


def parse(string, table):
    '''
    Parses Tibetan syllable string from latin script to unicode,
    using lookup table.
    '''

    # Check if what could potentially be valid wylie, is actually Sanskrit
    if len(string) == 3 and string[:2] in table['S_DOUBLE_CONSONANTS']:
        sanskrit_quick_check = True
    # Check for clear case Sanskrit syllables to save time
    elif any(string.startswith(r) for r in table['S_BASIC_RULES']):
        sanskrit_quick_check = True
    elif any(v in string for v in ('ai', 'au')):
        sanskrit_quick_check = True
    else:
        sanskrit_quick_check = (
            table['LATIN_A_CHUNG'] not in string
            and len(tuple(c for c in string
                          if c in table['TIBETAN_VOWELS'])) >= 2
        )

    is_sanskrit = (
        sanskrit_quick_check or (
            not string.startswith(table['GA_PREFIX'])
            and not set(string) <= table['LATIN_TIBETAN_ALPHABET_SET']
        )
    )

    if is_sanskrit:
        return analyze_sanskrit(string, table)

    try:
        latin_letters = tuple(letter_partition(
            string,
            table,
            letter_set='LATIN_TIBETAN_ALPHABET_SET',
            char_limit='MAX_TIB_CHAR_LEN'
        ))
    except ParseError:
        return analyze_sanskrit(string, table)

    vowel_indices = (
        index for index, char in enumerate(latin_letters)
        if char in table['TIBETAN_VOWELS']
    )

    try:
        first_vowel_index = next(vowel_indices)
    except StopIteration:
        raise InvalidTibetan(string)

    if first_vowel_index >= TIBETAN_VOWEL_LIMIT:
        return analyze_sanskrit(string, table)

    try:
        syllable = analyze_syllable[first_vowel_index](latin_letters, table)
        find_suffixes(syllable, first_vowel_index, latin_letters, table)
    except ParseError:
        return analyze_sanskrit(string, table)

    return ''.join(to_unicode(syllable, table))


def atleast_n_vowels(string, n, table):
    '''String contains more than n tibetan vowels'''
    vowels = tuple(c for c in string if c in table['TIBETAN_VOWELS'])
    return len(vowels) >= n


def to_unicode(syllable, table):
    '''Generator yields tibetan unicode from latin syllable'''
    for syllable_component, latin_char in syllable.items():
        if latin_char == table['LATIN_VOWEL_A']\
           and syllable_component != 'root':
            continue

        if latin_char in table['W_VOWELS'] and syllable_component == 'root':
            yield (table['TIBETAN_UNICODE'][table['LATIN_VOWEL_A']])

        if latin_char == table['GA_PREFIX']:
            latin_char = table['CONSONANTS'][2]
            syllable[syllable_component] = latin_char

        needs_subjoin = (
            syllable_component == 'subjoined'
            or syllable_component == 'secondsub'
            or (
                syllable_component == 'root'
                and syllable.get('super') is not None
            )
        )

        if needs_subjoin:
            yield chr(SUBOFFSET + ord(table['TIBETAN_UNICODE'][latin_char]))
        else:
            yield table['TIBETAN_UNICODE'][latin_char]


def generate_stacks(latin_letters, table):
    ''' Group letters into stacks, represented by a list '''

    stack = []
    prev, curr = itertools.tee(latin_letters)
    curr_char = next(curr, None)

    for prev_char, curr_char in zip(prev, curr):
        stack.append(prev_char)
        prev_match = prev_char in table['SW_VOWELS']
        curr_match = curr_char in table['SW_VOWELS']

        if prev_match == curr_match:
            continue

        if prev_match:
            yield stack
            stack = []

    if curr_char:
        stack.append(curr_char)
        yield stack


def generate_sanskrit_unicode(latin_string, letter_stacks, table):
    try:
        yield table['SPECIAL_CASE'][latin_string]
        return
    except KeyError:
        pass

    literal_va = table['SW_ROOTLETTERS'][28]
    literal_ba = table['CONSONANTS'][14]
    literal_rv = table['SW_ROOTLETTERS'][26] + table['SW_ROOTLETTERS'][28]

    for i, stack in enumerate(letter_stacks):
        if stack[0] in table['SW_VOWELS'][1:]:   # avoid leading `a`
            yield table['TIBINDIC_UNICODE'][table['LATIN_VOWEL_A']]
            yield table['TIBINDIC_UNICODE'][stack[0]]
        elif stack[0] == literal_va:
            yield table['TIBINDIC_UNICODE'][literal_ba]
        else:
            yield table['TIBINDIC_UNICODE'][stack[0]]

        stacked_letters = stack[1:]

        for j, letter in enumerate(stacked_letters):
            if letter == table['LATIN_VOWEL_A']:
                continue

            sna_ldan_case = (
                letter == table['SW_VOWELS'][-2]
                and latin_string in table['SNA_LDAN_CASES']
            )

            if sna_ldan_case:
                yield U_SNA_LDAN
                continue

            if letter in table['SW_VOWELS']:
                yield table['TIBINDIC_UNICODE'][letter]
                continue

            if ''.join(stack[:2]) == literal_rv:
                yield (
                    chr(SUBOFFSET +
                        ord(table['TIBINDIC_UNICODE'][literal_ba]))
                )
                continue

            # letter is 'y', 'r' or 'v'
            subjoin_special_case = (
                letter == table['SW_ROOTLETTERS'][25]
                or letter == table['SW_ROOTLETTERS'][26]
                or letter == table['SW_ROOTLETTERS'][28]
            )

            if subjoin_special_case:
                if stack.index(letter) < len(stack)-2:
                    yield table['STACK'][letter]
                    continue

                subjoin = None

                for regex in table['SW_REGEX'][letter]:
                    if regex.search(''.join(stack)):
                        subjoin = chr(
                            SUBOFFSET +
                            ord(table['TIBINDIC_UNICODE'][letter])
                        )
                        break

                yield subjoin or table['STACK'][letter]
                continue

            yield chr(SUBOFFSET + ord(table['TIBINDIC_UNICODE'][letter]))


def analyze_sanskrit(latin_string, table):
    try:
        latin_letters = letter_partition(
            latin_string,
            table,
            letter_set='LATIN_INDIC_ALPHABET_SET',
            char_limit='MAX_INDIC_CHAR_LEN'
        )
        letter_stacks = generate_stacks(latin_letters, table)
        sanskrit = generate_sanskrit_unicode(latin_string, letter_stacks, table)
        return ''.join(sanskrit)
    except (KeyError, ParseError):
        raise InvalidSanskrit(latin_string)
