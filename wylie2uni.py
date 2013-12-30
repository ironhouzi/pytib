import sys
import tables
from math import *

''' Translator
    Wylie to utf-8 conversion.

'''

TSHEG = u'\u0f0b'
SUBOFFSET = 0x50

class Translator(object):
    'Mainly modifies static variable: Translator.syllable'

    def __init__(self):
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        Translator.lookup = dict(zip(wTable, uTable))
        Translator.wTable = wTable
        Translator.uTable = uTable

    def mkSyllable(self, wylie):
        Translator.syllable = Syllable(self.toUni(wylie), wylie)

    def toUni(self, syllable):
        return Translator.lookup[str(syllable)]

    def toSub(self, syllable):
        return unichr(ord(Translator.lookup[str(syllable)]) + SUBOFFSET)

    def out(self):
        sys.stdout.write(Translator.syllable.uni)

    def addSuper(self, s):
        Translator.syllable.add(self.toSub(s), s)

    def add(self, s):
        Translator.syllable.wylie = ''.join([Translator.syllable.wylie, s])
        syll = Translator.syllable.wylie

        if syll in Translator.wTable:
            self.mkSyllable(syll)
            return

        byteCnt = self.countChars(syll)

        # char forms a multibyte wylie character:
        if byteCnt > 1:
            doSub = (self.isSuper(syll) or self.isSub(syll))
            noSub = self.isVow(syll, byteCnt)
            self.uniMutate(syll, byteCnt, doSub)
            return

        # char is a singlebyte wylie character:
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
            new = Translator.lookup[s[-i:]]

        Translator.syllable.uni = u''.join([old, new])

    def countChars(self, s):
        if len(s) < 2:
            return 1
        elif s[-3:] == 'tsh':
            return 3
        elif len(s) >= 2 and s[-2:] in Translator.lookup:
            return 2
        else:
            return 1

    def isSuper(self, s):
        if len(s) < 2 or not s[-2] in tables.SUPER:
            return False
        else:
            return True

    def isSub(self, s):
        if s[-1] in tables.SUB:
            return True
        else:
            return False

    def isVow(self, s, byteCnt):
        if s[-byteCnt-1] in tables.W_VOWELS:
            return True
        else:
            return False

    def isPre(self, s):
        if len(s) == 2 and s[-2] in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self):
        Translator.syllable.tsheg()
        self.out()

    def alphabet(self):
        i = 0

        for key in tables.W_ROOTLETTERS:
            self.mkSyllable(key)
            self.tsheg()
            i += 1

            if i % 4 == 0:
                sys.stdout.write("\n")

        sys.stdout.write("\n")

    def vowels(self):
        for key in tables.W_VOWELS:
            self.mkSyllable('a')
            self.add(key)
            self.tsheg()

        print

    def test(self, string):
        sys.stdout.write(string + " : ")
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
        self.uni   = u''.join([self.uni, uni])

def main():
    t = Translator()
    t.alphabet()
    t.vowels()
    t.test('bskyongs')
    t.test('skyongs')
    t.test('rgys')
    t.test('tshos')
    t.test('rnyongs')
    t.test('lhongs')
    t.test('rt')
    t.test('mgo')
    t.test('\'khor')
    t.test('bkhor')
    t.test('gnm')
    t.test('gnyis')

if __name__ =='__main__':
    main()
