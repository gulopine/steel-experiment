class Fixed(object):
    "A mixin that ensures the presence of a predetermined value"

    def __init__(self, value, *args, **kwargs):
        self.value = value
        super(Fixed, self).__init__(*args, **kwargs)

    def encode(self, value):
        # Always encode the fixed value
        return super(Fixed, self).encode(self.value)

    def decode(self, value):
        value = super(Fixed, self).decode(value)

        # Check that the value matches what it should be
        if value != self.value:
            raise ValueError("Expected %r, got %r" % (self.value, value))

        return value
