import steel
import unittest


class NameAwareOrderedDictTests(unittest.TestCase):
    def setUp(self):
        self.d = steel.NameAwareOrderedDict()

    def test_ignore_object(self):
        # Objects without a set_name() method should be ignored
        self.d['example'] = object()
        self.assertFalse(hasattr(self.d['example'], 'name'))

    def test_auto_name(self):
        # Objects with a set_name() method should be told their name
        class NamedObject:
            def set_name(self, name):
                self.name = name

        self.d['example'] = NamedObject()
        self.assertEqual(self.d['example'].name, 'example')

    def test_errors(self):
        # Make sure set_name() errors are raised, not swallowed
        class ErrorObject:
            "Just a simple object that errors out while setting its name"
            def set_name(self, name):
                raise TypeError('Something went wrong')

        with self.assertRaises(TypeError):
            self.d['example'] = ErrorObject()


class SizeTests(unittest.TestCase):
    def test_explicit_sizes(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)

        self.assertEqual(Test.size, 6)


class InstantiationTests(unittest.TestCase):
    def test_empty_args(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)

        obj = Test()

        self.assertNotIn('field1', obj.__dict__)
        self.assertNotIn('field2', obj.__dict__)

    def test_filled_args(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)

        obj = Test(field1=b'f1', field2=b'fld2')

        self.assertEqual(obj.field1, b'f1')
        self.assertEqual(obj.field2, b'fld2')


class StructureTupleTests(unittest.TestCase):
    def test_empty_args(self):
        class Test(steel.StructureTuple):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)

        obj = Test()

        self.assertIsInstance(obj, tuple)

        self.assertEqual(obj.field1, None)
        self.assertEqual(obj.field2, None)

    def test_filled_args(self):
        class Test(steel.Structure):
            field1 = steel.Bytes(size=2)
            field2 = steel.Bytes(size=4)

        obj = Test(field1=b'f1', field2=b'fld2')

        self.assertEqual(obj.field1, b'f1')
        self.assertEqual(obj.field2, b'fld2')
