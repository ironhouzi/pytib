import sys
import tables
from sys import argv

''' Translator
    Wylie to utf-8 conversion.

'''

TSHEG = u'\u0f0b'
SUBOFFSET = 0x50


class Translator(object):
    'Mainly modifies static variable: Translator.syllable'

    def __init__(self):
        Translator.syllable = Syllable('')
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        Translator.lookup = dict(zip(wTable, uTable))
        Translator.rulesSuper = dict(zip(tables.SUPER, tables.SUPER_RULES))
        Translator.rulesSub = dict(zip(tables.SUB,   tables.SUB_RULES))

    def newSyllable(self):
        Translator.syllable.wipe()

    def toUni(self, syllable):
        return Translator.lookup[str(syllable)]

    def toUniSub(self, syllable):
        return chr(ord(Translator.lookup[str(syllable)]) + SUBOFFSET)

    def output(self):
        sys.stdout.write(Translator.syllable.uni)

    def setStruct(self, key, value):
        Translator.syllable.struct[key] = value

    def clearSyllable(self):
        Translator.syllable.correct()

    def checkStruct(self, key):
        return Translator.syllable.struct[key]

    def vowelIndex(self, parts):
        # print("parts\n", parts)
        i = 0

        for char in parts:
            if char in tables.W_VOWELS:
                return i
            else:
                i += 1
        return -1

    def determineUni(self):
        parts = self.partition()
        self.clearSyllable()

        if len(parts) == 1:
            self.setStruct('root', parts[0])

            if parts[0] in tables.W_VOWELS:
                self.setStruct('vowel', parts[0])
            else:
                self.setStruct('root', 'a')
                self.setStruct('vowel', parts[0])

        # TODO Remove redundant vowel check
        if self.noVowels(parts):
            # print("returned nowowels")
            return

        else:
            i = self.vowelIndex(parts)
            # print("else.. i = ", i)

            # TODO remove extra iterations taken by g.ya

            if i == 0:
                if parts[0] in tables.W_VOWELS:
                    if parts[0] != 'a':
                        Translator.syllable.wylie = ''.join(['a', parts[0]])
                        self.setStruct('root', 'a')
                        self.setStruct('vowel', parts[0])
                    else:
                        self.setStruct('root',  parts[0])
                        self.setStruct('vowel', parts[0])

            if i == 1:      # 2nd letter is vowel
                # print("vowel(1)")
                self.setStruct('root', parts[0])
                self.setStruct('vowel', parts[1])

            elif i == 2:    # 3rd letter is vowel
                # print("vowel(2)")

                # if parts[0] == 'g.' and parts[1] == 'y':
                #     self.setStruct('prefix', parts[0])
                #     self.setStruct('root',   parts[1])

                if not self.validSuper(parts[0], parts[1]) \
                        and self.validSub(parts[1], parts[0]):

                    # print("vowel(2).case1")
                    self.setStruct('root',      parts[0])
                    self.setStruct('subjoined', parts[1])

                elif self.validSuper(parts[0], parts[1]) \
                        and not self.validSub(parts[1], parts[0]):

                    # print("vowel(2).case2")
                    self.setStruct('super', parts[0])
                    self.setStruct('root',  parts[1])

                else:
                    # print("vowel(2).case3")
                    self.setStruct('prefix', parts[0])
                    self.setStruct('root',   parts[1])

                self.setStruct('vowel',  parts[2])

            elif i == 3:    # 4th letter is vowel
                if self.checkIrregular(i, parts):
                    self.setStruct('root',      parts[0])
                    self.setStruct('subjoined', parts[1])
                    self.setStruct('secondsub', parts[2])
                    # print(Translator.syllable.struct)

                # print("vowel(3)")
                elif self.checkPrefix(parts[0]) \
                        and self.validSuper(parts[1], parts[2]) \
                        and not self.validSub(parts[2], parts[1]):
                    self.setStruct('prefix', parts[0])
                    self.setStruct('super',  parts[1])
                    self.setStruct('root',   parts[2])

                elif self.checkPrefix(parts[0]) \
                        and not self.validSuper(parts[1], parts[2]) \
                        and self.validSub(parts[2], parts[1]):
                    self.setStruct('prefix',    parts[0])
                    self.setStruct('root',      parts[1])
                    self.setStruct('subjoined', parts[2])

                elif not self.checkPrefix(parts[0]) \
                        and self.validSuper(parts[0], parts[1]) \
                        and self.validSub(parts[2], parts[1]):
                    self.setStruct('super',     parts[0])
                    self.setStruct('root',      parts[1])
                    self.setStruct('subjoined', parts[2])

                self.setStruct('vowel',  parts[3])

            elif i == 4:    # 5th letter is vowel (max allowed)
                if self.checkIrregular(i, parts):
                    self.setStruct('prefix',    parts[0])
                    self.setStruct('root',      parts[1])
                    self.setStruct('subjoined', parts[2])
                    self.setStruct('secondsub', parts[3])
                else:
                    # print("vowel(4)")
                    self.setStruct('prefix',    parts[0])
                    self.setStruct('super',     parts[1])
                    self.setStruct('root',      parts[2])
                    self.setStruct('subjoined', parts[3])

                self.setStruct('vowel',     parts[4])

            self.findPrefixes(i, parts)

    def checkIrregular(self, vowelPosition, parts):
        if parts[vowelPosition-1] == 'w' and \
                parts[vowelPosition-2] == 'r':
            # print("chIrr returned true")
            # print(parts)
            return True
        else:
            return False

    def findPrefixes(self, vowelPosition, parts):
        j = 0

        for i in range(vowelPosition+1, len(parts)):
            wyChar = parts[i]
            if wyChar:
                self.setStruct(tables.POSTVOWEL[j], wyChar)
                j += 1

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

                if part in tables.W_ROOTLETTERS + tables.W_VOWELS \
                        or part == 'g.':
                    result.append(part)
                    syll = syll[len(part):]

        return result

    def validSuper(self, head, root):
        if head not in tables.SUPER:
            # print("validsuper false")
            return False
        else:
            # if root in Translator.rulesSuper[head]:
            #     print("validsuper true")
            # else:
            #     print("validsuper false")

            return root in Translator.rulesSuper[head]

    def validSub(self, sub, root):
        if sub not in tables.SUB:
            # print("validsub false: not in SUB")
            return False
        else:
            # if root in Translator.rulesSub[sub]:
            #     print("validsub. root: ", root, "sub: ", sub, ":: true")
            # else:
            #     print("validsub false")

            return root in Translator.rulesSub[sub]

    def appendWyChar(self, char):
        Translator.syllable.wylie = ''.join([Translator.syllable.wylie, char])

    def add(self, char):
        self.appendWyChar(char)
        self.determineUni()
        self.renderUni()

    def renderUni(self):
        # print("render wylie:", Translator.syllable.wylie)
        for comp in tables.SYLLSTRUCT:
            # print("Starting loop iteration ", i, "for: ", comp)
            char = self.checkStruct(comp)

            if char == 'a' and comp != 'root':
                continue

            newString = [Translator.syllable.uni]

            if char:
                # print(Translator.syllable.struct)
                # print(i)

                # TODO: More efficient handling of g. irregular.
                if char == 'g.':
                    char = 'g'
                    self.setStruct(comp, char)

                if comp == 'subjoined' or comp == 'secondsub' \
                        or (comp == 'root' and self.checkStruct('super')):
                    # print(comp, " subjoining ", char)
                    newString.append(self.toUniSub(char))
                else:
                    # print(comp, " else: appending ", char)
                    newString.append(self.toUni(char))

                # print("appending: ", newString)
                Translator.syllable.uni = u''.join(newString)

    def checkPrefix(self, char):
        if char in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self):  # {{{
        Translator.syllable.tsheg()
        self.output()

    def alphabet(self):
        i = 0

        for key in tables.W_ROOTLETTERS:
            self.newSyllable()
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
                self.newSyllable()

            self.add(s)
            i += 1

        self.tsheg()
        print()

    def partTest(self, string):
        sys.stdout.write(string + " : ")

        self.newSyllable(string)
        l = self.partition()
        print(str(l))
# }}}


class Syllable(object):
    'Syllable structure'

    def __init__(self, wylie):
        self.wylie = wylie
        self.uni = u''
        self.struct = dict((key, '') for key in tables.SYLLSTRUCT)

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = u''.join([self.uni, TSHEG])

    def add(self, uni):
        self.uni = u''.join([self.uni, uni])

    def correct(self):
        self.uni = u''

        for s in tables.SYLLSTRUCT:
            self.struct[s] = ''

    def wipe(self):
        self.correct()
        self.wylie = ''


def main():
    t = Translator()
    # t.alphabet()
    # t.vowels()

    if len(argv) < 2:
        # t.partTest('bskyongs')
        # t.partTest('bre')
        # t.partTest('\'rba')
        # t.partTest('brnyes')
        # t.partTest('skyongs')
        # t.partTest('rgyas')
        # t.partTest('tshos')
        # t.partTest('rnyongs')
        # t.partTest('lhongs')
        # t.partTest('rta')
        # t.partTest('mgo')
        # t.partTest('mngar')
        # t.partTest('sangs')
        # t.partTest('sngas')
        # t.partTest('snags')
        # t.partTest('g.yag')

        # t.test('sangs')
        # t.test('bre')
        # t.test('rta')
        # t.test('mgo')
        # t.test('gya')
        # t.test('g.yag')
        # t.test('\'rba')
        # t.test('tshos')
        # t.test('lhongs')
        # t.test('mngar')
        # t.test('sngas')
        # t.test('rnyongs')
        # t.test('brnyes')
        # t.test('rgyas')
        # t.test('skyongs')
        # t.test('bskyongs')
        # t.test('grwa')
        # t.test('spre\'u')
        # t.test('spre\'u\'i')
        # t.test('\'dra')
        # t.test('\'bya')
        # t.test('\'gra')
        # t.test('\'gyang')
        # t.test('\'khra')
        # t.test('\'khyig')
        # t.test('\'kyags')
        # t.test('\'phre')
        # t.test('\'phyags')
        t.test('a')
        t.test('o')
        t.test('a\'am')
        t.test('ab')
        # t.test('bswa')
        # t.test('bha')
        return

    f = open(argv[1], 'r')

    for line in f:
        t.test(line.rstrip())

    f.close()

if __name__ == '__main__':
    main()
