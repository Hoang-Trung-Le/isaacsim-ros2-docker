from __future__ import annotations
import frozenlist._frozenlist
import typing
from collections.abc import MutableSequence
import _cython_3_0_11
import sys
import types

__all__ = [
    "FrozenList",
    "MutableSequence",
    "sys",
    "types"
]


class FrozenList():
    """
    FrozenList(items=None)
    """
    __pyx_vtable__: typing.Any  # PyCapsule()
    frozen: getset_descriptor # value = <attribute 'frozen' of 'frozenlist._frozenlist.FrozenList' objects>
    pass
__pyx_unpickle_FrozenList: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_FrozenList>
__test__ = {}
sys = sys
types = types
