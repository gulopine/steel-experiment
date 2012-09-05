from steel.fields import Field

__all__ = ['Bytes', 'String']


class Bytes(Field):
    def encode(self, value):
        # Nothing to do here
        return value

    def decode(self, value):
        # Nothing to do here
        return value


class String(Field):
    def __init__(self, *args, encoding, **kwargs):
        self.encoding = encoding
        super(String, self).__init__(*args, **kwargs)

    def encode(self, value):
        return value.encode(self.encoding)

    def decode(self, value):
        return value.decode(self.encoding)
