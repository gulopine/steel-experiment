import struct
from steel.fields import Field

__all__ = ['Integer']


class Integer(Field):
    "An integer represented as a sequence and bytes"

    # These map a number of bytes to a struct format code
    size_formats = {
        1: 'B',  # char
        2: 'H',  # short
        4: 'L',  # long
        8: 'Q',  # long long
    }

    def __init__(self, *args, signed=False, endianness='<', **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        code = self.size_formats[self.size]
        if signed:
            code = code.lower()
        self.format_code = endianness + code

    def encode(self, value):
        try:
            return struct.pack(self.format_code, value)
        except struct.error as e:
            raise ValueError(*e.args)

    def decode(self, value):
        # The index on the end is because unpack always returns a tuple
        try:
            return struct.unpack(self.format_code, value)[0]
        except struct.error as e:
            raise ValueError(*e.args)
