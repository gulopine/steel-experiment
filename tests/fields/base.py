import steel
import unittest


class FieldTests(unittest.TestCase):
    def test_auto_label(self):
        # One word
        field = steel.Bytes(size=1)
        field.set_name('byte')
        self.assertEqual(field.label, 'byte')

        # Two words
        field = steel.Bytes(size=1)
        field.set_name('two_bytes')
        self.assertEqual(field.label, 'two bytes')

    def test_manual_label(self):
        field = steel.Bytes(size=1, label='explicit')
        field.set_name('field')
        self.assertEqual(field.label, 'explicit')


class MapTests(unittest.TestCase):
    def setUp(self):
        self.field = steel.Bytes(size=1, map={
            b'a': 'A',
            b'b': 'B',
            b'c': 'C',
        })

    def test_encode(self):
        self.assertEqual(self.field.encode('A'), b'a')
        self.assertEqual(self.field.encode('B'), b'b')
        self.assertEqual(self.field.encode('C'), b'c')

    def test_decode(self):
        self.assertEqual(self.field.decode(b'a'), 'A')
        self.assertEqual(self.field.decode(b'b'), 'B')
        self.assertEqual(self.field.decode(b'c'), 'C')

    def test_encode_invalid(self):
        # It shouldn't be possible to encode a value not in the map
        with self.assertRaises(ValueError):
            self.field.decode('D')

    def test_decode_invalid(self):
        # It shouldn't be possible to encode a value not in the map
        with self.assertRaises(ValueError):
            self.field.decode(b'd')
