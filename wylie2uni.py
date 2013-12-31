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
        Translator.wyTable = wTable

    def newSyllable(self, wylie):
        Translator.syllable = Syllable(self.toUni(wylie), wylie)

    def toUni(self, syllable):
        return Translator.lookup[str(syllable)]

    def toUniSub(self, syllable):
        return chr(ord(Translator.lookup[str(syllable)]) + SUBOFFSET)

    def output(self):
        sys.stdout.write(Translator.syllable.uni)

    def subjoin(self, s):
        Translator.syllable.add(self.toUniSub(s), s)

    def add(self, char):
        Translator.syllable.wylie = ''.join([Translator.syllable.wylie, char])
        syll = Translator.syllable.wylie

        if char == 'a':
            return

        if syll in Translator.wyTable:
            self.newSyllable(syll)
            return

        byteCnt = self.countChars(syll)

        # char forms a multibyte wylie character:
        if byteCnt > 1:
            # if self.hasSuper(syll, byteCnt):
            #     print(char, "of ", syll, "has super/multi")
            # elif self.hasSub(syll, byteCnt):
            #     print(char, "of ", syll, "has sub/multi")
            doSub = (self.hasSuper(syll, byteCnt) or self.hasSub(syll, byteCnt))
            self.appendUni(syll, byteCnt, doSub)
            return

        # char is a singlebyte wylie character:
        if self.hasSuper(syll, byteCnt):
            # print(char, "of ", syll, "has super")
            self.subjoin(char)
            return

        if self.hasSub(syll, byteCnt):
            # print(char, "of ", syll, "has sub")
            if self.hasVowel(syll, byteCnt):
                Translator.syllable.add(self.toUni(char), char)
            else:
                self.subjoin(char)
            return

        Translator.syllable.add(self.toUni(char), char)


    def appendUni(self, s, i, doSub):
        old = Translator.syllable.uni[:-1]

        if doSub:
            new = self.toUniSub(s[-i:])
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

    def hasSuper(self, s, byteCnt):
        if len(s) > 1 and s[-byteCnt-1:-byteCnt] in tables.SUPER:
            return True
        else:
            return False

    def hasSub(self, s, byteCnt):
        if s[-byteCnt] in tables.SUB:
            return True
        else:
            return False

    def hasVowel(self, s, byteCnt):
        if s[-byteCnt-1] in tables.W_VOWELS:
            return True
        else:
            return False

    def tsheg(self):
        Translator.syllable.tsheg()
        self.output()

    def alphabet(self):
        i = 0

        for key in tables.W_ROOTLETTERS:
            self.newSyllable(key)
            self.tsheg()
            i += 1

            if i % 4 == 0:
                sys.stdout.write("\n")

        sys.stdout.write("\n")

    def vowels(self):
        for key in tables.W_VOWELS:
            self.newSyllable('a')
            self.add(key)
            self.tsheg()
        print()

    def test(self, string):
        sys.stdout.write(string + " : ")
        i = 0
        for s in string:
            if i == 0:
               self.newSyllable(s)
            else:
                self.add(s)
            i += 1

        self.tsheg()
        print()

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
    # t.alphabet()
    # t.vowels()
    t.test('bskyongs')
    t.test('skyongs')
    t.test('rgyas')
    t.test('tshos')
    t.test('rnyongs')
    t.test('lhongs')
    t.test('rta')
    t.test('mgo')
    t.test('\'khor')
    t.test('bkhor')
    t.test('gnam')
    t.test('gnyis')
    t.test('mngar')
    t.test('sangs')
    t.test('sngas')
    t.test('snags')

if __name__ =='__main__':
    main()
