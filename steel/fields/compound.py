from gettext import gettext as _

from steel.fields import Field

__all__ = ['Object', 'List']


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


class List(Field):
    def __init__(self, field, *args, size, **kwargs):
        self.field = field
        self.length = size
        super(List, self).__init__(*args, size=field.size * size, **kwargs)

    def encode(self, value):
        length = len(value)
        if length > self.length:
            raise ValueError(_('Too many %s objects to encode') % self.field.__class__.__name__)
        elif length < self.length:
            if self.field.has_default():
                value.extend(self.field.default for i in range(self.length - length))
            else:
                raise ValueError(_('Not enough %s objects to encode') % self.field.__class__.__name__)

        return b''.join(self.field.encode(v) for v in value)

    def decode(self, value):
        output = []
        for i in range(self.length):
            output.append(value[self.field.size * i:self.field.size * (i + 1)])

        return [self.field.decode(v) for v in output]
