'''
    Wylie2Uni
    Wylie to Unicode convertor
    Requires Python 3
'''

from pytib.tables import *
import re
from codecs import encode
from os import urandom

# TODO: Handle case where syllable ends with '/' or '//'


class Translator(object):
    '''Translates wylie and International Alphabet of Sanskrit Transliteration
    (IAST) into Tibetan Unicode (U+0F00 - U+0FFF).
    The Translator class analyzes and validifies a Syllable object.
    --------------
    Wylie analysis
    --------------
    This analysis is done after the initial Sanskrit check.The syllable is
    checked against the defined rules and if the wylie analysis returns False,
    the syllable will be defined to be Sanskrit.
    --------------
    Basic steps for the syllable computation:
        0. Perform initial Sanskrit check.
        1. Partition into a list of wylie letters, the Syllable.wylie string.
        2. Find the vowel position in the list.
        3. Define the syllable components (prefix, superscribed, etc.) for all
            letters before the vowel.
        4. Define the syllable components for the letters after the vowel.
        5. Compute the unicode string based on the analysis and store the
            unicode string in Syllable.uni.
    -----------------
    Sanskrit analysis
    -----------------
    The syllable will first be checked against isSanskrit(). Clear Sanskrit
    cases will be checked as well as a few cases where the syllable does pass
    the wylie checks, but are actually Sanskrit (tables.S_DOUBLE_CONSONANTS).
    If the syllable does not validate as True after this check, the syllable
    will be classified as Sanskrit if analyzeWylie() returns False.
    '''

    def __init__(self):
        wTable = (W_ROOTLETTERS + W_VOWELS)
        uTable = (U_ROOTLETTERS + U_VOWELS)
        swTable = (SW_ROOTLETTERS + SW_VOWELS)
        suTable = (SU_ROOTLETTERS + SU_VOWELS)
        self.wylieToUnicode = dict(zip(wTable, uTable))
        self.sanskritWylieToUnicode = dict(zip(swTable, suTable))
        self.validSuperjoinedList = dict(zip(SUPER, SUPER_RULES))
        self.validSubjoinedList = dict(zip(SUB, SUB_RULES))
        self.allWylieVowels = (W_VOWELS + (W_ROOTLETTERS[-1],))
        self.explicitSanskritVowels = SW_VOWELS[1:]
        self.errorVal = str(encode(urandom(8), 'hex'))[2:-1]
        sTable = (SUFFIXES, SUFFIX2S)
        self.validSuffix = dict(zip(POSTVOWEL, sTable))
        self.wylie_vowel_a = W_ROOTLETTERS[-1]

    def toUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = self.sanskritWylieToUnicode if isSanskrit else self.wylieToUnicode
        return lookup[str(wylieSyllable)]

    def toSubjoinedUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = self.sanskritWylieToUnicode if isSanskrit else self.wylieToUnicode
        return chr(ord(lookup[str(wylieSyllable)]) + SUBOFFSET)

    def modSyllableStructure(self, syllable, component, wylieLetter):
        syllable.structure[component] = wylieLetter

    def getCharacterFor(self, syllable, syllableComponent):
        return syllable.structure[syllableComponent]

    def getVowelIndices(self, wylieLetters, isSanskrit=False):
        vowelList = SW_VOWELS if isSanskrit else self.allWylieVowels
        result = []

        for i, char in enumerate(wylieLetters):
            if char in vowelList:

                # conjoin adjacent vowels
                if wylieLetters[i-1] in vowelList and result:
                    result[-1] += 1
                    continue

                result.append(i)

        return result

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

    # tuple index correlates to the syllable's vowel position
    analyzeBaseCase = (
        None,
        (lambda self, wylieLetters:
         wylieLetters[0] in W_ROOTLETTERS and
         wylieLetters[1] in self.allWylieVowels),
        (lambda _, wylieLetters:
         wylieLetters[0] == PREFIX_GA or
         wylieLetters[0] in PREFIXES and
         wylieLetters[1] in W_ROOTLETTERS),
        (lambda _, wylieLetters:
         wylieLetters[0] in SUPER and
         wylieLetters[1] in W_ROOTLETTERS and
         wylieLetters[2] in SUB),
        (lambda _, wylieLetters:
         wylieLetters[0] in PREFIXES and
         wylieLetters[1] in SUPER and
         wylieLetters[2] in W_ROOTLETTERS and
         wylieLetters[3] in SUB))

    def vowelAtFirstPosition(self, syllable, wylieLetters):
        if not wylieLetters[0] in self.allWylieVowels:
            return False

        self.modSyllableStructure(syllable, 'root', wylieLetters[0])

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
        if self.isIrregularSubjoin(3, wylieLetters):
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

    analyzeSyllable = (
        vowelAtFirstPosition,
        vowelAtSecondPosition,
        vowelAtThirdPosition,
        vowelAtFourthPosition,
        vowelAtFifthPosition)

    def invalidWylieString(self, syllable):
        if not syllable.wylie.startswith(PREFIX_GA):
            for c in syllable.wylie:
                if c not in W_ROOTLETTERS + W_VOWELS:
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

        if wylieLetters is None:
            return False

        syllable.clearUnicode()

        vowelPosition = self.getVowelIndices(wylieLetters)

        if not vowelPosition:
            return False

        vowelPosition = vowelPosition[0]
        res = self.analyzeSyllable[vowelPosition](self, syllable, wylieLetters)

        if res == self.errorVal:
            return False

        return self.findSuffixes(syllable, vowelPosition, wylieLetters)

    def stackSanskritLetters(self, vowelIndices, wylieLetters):
        vowelIndices = list(map(lambda x: x+1, vowelIndices))

        if vowelIndices[0] != 0:
            vowelIndices.insert(0, 0)

        if vowelIndices[-1] != len(wylieLetters):
            vowelIndices.append(len(wylieLetters))

        vowelIndices = zip(vowelIndices, vowelIndices[1:])
        letterStacks = []

        for p in vowelIndices:
            letterStacks.append(wylieLetters[p[0]:p[1]])

        return letterStacks

    def analyzeSanskrit(self, syllable):
        wylieLetters = self.partitionToWylie(syllable)

        if wylieLetters is None:
            return False

        syllable.clearUnicode()

        if len(wylieLetters) == 1:
            # TODO: fix missing method!
            self.singleWylieLetter(syllable, wylieLetters)

        vowelIndices = self.getVowelIndices(wylieLetters, True)

        if not vowelIndices:
            return False

        letterStacks = self.stackSanskritLetters(vowelIndices, wylieLetters)
        self.generateSanskritUnicode(syllable, letterStacks)

        return True

    def handleOm(self, syllable):
        if syllable.wylie == U_OM:
            syllable.uni = S_OM
            return True

        return False

    def isSnaLdan(self, syllable, letter):
        return letter == SW_VOWELS[-2] and \
            syllable.wylie in SNA_LDAN_CASES

    def potentialSanskritSubjoin(self, letter):
        '''letter is 'y', 'r' or 'v' ?'''
        return letter is SW_ROOTLETTERS[25] or \
            letter is SW_ROOTLETTERS[26] or \
            letter is SW_ROOTLETTERS[28]

    def handleSanskritSubjoin(self, letter, letters):
        if letters.index(letter) < len(letters)-2:
            return STACK[letter]

        for regex in SW_REGEX[letter]:
            r = re.compile(regex)

            if r.search(''.join(letters)):
                return self.toSubjoinedUnicode(letter, True)

        return STACK[letter]

    def generateSanskritUnicode(self, syllable, letterStacks):
        ''' letters is a list of sanskrit letters, the result of
        partitionToWylie().  '''

        if self.handleOm(syllable):
            return

        unicodeString = []
        litteral_va = SW_ROOTLETTERS[28]
        litteral_ba = W_ROOTLETTERS[14]
        litteral_rv = SW_ROOTLETTERS[26] + SW_ROOTLETTERS[28]

        for stack in letterStacks:
            if stack[0] in self.explicitSanskritVowels:
                unicodeString.append(self.toUnicode(self.wylie_vowel_a, True))
                unicodeString.append(self.toUnicode(stack[0], True))
            elif stack[0] is litteral_va:
                unicodeString.append(self.toUnicode(litteral_ba, True))
            else:
                unicodeString.append(self.toUnicode(stack[0], True))

            stackedLetters = stack[1:]

            for letter in stackedLetters:
                if letter is self.wylie_vowel_a:
                    continue
                elif self.isSnaLdan(syllable, letter):
                    unicodeString.append(S_SNA_LDAN)
                elif letter in SW_VOWELS:
                    unicodeString.append(self.toUnicode(letter, True))
                elif ''.join(stack[:2]) == litteral_rv:
                    letter = litteral_ba
                    unicodeString.append(self.toSubjoinedUnicode(letter, True))
                elif self.potentialSanskritSubjoin(letter):
                    unicodeResult = self.handleSanskritSubjoin(letter, stack)
                    unicodeString.append(unicodeResult)
                else:
                    unicodeString.append(self.toSubjoinedUnicode(letter, True))

        syllable.uni = ''.join(unicodeString)

    def isIrregularSubjoin(self, vowelPosition, wylieLetters):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''

        return wylieLetters[vowelPosition-1] == W_ROOTLETTERS[19] \
            and wylieLetters[vowelPosition-2] == W_ROOTLETTERS[24]

    def invalidSuffix(self, component, wylieChar):
        return component in POSTVOWEL[:2] \
            and wylieChar not in self.allWylieVowels \
            and wylieChar not in self.validSuffix[component]

    def findSuffixes(self, syllable, vowelPosition, wylieLetters):
        components = iter(POSTVOWEL)

        for wylieChar in wylieLetters[vowelPosition+1:]:
            syllableComponent = next(components)

            if self.invalidSuffix(syllableComponent, wylieChar):
                return False

            self.modSyllableStructure(syllable,
                                      syllableComponent,
                                      wylieChar)
        return True

    def partitionToWylie(self, syllable):
        '''Generates a list of wylie/IAST letters, from which the
        syllable.wylie string is composed of.
        Checks if the roman character(s) at the end of the wylie/IAST string
        forms a valid wylie letter and continues backwards through the
        wylie/IAST string, until the entire wylie string is partitioned.'''

        alphabet = []
        romanCharacterMax = 3

        if syllable.isSanskrit:
            alphabet = SW_ROOTLETTERS + SW_VOWELS
            romanCharacterMax = 2
        else:
            alphabet = W_ROOTLETTERS + W_VOWELS

        wylieLetters = []
        wylieSyllable = syllable.wylie

        while len(wylieSyllable) != 0:
            for i in range(romanCharacterMax, 0, -1):
                part = wylieSyllable[:i]

                if part == '':
                    break

                if part in alphabet or part == PREFIX_GA:
                    wylieLetters.append(part)
                    wylieSyllable = wylieSyllable[len(part):]
                elif i == 1 and part not in alphabet:
                    return None

        return wylieLetters

    def validSuperscribe(self, headLetter, rootLetter):
        if headLetter not in SUPER:
            return False
        else:
            return rootLetter in self.validSuperjoinedList[headLetter]

    def validSubscribe(self, rootLetter, subjoinedLetter):
        if subjoinedLetter not in SUB:
            return False
        else:
            return rootLetter in self.validSubjoinedList[subjoinedLetter]

    def needsSubjoin(self, syllable, component):
        return component == 'subjoined' or component == 'secondsub' \
            or (component == 'root'
                and self.getCharacterFor(syllable, 'super'))

    def generateWylieUnicode(self, syllable):
        for syllableComponent in SYLLSTRUCT:
            char = self.getCharacterFor(syllable, syllableComponent)

            if not char:
                continue

            newString = [syllable.uni]

            if char == self.wylie_vowel_a and syllableComponent != 'root':
                continue

            if char in W_VOWELS and syllableComponent == 'root':
                newString.append(self.toUnicode(self.wylie_vowel_a))

            # char == 'g.' ?
            if char == PREFIX_GA:
                char = W_ROOTLETTERS[2]
                self.modSyllableStructure(syllable,
                                          syllableComponent,
                                          char)

            if self.needsSubjoin(syllable, syllableComponent):
                newString.append(self.toSubjoinedUnicode(char))
            else:
                newString.append(self.toUnicode(char))

            syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        return char in PREFIXES

    def hasAtleastNVowels(self, string, n):
        vowels = (c for c in list(string) if c in self.allWylieVowels)

        for i, unused in enumerate(vowels):
            if i == n - 1:
                return True

        return False

    def hasNoAChung(self, string):
        return W_ROOTLETTERS[22] not in string

    def isSanskrit(self, syllable):
        string = syllable.wylie

        # Check if what could potentially be valid wylie, is actually Sanskrit
        if len(string) == 3 and string[0:2] in S_DOUBLE_CONSONANTS:
            return True

        # Check for clear case Sanskrit syllables to save time
        matches = S_BASIC_RULES

        for substring in matches:
            if string.startswith(substring):
                return True

        return 'ai' in string or 'au' in string or \
            self.hasAtleastNVowels(string, 2) and self.hasNoAChung(string)

    def getBytecodes(self, wylieString):
        syllable = Syllable(wylieString)
        self.analyze(syllable)
        return self.unicodeStringToCodes(syllable.uni)

    def unicodeStringToCodes(self, unicodeString):
        bytecodes = []

        for uni in unicodeString:
            bytecodes.append('U+{0:04X}'.format(ord(uni)))

        return bytecodes


class Syllable(object):
    '''Used to represent a part of a word written in Tibetan wylie, or in the
    case of a Tibetan transliteration of Sanskrit, it is represented as
    International Alphabet of Sanskrit Transliteration (IAST). This information
    is stored in Syllable.wylie.  Syllable.uni holds the equivalent string in
    Tibetan Unicode (U+0F00-U+0FFF).  If a Translator has performed its
    analysis on the Syllable object and found the contents in Syllable.wylie to
    be valid wylie, the result of the analysis is stored in self.structure
    (prefix, root letter, suffix, etc).'''

    # TODO: implement constraint for length of self.wylie

    def __init__(self, wylieString=''):
        self.wylie = wylieString
        self.uni = ''
        self.structure = dict((key, '') for key in SYLLSTRUCT)
        self.isSanskrit = False

    def __str__(self):
        return self.wylie

    def __repr__(self):
        return self.wylie

    def tsheg(self):
        self.uni = ''.join([self.uni, S_TSHEG])

    def clearUnicode(self):
        self.uni = ''

        for s in SYLLSTRUCT:
            self.structure[s] = ''
