#!/usr/bin/env python3
import click
import logging

from functools import partial
# from multiprocessing import Pool

from pytib.fp import parse
from pytib.wylie2uni import Translator, Syllable
from pytib.tables import (
    W_SYMBOLS, U_SYMBOLS, TSHEG, W_ROOTLETTERS, create_lookup
)


@click.command()
@click.option('--filename', '-f', help='Specify file to read',
              type=click.File(), nargs=1, default='-')
@click.option('--include', '-i', help='Include input in printout', is_flag=True)
@click.option('--codepoints', '-c', help='Print Unicode values', is_flag=True)
@click.option('--schol', '-s', help='Use polyglotta transliteration',
              is_flag=True)
@click.option('--new', '-n', help='Use new algorithm', is_flag=True)
@click.argument('wyliestring', required=False)
def pytib(filename, wyliestring, include, codepoints, schol, new):
    """ Docstring
    WYLIESTRING can be either a string literal or a file passed via STDIN or
    with the -f parameter.
    """

    def handle(content):
        for line in content:
            line_items = [[]]

            for word in line:
                if word in latin_shads:
                    line_items.append([symbolLookup[word]])
                    line_items.append([])
                    continue

                syllable.clear()
                translator.analyze(syllable, word)

                if syllable.uni:
                    line_items[-1].append(syllable.uni)
                else:
                    logging.warning("Could not parse: %s", syllable.wylie)
                    line_items.append([syllable.wylie])
                    line_items.append([])

            yield line_items

    if schol:
        # Schol/latin consonants
        consonants = (
            'k',  'kh',  'g',  'ṅ',
            'c',  'ch',  'j',  'ñ',
            't',  'th',  'd',  'n',
            'p',  'ph',  'b',  'm',
            'ts', 'tsh', 'dz', 'v',
            'ź',  'z',   '’',  'y',
            'r',  'l',   'ś',  's',
            'h',  'a'
        )

        latin_shads = ('|', '||')
    else:
        consonants = W_ROOTLETTERS
        latin_shads = W_SYMBOLS

    translator = Translator(consonants, '-')
    table = create_lookup(consonants, '-')
    syllable = Syllable()
    symbolLookup = dict(zip(latin_shads, U_SYMBOLS))

    content = wyliestring if wyliestring else filename.read()

    if codepoints:
        content = content.split('\n')
        result = tuple(
            translator.bytecodes(syllable, word.strip())
            for line in content for word in line.split()
        )
    else:
        lines = [line.split() for line in content.rstrip().splitlines()]
        fph = partial(
            fp_handle,
            latin_shads=latin_shads,
            symbolLookup=symbolLookup,
            table=table
        )

        handler = fph if new else handle
        tib_lines = handler(lines)

        result = ''.join(apply_tsheg(tib_lines))

    if include:
        print(content)

    print(result)


def not_tibetan(word):
    v = ord(word[0])
    return word in U_SYMBOLS or v < 0xf00 or v > 0x0fff


def apply_tsheg(tib_lines):
    for line in tib_lines:
        for segment in line:
            if not segment:
                continue

            if not_tibetan(segment[-1]):
                yield ' '.join(segment)
            else:
                yield TSHEG.join(segment)
            yield ' '
        yield '\n'


def fp_handle(content, latin_shads, symbolLookup, table):
    def handle_unsplit_shad(shad):
        tibetan = []

        for p in word.split(shad):
            if p == '':
                tibetan.append(symbolLookup[shad])
            else:
                tib_unicode = parse(p, table)

                if tib_unicode is None:
                    logging.warning("Could not parse: %s", p)
                    line_items.append([word])
                    line_items.append([])
                    return

                tibetan.append(tib_unicode)

        line_items[-1].append(''.join(tibetan))

    for line in content:
        line_items = [[]]

        for word in line:
            if word in latin_shads:         # word is a type of shad
                line_items.append([symbolLookup[word]])
                line_items.append([])
                continue
            elif latin_shads[1] in word:    # word contains double shad
                handle_unsplit_shad(latin_shads[1])
                continue
            elif latin_shads[0] in word:    # word contains shad
                handle_unsplit_shad(latin_shads[0])
                continue

            tib_unicode = parse(word, table)

            if tib_unicode is None:
                logging.warning("Could not parse: %s", word)
                line_items.append([word])
                line_items.append([])
            else:
                line_items[-1].append(tib_unicode)

        yield line_items


if __name__ == '__main__':
    pytib()
