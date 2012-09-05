import codecs
from steel.fields import Field
from steel.fields.mixin import Fixed

__all__ = ['Bytes', 'String', 'FixedBytes', 'FixedString']


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


class FixedBytes(Fixed, Bytes):
    "A stream of bytes that will always be set to the same value"

    # The mixin does the heavy lifting
    pass


class FixedString(Fixed, String):
    "A stream of bytes that will always be set to the same value"

    # The mixin does the heavy lifting
    pass
