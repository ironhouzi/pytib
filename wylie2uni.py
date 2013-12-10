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

U_VOWELS = [ u'\u0f72', u'\u0f74', u'\u0f7a', u'\u0f7c' ];

TSHEG = u'\u0f0b'

SUPER = [ 'r', 'l', 's' ];

SUB = [ 'y', 'r', 'l', 'w' ];

PREFIXES = [ 'g', 'd', 'b', 'm', '\'' ];

SUBOFFSET = 0x50


class Translator(object):
    'Mainly modifies static variable: Translator.syllable'

    def __init__(self):
        wTable = W_ROOTLETTERS + W_VOWELS
        uTable = U_ROOTLETTERS + U_VOWELS
        Translator.first = dict(zip(wTable, uTable))
        Translator.wTable = wTable
        Translator.uTable = uTable

    def mkSyllable(self, wylie):
        Translator.syllable = Syllable(self.toUni(wylie), wylie)

    def toUni(self, syllable):
        return Translator.first[str(syllable)]

    def toSub(self, syllable):
        return unichr(ord(Translator.first[str(syllable)]) + SUBOFFSET)

    def out(self):
        sys.stdout.write(Translator.syllable.uni)

    def addSuper(self, s):
        Translator.syllable.add(self.toSub(s), s)

    def add(self, s):
        # TODO: Remove redundant join
        syll = ''.join([Translator.syllable.wylie, s])

        if syll in Translator.wTable:
            self.mkSyllable(syll)
            return

        byteCnt = self.multibyte(syll)

        # Has multibyte wylie character:
        if byteCnt > 1:
            self.uniMutate(syll, byteCnt, self.isSuper(syll) or self.isSub(syll))
            return

        # Has singlebyte wylie character:
        # if self.isPre(syll):
        #     return

        if self.isSuper(syll):
            self.addSuper(s)
            return

        if self.isSub(syll):
            if self.isVow(syll, byteCnt):
                Translator.syllable.add(self.toUni(s), s)
            else:
                self.addSuper(s)
            return

        Translator.syllable.add(self.toUni(s), s)


    def uniMutate(self, s, i, doSub):
        old = Translator.syllable.uni[:-1]

        if doSub:
            new = self.toSub(s[-i:])
        else:
            new = Translator.first[s[-i:]]

        Translator.syllable.uni = u''.join([old, new])

    def multibyte(self, s):
        if len(s) < 2:
            return 1
        elif len(s) >= 3 and s[-3:] == 'tsh':
            return 3
        elif len(s) >= 2 and s[-2:] in Translator.first:
            return 2
        else:
            return 1

    def isSuper(self, s):
        if len(s) < 2 or not s[-2] in SUPER:
            return False
        else:
            return True

    def isSub(self, s):
        if s[-1] in SUB:
            return True
        else:
            return False

    def isVow(self, s, byteCnt):
        if s[-byteCnt-1] in W_VOWELS:
            return True
        else:
            return False

    def isPre(self, s):
        if len(s) == 2 and s[-2] in PREFIXES:
            return True
        else:
            return False

    def tsheg(self):
        Translator.syllable.tsheg()
        self.out()

    def alphabet(self):
        i = 0

        for key in W_ROOTLETTERS:
            self.mkSyllable(key)
            self.tsheg()
            i += 1

            if i % 4 == 0:
                sys.stdout.write("\n")

        sys.stdout.write("\n")

    def vowels(self):
        for key in W_VOWELS:
            self.mkSyllable('a')
            self.add(key)
            self.tsheg()

        print

    def test(self, string):
        sys.stdout.write(string + ": ")
        i = 0
        for s in string:
            if i == 0:
               self.mkSyllable(s)
            else:
                self.add(s)
            i += 1

        self.tsheg()
        print

class Syllable(object):
    'Syllable structure'

    def __init__(self, uni, wylie):
        self.uni   = uni
        self.wylie = wylie

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = u''.join([self.uni, TSHEG])

    def add(self, uni, wylie):
        self.wylie = u''.join([self.wylie, wylie])
        self.uni   = u''.join([self.uni, uni])

def main():
    t = Translator()
    t.alphabet()
    t.vowels()
    t.test('bskyongs')
    t.test('skyongs')
    t.test('rgys')
    t.test('rnyongs')
    t.test('lhongs')
    t.test('rt')
    t.test('mgo')
    t.test('\'khor')

if __name__ =='__main__':
    main()
