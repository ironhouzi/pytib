pytib
=====

Software for Tibetan word processing

Dependencies:
+ Python >= 3.6.
+ Tibetan Unicode font. I recommend [MS Himalaya](http://fontzone.net/font-details/microsoft-himalaya) for it's unprecedented functionality, being able to correctly render even the most obscure stacks from Tibetan transliterations of Sanskrit. Despite the excellent implementation work in MS Himalaya, the font can be rather illegible for intensive reading sessions. If you do require complicated stacking, [Noto Sans Tibetan](https://www.google.com/get/noto/#sans-tibt) supports both regular and bold types and fit very well with the fonts in the Noto font package which cover most of the spoken languages today.

Currently handles conversion of wylie, polyglotta and [IAST](http://en.wikipedia.org/wiki/Tibetan_alphabet#Transliteration_of_Sanskrit) to Tibetan Unicode. You are free to redefine the translation tables by creating a JSON file with the Tibetan/Sanskrit consonant, vowels and ga prefix forcing character and special characters. This JSON file can be passed to `ptib` using the `-c` or `--config` parameter.

The Tibetan/Sanskrit parsing algorithm is based on [software](http://www.kalacakra.org/print/print.htm) written by the late Edward Henning.

## Remaining work

[ ] Rule: Never tsheg after visarga.
[ ] Parse numerals.
[ ] Parse special characters.

## Uncertainties

[x] ~~The [ptib reader](pytib/read.py) never places a tsheg between syllable and shad.~~ Fixed! Only tsheg between nga and shad.
[ ] No, unambiguous algorithm to discern the use of anusvara/chandrabindu (rjes su nga ro/sna ldan). Currently, implemented as corner case lookups.
[ ] Apart from a few cases, the algorithm carries out strict translation and does not handle incorrectly spelled Tibetan transliteration of Sanskrit words. E.g. *maṅgalaṃ* becomes: མངྒལཾ - not: མངྒ་ལ, which is commonly seen in Tibetan texts. This would require the input: *maṅga laṃ*.
