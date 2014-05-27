'''
    Wylie2Uni
    Wylie to Unicode convertor
    Requires Python 3
'''

# TODO: Write unit tests!

import sys
import tables
from sys import argv


class Translator(object):
    '''Translates wylie into Tibetan Unicode
    Instantiates a Syllable object in the object variable self.syllable.
    Contain methods for analyzing and validifying the Syllable-object.
    Basic steps for the analysis:
        1. Partition the wylie string into wylie letters.
        2. Find the position of the vowel.
        3. Define the syllable components (prefix, superscribed, etc.) for all
            letters before the vowel.
        4. Define the syllable components for the letters after the vowel.
    '''

    def __init__(self):
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        self.wylieToUnicode = dict(zip(wTable, uTable))
        self.validSuperjoinedList = dict(zip(tables.SUPER, tables.SUPER_RULES))
        self.validSubjoinedList = dict(zip(tables.SUB, tables.SUB_RULES))

    def toUnicode(self, wylieSyllable):
        return self.wylieToUnicode[str(wylieSyllable)]

    def toSubjoinedUnicode(self, wylieSyllable):
        return chr(ord(self.wylieToUnicode[str(wylieSyllable)]) + tables.SUBOFFSET)

    def modSyllableStructure(self, syllable, component, wylieLetter):
        syllable.structure[component] = wylieLetter

    def getCharacterFor(self, syllable, syllableComponent):
        return syllable.structure[syllableComponent]

    def getVowelIndex(self, wylieLetters):
        for i, char in enumerate(wylieLetters):
            if char in tables.W_VOWELS:
                return i
        return -1

    def isSuperscribed(self, wylieLetters, vowelPosition):
        if vowelPosition == 2:
            return self.validSuperscribe(wylieLetters[0], wylieLetters[1]) \
                and not self.validSubscribe(wylieLetters[0], wylieLetters[1])
        else:   # vowelPosition == 3
            return self.isPrefix(wylieLetters[0]) \
                and self.validSuperscribe(wylieLetters[1], wylieLetters[2]) \
                and not self.validSubscribe(wylieLetters[1], wylieLetters[2])

    def isSubscribed(self, wylieLetters, vowelPosition):
        if vowelPosition == 2:
            return not self.validSuperscribe(wylieLetters[0], wylieLetters[1]) \
                and self.validSubscribe(wylieLetters[0], wylieLetters[1])
        else:   # vowelPosition == 3
            return self.isPrefix(wylieLetters[0]) \
                and not self.validSuperscribe(wylieLetters[1], wylieLetters[2]) \
                and self.validSubscribe(wylieLetters[1], wylieLetters[2])

    def vowelAtZero(self, syllable, wylieLetters):
        wylie_a_vowel = tables.W_ROOTLETTERS[-1]
        if wylieLetters[0] in tables.W_VOWELS:
            if wylieLetters[0] != wylie_a_vowel:
            # For single letter vowels w/o the 'a'. Prepends the vowel with
            # the 'a' character, to get correct unicode.
            # TODO  Move to generateUnicode().
                syllable.wylie = ''.join([wylie_a_vowel, wylieLetters[0]])
                self.modSyllableStructure(syllable, 'root', wylie_a_vowel)
                self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])
            else:
                self.modSyllableStructure(syllable, 'root',  wylieLetters[0])
                self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])

    def vowelAtOne(self, syllable, wylieLetters):
        self.modSyllableStructure(syllable, 'root', wylieLetters[0])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[1])

    def vowelAtTwo(self, syllable, wylieLetters):
        if self.isSubscribed(wylieLetters, 2):
            self.modSyllableStructure(syllable, 'root',      wylieLetters[0])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[1])
        elif self.isSuperscribed(wylieLetters, 2):
            self.modSyllableStructure(syllable, 'super', wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',  wylieLetters[1])
        else:
            self.modSyllableStructure(syllable, 'prefix', wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',   wylieLetters[1])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[2])

    def vowelAtThree(self, syllable, wylieLetters):
        if self.isIrregular(3, wylieLetters):
            self.modSyllableStructure(syllable, 'root',      wylieLetters[0])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[1])
            self.modSyllableStructure(syllable, 'secondsub', wylieLetters[2])
        elif self.isSuperscribed(wylieLetters, 3):
            self.modSyllableStructure(syllable, 'prefix', wylieLetters[0])
            self.modSyllableStructure(syllable, 'super',  wylieLetters[1])
            self.modSyllableStructure(syllable, 'root',   wylieLetters[2])
        elif self.isSubscribed(wylieLetters, 3):
            self.modSyllableStructure(syllable, 'prefix',    wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',      wylieLetters[1])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[2])
        else:
            self.modSyllableStructure(syllable, 'super',     wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',      wylieLetters[1])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[2])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[3])

    def vowelAtFour(self, syllable, wylieLetters):
        if self.isIrregular(4, wylieLetters):
            self.modSyllableStructure(syllable, 'prefix',    wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',      wylieLetters[1])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[2])
            self.modSyllableStructure(syllable, 'secondsub', wylieLetters[3])
        else:
            self.modSyllableStructure(syllable, 'prefix',    wylieLetters[0])
            self.modSyllableStructure(syllable, 'super',     wylieLetters[1])
            self.modSyllableStructure(syllable, 'root',      wylieLetters[2])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[3])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[4])

    analyzeSyllable = [vowelAtZero, vowelAtOne, vowelAtTwo,
                       vowelAtThree, vowelAtFour]

    def singleWylieLetter(self, syllable, wylieLetters):
        self.modSyllableStructure(syllable, 'root', wylieLetters[0])
        if wylieLetters[0] in tables.W_VOWELS:
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])
        else:
            wylie_a_vowel = tables.W_ROOTLETTERS[-1]
            self.modSyllableStructure(syllable, 'root', wylie_a_vowel)
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])

    def analyzeWylie(self, syllable):
        wylieLetters = self.partitionToWylie(syllable)
        syllable.clear()
        if len(wylieLetters) == 1:
            self.singleWylieLetter(syllable, wylieLetters)
        # TODO Remove redundant vowel check
        if self.hasNoVowel(wylieLetters):
            # TODO handle exception
            return
        else:
            vowelPosition = self.getVowelIndex(wylieLetters)
            self.analyzeSyllable[vowelPosition](self, syllable, wylieLetters)
            self.findSuffixes(syllable, vowelPosition, wylieLetters)

    def isIrregular(self, vowelPosition, wylieLetters):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''
        return wylieLetters[vowelPosition-1] == tables.W_ROOTLETTERS[19] \
                and wylieLetters[vowelPosition-2] == tables.W_ROOTLETTERS[24]

    def findSuffixes(self, syllable, vowelPosition, wylieLetters):
    # TODO: Iterator for POSTVOWEL.next *if* that doesn't impede performance
    # TODO: Fix ugliness in this method!
        j = 0
        for i in range(vowelPosition+1, len(wylieLetters)):
            wylieChar = wylieLetters[i]
            if wylieChar:
                self.modSyllableStructure(syllable,
                                          tables.POSTVOWEL[j],
                                          wylieChar)
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
        wylieLetters = []
        wylieSyllable = syllable.wylie
        while len(wylieSyllable) != 0:
            for i in range(3, 0, -1):
                part = wylieSyllable[:i]
                if part in tables.W_ROOTLETTERS + tables.W_VOWELS \
                        or part == tables.IRREGULAR_G:
                    wylieLetters.append(part)
                    wylieSyllable = wylieSyllable[len(part):]
        return wylieLetters

    def validSuperscribe(self, headLetter, rootLetter):
        if headLetter not in tables.SUPER:
            return False
        else:
            return rootLetter in self.validSuperjoinedList[headLetter]

    def validSubscribe(self, rootLetter, subjoinedLetter):
        if subjoinedLetter not in tables.SUB:
            return False
        else:
            return rootLetter in self.validSubjoinedList[subjoinedLetter]

    def appendWylieString(self, syllable, wylieString):
        syllable.wylie = ''.join([syllable.wylie, wylieString])

    def appendWylie(self, syllable, wylieString):
        self.appendWylieString(syllable, wylieString)
        self.analyzeWylie(syllable)
        self.generateUnicode(syllable)

    def needsSubjoin(self, syllable, component):
        return component == 'subjoined' or component == 'secondsub' \
                or (component == 'root' \
                and self.getCharacterFor(syllable, 'super'))

    def generateUnicode(self, syllable):
        wylie_a_vowel = tables.W_ROOTLETTERS[-1]
        for syllableComponent in tables.SYLLSTRUCT:
            char = self.getCharacterFor(syllable, syllableComponent)
            if char == wylie_a_vowel and syllableComponent != 'root':
                continue
            newString = [syllable.uni]
            if char:
    # TODO: More efficient handling of g. irregular.
                # char == 'g.' ?
                if char == tables.IRREGULAR_G:
                    char = tables.W_ROOTLETTERS[2]
                    self.modSyllableStructure(syllable, syllableComponent, char)
                if self.needsSubjoin(syllable, syllableComponent):
                    newString.append(self.toSubjoinedUnicode(char))
                else:
                    newString.append(self.toUnicode(char))
                syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        if char in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self, syllable):
        syllable.tsheg()
        return syllable.uni

    # {{{
    def testWylie(self, wylieString):
        syllable = Syllable('')
        for i, s in enumerate(wylieString):
            self.appendWylie(syllable, s)
        syllable.tsheg()
        print(wylieString + " : " + syllable.uni)

    def printBytecodes(self, string):
        syllable = Syllable('')
        print("Bytecodes for %s" % (string))
        for i, s in enumerate(string):
            self.appendWylie(syllable, s)
        for uni in syllable.uni:
            print('U+{0:04X}'.format(ord(uni)))
    # }}}


class Syllable(object):
    def __init__(self, wylieString):
        self.wylie = wylieString
        self.uni = ''
        self.structure = dict((key, '') for key in tables.SYLLSTRUCT)

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = u''.join([self.uni, tables.TSHEG])

    def appendUni(self, uni):
        self.uni = ''.join([self.uni, uni])

    def clear(self):
        self.uni = ''
        for s in tables.SYLLSTRUCT:
            self.structure[s] = ''


def main():
    t = Translator()
    if len(argv) < 2:
        t.printBytecodes('bskyongs')
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
