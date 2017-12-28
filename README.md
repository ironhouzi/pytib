pytib
=====

Software for Tibetan word processing

Dependencies:
+ Python >= 3.6.
+ Tibetan Unicode font. I recommend [MS Himalaya](http://fontzone.net/font-details/microsoft-himalaya) for it's unprecedented functionality, being able to correctly render even the most obscure stacks from Tibetan transliterations of Sanskrit.

Currently handles conversion of both wylie and [IAST](http://en.wikipedia.org/wiki/Tibetan_alphabet#Transliteration_of_Sanskrit) to Tibetan Unicode.

The wylie parsing algorithm is based on software written by [Edward Henning](http://www.kalacakra.org/print/print.htm).

## Uncertainties

[ ] The [ptib reader](pytib/read.py) never places a tsheg between syllable and shad.
[ ] No, unambiguous algorithm to discern the use of anusvara/chandrabindu (rjes su nga ro/sna ldan). Currently, implemented as corner case lookups.
[ ] Apart from a few cases, the algorithm carries out strict translation and does not handle incorrectly spelled Tibetan transliteration of Sanskrit words. E.g. *maṅgalaṃ* becomes: མངྒལཾ - not: མངྒ་ལ, which is commonly seen in Tibetan texts. This would require the input: *maṅga laṃ*.
