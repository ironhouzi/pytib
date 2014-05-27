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
    Basic steps for the analysis:
        1. Partition the wylie string into wylie letters.
        2. Find the position of the vowel.
        3. Define the syllable components (prefix, superscribed, etc.) for all
            letters before and including the vowel.
        4. Define the syllable components for the letters after the vowel.
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

    def modSyllableStructure(self, component, wylieLetter):
        self.syllable.structure[component] = wylieLetter

    def getCharacterFor(self, component):
        return self.syllable.structure[component]

    def getVowelIndex(self, wylieLetters):
        for i, char in enumerate(wylieLetters):
            if char in tables.W_VOWELS:
                return i
        return -1

    def isSuperscribed(self, wylieLetters, vowelPosition):
        if vowelPosition == 2:
            return self.validSuperscribe(wylieLetters[0], wylieLetters[1]) \
                and not self.validSubscribe(wylieLetters[1], wylieLetters[0])
        else:   # vowelPosition == 3
            return self.isPrefix(wylieLetters[0]) \
                and self.validSuperscribe(wylieLetters[1], wylieLetters[2]) \
                and not self.validSubscribe(wylieLetters[2], wylieLetters[1])

    def isSubscribed(self, wylieLetters, vowelPosition):
        if vowelPosition == 2:
            return not self.validSuperscribe(wylieLetters[0], wylieLetters[1]) \
                and self.validSubscribe(wylieLetters[1], wylieLetters[0])
        else:   # vowelPosition == 3
            return self.isPrefix(wylieLetters[0]) \
                and not self.validSuperscribe(wylieLetters[1], wylieLetters[2]) \
                and self.validSubscribe(wylieLetters[2], wylieLetters[1])

    def vowelAtZero(self, wylieLetters):
        if wylieLetters[0] in tables.W_VOWELS:
            # wylieLetters[0] != 'a' ?
            if wylieLetters[0] != W_ROOTLETTERS[-1]:
            # For single letter vowels w/o the 'a'. Prepends the vowel with
            # the 'a' character, to get correct unicode.
            # TODO  Move to renderUnicode().
                self.syllable.wylie = ''.join([W_ROOTLETTERS[-1],
                                               wylieLetters[0]])
                self.modSyllableStructure('root', W_ROOTLETTERS[-1])
                self.modSyllableStructure('vowel', wylieLetters[0])
            else:
                self.modSyllableStructure('root',  wylieLetters[0])
                self.modSyllableStructure('vowel', wylieLetters[0])

    def vowelAtOne(self, wylieLetters):
        self.modSyllableStructure('root', wylieLetters[0])
        self.modSyllableStructure('vowel', wylieLetters[1])

    def vowelAtTwo(self, wylieLetters):
        if self.isSubscribed(wylieLetters, 2):
            self.modSyllableStructure('root',      wylieLetters[0])
            self.modSyllableStructure('subjoined', wylieLetters[1])
        elif self.isSuperscribed(wylieLetters, 2):
            self.modSyllableStructure('super', wylieLetters[0])
            self.modSyllableStructure('root',  wylieLetters[1])
        else:
            self.modSyllableStructure('prefix', wylieLetters[0])
            self.modSyllableStructure('root',   wylieLetters[1])
        self.modSyllableStructure('vowel', wylieLetters[2])

    def vowelAtThree(self, wylieLetters):
        if self.isIrregular(3, wylieLetters):
            self.modSyllableStructure('root',      wylieLetters[0])
            self.modSyllableStructure('subjoined', wylieLetters[1])
            self.modSyllableStructure('secondsub', wylieLetters[2])
        elif self.isSuperscribed(wylieLetters, 3):
            self.modSyllableStructure('prefix', wylieLetters[0])
            self.modSyllableStructure('super',  wylieLetters[1])
            self.modSyllableStructure('root',   wylieLetters[2])
        elif self.isSubscribed(wylieLetters, 3):
            self.modSyllableStructure('prefix',    wylieLetters[0])
            self.modSyllableStructure('root',      wylieLetters[1])
            self.modSyllableStructure('subjoined', wylieLetters[2])
        else:
            self.modSyllableStructure('super',     wylieLetters[0])
            self.modSyllableStructure('root',      wylieLetters[1])
            self.modSyllableStructure('subjoined', wylieLetters[2])
        self.modSyllableStructure('vowel', wylieLetters[3])

    def vowelAtFour(self, wylieLetters):
        if self.isIrregular(4, wylieLetters):
            self.modSyllableStructure('prefix',    wylieLetters[0])
            self.modSyllableStructure('root',      wylieLetters[1])
            self.modSyllableStructure('subjoined', wylieLetters[2])
            self.modSyllableStructure('secondsub', wylieLetters[3])
        else:
            self.modSyllableStructure('prefix',    wylieLetters[0])
            self.modSyllableStructure('super',     wylieLetters[1])
            self.modSyllableStructure('root',      wylieLetters[2])
            self.modSyllableStructure('subjoined', wylieLetters[3])
        self.modSyllableStructure('vowel', wylieLetters[4])

    analyzeSyllable = [vowelAtZero, vowelAtOne, vowelAtTwo,
                       vowelAtThree, vowelAtFour]

    def singleWylieChar(self, wylieLetters):
        self.modSyllableStructure('root', wylieLetters[0])
        if wylieLetters[0] in tables.W_VOWELS:
            self.modSyllableStructure('vowel', wylieLetters[0])
        else:
            self.modSyllableStructure('root', 'a')
            self.modSyllableStructure('vowel', wylieLetters[0])

    def analyzeWylie(self):
        wylieLetters = self.partitionToWylie(self.syllable)
        self.syllable.clear()
        if len(wylieLetters) == 1:
            self.singleWylieChar(wylieLetters)
        # TODO Remove redundant vowel check
        if self.hasNoVowel(wylieLetters):
            return
        else:
            vowelPosition = self.getVowelIndex(wylieLetters)
            self.analyzeSyllable[vowelPosition](self, wylieLetters)
            self.findSuffixes(vowelPosition, wylieLetters)

    def isIrregular(self, vowelPosition, wylieLetters):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''
        if wylieLetters[vowelPosition-1] == tables.W_ROOTLETTERS[19] \
                and wylieLetters[vowelPosition-2] == tables.W_ROOTLETTERS[24]:
            return True
        else:
            return False

    def findSuffixes(self, vowelPosition, wylieLetters):
    # TODO: Iterator for POSTVOWEL.next *if* that doesn't impede performance
        j = 0
        for i in range(vowelPosition+1, len(wylieLetters)):
            wylieChar = wylieLetters[i]
            if wylieChar:
                self.modSyllableStructure(tables.POSTVOWEL[j], wylieChar)
                j += 1

    def hasNoVowel(self, wylieLetters):
        for char in wylieLetters:
            if char in tables.W_VOWELS:
                return False
        return True

    def partitionToWylie(self, syllable):
        '''Generates a list of wylie characters, from which the wylie string
            is composed of.
           Test if the i last roman letters in the wylie string matches a
           valid wylie character and continue until the entire wylie string
           is partitioned.'''
        result = []
        wylieSyllable = syllable.wylie
        while len(wylieSyllable) != 0:
            for i in range(3, 0, -1):
                part = wylieSyllable[:i]
                if part in tables.W_ROOTLETTERS + tables.W_VOWELS \
                        or part == tables.IRREGULAR_G:
                    result.append(part)
                    wylieSyllable = wylieSyllable[len(part):]
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
        self.analyzeWylie()
        self.renderUnicode()

    def needsSubjoin(self, component):
        if component == 'subjoined' or component == 'secondsub' \
                or (component == 'root' and self.getCharacterFor('super')):
            return True
        else:
            return False

    def renderUnicode(self):
        for syllableComponent in tables.SYLLSTRUCT:
            char = self.getCharacterFor(syllableComponent)
            if char == 'a' and syllableComponent != 'root':
                continue
            newString = [self.syllable.uni]
            if char:
    # TODO: More efficient handling of g. irregular.
                if char == 'g.':
                    char = 'g'
                    self.modSyllableStructure(syllableComponent, char)
                if self.needsSubjoin(syllableComponent):
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

    def listVowels(self):
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
    # t.listVowels()
    if len(argv) < 2:
        # t.printBytecodes('bskyongs')
        t.testWylie('sangs')
        t.testWylie('bre')
        t.testWylie('rta')
        t.testWylie('mgo')
        t.testWylie('gya')
        t.testWylie('g.yag')
        t.testWylie('\'rba')
        t.testWylie('tshos')
        t.testWylie('lhongs')
        t.testWylie('mngar')
        t.testWylie('sngas')
        t.testWylie('rnyongs')
        t.testWylie('brnyes')
        t.testWylie('rgyas')
        t.testWylie('skyongs')
        t.testWylie('bskyongs')
        t.testWylie('grwa')
        t.testWylie('spre\'u')
        t.testWylie('spre\'u\'i')
        t.testWylie('\'dra')
        t.testWylie('\'bya')
        t.testWylie('\'gra')
        t.testWylie('\'gyang')
        t.testWylie('\'khra')
        t.testWylie('\'khyig')
        t.testWylie('\'kyags')
        t.testWylie('\'phre')
        t.testWylie('\'phyags')
        t.testWylie('a')
        t.testWylie('o')
        t.testWylie('a\'am')
        t.testWylie('ab')
        t.testWylie('bswa')
        t.testWylie('bha')
        return
    f = open(argv[1], 'r')
    for line in f:
        t.testWylie(line.rstrip())
    f.close()

if __name__ == '__main__':
    main()
