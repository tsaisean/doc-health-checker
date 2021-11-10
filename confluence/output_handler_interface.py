import sys


class OutputHandlerMeta(type):
    """A OutputHandler metaclass"""

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        is_subclass = hasattr(subclass, 'print') and callable(subclass.print)

        if not is_subclass:
            print('Method "print" is not implemented for %s' % subclass.__class__.__name__, file=sys.stderr)

        return is_subclass


class OutputHandlerInterface(metaclass=OutputHandlerMeta):
    """This interface is used for concrete classes to inherit from.
    There is no need to define the OutputHandlerMeta methods as any class
    as they are implicitly made available via .__subclasscheck__().
    """
    pass
