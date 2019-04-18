import logging

from typing import Iterable
from pytib.core import parse
from pytib.tables import (U_SHADS, U_TSHEG, generate_tables)
from pytib.exceptions import InvalidLanguage

logger = logging.getLogger('pytib.core')


def read(content, table=None):
    '''
    Parses latin content from file or string to tibetan unicode.
    PLEASE NOTE: Always creates trailing newline! Use rstrip() to remove.
    '''

    if table is None:
        table = generate_tables()

    words = (line.split() for line in content.rstrip().splitlines())

    for line in _generate_tibetan_lines(words, table):
        for i, segment in enumerate(line):
            if not segment:
                continue
            elif not isinstance(segment, list):
                print(segment)
                yield segment
            elif _not_tibetan(segment[-1]):
                if _tsheg_before_shad(segment, table):
                    yield U_TSHEG.join(segment)
                else:
                    yield ' '.join(segment)
            else:
                yield U_TSHEG.join(segment)

            # Join line segments with a space, but don't create trailing spaces,
            # and account for line[-1] == []
            if i < (len(line) - (2 if not line[-1] else 1)):
                yield ' '

        yield '\n'


def _tsheg_before_shad(segment, table):
    ''' Tests if the current word is shad and the word before ends with nga '''
    return (
        len(segment) > 1
        and segment[-1] in U_SHADS
        and len(segment[-2]) > 1
        and segment[-2][-2:] == table['CONSONANTS'][3]
    )


def _not_tibetan(word):
    v = ord(word[0])
    return v < 0x0f00 or v > 0x0fff


def _not_latin_letter(char, table):
    return char not in table['LATIN_TIBETAN_ALPHABET'] and not char.isalpha()


def _partition_word(word: str, table) -> Iterable[str]:
    ''' Splits words if word contains separator (shad) marks. '''

    punctuation_indices = list(word.find(p) for p in table['PUNCTUATION_CHARS'])

    if not any(shad_index > -1 for shad_index in punctuation_indices):
        yield word
        return

    remainder = word

    while remainder != '':
        for punctuation in table['PUNCTUATION_CHARS']:
            part, separator, new_remainder = remainder.partition(punctuation)
            contains_punctuation = separator != ''

            if contains_punctuation:
                if part:
                    yield part

                yield separator
                remainder = new_remainder
                break
        else:
            yield part
            remainder = new_remainder


def shad_before_nga(prev_word, partitioned_word, table):
    if not prev_word:
        return False

    nga = table['CONSONANTS'][3]
    return prev_word[-len(partitioned_word):] == nga


def shad_before_ka_ga(prev_word, partitioned_word, table):
    if not prev_word:
        return False

    ka_ga = (table['CONSONANTS'][0], table['CONSONANTS'][2])
    return prev_word[-2:-1] in ka_ga


def _generate_tibetan_lines(content, table):
    '''
    The data structure used here is one list per content line. The elements of
    each list hold a sequence of words that are to be joined with a tsheg
    (Tibetan syllable/word separator). If a content line contains one ore more
    shad's (Tibetan sentence terminator), or a word that could not be parsed,
    the list representing this line, will contain multiple lists. E.g:

    The line `sangs rgyas` is represented as ['sangs', 'rgyas', []]. The line:
    `| sangs rgyas |` is represented as [['|'], ['sangs', 'rgyas'], ['|'], []],
    due to the shad (`|`).
    '''

    for line in content:
        line_items = [[]]

        for i, word in enumerate(line):
            prev_word = ''
            for j, partitioned_word in enumerate(_partition_word(word, table)):
                if partitioned_word in table['LATIN_SHADS']:    # terminator
                    # # if at start of a partitioned word, check previous line
                    # prev_word = (partitioned_word[-1] if j > 0
                    #              else line[max(i-1, 0)])
                    unicode_shad = table['SYMBOL_LOOKUP'][partitioned_word]

                    if shad_before_nga(prev_word, partitioned_word, table):
                        # tsheg between nga and shad
                        line_items.append([unicode_shad])
                    elif shad_before_ka_ga(prev_word, partitioned_word, table):
                        # normalize double shad to single when preceded by ka/ga
                        line_items.append(U_SHADS[0])
                    else:
                        # Join with last word avoids space converted to tsheg
                        line_items[-1].append(unicode_shad)

                    line_items.append([])
                    prev_word = partitioned_word
                    continue

                try:
                    tib_unicode = parse(partitioned_word, table)
                    line_items[-1].append(tib_unicode)
                except InvalidLanguage as e:
                    logger.debug(f'Could not parse: {e.input}')
                    line_items.append([e.input])
                    line_items.append([])

                prev_word = partitioned_word

        yield line_items
