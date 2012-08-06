from steel.fields import Field

__all__ = ['Bytes']


class Bytes(Field):
    def encode(self, value):
        # Nothing to do here
        return value

    def decode(self, value):
        # Nothing to do here
        return value
