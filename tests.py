# -*- coding: utf-8 -*-

import unittest
from wylie2uni import *

class sankritTest(unittest.TestCase):

    def setUp(self):
        self.defFile = open('resources/sanskrit_sample', 'r')

    def test_sanskrit(self):
        t = Translator()
        s = Syllable('')
        for d in self.defFile:
            s.wylie = d.strip()
            self.assertTrue(t.isSanskrit(s) or \
                    not t.analyzeWylie(s))

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
        'bswa',    'bha',     'grwa' ]

    u_defs = [
        'སངས་', 'བྲེ་',    'རྟ་',   'མགོ་',
        'གྱ་',   'གཡག་',  'འརྦ་',  'ཚོས་',
        'ལྷོངས་', 'མངར་',  'སྔས་',  'རྙོངས་',
        'བརྙེས་', 'རྒྱས་',   'སྐྱོངས་', 'བསྐྱོངས་',
        'གྲྭ་',   'སྤྲེའུ་',   'སྤྲེའུའི་', 'འདྲ་',
        'འབྱ་',  'འགྲ་',   'འགྱང་', 'འཁྲ་',
        'འཁྱིག་', 'འཀྱགས་', 'འཕྲེ་',  'འཕྱགས་',
        'ཨ་',   'ཨོ་',    'ཨའམ་', 'ཨབ་',
        'བསྭ་',  'བཧ་',   'གྲྭ་' ]

    def test_sanskrit(self):
        t = Translator()
        s = Syllable('')
        for i, d in enumerate(self.w_defs):
            s.wylie = d
            t.analyzeWylie(s)
            t.generateWylieUnicode(s)
            s.tsheg()
            self.assertTrue(s.uni == self.u_defs[i])


class BytecodeTest(unittest.TestCase):

    correct = [ 'U+0F56', 'U+0F66', 'U+0F90', 'U+0FB1',
                'U+0F7C', 'U+0F44', 'U+0F66' ]

    def test_bytecode(self):
        t = Translator()
        bytecodes = t.getBytecodes('bskyongs')
        self.assertTrue(bytecodes == self.correct)

    def test_bytecodeError(self):
        t = Translator()
        bytecodes = t.getBytecodes('skyong')
        self.assertFalse(bytecodes == self.correct)
