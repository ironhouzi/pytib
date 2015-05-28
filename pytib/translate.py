from pytib.tables import *

# TODO: create a dictionary of tuples containing all needed lookup information
#       These are needed:
#       * analyzeBaseCase
#       * named tuple for syllable structure ?

PREFIXES = get_chars(PREFIXES_I, consonants)

def toUnicode(latin_letter, lookup_table, offset):
    """ Docstring
   lookup_table should be a dictionary, sanskrit or tibetan
   offset should be either 0 or 0x50 (SUBOFFSET)
    """
    return chr(ord(lookup_table[str(latin_letter)]) + offset)

def getVowelIndices(word, vowels):
    """ Docstring
    word should be a wylie string
    vowels should be the list of valid vowels

    returns frozenset of unadjacent vowel positions for a given word

    Adjacent vowels must be removed to handle words with an explicit 'a'
    """
    indices = frozenset([i for i,c in enumerate(word) if c in vowels])
    adjacents = frozenset([i[0] for i in zip(indices, indices[1:])
                          if i[1] - i[0] == 1])
    return indices.difference(adjacents)

# TODO: use varargs for head/root-letter args
def validSuperscribe(head_letter, root_letter, superjoin, valid_superjoin):
    return head_letter in superjoin \
        and root_letter in valid_superjoin[head_letter]

# TODO: use varargs for head/root-letter args
def validSubscribe(root_letter, subjoined_letter, subjoined, valid_subjoined):
    return  subjoined_letter in subjoined \
        and root_letter in valid_subjoined[subjoined_letter]

def validate(wylieLetters, vowelPosition, sub=1):
    """ Docstring
    sub is 1 if checking subscribed and 0 if checking superscribed
    """
    truth_vector = [x % 2 == sub for x in range(4)]

    if vowelPosition == 2:
        return not (truth_vector[0] ^ validSuperscribe(wylieLetters[0],
                                                       wylieLetters[1])) \
            and not (truth_vector[1] ^ validSubscribe(wylieLetters[0],
                                                      wylieLetters[1]))
    else:   # vowelPosition == 3
        return wylieLetters[0] PREFIXES \
            and not (truth_vector[2] ^ validSuperscribe(wylieLetters[1],
                                                        wylieLetters[2])) \
            and not (truth_vector[3] ^ validSubscribe(wylieLetters[1],
                                                      wylieLetters[2]))

def invalidWylie(string, ga_prefix, latin_set):
    return not string.startswith(ga_prefix) \
        and any(char not in latin_set for char in string)

