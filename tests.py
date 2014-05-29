# -*- coding: utf-8 -*-

import unittest
from wylie2uni import *

class sankritTest(unittest.TestCase):

    def setUp(self):
        self.defFile = open('resources/sanskrit_sample', 'r')
        self.t = Translator()
        self.s = Syllable('')

    def test_sanskrit(self):
        for s in self.defFile:
            self.s.wylie = s.strip()
            self.assertTrue(self.t.isSanskrit(self.s) or \
                    not self.t.analyzeWylie(self.s))

    def tearDown(self):
        self.defFile.close()

class wylieTest(unittest.TestCase):
    w_defs = [
        'sangs',   'bre',     'rta',        'mgo',
        'gya',     'g.yag',   '\'rba',      'tshos',
        'lhongs',  'mngar',   'sngas',      'rnyongs',
        'brnyes',  'rgyas',   'skyongs',    'bskyongs',
        'grwa',    'spre\'u', 'spre\'u\'i', '\'dra',
        '\'bya',   '\'gra',   '\'gyang',    '\'khra',
        '\'khyig', '\'kyags', '\'phre',     '\'phyags',
        'a',       'o',       'a\'am',      'ab',
        'bswa',    'bha' ]

    u_defs = [
        'སངས་', 'བྲེ་',    'རྟ་',   'མགོ་',
        'གྱ་',   'གཡག་',  'འརྦ་',  'ཚོས་',
        'ལྷོངས་', 'མངར་',  'སྔས་',  'རྙོངས་',
        'བརྙེས་', 'རྒྱས་',   'སྐྱོངས་', 'བསྐྱོངས་',
        'གྲྭ་',   'སྤྲེའུ་',   'སྤྲེའུའི་', 'འདྲ་',
        'འབྱ་',  'འགྲ་',   'འགྱང་', 'འཁྲ་',
        'འཁྱིག་', 'འཀྱགས་', 'འཕྲེ་',  'འཕྱགས་',
        'ཨ་',   'ཨོ་',    'ཨའམ་', 'ཨབ་',
        'བསྭ་',  'བཧ་' ]

    def test_sanskrit(self):
        t = Translator()
        s = Syllable('')
        for i, d in enumerate(self.w_defs):
            s.wylie = d
            t.analyzeWylie(s)
            t.generateUnicode(s)
            s.tsheg()
            self.assertTrue(s.uni == self.u_defs[i])


if __name__ == '__main__':
    unittest.main()

