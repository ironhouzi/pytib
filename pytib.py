from sys import argv, stdout, stdin, exit
import click
import logging
from pytib.wylie2uni import Translator, Syllable
from pytib.tables import W_SYMBOLS, U_SYMBOLS, TSHEG, W_VOWELS, W_ROOTLETTERS


@click.command()
@click.option('--filename', '-f', help='Specify file to read', type=click.File(), nargs=1, default='-')
@click.option('--include', '-i', help='Include input in printout', is_flag=True)
@click.option('--codepoints', '-c', help='Print Unicode values', is_flag=True)
@click.option('--schol', '-s', help='Use polyglotta transliteration', is_flag=True)
@click.argument('wyliestring', required=False)
def pytib(filename, wyliestring, include, codepoints, schol):
    """ Docstring
    WYLIESTRING can be either a string literal or a file passed via STDIN or with the -f parameter.
    """

    def handle(content):
        if content in W_SYMBOLS:
            return symbolLookup[content]

        syllable.clear()
        syllable.wylie = content
        translator.analyze(syllable)

        if syllable.uni:
            return syllable.uni
        else:
            logging.warning("Could not parse: %s", syllable.wylie)
            return syllable.wylie

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
            'ź',  'z',   '’', 'y',
            'r',  'l',   'ś',  's',
            'h',  'a', )

        global W_SYMBOLS
        W_SYMBOLS = ('|', '||', )
    else:
        consonants = W_ROOTLETTERS

    translator = Translator(consonants, '-')
    syllable = Syllable()
    symbolLookup = dict(zip(W_SYMBOLS, U_SYMBOLS))

    content = wyliestring if wyliestring else filename.read()

    if codepoints:
        content = content.split('\n')
        result = [translator.bytecodes(syllable, word.strip())
                  for line in content for word in line.split()]
    else:
        lines = [line.split() for line in content.rstrip().splitlines()]
        tib_lines = [list(map(handle, line)) for line in lines]
        shads = [words.pop() if words and not_tibetan(words[-1]) else '' for words in tib_lines]
        translated_lines = [TSHEG.join(words) for words in tib_lines]
        result = '\n'.join(''.join(line) for line in zip(translated_lines, shads))

    if include:
        print(content)

    print(result)

if __name__ == '__main__':
    pytib()
