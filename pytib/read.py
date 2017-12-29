import logging

from pytib import parse
from pytib.tables import U_SYMBOLS, U_TSHEG

logger = logging.getLogger('pytib.core')


def read(content, table):
    words = tuple(line.split() for line in content.rstrip().splitlines())
    tib_lines = _handler(words, table)

    for line in tib_lines:
        for i, segment in enumerate(line):
            if not segment:
                continue
            elif _not_tibetan(segment[-1]):
                yield ' '.join(segment)
            else:
                yield U_TSHEG.join(segment)

            # Join line segments with a space, but don't create trailing spaces,
            # and account for line[-1] == []
            if i < (len(line) - (2 if not line[-1] else 1)):
                yield ' '

        yield '\n'


def _not_tibetan(word):
    v = ord(word[0])
    return word in U_SYMBOLS or v < 0x0f00 or v > 0x0fff


def _handler(content, table):
    '''
    The data structure used here is one list per content line. The elements of
    each list hold a sequence of words that are to be joined with a tsheg. If
    a content line contains one ore more shad's or a word that could not be
    parsed, the list representing this line, will contain multiple lists. E.g:

    The line `sangs rgyas` is represented as ['sangs', 'rgyas', []]. The line:
    `| sangs rgyas |` is represented as [['|'], ['sangs', 'rgyas'], ['|'], []].
    '''

    def handle_fail(word):
        if word.isalpha():
            # non-translated words are tsheg joined
            line_items[-1].append(word)
        else:
            # non-translated symbols are not tsheg joined
            line_items.append([word])
            line_items.append([])

    def handle_unsplit_shad(shad, word):
        ''' Handle words containing a shad character not separated by space '''

        tibetan = []
        for p in word.split(shad):
            if p == '':
                tibetan.append(table['SYMBOL_LOOKUP'][shad])

                if len(tibetan) > 1:     # terminating shad
                    line_items[-1].append(''.join(tibetan))
                    tibetan = []
                    line_items.append([])
            else:
                tib_unicode = parse(p, table)

                if tib_unicode is None:
                    logger.debug(f'Could not parse: {p}')
                    handle_fail(word)
                    return

                tibetan.append(tib_unicode)

        if tibetan:
            line_items[-1].append(''.join(tibetan))

    for line in content:
        line_items = [[]]

        for word in line:
            if word in table['LATIN_SHADS']:         # word is a type of shad
                line_items.append([table['SYMBOL_LOOKUP'][word]])
                line_items.append([])
                continue
            elif table['LATIN_SHADS'][1] in word:    # word contains double shad
                handle_unsplit_shad(table['LATIN_SHADS'][1], word)
                continue
            elif table['LATIN_SHADS'][0] in word:    # word contains shad
                handle_unsplit_shad(table['LATIN_SHADS'][0], word)
                continue

            tib_unicode = parse(word, table)

            if tib_unicode is None:
                logger.debug(f'Could not parse: {word}')
                handle_fail(word)
            else:
                line_items[-1].append(tib_unicode)

        yield line_items
