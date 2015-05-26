# -*- coding: utf-8 -*-

import unittest
from pytib.wylie2uni import Translator
from pytib.wylie2uni import Syllable


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
              'bswa',    'grwa', )

    u_defs = ('སངས་', 'བྲེ་',    'རྟ་',   'མགོ་',
              'གྱ་',   'གཡག་',  'འརྦ་',  'ཚོས་',
              'ལྷོངས་', 'མངར་',  'སྔས་',  'རྙོངས་',
              'བརྙེས་', 'རྒྱས་',   'སྐྱོངས་', 'བསྐྱོངས་',
              'གྲྭ་',   'སྤྲེའུ་',   'སྤྲེའུའི་', 'འདྲ་',
              'འབྱ་',  'འགྲ་',   'འགྱང་', 'འཁྲ་',
              'འཁྱིག་', 'འཀྱགས་', 'འཕྲེ་',  'འཕྱགས་',
              'ཨ་',   'ཨོ་',    'ཨའམ་', 'ཨབ་',
              'བསྭ་',  'གྲྭ་', )

    def test_assorted(self):
        t = Translator()
        s = Syllable()
        for i, d in enumerate(self.w_defs):
            t.analyze(s, d)
            s.tsheg()
            self.assertEqual(s.uni, self.u_defs[i])


class BytecodeTest(unittest.TestCase):

    correct = "U+0F56, U+0F66, U+0F90, U+0FB1, U+0F7C, U+0F44, U+0F66"

    def test_bytecode(self):
        t = Translator()
        syllable = Syllable()
        bytecodes = t.bytecodes(syllable, 'bskyongs')
        self.assertEqual(bytecodes, self.correct)

    def test_bytecodeError(self):
        t = Translator()
        syllable = Syllable()
        bytecodes = t.bytecodes(syllable, 'skyong')
        self.assertNotEqual(bytecodes, self.correct)


class SanskritGenerationTest(unittest.TestCase):

    t = Translator()

    def analyzeAndCheck(self, uni, wylie):
        s = Syllable()
        self.t.analyze(s, wylie)
        self.assertEqual(s.uni, uni)

    # TODO: find counter case
    def test_hung(self):
        uni = '\u0f67' + '\u0f75' + '\u0f83'
        wylie = 'hūṃ'
        self.analyzeAndCheck(uni, wylie)

    def test_om(self):
        uni = '\u0f00'
        wylie = 'oṃ'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_phat(self):
        uni = '\u0f55' + '\u0f4a'
        wylie = 'phaṭ'
        self.analyzeAndCheck(uni, wylie)

    def test_bighnan(self):
        uni = '\u0f56' + '\u0f72' + '\u0f43' + '\u0fa3' + '\u0f71' + '\u0f53'
        wylie = 'bighnān'
        self.analyzeAndCheck(uni, wylie)

    def test_ah(self):
        uni = '\u0f68' + '\u0f71' + '\u0f7f'
        wylie = 'āḥ'
        self.analyzeAndCheck(uni, wylie)

    def test_mandal(self):
        uni = '\u0f58' + '\u0f53' + '\u0f9c' + '\u0f63'
        wylie = 'manḍal'
        self.analyzeAndCheck(uni, wylie)

    def test_sanskrit_tib_genitive(self):
        uni = '\u0F64' + '\u0F71' + '\u0F40' + '\u0FB1' + '\u0F60' + '\u0F72'
        wylie = "śākya'i"
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_sarva(self):
        uni = '\u0F66' + '\u0F62' + '\u0FA6'
        wylie = 'sarva'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_vajra(self):
        uni = '\u0F56' + '\u0F5B' + '\u0FB2'
        wylie = 'vajra'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_badzra(self):
        uni = '\u0F56' + '\u0F5B' + '\u0FB2'
        s = Syllable()
        self.t.analyze(s, 'badzra')
        self.assertNotEqual(s.uni, uni)

    # TODO: find counter case
    def test_hksmlvryam(self):
        uni = '\u0f67' + '\u0fb9' + '\u0fa8' + '\u0fb3' + '\u0fba' + \
            '\u0fbc' + '\u0fbb' + '\u0f83'
        wylie = 'hkṣmlvryaṃ'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_tthddhnaa(self):
        uni = '\u0f4a' + '\u0f9b' + '\u0f9c' + '\u0f9d' + '\u0f9e' + '\u0f71'
        wylie = 'ṭṭhḍḍhṇā'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_shunyata(self):
        uni = '\u0f64' + '\u0f75' + '\u0f53' + '\u0fb1' + '\u0f4f' + '\u0f71'
        wylie = 'śūnyatā'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_kyai(self):
        uni = '\u0f40' + '\u0fb1' + '\u0f7b'
        wylie = 'kyai'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_lakshmyai(self):
        uni = '\u0f63' + '\u0f69' + '\u0fa8' + '\u0fb1' + '\u0f7b'
        wylie = 'lakṣmyai'
        self.analyzeAndCheck(uni, wylie)

    # TODO: find counter case
    def test_akshye(self):
        uni = '\u0f68' + '\u0f69' + '\u0fb1' + '\u0f7a'
        wylie = 'akṣye'
        self.analyzeAndCheck(uni, wylie)

    def test_ai(self):
        uni = '\u0F68' + '\u0F7B'
        wylie = 'ai'
        self.analyzeAndCheck(uni, wylie)

    def test_au(self):
        uni = '\u0F68' + '\u0F7D'
        wylie = 'au'
        self.analyzeAndCheck(uni, wylie)
