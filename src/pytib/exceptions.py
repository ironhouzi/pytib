class ParseError(Exception):
    pass


class InvalidLanguage(ParseError):
    def __init__(self, input_word):
        self.input = input_word


class InvalidTibetan(InvalidLanguage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSanskrit(InvalidLanguage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidConfig(ParseError):
    def __init__(self, msg, config_item=None):
        self.msg = msg
        self.config_item = config_item
