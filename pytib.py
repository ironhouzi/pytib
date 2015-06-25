from sys import argv, stdout, stdin, exit
import click
import logging
from pytib.wylie2uni import Translator, Syllable
from pytib.tables import W_SYMBOLS, U_SYMBOLS, TSHEG, W_VOWELS, W_ROOTLETTERS


@click.command()
@click.option('--filename', '-f',
              help='Specify file to read',
              type=click.File(), nargs=1, default='-')
@click.option('--include', '-i', help='Include input in printout', is_flag=True)
@click.option('--codepoints', '-c', help='Print Unicode values', is_flag=True)
@click.option('--schol', '-s', help='Use polyglotta transliteration', is_flag=True)
@click.option('--whitespace', '-w',
              help='Decimal Unicode codepoint for whitespace character.',
              default=8195, nargs=1)
@click.argument('wyliestring', required=False)
def pytib(filename, wyliestring, include, codepoints, schol, whitespace):
    """
    WYLIESTRING can be either a string literal or a file passed via STDIN or
    with the -f parameter.

    WHITESPACE defaults to U+2003 (EM SPACE) and _must_
    be written as a decimal value, _not_ hexadecimal.
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

    def not_tibetan(word):
        return word in U_SYMBOLS or 0xf00 < ord(word[0]) > 0x0fff

    if schol:
        # Schol/latin consonants
        # TODO: pass list from json file
        consonants = (
            'k',  'kh',  'g',  'ṅ',
            'c',  'ch',  'j',  'ñ',
            't',  'th',  'd',  'n',
            'p',  'ph',  'b',  'm',
            'ts', 'tsh', 'dz', 'v',
            'ź',  'z',   '’', 'y',
            'r',  'l',   'ś',  's',
            'h',  'a', )

        latin_shads = ('|', '||', )
    else:
        consonants = W_ROOTLETTERS
        latin_shads = W_SYMBOLS

    whitespace = chr(whitespace)
    translator = Translator(consonants, '-')
    syllable = Syllable()
    symbolLookup = dict(zip(latin_shads, U_SYMBOLS))

    content = wyliestring if wyliestring else filename.read()

    if codepoints:
        content = content.split('\n')
        result = [translator.bytecodes(syllable, word.strip())
                  for line in content for word in line.split()]
    else:
        lines = [line.split() for line in content.rstrip().splitlines()]
        tib_lines = [list(map(handle, line)) for line in lines]
        post_joined_shads_lines = []

        for line in tib_lines:
            new_line = []
            join_flag = False

            for word in line:
                if word in U_SYMBOLS and not new_line:
                    shad_w_space = ''.join([word, whitespace])
                    new_line[-1] = ''.join([new_line[-1], shad_w_space])
                    join_flag = True
                elif join_flag:
                    new_line[-1] = ''.join([new_line[-1], word])
                    join_flag = False
                else:
                    new_line.append(word)

            post_joined_shads_lines.append(new_line)

    translated_lines = [TSHEG.join(words) for words in post_joined_shads_lines]
    result = '\n'.join(''.join(line) for line in translated_lines)

    if include:
        print(content)

    print(result)

if __name__ == '__main__':
    pytib()
