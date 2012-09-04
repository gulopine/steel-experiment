import steel
import io
import unittest


class SeekIO(io.BytesIO):
    """
    A variation of BytesIO that keeps track of all .seek() activity.
    This can test whether files are accessed as efficiently as possible.
    """
    def __init__(self, *args, **kwargs):
        super(SeekIO, self).__init__(*args, **kwargs)
        self.seeks = []

    def seek(self, offset, *args, **kwargs):
        # Log it for later
        self.seeks.append(offset)

        # *args and **kwargs probably aren't necessary,
        # but it's a good idea anyway, just in case.
        return super(SeekIO, self).seek(offset, *args, **kwargs)


class SeekTests(unittest.TestCase):
    def setUp(self):
        self.data = b'abc'

        class Test(steel.Structure):
            a = steel.Bytes(size=1)  # offset 0
            b = steel.Bytes(size=1)  # offset 1
            c = steel.Bytes(size=1)  # offset 2
        self.Structure = Test

    def test_sequential_access(self):
        file = SeekIO(self.data)
        obj = self.Structure.load(file)

        self.assertEqual(obj.a, b'a')
        self.assertEqual(obj.b, b'b')
        self.assertEqual(obj.c, b'c')

        self.assertEqual(file.seeks, [0, 1, 2])

    def test_random_access(self):
        file = SeekIO(self.data)
        obj = self.Structure.load(file)

        self.assertEqual(obj.b, b'b')
        self.assertEqual(obj.c, b'c')
        self.assertEqual(obj.a, b'a')

        self.assertEqual(file.seeks, [0, 1, 2])

    def test_lazy_sequential_access(self):
        file = SeekIO(self.data)
        obj = self.Structure.load(file, eager=False)

        self.assertEqual(obj.a, b'a')
        self.assertEqual(obj.b, b'b')
        self.assertEqual(obj.c, b'c')

        self.assertEqual(file.seeks, [0, 1, 2])

    def test_lazy_random_access(self):
        file = SeekIO(self.data)
        obj = self.Structure.load(file, eager=False)

        self.assertEqual(obj.b, b'b')
        self.assertEqual(obj.c, b'c')
        self.assertEqual(obj.a, b'a')

        self.assertEqual(file.seeks, [1, 2, 0])
