def partition(wylieSyllable, max_char_len, alphabet, g_prefix):
    wylieLetters = []

    while len(wylieSyllable) != 0:
        for latin_tib_char_len in range(max_char_len, 0, -1):
            part = wylieSyllable[:latin_tib_char_len]

            if part == g_prefix or part in alphabet:
                wylieLetters.append(part)
                wylieSyllable = wylieSyllable[latin_tib_char_len:]

            elif part == '':
                break

            elif latin_tib_char_len == 1 and part not in alphabet:
                return None

    return wylieLetters
