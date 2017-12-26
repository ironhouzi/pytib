'''
    Wylie2Uni
    Wylie to Unicode convertor
    Requires Python 3.6
'''

from pytib.tables import (
    W_ROOTLETTERS, W_VOWELS, SW_ROOTLETTERS, SW_VOWELS, ACHUNG_INDEX,
    U_ROOTLETTERS, U_VOWELS, SU_ROOTLETTERS, SU_VOWELS, U_ACHUNG, RAGO_INDICES,
    LAGO_INDICES, SAGO_INDICES, defs, SUPER_INDICES, WAZUR_INDICES,
    YATA_INDICES, RATA_INDICES, LATA_INDICES, SUB_INDICES, suffix_rules,
    get_chars, PREFIXES_I, SUBOFFSET, U_OM, S_OM, SNA_LDAN_CASES, STACK,
    SW_REGEX, S_SNA_LDAN, POSTVOWEL, SYLLSTRUCT, S_DOUBLE_CONSONANTS,
    S_BASIC_RULES, TSHEG
)
import re
import logging

logging.basicConfig(filename='wylie2uni.log', level=logging.DEBUG)
ERROR = -1

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

    def __init__(self, consonants=W_ROOTLETTERS, ga_prefix_marker='.'):
        self.consonants = consonants
        self.latin_table = (consonants + W_VOWELS)
        table = (SW_ROOTLETTERS + SW_VOWELS + (consonants[ACHUNG_INDEX],))
        self.latin_sanskrit_table = table
        u_table = (U_ROOTLETTERS + U_VOWELS)
        su_table = (SU_ROOTLETTERS + SU_VOWELS + (U_ACHUNG,))

        self.tibetan = dict(zip(self.latin_table, u_table))
        self.sanskrit = dict(zip(self.latin_sanskrit_table, su_table))

        s = (RAGO_INDICES, LAGO_INDICES, SAGO_INDICES,)
        self.superjoin, self.validSuperjoin = defs(s, SUPER_INDICES, consonants)

        s = (WAZUR_INDICES, YATA_INDICES, RATA_INDICES, LATA_INDICES, )
        self.sub, self.validSubjoinedList = defs(s, SUB_INDICES, consonants)

        self.validSuffix = suffix_rules(consonants)
        self.prefixes = get_chars(PREFIXES_I, consonants)

        self.allWylieVowels = W_VOWELS + (consonants[-1],)
        self.explicitSanskritVowels = SW_VOWELS[1:]
        self.wylie_vowel_a = consonants[-1]
        self.ga_prefix = ''.join([consonants[2], ga_prefix_marker])

        self.latin_set = set(self.latin_table)
        self.sanskrit_set = set(self.latin_sanskrit_table)
        self.max_tib_char_len = max(map(len, self.latin_table))
        self.max_sanskrit_char_len = max(map(len, self.latin_sanskrit_table))

    def toUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = self.sanskrit if isSanskrit else self.tibetan
        return lookup[str(wylieSyllable)]

    def toSubjoinedUnicode(self, wylieSyllable, isSanskrit=False):
        lookup = self.sanskrit if isSanskrit else self.tibetan
        return chr(ord(lookup[str(wylieSyllable)]) + SUBOFFSET)

    # TODO: pass vowel list as argument instead of a boolean
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
            return (
                self.validSuperscribe(wylieLetters[0], wylieLetters[1])
                and not self.validSubscribe(wylieLetters[0], wylieLetters[1])
            )
        else:   # vowelPosition == 3
            return (
                self.isPrefix(wylieLetters[0])
                and self.validSuperscribe(wylieLetters[1], wylieLetters[2])
                and not self.validSubscribe(wylieLetters[1], wylieLetters[2])
            )

    def isSubscribed(self, wylieLetters, vowelPosition):
        if vowelPosition == 2:
            return (
                not self.validSuperscribe(wylieLetters[0], wylieLetters[1])
                and self.validSubscribe(wylieLetters[0], wylieLetters[1])
            )
        else:   # vowelPosition == 3
            return (
                self.isPrefix(wylieLetters[0])
                and not self.validSuperscribe(wylieLetters[1], wylieLetters[2])
                and self.validSubscribe(wylieLetters[1], wylieLetters[2])
            )

    # tuple index correlates to the syllable's vowel position
    analyzeBaseCase = (
        None,
        (lambda self, wylieLetters:
         wylieLetters[0] in self.consonants and
         wylieLetters[1] in self.allWylieVowels),
        (lambda self, wylieLetters:
         wylieLetters[0] == self.ga_prefix or
         wylieLetters[0] in self.prefixes and
         wylieLetters[1] in self.consonants),
        (lambda self, wylieLetters:
         wylieLetters[0] in self.superjoin and
         wylieLetters[1] in self.consonants and
         wylieLetters[2] in self.sub),
        (lambda self, wylieLetters:
         wylieLetters[0] in self.prefixes and
         wylieLetters[1] in self.superjoin and
         wylieLetters[2] in self.consonants and
         wylieLetters[3] in self.sub))

    def vowelAtFirstPosition(self, syllable, wylieLetters):
        syllable.structure['root'] = wylieLetters[0]

    def vowelAtSecondPosition(self, syllable, wylieLetters):
        if not self.analyzeBaseCase[1](self, wylieLetters):
            return ERROR

        syllable.structure['root'] = wylieLetters[0]
        syllable.structure['vowel'] = wylieLetters[1]

    def vowelAtThirdPosition(self, syllable, wylieLetters):
        if self.isSubscribed(wylieLetters, 2):
            syllable.structure['root'] = wylieLetters[0]
            syllable.structure['subjoined'] = wylieLetters[1]
        elif self.isSuperscribed(wylieLetters, 2):
            syllable.structure['super'] = wylieLetters[0]
            syllable.structure['root'] = wylieLetters[1]
        elif self.analyzeBaseCase[2](self, wylieLetters):
            syllable.structure['prefix'] = wylieLetters[0]
            syllable.structure['root'] = wylieLetters[1]
        else:
            return ERROR

        syllable.structure['vowel'] = wylieLetters[2]

    def vowelAtFourthPosition(self, syllable, wylieLetters):
        if self.isIrregularSubjoin(3, wylieLetters):
            syllable.structure['root'] = wylieLetters[0]
            syllable.structure['subjoined'] = wylieLetters[1]
            syllable.structure['secondsub'] = wylieLetters[2]
        elif self.isSuperscribed(wylieLetters, 3):
            syllable.structure['prefix'] = wylieLetters[0]
            syllable.structure['super'] = wylieLetters[1]
            syllable.structure['root'] = wylieLetters[2]
        elif self.isSubscribed(wylieLetters, 3):
            syllable.structure['prefix'] = wylieLetters[0]
            syllable.structure['root'] = wylieLetters[1]
            syllable.structure['subjoined'] = wylieLetters[2]
        elif self.analyzeBaseCase[3](self, wylieLetters):
            syllable.structure['super'] = wylieLetters[0]
            syllable.structure['root'] = wylieLetters[1]
            syllable.structure['subjoined'] = wylieLetters[2]
        else:
            return ERROR

        syllable.structure['vowel'] = wylieLetters[3]

    def vowelAtFifthPosition(self, syllable, wylieLetters):
        if not self.analyzeBaseCase[4](self, wylieLetters):
            return ERROR

        syllable.structure['prefix'] = wylieLetters[0]
        syllable.structure['super'] = wylieLetters[1]
        syllable.structure['root'] = wylieLetters[2]
        syllable.structure['subjoined'] = wylieLetters[3]
        syllable.structure['vowel'] = wylieLetters[4]

    analyzeSyllable = (
        vowelAtFirstPosition,
        vowelAtSecondPosition,
        vowelAtThirdPosition,
        vowelAtFourthPosition,
        vowelAtFifthPosition)

    def invalidWylie(self, syllable):
        return (
            not syllable.wylie.startswith(self.ga_prefix)
            and any(char not in self.latin_set for char in syllable.wylie)
        )

    def analyze(self, syllable, string):
        syllable.wylie = string
        syllable.isSanskrit = self.isSanskrit(syllable)

        if not syllable.isSanskrit:
            syllable.isSanskrit = not self.analyzeWylie(syllable)
        # TODO: cleanup logic
        if syllable.isSanskrit:
            self.analyzeSanskrit(syllable)
        else:
            self.generateWylieUnicode(syllable)

    def analyzeWylie(self, syllable):
        if self.invalidWylie(syllable):
            return False

        wylieLetters = self.partitionToWylie(syllable)

        if wylieLetters is None:
            return False

        syllable.clear()

        vowelPosition = self.getVowelIndices(wylieLetters)

        if not vowelPosition:
            return False

        vowelPosition = vowelPosition[0]

        if vowelPosition >= len(self.analyzeSyllable):
            logging.warning("Oversized vowel position: %d for «%s»",
                            vowelPosition, syllable.wylie)
            return False

        res = self.analyzeSyllable[vowelPosition](self, syllable, wylieLetters)

        if res == ERROR:
            return False

        return self.findSuffixes(syllable, vowelPosition, wylieLetters)

    def stackSanskritLetters(self, vowelIndices, wylieLetters):
        vowelIndices = list(map(lambda x: x+1, vowelIndices))

        if vowelIndices[0] != 0:
            vowelIndices.insert(0, 0)

        if vowelIndices[-1] != len(wylieLetters):
            vowelIndices.append(len(wylieLetters))

        vowelIndices = zip(vowelIndices, vowelIndices[1:])

        return [wylieLetters[i[0]:i[1]] for i in vowelIndices]

    def analyzeSanskrit(self, syllable):
        wylieLetters = self.partitionToWylie(syllable)

        if wylieLetters is None:
            return False

        syllable.clear()
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
        litteral_ba = self.consonants[14]
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

        return wylieLetters[vowelPosition-1] == self.consonants[19] \
            and wylieLetters[vowelPosition-2] == self.consonants[24]

    def invalidSuffix(self, component, wylieChar):
        return component in POSTVOWEL[:2] \
            and wylieChar not in self.allWylieVowels \
            and wylieChar not in self.validSuffix[component]

    def findSuffixes(self, syllable, vowelPosition, wylieLetters):
        components = iter(POSTVOWEL)

        for wylieChar in wylieLetters[vowelPosition+1:]:
            try:
                syllableComponent = next(components)
            except StopIteration:
                break

            if self.invalidSuffix(syllableComponent, wylieChar):
                return False

            syllable.structure[syllableComponent] = wylieChar
        return True

    def partitionToWylie(self, syllable):
        '''Generates a list of wylie/IAST letters, from which the
        syllable.wylie string is composed of.
        Checks if the roman character(s) at the end of the wylie/IAST string
        forms a valid wylie letter and continues backwards through the
        wylie/IAST string, until the entire wylie string is partitioned.'''

        if syllable.isSanskrit:
            alphabet = self.sanskrit_set
            max_char_len = self.max_sanskrit_char_len
        else:
            alphabet = self.latin_set
            max_char_len = self.max_tib_char_len

        wylieLetters = []
        wylieSyllable = syllable.wylie

        while len(wylieSyllable) != 0:
            for i in range(max_char_len, 0, -1):
                part = wylieSyllable[:i]

                if part == '':
                    break

                if part == self.ga_prefix or part in alphabet:
                    wylieLetters.append(part)
                    wylieSyllable = wylieSyllable[i:]

                elif i == 1 and part not in alphabet:
                    return None

        return wylieLetters

    def validSuperscribe(self, headLetter, rootLetter):
        return (
            headLetter in self.superjoin
            and rootLetter in self.validSuperjoin[headLetter]
        )

    def validSubscribe(self, rootLetter, subjoinedLetter):
        return (
            subjoinedLetter in self.sub and
            rootLetter in self.validSubjoinedList[subjoinedLetter]
        )

    def needsSubjoin(self, syllable, component):
        return (
            component == 'subjoined'
            or component == 'secondsub'
            or (component == 'root' and syllable.structure['super'])
        )

    def generateWylieUnicode(self, syllable):
        for syllableComponent in SYLLSTRUCT:
            char = syllable.structure[syllableComponent]

            if not char:
                continue

            newString = [syllable.uni]

            if char == self.wylie_vowel_a and syllableComponent != 'root':
                continue

            if char in W_VOWELS and syllableComponent == 'root':
                newString.append(self.toUnicode(self.wylie_vowel_a))

            # char == 'g.' ?
            if char == self.ga_prefix:
                char = self.consonants[2]
                syllable.structure[syllableComponent] = char

            if self.needsSubjoin(syllable, syllableComponent):
                newString.append(self.toSubjoinedUnicode(char))
            else:
                newString.append(self.toUnicode(char))

            syllable.uni = ''.join(newString)

    def isPrefix(self, char):
        return char in self.prefixes

    def hasAtleastNVowels(self, string, n):
        vowels = tuple(c for c in string if c in self.allWylieVowels)
        return len(vowels) >= n

    def hasNoAChung(self, string):
        return self.consonants[ACHUNG_INDEX] not in string

    def isSanskrit(self, syllable):
        string = syllable.wylie

        # Check if what could potentially be valid wylie, is actually Sanskrit
        if len(string) == 3 and string[:2] in S_DOUBLE_CONSONANTS:
            return True

        # Check for clear case Sanskrit syllables to save time
        if any(string.startswith(r) for r in S_BASIC_RULES):
            return True

        if any(sanskrit_vowel in string for sanskrit_vowel in ('ai', 'au')):
            return True

        return self.hasAtleastNVowels(string, 2) and self.hasNoAChung(string)

    def bytecodes(self, syllable, wylie_string):
        self.analyze(syllable, wylie_string)

        for c in syllable.uni:
            yield f'U+{ord(c):04X}'


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
        self.uni = ''.join([self.uni, TSHEG])

    def clear(self):
        self.uni = ''

        for s in SYLLSTRUCT:
            self.structure[s] = ''
