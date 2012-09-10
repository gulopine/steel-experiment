import codecs
from gettext import gettext as _

from steel.fields import Field
from steel.fields.mixin import Fixed

__all__ = ['Bytes', 'String', 'FixedBytes', 'FixedString']


class Bytes(Field):
    _("A stream of bytes that should be left unconverted")

    # Nothing to do here
    pass


class String(Field):
    _("A string that gets converted using a specified encoding")

    def __init__(self, *args, encoding, **kwargs):
        if hasattr(encoding, 'encode') and hasattr(encoding, 'decode'):
            # Completely custom codecs can be used directly
            self.codec = encoding
        else:
            # Otherwise, look it up in the registered system codecs
            # This also bails out early if the encoding isn't valid
            self.codec = codecs.lookup(encoding)

        super(String, self).__init__(*args, **kwargs)

    def encode(self, value):
        value = self.codec.encode(value)[0]

        return super(String, self).encode(value)

    def decode(self, value):
        value = self.codec.decode(value)[0]

        return super(String, self).decode(value)


class FixedBytes(Fixed, Bytes):
    _("A stream of bytes that will always be set to the same value")

    def __init__(self, value, *args, size=None, **kwargs):
        if size is None:
            size = len(value)
        super(FixedBytes, self).__init__(value, *args, size=size, **kwargs)

    # The mixin does the heavy lifting


class FixedString(Fixed, String):
    _("A string that will always be set to the same value")

    def __init__(self, value, *args, size=None, encoding, **kwargs):
        if size is None:
            size = len(value.encode(encoding))
        super(FixedString, self).__init__(value, *args, size=size, encoding=encoding, **kwargs)

    # The mixin does the heavy lifting
