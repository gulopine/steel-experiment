import steel
import unittest


class BytesTests(unittest.TestCase):
    def test_encode(self):
        field = steel.Bytes(size=3)
        self.assertEqual(field.encode(b'abc'), b'abc')

    def test_decode(self):
        field = steel.Bytes(size=3)
        self.assertEqual(field.decode(b'abc'), b'abc')


class StringTests(unittest.TestCase):
    def test_missing_encoding(self):
        with self.assertRaises(TypeError):
            # Instantiate without an encoding
            steel.String(size=3)

    def test_invalid_encoding(self):
        with self.assertRaises(LookupError):
            # Instantiate without an encoding
            steel.String(size=3, encoding='invalid')

    def test_encoding(self):
        # Simple encoding
        field = steel.String(size=3, encoding='ascii')
        self.assertEqual(field.encode('abc'), b'abc')

    def test_decoding(self):
        # Simple encoding
        field = steel.String(size=3, encoding='ascii')
        self.assertEqual(field.decode(b'abc'), 'abc')


class FixedBytesTests(unittest.TestCase):
    def test_encode(self):
        field = steel.FixedBytes(b'abc', size=3)

        # It should encode the fixed value no matter what
        self.assertEqual(field.encode(None), b'abc')
        self.assertEqual(field.encode(b'abc'), b'abc')

    def test_decode(self):
        field = steel.FixedBytes(b'abc', size=3)

        # If the value is correct, everything works fine
        self.assertEqual(field.decode(b'abc'), b'abc')

        # An incorrect value raises a ValueError
        with self.assertRaises(ValueError):
            field.decode(b'def')


class FixedStringTests(unittest.TestCase):
    def test_encode(self):
        field = steel.FixedString('abc', encoding='ascii', size=3)

        # It should encode the fixed value no matter what
        self.assertEqual(field.encode(None), b'abc')
        self.assertEqual(field.encode(b'abc'), b'abc')

    def test_decode(self):
        field = steel.FixedString('abc', encoding='ascii', size=3)

        # If the value is correct, everything works fine
        self.assertEqual(field.decode(b'abc'), 'abc')

        # An incorrect value raises a ValueError
        with self.assertRaises(ValueError):
            field.decode(b'def')
