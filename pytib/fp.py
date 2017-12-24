import logging

# from tables import Table


class InvalidTibetan(Exception):
    pass


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


def is_superscribed(latin, vowel_position, table):
    if vowel_position == 2:
        return (
            valid_superscribe(latin[0], latin[1], table)
            and not valid_subscribe(latin[0], latin[1], table)
        )
    else:   # vowel_position == 3
        return (
            latin[0] in table['PREFIXES']
            and valid_superscribe(latin[1], latin[2], table)
            and not valid_subscribe(latin[1], latin[2], table)
        )


def is_subscribed(latin, vowel_position, table):
    if vowel_position == 2:
        return (
            not valid_superscribe(latin[0], latin[1], table)
            and valid_subscribe(latin[0], latin[1], table)
        )
    else:   # vowel_position == 3
        return (
            latin[0] in table['PREFIXES']
            and not valid_superscribe(latin[1], latin[2], table)
            and valid_subscribe(latin[1], latin[2], table)
        )


def vowel_pos_0(latin, table):
    if not latin[0] in table['TIBETAN_VOWELS']:
        return None

    return dict(root=latin[0])


def vowel_pos_1(latin, table):
    if not latin[0] in table['CONSONANTS'] \
       and latin[1] in table['TIBETAN_VOWELS']:
        return None

    return dict(root=latin[0], vowel=latin[1])


def vowel_pos_2(latin, table):
    if is_subscribed(latin, 2, table):
        result = dict(root=latin[0], subjoined=latin[1])
    elif is_superscribed(latin, 2, table):
        result = dict(super=latin[0], root=latin[1])
    elif (latin[0] == table['GA_PREFIX']
          or latin[0] in table['PREFIXES']
          and latin[1] in table['CONSONANTS']):
        result = dict(prefix=latin[0], root=latin[1])
    else:
        return None

    result['vowel'] = latin[2]

    return result


def vowel_pos_3(latin, table):
    if latin[2] == table['CONSONANTS'][19]\
       and latin[1] == table['CONSONANTS'][24]:
        # syllable has both 'w' and 'r' as subscribed letters
        result = dict(root=latin[0], subjoined=latin[1], secondsub=latin[2])
    elif is_superscribed(latin, 3, table):
        result = dict(prefix=latin[0], super=latin[1], root=latin[2])
    elif is_subscribed(latin, 3, table):
        result = dict(prefix=latin[0], root=latin[1], subjoined=latin[2])
    elif (latin[0] in table['SUPERJOIN']
          and latin[1] in table['CONSONANTS']
          and latin[2] in table['SUB']):
        result = dict(super=latin[0], root=latin[1], subjoined=latin[2])
    else:
        return None

    result['vowel'] = latin[3]

    return result


def vowel_pos_4(latin, table):
    if not (latin[0] in table['PREFIXES']
            and latin[1] in table['SUPERJOIN']
            and latin[2] in table['CONSONANTS']
            and latin[3] in table['SUB']):
        return None

    return dict(
        prefix=latin[0],
        super=latin[1],
        root=latin[2],
        subjoined=latin[3],
        vowel=latin[4]
    )


analyze_syllable = (
    vowel_pos_0,
    vowel_pos_1,
    vowel_pos_2,
    vowel_pos_3,
    vowel_pos_4,
)


def find_suffixes(syllable, vowel_position, latin, table):
    '''Identifies the syllable suffixes'''

    post_vowels = iter(table['POSTVOWEL'])

    for latin_suffix in latin[vowel_position+1:]:
        try:
            post_vowel = next(post_vowels)
        except StopIteration:
            break   # Disallow multiple genetive vowels

        invalid_suffix = (
            post_vowel in table['POSTVOWEL'][:2]
            and latin_suffix not in table['TIBETAN_VOWELS']
            and latin_suffix not in table['VALID_SUFFIX'][post_vowel]
        )

        if invalid_suffix:
            return None

        syllable[post_vowel] = latin_suffix

    return syllable


def letter_partition(string, table, alphabet, max_char_len):
    '''
    Checks if the roman character(s) at the end of the wylie/IAST string
    forms a valid wylie letter and continues backwards through the
    wylie/IAST string, until the entire wylie string is partitioned.
    '''

    while len(string) != 0:
        for i in range(max_char_len, 0, -1):
            part = string[:i]

            if part == '':
                break

            if part == table['GA_PREFIX'] or part in alphabet:
                yield part
                string = string[i:]
            elif i == 1 and part not in alphabet:
                raise InvalidTibetan


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
        vowels = tuple(c for c in string if c in table['TIBETAN_VOWELS'])
        atleast_two_vowels = len(vowels) >= 2

        sanskrit_quick_check = (
            table['LATIN_A_CHUNG'] not in string
            and atleast_two_vowels
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
        latin = list(letter_partition(
            string,
            table,
            alphabet=table['LATIN_TIBETAN_ALPHABET_SET'],
            max_char_len=table['MAX_TIB_CHAR_LEN']
        ))
    except InvalidTibetan:
        return analyze_sanskrit(string, table)

    # TODO: measure performance using tib vowel set
    vowel_positions = tuple(
        index for index, char in enumerate(latin)
        if char in table['TIBETAN_VOWELS']
    )

    # Any adjacent vowels constitutes a sanskrit word
    vowel_index_pairs = zip(vowel_positions[::-1], vowel_positions[-2::-1])
    adjacent_vowels = (x - y == 1 for x, y in vowel_index_pairs)

    if len(vowel_positions) != 1 and any(adjacent_vowels):
        return analyze_sanskrit(string, table)

    first_vowel_index = vowel_positions[0]

    if first_vowel_index >= len(analyze_syllable):
        logging.warning(
            f'Oversized vowel position: {first_vowel_index} for «{latin}»'
        )
        return analyze_sanskrit(string, table)

    syllable = analyze_syllable[first_vowel_index](latin, table)
    syllable = find_suffixes(syllable, first_vowel_index, latin, table)

    if syllable is None:
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
            yield (
                chr(table['SUBJOIN'] +
                    ord(table['TIBETAN_UNICODE'][latin_char]))
            )
        else:
            yield table['TIBETAN_UNICODE'][latin_char]


def vowel_positions(latin, table):
    result = []

    for i, char in enumerate(latin):
        if char in table['SW_VOWELS']:

            # conjoin adjacent vowels
            if latin[i-1] in table['SW_VOWELS'] and result:
                result[-1] += 1
                continue

            result.append(i)

    return result


def stackSanskritLetters(vowelIndices, latin):
    vowelIndices = list(i+1 for i in vowelIndices)

    if vowelIndices[0] != 0:
        vowelIndices.insert(0, 0)

    if vowelIndices[-1] != len(latin):
        vowelIndices.append(len(latin))

    vowelIndices = zip(vowelIndices, vowelIndices[1:])

    for i in vowelIndices:
        yield latin[i[0]:i[1]]


def generateSanskritUnicode(latin, letterStacks, table):
    if latin['string'] == table['U_OM']:
        yield table['S_OM']
        raise StopIteration

    literal_va = table['SW_ROOTLETTERS'][28]
    literal_ba = table['CONSONANTS'][14]
    literal_rv = table['SW_ROOTLETTERS'][26] + table['SW_ROOTLETTERS'][28]

    for i, stack in enumerate(letterStacks):
        if stack[0] in table['SW_VOWELS'][1:]:   # avoid leading `a`
            yield table['TIBINDIC_UNICODE'][table['LATIN_VOWEL_A']]
            yield table['TIBINDIC_UNICODE'][stack[0]]
        elif stack[0] is literal_va:
            yield table['TIBINDIC_UNICODE'][literal_ba]
        else:
            yield table['TIBINDIC_UNICODE'][stack[0]]

        stackedLetters = stack[1:]

        for j, letter in enumerate(stackedLetters):
            if letter is table['LATIN_VOWEL_A']:
                continue

            sna_ldan_case = (
                letter == table['SW_VOWELS'][-2]
                and latin['string'] in table['SNA_LDAN_CASES']
            )

            if sna_ldan_case:
                yield table['S_SNA_LDAN']
                continue

            if letter in table['SW_VOWELS']:
                yield table['TIBINDIC_UNICODE'][letter]
                continue

            if ''.join(stack[:2]) == literal_rv:
                yield (
                    chr(table['SUBJOIN'] +
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
                            table['SUBJOIN'] +
                            ord(table['TIBINDIC_UNICODE'][letter])
                        )
                        break

                yield subjoin or table['STACK'][letter]
                continue

            yield chr(table['SUBJOIN'] + ord(table['TIBINDIC_UNICODE'][letter]))


def analyze_sanskrit(latin_string, table):
    try:
        parts = list(letter_partition(
            latin_string,
            table,
            alphabet=table['LATIN_INDIC_ALPHABET_SET'],
            max_char_len=table['MAX_INDIC_CHAR_LEN']
        ))
    except InvalidTibetan:
        return None

    latin = dict(parts=parts, string=latin_string)

    if latin['parts'] is None:
        return None

    vowel_indices = vowel_positions(latin['parts'], table)

    if not vowel_indices:
        return None

    letterStacks = stackSanskritLetters(vowel_indices, latin['parts'])
    return ''.join(generateSanskritUnicode(latin, letterStacks, table))
