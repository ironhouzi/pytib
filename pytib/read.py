import logging

from pytib import parse
from pytib.tables import (U_SHADS, U_TSHEG, U_ROOTLETTERS,
                          U_SYMBOLS, generate_tables)
from pytib.exceptions import InvalidLanguage

logger = logging.getLogger('pytib.core')


def read(content, table=None):
    '''
    Parses latin content of file or string given the specified table.
    PLEASE NOTE: Always creates trailing newline! Use rstrip() to remove.
    '''

    if table is None:
        table = generate_tables()

    words = (line.split() for line in content.rstrip().splitlines())

    for line in _generate_tibetan_lines(words, table):
        for i, segment in enumerate(line):
            if not segment:
                continue
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


def _generate_tibetan_lines(content, table):
    '''
    The data structure used here is one list per content line. The elements of
    each list hold a sequence of words that are to be joined with a tsheg. If
    a content line contains one ore more shad's or a word that could not be
    parsed, the list representing this line, will contain multiple lists. E.g:

    The line `sangs rgyas` is represented as ['sangs', 'rgyas', []]. The line:
    `| sangs rgyas |` is represented as [['|'], ['sangs', 'rgyas'], ['|'], []].
    '''

    def handle_unsplit_char(char, word):
        ''' Handle words containing non-alphabet characters '''

        tibetan = []
        rest = word
        preceding_nga = False

        while rest != '':
            head, separator, tail = rest.partition(char)

            if head:
                try:
                    tib_unicode = parse(head, table)
                    tibetan.append(tib_unicode)
                    preceding_nga = tib_unicode[-1] == U_ROOTLETTERS[3]
                except InvalidLanguage as e:
                    logger.debug(f'Could not parse: {e.input}')
                    line_items.append([head])
                    line_items.append([])

            result = table['SYMBOL_LOOKUP'].get(separator, separator)

            if preceding_nga and result in U_SHADS:
                tibetan.append(U_TSHEG)

            if result:
                tibetan.append(result)

                if result in U_SYMBOLS:
                    line_items[-1].append(''.join(tibetan))
                    line_items.append([])
                    tibetan = []

            rest = tail

        if tibetan:
            line_items[-1].append(''.join(tibetan))

            if tibetan[-1] in U_SYMBOLS:
                line_items.append([])

    for line in content:
        line_items = [[]]

        for i, word in enumerate(line):
            if word in table['LATIN_SHADS']:         # word is a type of shad
                prev_word = line[max(i-1, 0)]
                preceding_nga = prev_word[-2:] == table['CONSONANTS'][3]

                if preceding_nga:
                    line_items[-1].append(table['SYMBOL_LOOKUP'][word])
                else:
                    line_items.append([table['SYMBOL_LOOKUP'][word]])

                line_items.append([])
                continue
            elif table['LATIN_SHADS'][1] in word:    # word contains double shad
                handle_unsplit_char(table['LATIN_SHADS'][1], word)
                continue
            elif table['LATIN_SHADS'][0] in word:    # word contains shad
                handle_unsplit_char(table['LATIN_SHADS'][0], word)
                continue
            elif _not_latin_letter(word[0], table):
                handle_unsplit_char(word[0], word)
                continue
            elif _not_latin_letter(word[-1], table):
                handle_unsplit_char(word[-1], word)
                continue

            try:
                tib_unicode = parse(word, table)
                line_items[-1].append(tib_unicode)
            except InvalidLanguage as e:
                logger.debug(f'Could not parse: {e.input}')

                if e.input.isalpha():
                    # non-translated words are tsheg joined
                    line_items[-1].append(e.input)
                else:
                    # non-translated symbols are not tsheg joined
                    line_items.append([e.input])
                    line_items.append([])

        yield line_items
