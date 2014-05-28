pytib
=====

Software for Tibetan word processing

Dependencies:
+ Python 3.3
+ Tibetan Unicode font. I recommend [MS Himalaya](http://fontzone.net/font-details/microsoft-himalaya) for it's unprecedented functionality, being able to correctly render even the most obscure stacks from Tibetan transliterations of Sanskrit.

Currently only handles wylie to Tibetan Unicode conversion.

The wylie parsing algorithm is based on software written by [Edward Henning](http://www.kalacakra.org/print/print.htm).

It is also worth mentioning that the current version takes single letter vowel wylie strings ('o', 'i', 'u', 'e') and prepends an 'a' to these, turning them into: ('ao', 'ai', 'au', 'ae').
