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
