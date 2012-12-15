import steel
import unittest


class ObjectTests(unittest.TestCase):
    def setUp(self):
        class B(steel.Structure):
            field1 = steel.Bytes(size=3)
            field2 = steel.Bytes(size=3)
        self.B = B

        class A(steel.Structure):
            field1 = steel.Integer(size=1)
            field2 = steel.Object(B)

        self.A = A

    def test_size(self):
        self.assertEqual(self.B.size, 6)
        self.assertEqual(self.A.size, 7)

    def test_encode(self):
        field = steel.Object(self.B)
        value = self.B(field1=b'abc', field2=b'def')
        value = field.encode(value)

        self.assertEqual(value, b'abcdef')

    def test_decode(self):
        field = steel.Object(self.B)
        value = field.decode(b'abcdef')

        self.assertIsInstance(value, self.B)

        self.assertEqual(value.field1, b'abc')
        self.assertEqual(value.field2, b'def')


class ListTests(unittest.TestCase):
    def setUp(self):
        self.field = steel.List(steel.Integer(size=1), size=4)

    def test_encode(self):
        value = self.field.encode([1, 2, 3, 4])
        self.assertEqual(value, b'\x01\x02\x03\x04')

    def test_decode(self):
        value = self.field.decode(b'\x01\x02\x03\x04')
        self.assertEqual(value, [1, 2, 3, 4])

    def test_encode_too_few(self):
        with self.assertRaises(ValueError):
            self.field.encode([1, 2, 3])

    def test_encode_too_many(self):
        with self.assertRaises(ValueError):
            self.field.encode([1, 2, 3, 4, 5, 6, 7])

    def test_encode_defaults(self):
        field = steel.List(steel.Integer(size=1, default=0), size=4)
        value = field.encode([1, 2, 3])
        self.assertEqual(value, b'\x01\x02\x03\x00')
