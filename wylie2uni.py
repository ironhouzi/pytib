# TODO: Write unit tests!

import sys
import tables

'''Wylie2Uni
    Wylie to Unicode convertor'''

TSHEG = u'\u0f0b'
SUBOFFSET = 0x50


class Translator(object):
    '''Translates wylie into Tibetan Unicode, by mainly modifying the static
        variable: Translator.syllable'''

    def __init__(self):
        Translator.syllable = Syllable('')
        wTable = tables.W_ROOTLETTERS + tables.W_VOWELS
        uTable = tables.U_ROOTLETTERS + tables.U_VOWELS
        Translator.lookup = dict(zip(wTable, uTable))
        Translator.rulesSuper = dict(zip(tables.SUPER, tables.SUPER_RULES))
        Translator.rulesSub = dict(zip(tables.SUB,   tables.SUB_RULES))

    def newSyllable(self):
        Translator.syllable.new()

    def toUnicode(self, syllable):
        return Translator.lookup[str(syllable)]

    def toSubjoinedUnicode(self, syllable):
        return chr(ord(Translator.lookup[str(syllable)]) + SUBOFFSET)

    def outputUnicode(self):
        if __name__ == "__main__":
            sys.stdout.write(Translator.syllable.uni)
        else:
            return Translator.syllable.uni

    def setStruct(self, key, value):
        Translator.syllable.struct[key] = value

    def clearSyllable(self):
        Translator.syllable.clear()

    def getCharacterOf(self, key):
        return Translator.syllable.struct[key]

    def getVowelIndex(self, parts):
        for i, char in enumerate(parts):
            if char in tables.W_VOWELS:
                return i
        return -1

    def isSuperscribed(self, parts, vowelPosition):
        if vowelPosition == 2:
            if self.validSuperscribe(parts[0], parts[1]) \
                    and not self.validSubscribe(parts[1], parts[0]):
                return True
            else:
                return False

        else:   # vowelPosition == 3
            if self.isPrefix(parts[0]) \
                    and self.validSuperscribe(parts[1], parts[2]) \
                    and not self.validSubscribe(parts[2], parts[1]):
                return True
            else:
                return False

    def isSubscribed(self, parts, vowelPosition):
        if vowelPosition == 2:
            if not self.validSuperscribe(parts[0], parts[1]) \
                    and self.validSubscribe(parts[1], parts[0]):
                return True
            else:
                return False

        else:   # vowelPosition == 3
            if self.isPrefix(parts[0]) \
                    and not self.validSuperscribe(parts[1], parts[2]) \
                    and self.validSubscribe(parts[2], parts[1]):
                return True
            else:
                return False

    def normalWylie(self, parts, vowelPosition):
    # TODO remove extra iterations taken by g.ya
    # TODO replace ugly predicates with functions

        if vowelPosition == 0:
            if parts[0] in tables.W_VOWELS:
                if parts[0] != 'a':
    # TODO This gives incorrect wylie. Move to renderUnicode().
                    Translator.syllable.wylie = ''.join(['a', parts[0]])
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
        syll = Translator.syllable.wylie

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
            return root in Translator.rulesSuper[head]

    def validSubscribe(self, sub, root):
        if sub not in tables.SUB:
            return False

        else:
            return root in Translator.rulesSub[sub]

    def appendWylieChar(self, char):
        Translator.syllable.wylie = ''.join([Translator.syllable.wylie, char])

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

            newString = [Translator.syllable.uni]

            if char:
    # TODO: More efficient handling of g. irregular.
                if char == 'g.':
                    char = 'g'
                    self.setStruct(comp, char)

                if self.needsSubjoin(comp):
                    newString.append(self.toSubjoinedUnicode(char))

                else:
                    newString.append(self.toUnicode(char))

                Translator.syllable.uni = u''.join(newString)

    def isPrefix(self, char):
        if char in tables.PREFIXES:
            return True
        else:
            return False

    def tsheg(self):
        Translator.syllable.tsheg()
        self.outputUnicode()

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

    def test(self, string):
        sys.stdout.write(string + " : ")

        self.newSyllable()
        for i, s in enumerate(string):
            self.add(s)

        self.tsheg()
        print()

    def partTest(self, string):
        sys.stdout.write(string + " : ")

        self.newSyllable(string)
        l = self.partition()
        print(str(l))
    # }}}


class Syllable(object):
    '''Used as static object for the Translator class'''

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

    def new(self):
        self.clear()
        self.wylie = ''


def main():
    t = Translator()
    # t.alphabet()
    # t.vowels()

    if len(argv) < 2:
        t.test('sangs')
        t.test('bre')
        t.test('rta')
        t.test('mgo')
        t.test('gya')
        t.test('g.yag')
        t.test('\'rba')
        t.test('tshos')
        t.test('lhongs')
        t.test('mngar')
        t.test('sngas')
        t.test('rnyongs')
        t.test('brnyes')
        t.test('rgyas')
        t.test('skyongs')
        t.test('bskyongs')
        t.test('grwa')
        t.test('spre\'u')
        t.test('spre\'u\'i')
        t.test('\'dra')
        t.test('\'bya')
        t.test('\'gra')
        t.test('\'gyang')
        t.test('\'khra')
        t.test('\'khyig')
        t.test('\'kyags')
        t.test('\'phre')
        t.test('\'phyags')
        t.test('a')
        t.test('o')
        t.test('a\'am')
        t.test('ab')
        t.test('bswa')
        # t.test('bha')
        return

    f = open(argv[1], 'r')

    for line in f:
        t.test(line.rstrip())

    f.close()

if __name__ == '__main__':
    from sys import argv
    main()
