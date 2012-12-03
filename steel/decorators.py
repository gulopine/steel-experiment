"""
A collection of decorators to ease the production and use of some of the
methods used throughout the framework.
"""

import functools


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


class ClassInstanceMethod(object):
    """
    A descriptor that calls a function either as an instance method or as a
    class method, depending on where it was accessed. It gets called either
    way, but what it gets sent will vary depending on the context.
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        @functools.wraps(self.func)
        def wrapper(*args, **kwargs):
            if instance is None:
                return self.func(owner, *args, **kwargs)
            else:
                return self.func(owner, instance, *args, **kwargs)

        return wrapper


def classinstancemethod(func):
    return ClassInstanceMethod(func)
