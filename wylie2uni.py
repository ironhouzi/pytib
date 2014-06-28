'''
    Wylie2Uni
    Wylie to Unicode convertor
    Requires Python 3
'''

import tables
from codecs import encode
from os import urandom


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
        wTable = (tables.W_ROOTLETTERS + tables.W_VOWELS)
        uTable = (tables.U_ROOTLETTERS + tables.U_VOWELS)
        swTable = (tables.SW_ROOTLETTERS + tables.SW_VOWELS)
        suTable = (tables.SU_ROOTLETTERS + tables.SU_VOWELS)
        self.wylieToUnicode = dict(zip(wTable, uTable))
        self.sanskritWylieToUnicode = dict(zip(swTable, suTable))
        self.validSuperjoinedList = dict(zip(tables.SUPER, tables.SUPER_RULES))
        self.validSubjoinedList = dict(zip(tables.SUB, tables.SUB_RULES))
        self.allWylieVowels = (tables.W_VOWELS + (tables.W_ROOTLETTERS[-1],))
        self.explicitSanskritVowels = tables.SW_VOWELS[1:]
        self.errorVal = str(encode(urandom(8), 'hex'))[2:-1]
        sTable = (tables.SUFFIXES, tables.SUFFIX2S)
        self.validSuffix = dict(zip(tables.POSTVOWEL, sTable))
        self.wylie_vowel_a = tables.W_ROOTLETTERS[-1]

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

    def getVowelIndices(self, wylieLetters, isSanskrit=False):
        vowelList = []
        result = []

        if isSanskrit:
            vowelList = tables.SW_VOWELS
        else:
            vowelList = self.allWylieVowels

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
         wylieLetters[0] in tables.W_ROOTLETTERS and
         wylieLetters[1] in self.allWylieVowels),
        (lambda self, wylieLetters:
         wylieLetters[0] == tables.PREFIX_GA or
         wylieLetters[0] in tables.PREFIXES and
         wylieLetters[1] in tables.W_ROOTLETTERS),
        (lambda self, wylieLetters:
         wylieLetters[0] in tables.SUPER and
         wylieLetters[1] in tables.W_ROOTLETTERS and
         wylieLetters[2] in tables.SUB),
        (lambda self, wylieLetters:
         wylieLetters[0] in tables.PREFIXES and
         wylieLetters[1] in tables.SUPER and
         wylieLetters[2] in tables.W_ROOTLETTERS and
         wylieLetters[3] in tables.SUB))

    def vowelAtFirstPosition(self, syllable, wylieLetters):
        if not wylieLetters[0] in self.allWylieVowels:
            return False

        if wylieLetters[0] in self.allWylieVowels:
            if wylieLetters[0] != self.wylie_vowel_a:
                # For single letter vowels w/o the 'a'. Prepends the vowel with
                # the 'a' character, to get correct unicode.
                # TODO  Move to generateWylieUnicode().
                syllable.wylie = ''.join([self.wylie_vowel_a, wylieLetters[0]])
                self.modSyllableStructure(syllable, 'root', self.wylie_vowel_a)
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

    analyzeSyllable = (
        vowelAtFirstPosition,
        vowelAtSecondPosition,
        vowelAtThirdPosition,
        vowelAtFourthPosition,
        vowelAtFifthPosition)

    def singleWylieLetter(self, syllable, wylieLetters):
        self.modSyllableStructure(syllable, 'root', wylieLetters[0])

        if wylieLetters[0] in self.allWylieVowels:
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])
        else:
            self.modSyllableStructure(syllable, 'root', self.wylie_vowel_a)
            self.modSyllableStructure(syllable, 'vowel', wylieLetters[0])

    def invalidWylieString(self, syllable):
        if not syllable.wylie.startswith(tables.PREFIX_GA):
            for c in syllable.wylie:
                if c not in tables.W_ROOTLETTERS + tables.W_VOWELS:
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

        syllable.clear()

        if len(wylieLetters) == 1:
            self.singleWylieLetter(syllable, wylieLetters)

        vowelPosition = self.getVowelIndices(wylieLetters)

        if not vowelPosition:
            return False

        vowelPosition = vowelPosition[0]
        res = self.analyzeSyllable[vowelPosition](self, syllable, wylieLetters)

        if res == self.errorVal:
            return False

        return self.findSuffixes(syllable, vowelPosition, wylieLetters)

    def stackSanskritLetters(self, vowelIndices, wylieLetters):
        letterStacks = []
        vowelIndices = list(map(lambda x: x+1, vowelIndices))

        if vowelIndices[0] != 0:
            vowelIndices.insert(0, 0)

        if vowelIndices[-1] != len(wylieLetters):
            vowelIndices.append(len(wylieLetters))

        vowelIndices = zip(vowelIndices, vowelIndices[1:])

        for p in vowelIndices:
            letterStacks.append(wylieLetters[p[0]:p[1]])

        return letterStacks

    def analyzeSanskrit(self, syllable):
        wylieLetters = self.partitionToWylie(syllable)

        if wylieLetters is None:
            return False

        # TODO signify importance of this line
        syllable.clear()

        if len(wylieLetters) == 1:
            self.singleWylieLetter(syllable, wylieLetters)

        vowelIndices = self.getVowelIndices(wylieLetters, True)

        if not vowelIndices:
            return False

        letterStacks = self.stackSanskritLetters(vowelIndices, wylieLetters)
        self.generateSanskritUnicode(syllable, letterStacks)

        return True

    def handleOm(self, syllable):
        if syllable.wylie == tables.U_OM:
            syllable.uni = tables.S_OM
            return True

        return False

    def isSnaLdan(self, syllable, letter):
        return letter == tables.SW_VOWELS[-2] and \
            syllable.wylie in tables.SNA_LDAN_CASES

    def dzBeforeRa(self, letters, position):
        return letters[position] is tables.SW_ROOTLETTERS[7] and \
            len(letters) > position+1 and \
            letters[position+1] is tables.SW_ROOTLETTERS[26]

    # def vaAfterRa(self, letters, position):
    #     return letters[position] is tables.SW_ROOTLETTERS[28] and \
    #         position > 0 and letters[position-1] is tables.SW_ROOTLETTERS[26]

    def potentialSubjoin(self, letter):
        '''Is letter 'y', 'r' or 'v' ?'''
        return letter is tables.SW_ROOTLETTERS[25] or \
            letter is tables.SW_ROOTLETTERS[26] or \
            letter is tables.SW_ROOTLETTERS[28]

    def handleSanskritSubjoin(self, letter, letters):
        if letters.index(letter) < len(letters)-2:
            return tables.STACK[letter]

        lookup = self.sanskritWylieToUnicode
        

    def generateSanskritUnicode(self, syllable, letterStacks):
        '''
        letters is a list of sanskrit letters, the result of
        partitionToWylie().
        '''

        if self.handleOm(syllable):
            return

        unicodeString = []
        litteral_va = tables.SW_ROOTLETTERS[28]
        litteral_ba = tables.W_ROOTLETTERS[14]

        for stack in letterStacks:
            if stack[0] in self.explicitSanskritVowels:
                unicodeString.append(tables.U_ROOTLETTERS[-1])
                unicodeString.append(self.toUnicode(stack[0], True))
            elif stack[0] is litteral_va:
                unicodeString.append(self.toUnicode(litteral_ba, True))
            else:
                unicodeString.append(self.toUnicode(stack[0], True))

            stack = stack[1:]

            for letter in stack:
                if letter is self.wylie_vowel_a:
                    continue
                elif self.isSnaLdan(syllable, letter):
                    unicodeString.append(tables.S_SNA_LDAN)
                elif letter in tables.SW_VOWELS:
                    unicodeString.append(self.toUnicode(letter, True))
                elif self.potentialSubjoin(letter):
                    unicodeResult = self.handleSanskritSubjoin(letter, stack)
                    unicodeString.append(unicodeResult)
                else:
                    unicodeString.append(self.toSubjoinedUnicode(letter, True))

        syllable.uni = ''.join(unicodeString)

    def isIrregular(self, vowelPosition, wylieLetters):
        '''Checks if the syllable has both 'w' and 'r' as subscribed letters'''

        return wylieLetters[vowelPosition-1] == tables.W_ROOTLETTERS[19] \
            and wylieLetters[vowelPosition-2] == tables.W_ROOTLETTERS[24]

    def invalidSuffix(self, component, wylieChar):
        return component in tables.POSTVOWEL[:2] \
            and wylieChar not in self.allWylieVowels \
            and wylieChar not in self.validSuffix[component]

    def findSuffixes(self, syllable, vowelPosition, wylieLetters):
        components = iter(tables.POSTVOWEL)

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
        Checks if the roman character(s)
        at the end of the wylie/IAST string forms a valid wylie letter and
        continues backwards through the wylie/ IAST string, until the entire
        wylie string is partitioned.'''

        alphabet = []
        romanCharacterMax = 3

        if syllable.isSanskrit:
            alphabet = tables.SW_ROOTLETTERS + tables.SW_VOWELS
            romanCharacterMax = 2
        else:
            alphabet = tables.W_ROOTLETTERS + tables.W_VOWELS

        wylieLetters = []
        wylieSyllable = syllable.wylie

        while len(wylieSyllable) != 0:
            for i in range(romanCharacterMax, 0, -1):
                part = wylieSyllable[:i]

                if part == '':
                    break

                if part in alphabet or part == tables.PREFIX_GA:
                    wylieLetters.append(part)
                    wylieSyllable = wylieSyllable[len(part):]
                elif i == 1 and part not in alphabet:
                    return None

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
            or (component == 'root'
                and self.getCharacterFor(syllable, 'super'))

    def generateWylieUnicode(self, syllable):
        for syllableComponent in tables.SYLLSTRUCT:
            char = self.getCharacterFor(syllable, syllableComponent)

            if char == self.wylie_vowel_a and syllableComponent != 'root':
                continue

            newString = [syllable.uni]

            if char:
                # char == 'g.' ?
                if char == tables.PREFIX_GA:
                    char = tables.W_ROOTLETTERS[2]
                    self.modSyllableStructure(syllable,
                                              syllableComponent,
                                              char)
                if self.needsSubjoin(syllable, syllableComponent):
                    newString.append(self.toSubjoinedUnicode(char))
                else:
                    newString.append(self.toUnicode(char))

                syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        return char in tables.PREFIXES

    def hasAtleastNVowels(self, string, n):
        vowels = (c for c in list(string) if c in self.allWylieVowels)

        for i, unused in enumerate(vowels):
            if i == n - 1:
                return True

        return False

    def hasNoAChung(self, string):
        return tables.W_ROOTLETTERS[22] not in string

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
        self.uni = ''.join([self.uni, tables.S_TSHEG])

    def clear(self):
        self.uni = ''

        for s in tables.SYLLSTRUCT:
            self.structure[s] = ''
