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
        syllable.wylie = content.strip()
        translator.analyze(syllable)
        return syllable.uni

    def codepoint(content):
        syllable.wylie = content.strip()
        translator.analyze(syllable)
        return ', '.join("U+0{0:X}".format(ord(c)) for c in syllable.uni)

    translator = Translator()
    syllable = Syllable()
    symbolLookup = dict(zip(W_SYMBOLS, U_SYMBOLS))

    content = wyliestring if wyliestring else filename.read().rstrip()

    if codepoints:
        result = [codepoint(word) for word in content.split()]
    else:
        result = [handle(word) for word in content.split()]

    if include:
        print(content)

    print(S_TSHEG.join(result))

if __name__ == '__main__':
    pytib()
