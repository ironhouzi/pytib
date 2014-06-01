import wylie2uni
import tables
from sys import argv
from sys import stdout

def main():
    if len(argv) < 1:
        sys.exit()
    t = wylie2uni.Translator()
    s = wylie2uni.Syllable('')
    symbolLookup = dict(zip(tables.W_SYMBOLS, tables.U_SYMBOLS))
    f = open(argv[1], 'r')
    for line in f:
        if line is '\n':
            continue
        stdout.write("\n%s" % (line))
        # print()
        words = line.split()
        for d in words:
            d = d.strip()
            if d in tables.W_SYMBOLS:
                stdout.write(symbolLookup[d])
                continue
            s.wylie = d
            t.analyze(s)
            s.tsheg()
            stdout.write(s.uni)
    print()
    f.close()

if __name__ == '__main__':
    main()
