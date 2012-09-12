from gettext import gettext as _

from steel.base import NameAwareOrderedDict

__all__ = ['Field']
NotProvided = object()


class Field:
    def __init__(self, label='', *, size, offset=None, map=None,
                 default=NotProvided):
        self.label = label
        self.size = size
        self.offset = offset
        self.map = map or {}
        self.inverse_map = dict(zip(self.map.values(), self.map.keys()))
        self.default = default

    def seek(self, file):
        file.seek(self.offset)

    def read(self, file):
        # If the size can be determined easily, read
        # that number of bytes and return it directly.
        if self.size is not None:
            data = file.read(self.size)
            if len(data) < self.size:
                # Can't read enough data from the stream to decode the field
                raise EOFError
            return data

        # Otherwise, the field needs to supply its own
        # technique for determining how much data to read.
        raise NotImplementedError()

    def set_name(self, name):
        self.name = name
        self.label = self.label or name.replace('_', ' ')

    def attach_to_class(self, cls):
        cls._fields[self.name] = self

        if self.offset is None:
            # Only set from the external offset if not supplied on the field
            self.offset = cls.size

        cls.size = self.offset + self.size

    def read_value(self, file):
        try:
            self.seek(file)
            data = self.read(file)
        except EOFError:
            if self.default is not NotProvided:
                return self.default
            raise ValueError(_('Attribute %r has no data') % self.name)

        return self.decode(data)

    def write_value(self, file, value=NotProvided):
        if value is NotProvided:
            if self.default is NotProvided:
                raise ValueError(_('Attribute %r has no value' % self.name))
            else:
                value = self.default

        self.seek(file)
        data = self.encode(value)
        file.write(data)

    def encode(self, value):
        if self.inverse_map:
            # Decode the value again according to the map
            if value in self.inverse_map:
                value = self.inverse_map[value]
            else:
                raise ValueError(_('%r is not a valid value' % value))

        return value

    def decode(self, value):
        if self.map:
            # Decode the value again according to the map
            if value in self.map:
                value = self.map[value]
            else:
                raise ValueError(_('%r is not a valid value' % value))

        return value

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s: %s>' % (self.name, type(self).__name__)
        else:
            return '<%s>' % type(self).__name__
