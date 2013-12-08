''' Wylie2uni
    Wylie to utf-8 conversion.

'''
class Wylie2uni(object):
    'Main workhorse for the program'

    W_ROOTLETTERS = [
        'k',  'kh',  'g',  'ng',
        'c',  'ch',  'j',  'ny',
        't',  'th',  'd',  'n',
        'p',  'ph',  'b',  'm',
        'ts', 'tsh', 'dz', 'w',
        'zh', 'z',   '\'', 'y',
        'r',  'l',   'sh', 's',
        'h',  'a' ];

    U_ROOTLETTERS = [
        u'\u0f40', u'\u0f41', u'\u0f42', u'\u0f44',
        u'\u0f45', u'\u0f46', u'\u0f47', u'\u0f49',
        u'\u0f4f', u'\u0f50', u'\u0f51', u'\u0f53',
        u'\u0f54', u'\u0f55', u'\u0f56', u'\u0f58',
        u'\u0f59', u'\u0f5a', u'\u0f5b', u'\u0f5d',
        u'\u0f5e', u'\u0f5f', u'\u0f60', u'\u0f61',
        u'\u0f62', u'\u0f63', u'\u0f64', u'\u0f66',
        u'\u0f67', u'\u0f68' ];

    def __init__(self):
        self.step1 = dict(zip(self.W_ROOTLETTERS, self.U_ROOTLETTERS))

    def translate(self, syllable):
        print "%s" % (self.step1[syllable])

def main():
    w = Wylie2uni()
    for key in w.step1.keys():
        w.translate(key)

if __name__ =='__main__':
    main()
