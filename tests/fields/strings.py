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
