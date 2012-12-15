from gettext import gettext as _

from steel.fields import Field

__all__ = ['Object']


class Object(Field):
    def __init__(self, structure, *args, **kwargs):
        self.structure = structure
        super(Object, self).__init__(*args, size=structure.size, **kwargs)

    def encode(self, value):
        value = value.dumps()
        return super(Object, self).encode(value)

    def decode(self, value):
        value = self.structure.loads(value)
        return super(Object, self).decode(value)
