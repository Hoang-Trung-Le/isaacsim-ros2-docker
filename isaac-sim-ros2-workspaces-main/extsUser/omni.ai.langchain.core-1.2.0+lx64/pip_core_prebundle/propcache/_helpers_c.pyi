from __future__ import annotations
import propcache._helpers_c
import typing
from types import GenericAlias
import _cython_3_0_11

__all__ = [
    "GenericAlias",
    "cached_property",
    "under_cached_property"
]


class cached_property():
    """
    cached_property(func)
    Use as a class method decorator.  It operates almost exactly like
        the Python `@property` decorator, but it puts the result of the
        method it decorates into the instance dict after the first call,
        effectively replacing the function it decorates with an instance
        variable.  It is, in Python parlance, a data descriptor.

        
    """
    func: getset_descriptor # value = <attribute 'func' of 'propcache._helpers_c.cached_property' objects>
    pass
class under_cached_property():
    """
    under_cached_property(wrapped)
    Use as a class method decorator.  It operates almost exactly like
        the Python `@property` decorator, but it puts the result of the
        method it decorates into the instance dict after the first call,
        effectively replacing the function it decorates with an instance
        variable.  It is, in Python parlance, a data descriptor.

        
    """
    wrapped: getset_descriptor # value = <attribute 'wrapped' of 'propcache._helpers_c.under_cached_property' objects>
    pass
__pyx_unpickle_cached_property: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_cached_property>
__pyx_unpickle_under_cached_property: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_under_cached_property>
__test__ = {}
