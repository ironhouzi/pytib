'''Wylie2Uni
    Wylie to Unicode convertor'''

# TODO: Write unit testWylies!

import sys
import tables
from sys import argv

TSHEG = u'\u0f0b'
SUBOFFSET = 0x50


class Translator(object):
    '''Translates wylie into Tibetan Unicode'''

    def __init__(self):
        self.syllable = Syllable('')
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        self.lookup = dict(zip(wTable, uTable))
        self.rulesSuper = dict(zip(tables.SUPER, tables.SUPER_RULES))
        self.rulesSub = dict(zip(tables.SUB,   tables.SUB_RULES))

    def newSyllable(self):
        self.syllable = Syllable('')

    def toUnicode(self, syllable):
        return self.lookup[str(syllable)]

    def toSubjoinedUnicode(self, syllable):
        return chr(ord(self.lookup[str(syllable)]) + SUBOFFSET)

    def setStruct(self, key, value):
        self.syllable.struct[key] = value

    def clearSyllable(self):
        self.syllable.clear()

    def getCharacterOf(self, key):
        return self.syllable.struct[key]

    def getVowelIndex(self, parts):
        for i, char in enumerate(parts):
            if char in tables.W_VOWELS:
                return i
        return -1

    def isSuperscribed(self, parts, vowelPosition):
        if vowelPosition == 2:
            return self.validSuperscribe(parts[0], parts[1]) \
                and not self.validSubscribe(parts[1], parts[0])
        else:   # vowelPosition == 3
            return self.isPrefix(parts[0]) \
                and self.validSuperscribe(parts[1], parts[2]) \
                and not self.validSubscribe(parts[2], parts[1])

    def isSubscribed(self, parts, vowelPosition):
        if vowelPosition == 2:
            return not self.validSuperscribe(parts[0], parts[1]) \
                and self.validSubscribe(parts[1], parts[0])

        else:   # vowelPosition == 3
            return self.isPrefix(parts[0]) \
                and not self.validSuperscribe(parts[1], parts[2]) \
                and self.validSubscribe(parts[2], parts[1])

    def normalWylie(self, parts, vowelPosition):
        if vowelPosition == 0:
            if parts[0] in tables.W_VOWELS:
                if parts[0] != 'a':
    # TODO This gives incorrect wylie. Move to renderUnicode().
                    self.syllable.wylie = ''.join(['a', parts[0]])
                    self.setStruct('root', 'a')
                    self.setStruct('vowel', parts[0])
                else:
                    self.setStruct('root',  parts[0])
                    self.setStruct('vowel', parts[0])

        if vowelPosition == 1:
            self.setStruct('root', parts[0])
            self.setStruct('vowel', parts[1])

        elif vowelPosition == 2:
            if self.isSubscribed(parts, vowelPosition):
                self.setStruct('root',      parts[0])
                self.setStruct('subjoined', parts[1])

            elif self.isSuperscribed(parts, vowelPosition):
                self.setStruct('super', parts[0])
                self.setStruct('root',  parts[1])

            else:
                self.setStruct('prefix', parts[0])
                self.setStruct('root',   parts[1])

            self.setStruct('vowel',  parts[2])

        elif vowelPosition == 3:
            if self.isIrregular(vowelPosition, parts):
                self.setStruct('root',      parts[0])
                self.setStruct('subjoined', parts[1])
                self.setStruct('secondsub', parts[2])

            elif self.isSuperscribed(parts, vowelPosition):
                self.setStruct('prefix', parts[0])
                self.setStruct('super',  parts[1])
                self.setStruct('root',   parts[2])

            elif self.isSubscribed(parts, vowelPosition):
                self.setStruct('prefix',    parts[0])
                self.setStruct('root',      parts[1])
                self.setStruct('subjoined', parts[2])

            else:
                self.setStruct('super',     parts[0])
                self.setStruct('root',      parts[1])
                self.setStruct('subjoined', parts[2])

            self.setStruct('vowel',  parts[3])

        elif vowelPosition == 4:  # (max allowed)
            if self.isIrregular(vowelPosition, parts):
                self.setStruct('prefix',    parts[0])
                self.setStruct('root',      parts[1])
                self.setStruct('subjoined', parts[2])
                self.setStruct('secondsub', parts[3])
            else:
                self.setStruct('prefix',    parts[0])
                self.setStruct('super',     parts[1])
                self.setStruct('root',      parts[2])
                self.setStruct('subjoined', parts[3])

            self.setStruct('vowel', parts[4])

    def singleWylieCharacter(self, parts):
        self.setStruct('root', parts[0])

        if parts[0] in tables.W_VOWELS:
            self.setStruct('vowel', parts[0])
        else:
            self.setStruct('root', 'a')
            self.setStruct('vowel', parts[0])

    def determineWylie(self):
        parts = self.partition()
        self.clearSyllable()

        if len(parts) == 1:
            self.singleWylieCharacter(parts)

    # TODO Remove redundant vowel check
        if self.noVowels(parts):
            return

        else:
            vowelPosition = self.getVowelIndex(parts)
            self.normalWylie(parts, vowelPosition)
            self.findSuffixes(vowelPosition, parts)

    def isIrregular(self, vowelPosition, parts):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''

        if parts[vowelPosition-1] == 'w' \
                and parts[vowelPosition-2] == 'r':
            return True
        else:
            return False

    def findSuffixes(self, vowelPosition, parts):
    # TODO: Iterator for POSTVOWEL.next *if* that doesn't impede performance
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
        '''Generates a list of wylie characters, from which the wylie string
            is composed of.'''

        result = []
        syll = self.syllable.wylie

        while len(syll) != 0:
            for i in range(3, 0, -1):
                part = syll[:i]

                if part in tables.W_ROOTLETTERS + tables.W_VOWELS \
                        or part == 'g.':
                    result.append(part)
                    syll = syll[len(part):]

        return result

    def validSuperscribe(self, head, root):
        if head not in tables.SUPER:
            return False
        else:
            return root in self.rulesSuper[head]

    def validSubscribe(self, sub, root):
        if sub not in tables.SUB:
            return False

        else:
            return root in self.rulesSub[sub]

    def appendWylieChar(self, char):
        self.syllable.wylie = ''.join([self.syllable.wylie, char])

    def add(self, char):
        self.appendWylieChar(char)
        self.determineWylie()
        self.renderUnicode()

    def needsSubjoin(self, comp):
        if comp == 'subjoined' or comp == 'secondsub' \
                or (comp == 'root' and self.getCharacterOf('super')):
            return True
        else:
            return False

    def renderUnicode(self):
        for comp in tables.SYLLSTRUCT:
            char = self.getCharacterOf(comp)

            if char == 'a' and comp != 'root':
                continue

            newString = [self.syllable.uni]

            if char:
    # TODO: More efficient handling of g. irregular.
                if char == 'g.':
                    char = 'g'
                    self.setStruct(comp, char)

                if self.needsSubjoin(comp):
                    newString.append(self.toSubjoinedUnicode(char))

                else:
                    newString.append(self.toUnicode(char))

                self.syllable.uni = u''.join(newString)

    def isPrefix(self, char):
        if char in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self):
        self.syllable.tsheg()
        return self.syllable.uni

    def alphabet(self):  # {{{
        for i, key in enumerate(tables.W_ROOTLETTERS):
            self.newSyllable()
            self.tsheg()

            if i % 4 == 0:
                sys.stdout.write("\n")

        sys.stdout.write("\n")

    def vowels(self):
        for key in tables.W_VOWELS:
            self.newSyllable('a')
            self.add(key)
            self.tsheg()
        print()

    def testWylie(self, string):
        self.newSyllable()

        for i, s in enumerate(string):
            self.add(s)

        print(string + " : " + self.tsheg())

    def printBytecodes(self, string):
        self.newSyllable()

        for i, s in enumerate(string):
            self.add(s)

        for uni in self.syllable.uni:
            print('U+{0:04X}'.format(ord(uni)))


    # }}}


class Syllable(object):
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

    def clear(self):
        self.uni = u''
        for s in tables.SYLLSTRUCT:
            self.struct[s] = ''


def main():
    t = Translator()
    # t.alphabet()
    # t.vowels()

    if len(argv) < 2:
        t.printBytecodes('bskyongs')
        # t.testWylie('sangs')
        # t.testWylie('bre')
        # t.testWylie('rta')
        # t.testWylie('mgo')
        # t.testWylie('gya')
        # t.testWylie('g.yag')
        # t.testWylie('\'rba')
        # t.testWylie('tshos')
        # t.testWylie('lhongs')
        # t.testWylie('mngar')
        # t.testWylie('sngas')
        # t.testWylie('rnyongs')
        # t.testWylie('brnyes')
        # t.testWylie('rgyas')
        # t.testWylie('skyongs')
        # t.testWylie('bskyongs')
        # t.testWylie('grwa')
        # t.testWylie('spre\'u')
        # t.testWylie('spre\'u\'i')
        # t.testWylie('\'dra')
        # t.testWylie('\'bya')
        # t.testWylie('\'gra')
        # t.testWylie('\'gyang')
        # t.testWylie('\'khra')
        # t.testWylie('\'khyig')
        # t.testWylie('\'kyags')
        # t.testWylie('\'phre')
        # t.testWylie('\'phyags')
        # t.testWylie('a')
        # t.testWylie('o')
        # t.testWylie('a\'am')
        # t.testWylie('ab')
        # t.testWylie('bswa')
        # t.testWylie('bha')
        return

    f = open(argv[1], 'r')

    for line in f:
        t.testWylie(line.rstrip())

    f.close()

if __name__ == '__main__':
    main()
