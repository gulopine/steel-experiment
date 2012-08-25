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
        class NamedObject(object):
            def set_name(self, name):
                self.name = name

        self.d['example'] = NamedObject()
        self.assertEqual(self.d['example'].name, 'example')

    def test_errors(self):
        # Make sure set_name() errors are raised, not swallowed
        class ErrorObject(object):
            "Just a simple object that errors out while setting its name"
            def set_name(self, name):
                raise TypeError('Something went wrong')

        with self.assertRaises(TypeError):
            self.d['example'] = ErrorObject()
