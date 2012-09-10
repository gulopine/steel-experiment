import steel
import unittest


class IntegerTests(unittest.TestCase):
    def test_char_encode(self):
        field = steel.Integer(size=1)
        self.assertEqual(field.encode(1), b'\x01')

    def test_char_decode(self):
        field = steel.Integer(size=1)
        self.assertEqual(field.decode(b'\x01'), 1)

    def test_short_encode(self):
        field = steel.Integer(size=2)
        self.assertEqual(field.encode(2), b'\x02\x00')

    def test_short_decode(self):
        field = steel.Integer(size=2)
        self.assertEqual(field.decode(b'\x02\x00'), 2)

    def test_long_encode(self):
        field = steel.Integer(size=4)
        self.assertEqual(field.encode(4), b'\x04\x00\x00\x00')

    def test_long_decode(self):
        field = steel.Integer(size=4)
        self.assertEqual(field.decode(b'\x04\x00\x00\x00'), 4)

    def test_long_long_encode(self):
        field = steel.Integer(size=8)
        self.assertEqual(field.encode(8), b'\x08\x00\x00\x00\x00\x00\x00\x00')

    def test_long_long_decode(self):
        field = steel.Integer(size=8)
        self.assertEqual(field.decode(b'\x08\x00\x00\x00\x00\x00\x00\x00'), 8)

    def test_big_endian_encode(self):
        field = steel.Integer(size=2, endianness='>')
        self.assertEqual(field.encode(2), b'\x00\x02')

    def test_big_endian_decode(self):
        field = steel.Integer(size=2, endianness='>')
        self.assertEqual(field.decode(b'\x00\x02'), 2)

    def test_too_large_encode(self):
        field = steel.Integer(size=1)
        with self.assertRaises(ValueError):
            field.encode(256)

    def test_signed_encode(self):
        field = steel.Integer(size=1, signed=True)
        self.assertEqual(field.encode(1), b'\x01')
        self.assertEqual(field.encode(-1), b'\xff')

    def test_signed_decode(self):
        field = steel.Integer(size=1, signed=True)
        self.assertEqual(field.decode(b'\x01'), 1)
        self.assertEqual(field.decode(b'\xff'), -1)

    def test_signed_big_endian_encode(self):
        field = steel.Integer(size=2, signed=True, endianness='>')
        self.assertEqual(field.encode(2), b'\x00\x02')
        self.assertEqual(field.encode(-2), b'\xff\xfe')

    def test_signed_big_endian_decode(self):
        field = steel.Integer(size=2, signed=True, endianness='>')
        self.assertEqual(field.decode(b'\x00\x02'), 2)
        self.assertEqual(field.decode(b'\xff\xfe'), -2)

    def test_unsigned_negative_encode(self):
        field = steel.Integer(size=1)
        with self.assertRaises(ValueError):
            field.encode(-1)

    def test_too_large_signed_encode(self):
        field = steel.Integer(size=1, signed=True)
        with self.assertRaises(ValueError):
            field.encode(128)

    def test_too_large_negative_signed_encode(self):
        field = steel.Integer(size=1, signed=True)
        with self.assertRaises(ValueError):
            field.encode(-129)


class FixedIntegerTests(unittest.TestCase):
    def test_encode(self):
        field = steel.FixedInteger(42, size=1)

        # It should encode the fixed value no matter what
        self.assertEqual(field.encode(None), b'*')
        self.assertEqual(field.encode(42), b'*')

    def test_decode(self):
        field = steel.FixedInteger(42, size=1)

        # If the value is correct, everything works fine
        self.assertEqual(field.decode(b'*'), 42)

        # An incorrect value raises a ValueError
        with self.assertRaises(ValueError):
            field.decode(b'+')

    def test_auto_size(self):
        # Size isn't necessary if it can be inferred from the value
        field = steel.FixedInteger(42)
        self.assertEqual(field.size, 1)

        field = steel.FixedInteger(420)
        self.assertEqual(field.size, 2)

        field = steel.FixedInteger(71420)
        # This can technically be stored in 3 bytes, but the conversion
        # requires a 4-byte field to hold that much data
        self.assertEqual(field.size, 4)

        # This value is too big even for an 8-byte integer
        with self.assertRaises(ValueError):
            steel.FixedInteger(100000000000000000000)
