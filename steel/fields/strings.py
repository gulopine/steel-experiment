import codecs
from steel.fields import Field

__all__ = ['Bytes', 'String']


class Bytes(Field):
    "A stream of bytes that should be left unconverted"

    def encode(self, value):
        # Nothing to do here
        return value

    def decode(self, value):
        # Nothing to do here
        return value


class String(Field):
    "A string that gets converted using a specified encoding"

    def __init__(self, *args, encoding, **kwargs):
        # Bail out early if the encoding isn't valid
        codecs.lookup(encoding)

        self.encoding = encoding
        super(String, self).__init__(*args, **kwargs)

    def encode(self, value):
        return value.encode(self.encoding)

    def decode(self, value):
        return value.decode(self.encoding)
