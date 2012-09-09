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
