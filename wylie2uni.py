import sys
from math import *

''' Translator
    Wylie to utf-8 conversion.

'''

W_ROOTLETTERS = [
    'k',  'kh',  'g',  'ng',
    'c',  'ch',  'j',  'ny',
    't',  'th',  'd',  'n',
    'p',  'ph',  'b',  'm',
    'ts', 'tsh', 'dz', 'w',
    'zh', 'z',   '\'', 'y',
    'r',  'l',   'sh', 's',
    'h',  'a' ];

U_ROOTLETTERS = [
    u'\u0f40', u'\u0f41', u'\u0f42', u'\u0f44',
    u'\u0f45', u'\u0f46', u'\u0f47', u'\u0f49',
    u'\u0f4f', u'\u0f50', u'\u0f51', u'\u0f53',
    u'\u0f54', u'\u0f55', u'\u0f56', u'\u0f58',
    u'\u0f59', u'\u0f5a', u'\u0f5b', u'\u0f5d',
    u'\u0f5e', u'\u0f5f', u'\u0f60', u'\u0f61',
    u'\u0f62', u'\u0f63', u'\u0f64', u'\u0f66',
    u'\u0f67', u'\u0f68' ];

W_VOWELS = [ 'i', 'u', 'e', 'o' ];

U_VOWELS = [ '\u0f72', '\u0f74', '\u0f7a', '\u0f7c' ];

TSHEG = u'\u0f0c'

class Translator(object):
    'Main workhorse for the program'

    def __init__(self):
        Translator.first = dict(zip(W_ROOTLETTERS, U_ROOTLETTERS))
        Translator.vowel = dict(zip(W_VOWELS, U_VOWELS))

    def mkSyllable(self, wylie):
        Translator.syllable = Syllable(self.toUni(wylie), wylie)

    def toUni(self, syllable):
        return Translator.first[str(syllable)]

    def out(self):
        sys.stdout.write(Translator.syllable.uni)

    def alphabet(self):
        i = 1

        for key in W_ROOTLETTERS:
            s = Syllable(self.toUni(key), key)
            self.out(s.tsheg())

            if i%4 == 0:
                sys.stdout.write("\n")

            i += 1

        sys.stdout.write("\n")


class Syllable(object):
    'Syllable structure'

    def __init__(self, uni, wylie):
        self.uni   = uni
        self.wylie = wylie
        self.count = len(wylie)

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        return u''.join([self.uni, TSHEG])

def main():
    t = Translator()
    t.alphabet()

if __name__ =='__main__':
    main()
