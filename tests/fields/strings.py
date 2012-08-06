import steel
import unittest


class BytesTests(unittest.TestCase):
    def test_encode(self):
        field = steel.Bytes(size=3)
        self.assertEqual(field.encode(b'abc'), b'abc')

    def test_decode(self):
        field = steel.Bytes(size=3)
        self.assertEqual(field.decode(b'abc'), b'abc')
