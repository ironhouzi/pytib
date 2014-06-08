# -*- coding: utf-8 -*-

import unittest
from wylie2uni import Translator
from wylie2uni import Syllable


class sankritTest(unittest.TestCase):

    def setUp(self):
        self.defFile = open('resources/sanskrit_sample', 'r')

    def test_sanskrit(self):
        t = Translator()
        s = Syllable('')
        for d in self.defFile:
            s.wylie = d.strip()
            self.assertTrue(t.isSanskrit(s) or not t.analyzeWylie(s))

    def tearDown(self):
        self.defFile.close()


# Rough test. TODO: break up into individual tests.
class wylieTest(unittest.TestCase):

    w_defs = ('sangs',   'bre',     'rta',        'mgo',
              'gya',     'g.yag',   '\'rba',      'tshos',
              'lhongs',  'mngar',   'sngas',      'rnyongs',
              'brnyes',  'rgyas',   'skyongs',    'bskyongs',
              'grwa',    'spre\'u', 'spre\'u\'i', '\'dra',
              '\'bya',   '\'gra',   '\'gyang',    '\'khra',
              '\'khyig', '\'kyags', '\'phre',     '\'phyags',
              'a',       'o',       'a\'am',      'ab',
              'bswa',    'bha',     'grwa', )

    u_defs = ('སངས་', 'བྲེ་',    'རྟ་',   'མགོ་',
              'གྱ་',   'གཡག་',  'འརྦ་',  'ཚོས་',
              'ལྷོངས་', 'མངར་',  'སྔས་',  'རྙོངས་',
              'བརྙེས་', 'རྒྱས་',   'སྐྱོངས་', 'བསྐྱོངས་',
              'གྲྭ་',   'སྤྲེའུ་',   'སྤྲེའུའི་', 'འདྲ་',
              'འབྱ་',  'འགྲ་',   'འགྱང་', 'འཁྲ་',
              'འཁྱིག་', 'འཀྱགས་', 'འཕྲེ་',  'འཕྱགས་',
              'ཨ་',   'ཨོ་',    'ཨའམ་', 'ཨབ་',
              'བསྭ་',  'བཧ་',   'གྲྭ་', )

    def test_sanskrit(self):
        t = Translator()
        s = Syllable('')
        for i, d in enumerate(self.w_defs):
            s.wylie = d
            t.analyzeWylie(s)
            t.generateWylieUnicode(s)
            s.tsheg()
            self.assertEqual(s.uni, self.u_defs[i])


class BytecodeTest(unittest.TestCase):

    correct = ['U+0F56', 'U+0F66', 'U+0F90', 'U+0FB1',
               'U+0F7C', 'U+0F44', 'U+0F66']

    def test_bytecode(self):
        t = Translator()
        bytecodes = t.getBytecodes('bskyongs')
        self.assertEqual(bytecodes, self.correct)

    def test_bytecodeError(self):
        t = Translator()
        bytecodes = t.getBytecodes('skyong')
        self.assertNotEqual(bytecodes, self.correct)


class SanskritGenerationTest(unittest.TestCase):

    t = Translator()
    s = Syllable('')

    def analyzeAndCheck(self, uni):
        self.t.analyze(self.s)
        self.assertEqual(self.s.uni, uni)

    # TODO: find counter case
    def test_hung(self):
        uni = '\u0f67' + '\u0f75' + '\u0f83'
        self.s.wylie = 'hūṃ'
        self.analyzeAndCheck(uni)

    # TODO: find counter case
    def test_tva(self):
        uni = '\u0f4f' + '\u0fad'
        self.s.wylie = 'tva'
        self.analyzeAndCheck(uni)

    def test_om(self):
        uni = '\u0f00'
        self.s.wylie = 'oṃ'
        self.analyzeAndCheck(uni)

    # TODO: find counter case
    def test_phat(self):
        uni = '\u0f55' + '\u0f4a'
        self.s.wylie = 'phaṭ'
        self.analyzeAndCheck(uni)

    def test_bighnan(self):
        uni = '\u0f56' + '\u0f72' + '\u0f43' + '\u0fa3' + '\u0f71' + '\u0f53'
        self.s.wylie = 'bighnān'
        self.analyzeAndCheck(uni)

    def test_ah(self):
        uni = '\u0f68' + '\u0f71' + '\u0f7f'
        self.s.wylie = 'āḥ'
        self.analyzeAndCheck(uni)

    def test_mandal(self):
        uni = '\u0f58' + '\u0f53' + '\u0f9c' + '\u0f63'
        self.s.wylie = 'manḍal'
        self.analyzeAndCheck(uni)

    # TODO: find counter case
    def test_sarva(self):
        uni = '\u0F66' + '\u0F62' + '\u0FA6'
        self.s.wylie = 'sarva'
        self.analyzeAndCheck(uni)

    # TODO: find counter case
    def test_vajra(self):
        uni = '\u0F56' + '\u0F5B' + '\u0FB2'
        self.s.wylie = 'vajra'
        self.analyzeAndCheck(uni)

    # TODO: find counter case
    def test_badzra(self):
        uni = '\u0F56' + '\u0F5B' + '\u0FB2'
        self.s.wylie = 'badzra'
        self.t.analyze(self.s)
        self.assertNotEqual(self.s.uni, uni)

    # TODO: find counter case
    def test_tthddhnaa(self):
        uni = '\u0f4a' + '\u0f9b' + '\u0f9c' + '\u0f9d' + '\u0f9e' + '\u0f71'
        self.s.wylie = 'ṭṭhḍḍhṇā'
        self.analyzeAndCheck(uni)
