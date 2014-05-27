'''Wylie2Uni
    Wylie to Unicode convertor'''

# TODO: Write unit testWylies!

import sys
import tables
from sys import argv

TSHEG = '\u0f0b'
SUBOFFSET = 0x50


class Translator(object):
    '''Translates wylie into Tibetan Unicode
    Instantiates a Syllable object in the object variable self.syllable.
    Contain methods for analyzing and validifying the Syllable-object.
    '''

    def __init__(self):
        self.syllable = Syllable('')
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        self.lookup = dict(zip(wTable, uTable))
        self.validSuperjoinedList = dict(zip(tables.SUPER, tables.SUPER_RULES))
        self.validSubjoinedList = dict(zip(tables.SUB, tables.SUB_RULES))

    def newSyllable(self):
        self.syllable = Syllable('')

    def toUnicode(self, syllable):
        return self.lookup[str(syllable)]

    def toSubjoinedUnicode(self, syllable):
        return chr(ord(self.lookup[str(syllable)]) + SUBOFFSET)

    def modifySyllable(self, component, letter):
        self.syllable.structure[component] = letter

    def getCharacterOf(self, component):
        return self.syllable.structure[component]

    def getVowelIndex(self, vowelParts):
        for i, char in enumerate(vowelParts):
            if char in tables.W_VOWELS:
                return i
        return -1

    def isSuperscribed(self, vowelParts, vowelPosition):
        if vowelPosition == 2:
            return self.validSuperscribe(vowelParts[0], vowelParts[1]) \
                and not self.validSubscribe(vowelParts[1], vowelParts[0])
        else:   # vowelPosition == 3
            return self.isPrefix(vowelParts[0]) \
                and self.validSuperscribe(vowelParts[1], vowelParts[2]) \
                and not self.validSubscribe(vowelParts[2], vowelParts[1])

    def isSubscribed(self, vowelParts, vowelPosition):
        if vowelPosition == 2:
            return not self.validSuperscribe(vowelParts[0], vowelParts[1]) \
                and self.validSubscribe(vowelParts[1], vowelParts[0])
        else:   # vowelPosition == 3
            return self.isPrefix(vowelParts[0]) \
                and not self.validSuperscribe(vowelParts[1], vowelParts[2]) \
                and self.validSubscribe(vowelParts[2], vowelParts[1])

    def vowelAtZero(self, vowelParts):
        if vowelParts[0] in tables.W_VOWELS:
            if vowelParts[0] != 'a':
            # TODO This gives incorrect wylie. Move to renderUnicode().
                self.syllable.wylie = ''.join(['a', vowelParts[0]])
                self.modifySyllable('root', 'a')
                self.modifySyllable('vowel', vowelParts[0])
            else:
                self.modifySyllable('root',  vowelParts[0])
                self.modifySyllable('vowel', vowelParts[0])

    def vowelAtOne(self, vowelParts):
        self.modifySyllable('root', vowelParts[0])
        self.modifySyllable('vowel', vowelParts[1])

    def vowelAtTwo(self, vowelParts):
        if self.isSubscribed(vowelParts, 2):
            self.modifySyllable('root',      vowelParts[0])
            self.modifySyllable('subjoined', vowelParts[1])
        elif self.isSuperscribed(vowelParts, 2):
            self.modifySyllable('super', vowelParts[0])
            self.modifySyllable('root',  vowelParts[1])
        else:
            self.modifySyllable('prefix', vowelParts[0])
            self.modifySyllable('root',   vowelParts[1])
        self.modifySyllable('vowel', vowelParts[2])

    def vowelAtThree(self, vowelParts):
        if self.isIrregular(3, vowelParts):
            self.modifySyllable('root',      vowelParts[0])
            self.modifySyllable('subjoined', vowelParts[1])
            self.modifySyllable('secondsub', vowelParts[2])
        elif self.isSuperscribed(vowelParts, 3):
            self.modifySyllable('prefix', vowelParts[0])
            self.modifySyllable('super',  vowelParts[1])
            self.modifySyllable('root',   vowelParts[2])
        elif self.isSubscribed(vowelParts, 3):
            self.modifySyllable('prefix',    vowelParts[0])
            self.modifySyllable('root',      vowelParts[1])
            self.modifySyllable('subjoined', vowelParts[2])
        else:
            self.modifySyllable('super',     vowelParts[0])
            self.modifySyllable('root',      vowelParts[1])
            self.modifySyllable('subjoined', vowelParts[2])
        self.modifySyllable('vowel', vowelParts[3])

    def vowelAtFour(self, vowelParts):
        if self.isIrregular(4, vowelParts):
            self.modifySyllable('prefix',    vowelParts[0])
            self.modifySyllable('root',      vowelParts[1])
            self.modifySyllable('subjoined', vowelParts[2])
            self.modifySyllable('secondsub', vowelParts[3])
        else:
            self.modifySyllable('prefix',    vowelParts[0])
            self.modifySyllable('super',     vowelParts[1])
            self.modifySyllable('root',      vowelParts[2])
            self.modifySyllable('subjoined', vowelParts[3])
        self.modifySyllable('vowel', vowelParts[4])

    analyzeSyllable = [vowelAtZero, vowelAtOne, vowelAtTwo,
                       vowelAtThree, vowelAtFour]

    def singleWylieCharacter(self, vowelParts):
        self.modifySyllable('root', vowelParts[0])
        if vowelParts[0] in tables.W_VOWELS:
            self.modifySyllable('vowel', vowelParts[0])
        else:
            self.modifySyllable('root', 'a')
            self.modifySyllable('vowel', vowelParts[0])

    def determineWylie(self):
        vowelParts = self.partition()
        self.syllable.clear()
        if len(vowelParts) == 1:
            self.singleWylieCharacter(vowelParts)
        # TODO Remove redundant vowel check
        if self.noVowels(vowelParts):
            return
        else:
            vowelPosition = self.getVowelIndex(vowelParts)
            self.analyzeSyllable[vowelPosition](self, vowelParts)
            self.findSuffixes(vowelPosition, vowelParts)

    def isIrregular(self, vowelPosition, vowelParts):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''
        if vowelParts[vowelPosition-1] == 'w' \
                and vowelParts[vowelPosition-2] == 'r':
            return True
        else:
            return False

    def findSuffixes(self, vowelPosition, vowelParts):
    # TODO: Iterator for POSTVOWEL.next *if* that doesn't impede performance
        j = 0
        for i in range(vowelPosition+1, len(vowelParts)):
            wylieChar = vowelParts[i]
            if wylieChar:
                self.modifySyllable(tables.POSTVOWEL[j], wylieChar)
                j += 1

    def noVowels(self, vowelParts):
        for char in vowelParts:
            if char in tables.W_VOWELS:
                return False
        return True

    def partition(self):
        '''Generates a list of wylie characters, from which the wylie string
            is composed of.
           Test if the i last roman letters in the wylie string matches a
           valid wylie character and continue until the entire wylie string
           is partitioned.'''
        result = []
        syllable = self.syllable.wylie
        while len(syllable) != 0:
            for i in range(3, 0, -1):
                part = syllable[:i]
                if part in tables.W_ROOTLETTERS + tables.W_VOWELS \
                        or part == 'g.':
                    result.append(part)
                    syllable = syllable[len(part):]
        return result

    def validSuperscribe(self, headLetter, rootLetter):
        if headLetter not in tables.SUPER:
            return False
        else:
            return rootLetter in self.validSuperjoinedList[headLetter]

    def validSubscribe(self, subjoinedLetter, rootLetter):
        if subjoinedLetter not in tables.SUB:
            return False
        else:
            return rootLetter in self.validSubjoinedList[subjoinedLetter]

    def appendWylieChar(self, char):
        self.syllable.wylie = ''.join([self.syllable.wylie, char])

    def appendLetter(self, char):
        self.appendWylieChar(char)
        self.determineWylie()
        self.renderUnicode()

    def needsSubjoin(self, component):
        if component == 'subjoined' or component == 'secondsub' \
                or (component == 'root' and self.getCharacterOf('super')):
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
                    self.modifySyllable(comp, char)
                if self.needsSubjoin(comp):
                    newString.append(self.toSubjoinedUnicode(char))
                else:
                    newString.append(self.toUnicode(char))
                self.syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        if char in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self):
        self.syllable.tsheg()
        return self.syllable.uni

    def listAlphabet(self):  # {{{
        for i, key in enumerate(tables.W_ROOTLETTERS):
            self.newSyllable()
            self.tsheg()
            if i % 4 == 0:
                sys.stdout.write("\n")
        sys.stdout.write("\n")

    def vowels(self):
        for key in tables.W_VOWELS:
            self.newSyllable('a')
            self.appendLetter(key)
            self.tsheg()
        print()

    def testWylie(self, wylieString):
        self.newSyllable()
        for i, s in enumerate(wylieString):
            self.appendLetter(s)
        print(wylieString + " : " + self.tsheg())

    def printBytecodes(self, string):
        self.newSyllable()
        for i, s in enumerate(string):
            self.appendLetter(s)
        for uni in self.syllable.uni:
            print('U+{0:04X}'.format(ord(uni)))
    # }}}


class Syllable(object):
    def __init__(self, wylie):
        self.wylie = wylie
        self.uni = ''
        self.structure = dict((key, '') for key in tables.SYLLSTRUCT)

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = u''.join([self.uni, TSHEG])

    def appendUni(self, uni):
        self.uni = ''.join([self.uni, uni])

    def clear(self):
        self.uni = u''
        for s in tables.SYLLSTRUCT:
            self.structure[s] = ''


def main():
    t = Translator()
    # t.listAlphabet()
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
