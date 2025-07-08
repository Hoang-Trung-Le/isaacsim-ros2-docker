from __future__ import annotations
import yarl._quoting_c
import typing
import _cython_3_0_11

__all__ = [
    "ascii_letters",
    "digits",
    "i"
]


class _Quoter():
    """
    _Quoter(unicode safe=u'', *, unicode protected=u'', bool qs=False, bool requote=True)
    """
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
class _Unquoter():
    """
    _Unquoter(ignore=u'', *, unsafe=u'', qs=False)
    """
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
__pyx_unpickle__Quoter: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle__Quoter>
__pyx_unpickle__Unquoter: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle__Unquoter>
__test__ = {}
ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
i = 127
