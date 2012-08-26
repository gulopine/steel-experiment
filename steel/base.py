import collections
from gettext import gettext as _


class NameAwareOrderedDict(collections.OrderedDict):
    """
    A custom namespace that not only orders its items, but can
    also make those items aware of their names immediately.
    It also helps maintain the list of fields in the stack.
    """

    def __setitem__(self, name, obj):
        super(NameAwareOrderedDict, self).__setitem__(name, obj)
        if hasattr(obj, 'set_name'):
            obj.set_name(name)


class StructureMetaclass(type):
    @classmethod
    def __prepare__(cls, name, bases, **options):
        return NameAwareOrderedDict()

    def __new__(cls, name, bases, attrs, **options):
        # Nothing to do here, but we need to make sure options
        # don't get passed in to type.__new__() itself.
        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs, **options):
        cls._fields = collections.OrderedDict()

        for name, attr in attrs.items():
            if hasattr(attr, 'attach_to_class'):
                attr.attach_to_class(cls)


class Structure(metaclass=StructureMetaclass):
    size = 0

    def __init__(self, *args, **kwargs):
        self._file = len(args) > 0 and args[0] or None
        self._mode = self._file and 'rb' or 'wb'

        if self._file and kwargs:
            raise TypeError(_('Cannot supply a file and attributes together'))

        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self):
        return _('<Binary Data>')

    def __repr__(self):
        return '<%s: %s>' % (type(self).__name__, self)
