from sys import argv, stdout, stdin, exit
import click
from pytib.wylie2uni import Translator, Syllable
from pytib.tables import W_SYMBOLS, U_SYMBOLS, S_TSHEG

@click.command()
@click.option('--filename', '-f', help='Specify file to read', type=click.File(), nargs=1, default='-')
@click.option('--include', '-i', help='Include input in printout', is_flag=True)
@click.option('--codepoints', '-c', help='Print Unicode values', is_flag=True)
@click.argument('wyliestring', required=False)
def pytib(filename, wyliestring, include, codepoints):
    """ Docstring
    WYLIESTRING can be either a string litteral or a file passed via STDIN or with the -f parameter.
    """

    def handle(content):
        if content in W_SYMBOLS:
            return symbolLookup[content]

        syllable.uni = ''
        syllable.wylie = content
        translator.analyze(syllable)
        return syllable.uni if syllable.uni else syllable.wylie

    def codepoint(content):
        syllable.wylie = content.strip()
        translator.analyze(syllable)
        return ', '.join("U+0{0:X}".format(ord(c)) for c in syllable.uni)

    translator = Translator()
    syllable = Syllable()
    symbolLookup = dict(zip(W_SYMBOLS, U_SYMBOLS))

    content = wyliestring if wyliestring else filename.read()

    if codepoints:
        content = content.split('\n')
        result = [codepoint(word) for line in content for word in line.split()]
    else:
        lines = [line.split() for line in content.rstrip().split('\n')]
        tib_lines = [list(map(handle, line)) for line in lines]
        shads = [line.pop() if line[-1] in U_SYMBOLS else '' for line in tib_lines]
        translated_lines = [S_TSHEG.join(words) for words in tib_lines]
        result = '\n'.join(''.join(line) for line in zip(translated_lines, shads))

    if include:
        print(content)

    print(result)

if __name__ == '__main__':
    pytib()
