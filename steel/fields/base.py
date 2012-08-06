from gettext import gettext as _

from steel.base import NameAwareOrderedDict

__all__ = ['Field']
NotProvided = object()


class Field:
    def __init__(self, label='', *, size, offset=0, default=NotProvided):
        self.label = label
        self.size = size
        self.offset = offset
        self.default = default

    def seek(self, file):
        file.seek(self.offset)

    def read(self, file):
        # If the size can be determined easily, read
        # that number of bytes and return it directly.
        if self.size is not None:
            data = file.read(self.size)
            if len(data) < size:
                # Can't read enough data from the stream to decode the field
                raise EOFError
            return data

        # Otherwise, the field needs to supply its own
        # technique for determining how much data to read.
        raise NotImplementedError()

    def set_name(self, name):
        self.name = name
        label = self.label or name.replace('_', ' ')
        self.label = label.title()

    def attach_to_class(self, cls):
        cls._fields[self.name] = self

    def __get__(self, instance, owner):
        if not instance:
            return self

        if self.name not in instance.__dict__:
            try:
                self.seek(instance._file)
                data = self.read(instance._file)
            except EOFError:
                if self.default is not NotProvided:
                    return self.default
                raise AttributeError(_('Attribute %r has no data') % self.name)
            instance._raw_values[self.name] = data
            instance.__dict__[self.name] = self.decode(data)

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        instance._raw_values[self.name] = self.encode(value)

    def __repr__(self):
        if hasattr(self, 'name'):
            return '<%s: %s>' % (self.name, type(self).__name__)
        else:
            return '<%s>' % type(self).__name__
