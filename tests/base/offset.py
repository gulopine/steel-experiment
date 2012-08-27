import steel
import unittest


class OffsetTests(unittest.TestCase):
    def test_auto_offset(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)
            field3 = steel.Bytes(size=1)

        self.assertEqual(Test.field1.offset, 0)
        self.assertEqual(Test.field2.offset, 2)
        self.assertEqual(Test.field3.offset, 6)

    def test_manual_offset(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(offset=2, size=2)
            field2 = steel.Bytes(offset=10, size=4)
            field3 = steel.Bytes(offset=16, size=1)

        self.assertEqual(Test.field1.offset, 2)
        self.assertEqual(Test.field2.offset, 10)
        self.assertEqual(Test.field3.offset, 16)

    def test_mixed_offsets(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(offset=10, size=4)
            field3 = steel.Bytes(size=1)

        self.assertEqual(Test.field1.offset, 0)
        self.assertEqual(Test.field2.offset, 10)
        # This is field2's offset plus field2's size
        self.assertEqual(Test.field3.offset, 14)
