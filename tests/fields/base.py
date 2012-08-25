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
