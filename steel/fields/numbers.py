from gettext import gettext as _

import struct
from steel.fields import Field
from steel.fields.mixin import Fixed

__all__ = ['Integer', 'FixedInteger']


class Integer(Field):
    _("An integer represented as a sequence and bytes")

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
            value = struct.pack(self.format_code, value)
        except struct.error as e:
            raise ValueError(*e.args)

        return super(Integer, self).encode(value)

    def decode(self, value):
        # The index on the end is because unpack always returns a tuple
        try:
            value = struct.unpack(self.format_code, value)[0]
        except struct.error as e:
            raise ValueError(*e.args)

        return super(Integer, self).decode(value)


class FixedInteger(Fixed, Integer):
    _("An integer that will always be set to the same value")

    def __init__(self, value, *args, size=None, **kwargs):
        if size is None:
            min_size = int((value.bit_length() + 7) / 8) or 1
            for size in sorted(self.size_formats):
                # Find the smallest known format that can hold this value
                if size >= min_size:
                    break
            else:
                # This is only reached if the break above never fires
                raise ValueError(_('Value is too large to store as an integer'))
        super(FixedInteger, self).__init__(value, *args, size=size, **kwargs)

    # The mixin does the heavy lifting
