import wylie2uni
import tables
from sys import argv
from sys import stdout
from sys import exit


def main():
    if len(argv) < 1:
        print("Usage: filereader.py <file> <include original file in output?>")
        exit()
    t = wylie2uni.Translator()
    s = wylie2uni.Syllable('')
    includeOriginal = False
    if len(argv) > 2:
        includeOriginal = True
    symbolLookup = dict(zip(tables.W_SYMBOLS, tables.U_SYMBOLS))
    f = open(argv[1], 'r')
    for line in f:
        if includeOriginal:
            stdout.write("\n%s" % (line))
        else:
            print()
        words = line.split()
        for d in words:
            d = d.strip()
            if d in tables.W_SYMBOLS:
                stdout.write(symbolLookup[d])
                continue
            # if d == 'vajra':
            #     continue
            s.wylie = d
            t.analyze(s)
            s.tsheg()
            stdout.write(s.uni)
    print()
    f.close()

if __name__ == '__main__':
    main()
