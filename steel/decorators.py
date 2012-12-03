"""
A collection of decorators to ease the production and use of some of the
methods used throughout the framework.
"""


class ClassProperty(object):
    """
    A variation of a standard property descriptor that executes the decorated
    function when the descriptor is accessed as a class attribute.
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)

    # __set__ and __delete__ don't fire when access on a class


def classproperty(func):
    return ClassProperty(func)
