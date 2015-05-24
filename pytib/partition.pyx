def partition(wylieSyllable, max_char_len, alphabet, g_prefix):
    wylieLetters = []

    while len(wylieSyllable) != 0:
        for latin_tib_char_len in range(max_char_len, 0, -1):
            part = wylieSyllable[:latin_tib_char_len]

            if part == '':
                break

            if part == g_prefix or part in alphabet:
                wylieLetters.append(part)
                wylieSyllable = wylieSyllable[latin_tib_char_len:]

            elif latin_tib_char_len == 1 and part not in alphabet:
                return None

    return wylieLetters

PREVOWEL = ('prefix',
            'super',
            'root',
            'subjoined',
            'secondsub',
            'vowel', )

POSTVOWEL = ('suffix',
             'suffix2',
             'genitive',
             'genvowel', )

SYLLSTRUCT = PREVOWEL + POSTVOWEL
W_VOWELS = ('i', 'u', 'e', 'o', )

def generateWylieUnicode(self, syllable):
    for syllableComponent in SYLLSTRUCT:
        char = syllable.structure[syllableComponent]

        if not char:
            continue

        if char == self.wylie_vowel_a and syllableComponent != 'root':
            continue

        newString = [syllable.uni]

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
