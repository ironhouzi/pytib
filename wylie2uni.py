'''
    Wylie2Uni
    Wylie to Unicode convertor
    Requires Python 3
'''

import tables
from codecs import encode
from os import urandom
from sys import argv


class Translator(object):
    '''Translates wylie into Tibetan Unicode
    Contain methods for analyzing and validifying a Syllable object.
    --------------
    Wylie analysis
    --------------
    This analysis is ran after the initial Sanskrit check.The syllable is
    checked against the defined rules and if the wylie analysis returns False,
    the syllable will be defined as Sanskrit.
    --------------
    Basic steps for the syllable computation:
        0. Perform initial Sanskrit check.
        1. Partition into a list of wylie letters: the Syllable.wylie string.
        2. Find the vowel position in the list.
        3. Define the syllable components (prefix, superscribed, etc.) for all
            letters before the vowel.
        4. Define the syllable components for the letters after the vowel.
        5. Compute the unicode string based on the analysis and store the
            unicode string in Syllable.uni.
    -----------------
    Sanskrit analysis
    -----------------
    The syllable will first be ran against the initial Sanskrit check. Clear
    Sanskrit cases will be checked as well as a few cases where the syllable
    does pass the wylie checks, but are actually Sanskrit
    (tables.S_DOUBLE_CONSONANTS).
    '''

    def __init__(self):
        wTable = (tables.W_ROOTLETTERS + tables.W_VOWELS)
        uTable = (tables.U_ROOTLETTERS + tables.U_VOWELS)
        swTable = (tables.SW_ROOTLETTERS + tables.SW_VOWELS)
        suTable = (tables.SU_ROOTLETTERS + tables.SU_VOWELS)
        self.wylieToUnicode = dict(zip(wTable, uTable))
        self.sanskritWylieToUnicode = dict(zip(swTable, suTable))
        self.validSuperjoinedList = dict(zip(tables.SUPER, tables.SUPER_RULES))
        self.validSubjoinedList = dict(zip(tables.SUB, tables.SUB_RULES))
        self.allVowels = (tables.W_VOWELS + (tables.W_ROOTLETTERS[-1],))
        self.errorVal = str(encode(urandom(8), 'hex'))[2:-1]
        sTable = (tables.SUFFIXES, tables.SUFFIX2S)
        self.validSuffix = dict(zip(tables.POSTVOWEL, sTable))

    def toUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = None
        if isSanskrit:
            lookup = self.sanskritWylieToUnicode
        else:
            lookup = self.wylieToUnicode
        return lookup[str(wylieSyllable)]

    def toSubjoinedUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = None
        if isSanskrit:
            lookup = self.sanskritWylieToUnicode
        else:
            lookup = self.wylieToUnicode
        return chr(ord(lookup[str(wylieSyllable)]) + tables.SUBOFFSET)

    def modSyllableStructure(self, syllable, component, wylieLetter):
        syllable.structure[component] = wylieLetter

    def getCharacterFor(self, syllable, syllableComponent):
        return syllable.structure[syllableComponent]

    def getVowelIndex(self, wylieLetters, isSanskrit=False):
        vowelList = []
        if isSanskrit:
            vowelList = tables.SW_VOWELS + (tables.W_ROOTLETTERS[-1], )
        else:
            vowelList = self.allVowels
        for i, char in enumerate(wylieLetters):
            if char in vowelList:
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

    # element index correlates to the syllable's vowel position
    analyzeBaseCase = (None,
                       (lambda self, wylieLetters : \
                               wylieLetters[0] in tables.W_ROOTLETTERS and \
                               wylieLetters[1] in self.allVowels),
                       (lambda self, wylieLetters : \
                               wylieLetters[0] == tables.PREFIX_GA or \
                               wylieLetters[0] in tables.PREFIXES and \
                               wylieLetters[1] in tables.W_ROOTLETTERS),
                       (lambda self, wylieLetters : \
                               wylieLetters[0] in tables.SUPER and \
                               wylieLetters[1] in tables.W_ROOTLETTERS and \
                               wylieLetters[2] in tables.SUB),
                       (lambda self, wylieLetters : \
                               wylieLetters[0] in tables.PREFIXES and \
                               wylieLetters[1] in tables.SUPER and \
                               wylieLetters[2] in tables.W_ROOTLETTERS and \
                               wylieLetters[3] in tables.SUB)
                      )

    def vowelAtFirstPosition(self, syllable, wylieLetters):
        if not wylieLetters[0] in self.allVowels:
            return False
        wylie_a_vowel = tables.W_ROOTLETTERS[-1]
        if wylieLetters[0] in self.allVowels:
            if wylieLetters[0] != wylie_a_vowel:
            # For single letter vowels w/o the 'a'. Prepends the vowel with
            # the 'a' character, to get correct unicode.
            # TODO  Move to generateWylieUnicode().
                syllable.wylie = ''.join([wylie_a_vowel, wylieLetters[0]])
                self.modSyllableStructure(syllable, 'root', wylie_a_vowel)
            else:
                self.modSyllableStructure(syllable, 'root', wylieLetters[0])
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])

    def vowelAtSecondPosition(self, syllable, wylieLetters):
        if not self.analyzeBaseCase[1](self, wylieLetters):
            return self.errorVal
        self.modSyllableStructure(syllable, 'root', wylieLetters[0])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[1])

    def vowelAtThirdPosition(self, syllable, wylieLetters):
        if self.isSubscribed(wylieLetters, 2):
            self.modSyllableStructure(syllable, 'root',      wylieLetters[0])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[1])
        elif self.isSuperscribed(wylieLetters, 2):
            self.modSyllableStructure(syllable, 'super', wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',  wylieLetters[1])
        elif self.analyzeBaseCase[2](self, wylieLetters):
            self.modSyllableStructure(syllable, 'prefix', wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',   wylieLetters[1])
        else:
            return self.errorVal
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[2])

    def vowelAtFourthPosition(self, syllable, wylieLetters):
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
        elif self.analyzeBaseCase[3](self, wylieLetters):
            self.modSyllableStructure(syllable, 'super',     wylieLetters[0])
            self.modSyllableStructure(syllable, 'root',      wylieLetters[1])
            self.modSyllableStructure(syllable, 'subjoined', wylieLetters[2])
        else:
            return self.errorVal
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[3])

    def vowelAtFifthPosition(self, syllable, wylieLetters):
        if not self.analyzeBaseCase[4](self, wylieLetters):
            return self.errorVal
        self.modSyllableStructure(syllable, 'prefix',    wylieLetters[0])
        self.modSyllableStructure(syllable, 'super',     wylieLetters[1])
        self.modSyllableStructure(syllable, 'root',      wylieLetters[2])
        self.modSyllableStructure(syllable, 'subjoined', wylieLetters[3])
        self.modSyllableStructure(syllable, 'vowel', wylieLetters[4])

    analyzeSyllable = (vowelAtFirstPosition, vowelAtSecondPosition,
                       vowelAtThirdPosition, vowelAtFourthPosition,
                       vowelAtFifthPosition)

    def singleWylieLetter(self, syllable, wylieLetters):
        self.modSyllableStructure(syllable, 'root', wylieLetters[0])
        if wylieLetters[0] in self.allVowels:
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])
        else:
            wylie_a_vowel = tables.W_ROOTLETTERS[-1]
            self.modSyllableStructure(syllable, 'root', wylie_a_vowel)
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])

    def invalidWylieString(self, syllable):
        if not syllable.wylie.startswith(tables.PREFIX_GA):
            for c in syllable.wylie:
                if not c in tables.W_ROOTLETTERS + tables.W_VOWELS:
                    return True
        return False

    def analyze(self, syllable):
        syllable.isSanskrit = self.isSanskrit(syllable)
        if not syllable.isSanskrit:
            syllable.isSanskrit = not self.analyzeWylie(syllable)
        if syllable.isSanskrit:
            self.analyzeSanskrit(syllable)
        else:
            self.generateWylieUnicode(syllable)

    def analyzeWylie(self, syllable):
        if self.invalidWylieString(syllable):
            return False
        wylieLetters = self.partitionToWylie(syllable)
        syllable.clear()
        if len(wylieLetters) == 1:
            self.singleWylieLetter(syllable, wylieLetters)
        vowelPosition = self.getVowelIndex(wylieLetters)
        if vowelPosition < 0:
            return False
        res = self.analyzeSyllable[vowelPosition](self, syllable, wylieLetters)
        if res == self.errorVal:
            return False
        return self.findSuffixes(syllable, vowelPosition, wylieLetters)

    def analyzeSanskrit(self, syllable):
        wylieLetters = self.partitionToWylie(syllable)
        syllable.clear()
        if len(wylieLetters) == 1:
            self.singleWylieLetter(syllable, wylieLetters)
        vowelPosition = self.getVowelIndex(wylieLetters, True)
        if vowelPosition < 0:
            return False
        self.generateSanskritUnicode(syllable, wylieLetters)
        return True

    def generateSanskritUnicode(self, syllable, wylieLetters):
        if syllable.wylie == tables.U_OM:
            syllable.uni = tables.S_OM
            return
        stack = [self.toUnicode(wylieLetters[0], True)]
        for i in range(1, len(wylieLetters)):
            if wylieLetters[i] == tables.W_ROOTLETTERS[-1]:
                continue
            if wylieLetters[i] in tables.SW_VOWELS + (tables.W_ROOTLETTERS[-1],):
                stack.append(self.toUnicode(wylieLetters[i], True))
            else:
                stack.append(self.toSubjoinedUnicode(wylieLetters[i], True))
        syllable.uni = ''.join(stack)

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
                syllableComponent = tables.POSTVOWEL[j]
                if j < 2 and not wylieChar in self.allVowels and not wylieChar in self.validSuffix[syllableComponent]:
                    return False
                self.modSyllableStructure(syllable, syllableComponent, wylieChar)
                j += 1
        return True

    def partitionToWylie(self, syllable):
        '''Generates a list of wylie characters, from which the wylie string
           is composed of.
           Test if the i last roman letters in the wylie string matches a
           valid wylie character and continue until the entire wylie string
           is partitioned.'''
        alphabet = []
        if syllable.isSanskrit:
            alphabet = tables.SW_ROOTLETTERS + tables.SW_VOWELS + (tables.W_ROOTLETTERS[-1], )
        else:
            alphabet = tables.W_ROOTLETTERS + tables.W_VOWELS
        wylieLetters = []
        wylieSyllable = syllable.wylie
        while len(wylieSyllable) != 0:
            for i in range(3, 0, -1):
                part = wylieSyllable[:i]
                if part in alphabet or part == tables.PREFIX_GA:
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

    def needsSubjoin(self, syllable, component):
        return component == 'subjoined' or component == 'secondsub' \
                or (component == 'root' \
                and self.getCharacterFor(syllable, 'super'))

    def generateWylieUnicode(self, syllable):
        wylie_a_vowel = tables.W_ROOTLETTERS[-1]
        for syllableComponent in tables.SYLLSTRUCT:
            char = self.getCharacterFor(syllable, syllableComponent)
            if char == wylie_a_vowel and syllableComponent != 'root':
                continue
            newString = [syllable.uni]
            if char:
                # char == 'g.' ?
                if char == tables.PREFIX_GA:
                    char = tables.W_ROOTLETTERS[2]
                    self.modSyllableStructure(syllable, syllableComponent, char)
                if self.needsSubjoin(syllable, syllableComponent):
                    newString.append(self.toSubjoinedUnicode(char))
                else:
                    newString.append(self.toUnicode(char))
                syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        return char in tables.PREFIXES

    def isSanskrit(self, syllable):
        string = syllable.wylie
        # Check if what could potentially be valid wylie, is actually Sanskrit
        if len(string) == 3 and string[0:2] in tables.S_DOUBLE_CONSONANTS:
            return True
        # Check for clear case Sanskrit syllables to save time
        matches = tables.S_BASIC_RULES
        for substring in matches:
            if string.startswith(substring):
                return True
        return 'ai' in string or 'au' in string

    def getBytecodes(self, wylieString):
        syllable = Syllable(wylieString)
        self.analyze(syllable)
        bytecodes = []
        for uni in syllable.uni:
            bytecodes.append('U+{0:04X}'.format(ord(uni)))
        return bytecodes


class Syllable(object):
    def __init__(self, wylieString):
        self.wylie = wylieString
        self.uni = ''
        self.structure = dict((key, '') for key in tables.SYLLSTRUCT)
        self.isSanskrit = False

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = ''.join([self.uni, tables.TSHEG])

    def clear(self):
        self.uni = ''
        for s in tables.SYLLSTRUCT:
            self.structure[s] = ''
