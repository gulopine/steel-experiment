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

    def __init__(self, *args, endianness='<', **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        self.format_code = endianness + self.size_formats[self.size]

    def encode(self, value):
        return struct.pack(self.format_code, value)

    def decode(self, value):
        # The index on the end is because unpack always returns a tuple
        return struct.unpack(self.format_code, value)[0]
