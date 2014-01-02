import sys
import tables
from math import *
from sys import argv

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
        Translator.rulesSuper = dict(zip(tables.SUPER, tables.SUPER_RULES))
        Translator.rulesSub   = dict(zip(tables.SUB,   tables.SUB_RULES))

    def newSyllable(self, wylie):
        Translator.syllable = Syllable(wylie)

    def toUni(self, syllable):
        return Translator.lookup[str(syllable)]

    def toUniSub(self, syllable):
        return chr(ord(Translator.lookup[str(syllable)]) + SUBOFFSET)

    def output(self):
        sys.stdout.write(Translator.syllable.uni)

    def subjoin(self, s):
        Translator.syllable.add(self.toUniSub(s), s)

    def setStruct(self, key, value):
        Translator.syllable.struct[key] = value

    def clearStruct(self):
        Translator.syllable.struct = tables.SYLLSTRUCT

    def vowelIndex(self, parts):
        n = 0

        for i in parts:
            if i in tables.W_VOWELS:
                return i
            else:
                n += 1
        return n

    def determineUni(self):
        parts = self.partition()
        self.clearStruct

        if len(parts) == 1:
            self.setStruct('root', parts[0])

            if syll in tables.W_VOWELS:
                self.setStruct('vowel', parts[0])

        elif noVowels(parts):
            return

        else:
            i = self.vowelIndex(parts)

            if i == 1:      # 2nd letter is vowel
                self.setStruct('root' , parts[0])
                self.setStruct('vowel', parts[1])

            elif i == 2:    # 3rd letter is vowel
                if validSuper(parts[0], parts[1])
                and not validSub(parts[1], parts[0])
                and not checkPrefix(parts[0]):
                    setStruct('super', parts[0])
                    setStruct('root',  parts[1])

                elif not validSuper(parts[0], parts[1])
                and validSub(parts[1], parts[0])
                and not checkPrefix(parts[0]):
                    setStruct('root',  parts[0])
                    setStruct('super', parts[1])

                elif not validSuper(parts[0], parts[1])
                and not validSub(parts[1], parts[0])
                and checkPrefix(parts[0]):
                    setStruct('prefix', parts[0])
                    setStruct('root',   parts[1])

                setStruct('vowel',  parts[2])

            elif i == 3:    # 4th letter is vowel
                if checkPrefix(parts[0])
                and validSuper(parts[1], parts[2])
                and not validSub(parts[2], parts[1]):
                    setStruct('prefix', parts[0])
                    setStruct('super',  parts[1])
                    setStruct('root',   parts[2])

                if checkPrefix(parts[0])
                and not validSuper(parts[1], parts[2])
                and validSub(parts[2], parts[1]):
                    setStruct('prefix',     parts[0])
                    setStruct('root',       parts[2])
                    setStruct('subjoined',  parts[1])

                if not checkPrefix(parts[0])
                and validSuper(parts[1], parts[2])
                and not validSub(parts[2], parts[1]):
                    setStruct('super',      parts[0])
                    setStruct('root',       parts[1])
                    setStruct('subjoined',  parts[2])

                setStruct('vowel',  parts[3])

            elif i == 4:    # 5th letter is vowel (max allowed)
                setStruct('prefix',     parts[0])
                setStruct('super',      parts[1])
                setStruct('root',       parts[2])
                setStruct('subjoined',  parts[3])
                setStruct('vowel',      parts[4])

    # TODO: Handle letters past vowel!

    def noVowels(self, parts):
        for char in parts:
            if char in tables.W_VOWELS:
                return False

        return True

    def partition(self):
        result = []
        syll = Translator.syllable.wylie

        while len(syll) != 0:
            for i in range(3, 0, -1):
                part = syll[:i]

                if part in tables.W_ROOTLETTERS + tables.W_VOWELS or part == '.':
                    result.append(part)
                    syll = syll[len(part):]

        return result

    def validSuper(self, head, root):
        if head not in tables.SUPER:
            return False
        else:
            return root in Translator.rulesSuper[head]

    def validSub(self, sub, root):
        if sub not in tables.SUB:
            return False
        else:
            return root in Translator.rulesSub[sub]

    def appendWyChar(self, char):
        Translator.syllable.wylie = ''.join([Translator.syllable.wylie, char])

    # {{{
    # def add(self, char):
    #     Translator.syllable.wylie = ''.join([Translator.syllable.wylie, char])
    #     syll = Translator.syllable.wylie

    #     if char == 'a' or char == '.':
    #         return

    #     if syll in Translator.wyTable:
    #         self.newSyllable(syll)
    #         return

    #     byteCnt = self.countChars(syll)

    #     # char forms a multibyte wylie character:
    #     if byteCnt > 1:
    #         if self.hasSuper(syll, byteCnt):
    #             print(char, "of ", syll, "has super/multi")
    #         elif self.hasSub(syll, byteCnt):
    #             print(char, "of ", syll, "has sub/multi")

    #         doSub = (self.hasSuper(syll, byteCnt) or self.hasSub(syll, byteCnt))
    #         self.appendUni(syll, byteCnt, doSub)
    #         return

    #     # char is a singlebyte wylie character:
    #     if self.checkPrefix(syll, byteCnt):
    #         print("syll = ", syll, " byteCnt = ", byteCnt, "prefix!")
    #         Translator.syllable.hasPrefix = True
    #         Translator.syllable.add(self.toUni(char), char)
    #         return

    #     if self.hasSuper(syll, byteCnt):
    #         print(char, "of ", syll, "has super")
    #         self.subjoin(char)
    #         return

    #     print("prefix check: ")
    #     if len(syll) == 2:
    #         print("len is 2")
    #     elif Translator.syllable.hasPrefix:
    #         print("has prefix")
    #     if len(syll) == 2 and Translator.syllable.hasPrefix:
    #         Translator.syllable.add(self.toUni(char), char)

    #     if self.hasSub(syll, byteCnt):
    #         print(char, "of ", syll, "has sub")
    #         if self.hasVowel(syll, byteCnt):
    #             Translator.syllable.add(self.toUni(char), char)
    #         else:
    #             self.subjoin(char)
    #         return

    #     Translator.syllable.add(self.toUni(char), char)
    # }}}

    def appendUni(self, s, i, doSub):
        old = Translator.syllable.uni[:-1]

        if doSub:
            new = self.toUniSub(s[-i:])
        else:
            new = Translator.lookup[s[-i:]]

        Translator.syllable.uni = u''.join([old, new])

    def countChars(self, s):#{{{
        if len(s) < 2:
            return 1
        elif s[-3:] == 'tsh':
            return 3
        elif len(s) >= 2 and s[-2:] in Translator.lookup:
            return 2
        else:
            return 1

    def checkPrefix(self, char):
        if char in tables.PREFIXES:
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
        print()#}}}

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

    def partTest(self, string):
        sys.stdout.write(string + " : ")

        self.newSyllable(string)
        l = self.partition()
        print(str(l))

class Syllable(object):
    'Syllable structure'

    def __init__(self, wylie):
        self.wylie = wylie
        self.struct = tables.SYLLSTRUCT

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = u''.join([self.uni, TSHEG])

    def add(self, uni, wylie):
        self.uni = u''.join([self.uni, uni])

def main():
    t = Translator()
    # t.alphabet()
    # t.vowels()

    if len(argv) < 2:
        t.partTest('bskyongs')
        t.partTest('bre')
        t.partTest('\'rba')
        t.partTest('brnyes')
        t.partTest('skyongs')
        t.partTest('rgyas')
        t.partTest('tshos')
        t.partTest('rnyongs')
        t.partTest('lhongs')
        t.partTest('rta')
        t.partTest('mgo')
        t.partTest('mngar')
        t.partTest('sangs')
        t.partTest('sngas')
        t.partTest('snags')
        t.partTest('g.yag')

        # t.test('bskyongs')
        # t.test('bre')
        # t.test('\'rba')
        # t.test('brnyes')
        # t.test('skyongs')
        # t.test('rgyas')
        # t.test('tshos')
        # t.test('rnyongs')
        # t.test('lhongs')
        # t.test('rta')
        # t.test('mgo')
        # t.test('mngar')
        # t.test('sangs')
        # t.test('sngas')
        # t.test('snags')
        # t.test('g.yag')
        return

    f = open(argv[1], 'r')

    for line in f:
        t.test(line.rstrip())

    f.close()

if __name__ =='__main__':
    main()
