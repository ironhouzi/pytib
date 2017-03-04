#!/usr/bin/env python3
import click
import logging

from pytib.fp import parse
from pytib.wylie2uni import Translator, Syllable
from pytib.tables import W_SYMBOLS, U_SYMBOLS, TSHEG, W_ROOTLETTERS, Table


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
        if content in latin_shads:
            return symbolLookup[content]

        syllable.clear()
        translator.analyze(syllable, content)

        if syllable.uni:
            return syllable.uni
        else:
            logging.warning("Could not parse: %s", syllable.wylie)
            return syllable.wylie

    def fp_handle(content):
        if content in latin_shads:
            return symbolLookup[content]

        tib_unicode = parse(content, table)

        if tib_unicode is None:
            logging.warning("Could not parse: %s", syllable.wylie)
            return content

        return tib_unicode

    def not_tibetan(word):
        return word in U_SYMBOLS or 0xf00 < ord(word[0]) > 0x0fff

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
    table = Table(consonants, '-')
    syllable = Syllable()
    symbolLookup = dict(zip(latin_shads, U_SYMBOLS))
    handler = fp_handle if new else handle

    content = wyliestring if wyliestring else filename.read()

    if codepoints:
        content = content.split('\n')
        result = [translator.bytecodes(syllable, word.strip())
                  for line in content for word in line.split()]
    else:
        lines = [line.split() for line in content.rstrip().splitlines()]
        tib_lines = [list(map(handler, line)) for line in lines]
        # generate list of lines to be terminated by a shad
        shads = [words.pop() if words and not_tibetan(words[-1]) else ''
                 for words in tib_lines]
        translated_lines = [TSHEG.join(words) for words in tib_lines]
        result = '\n'.join(
            ''.join(line) for line in zip(translated_lines, shads)
        )

    if include:
        print(content)

    print(result)


if __name__ == '__main__':
    pytib()
