from sys import argv, stdout, stdin, exit
import click
import wylie2uni
import tables

@click.command()
@click.option('--filename', '-f', help='Specify file to read', type=click.File(), nargs=1, default='-')
@click.option('--include', '-i', help='Include input in printout', is_flag=True)
@click.option('--codepoints', '-c', help='Print Unicode values', is_flag=True)
@click.argument('string', required=False)
def pytib(filename, string, include, codepoints):
    def handle(content):
        syllable.wylie = content.strip()
        translator.analyze(syllable)
        return syllable.uni

    def codepoint(content):
        syllable.wylie = content.strip()
        translator.analyze(syllable)
        return ', '.join("U+0{0:X}".format(ord(c)) for c in syllable.uni)

    translator = wylie2uni.Translator()
    syllable = wylie2uni.Syllable('')
    symbolLookup = dict(zip(tables.W_SYMBOLS, tables.U_SYMBOLS))

    content = string if string else filename.read().rstrip()

    if codepoints:
        result = [codepoint(word) for word in content.split()]
    else:
        result = [handle(word) for word in content.split()]

    if include:
        print(content)

    print(tables.S_TSHEG.join(result))

if __name__ == '__main__':
    pytib()
