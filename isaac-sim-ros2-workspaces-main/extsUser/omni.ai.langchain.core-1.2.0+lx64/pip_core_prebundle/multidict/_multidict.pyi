from __future__ import annotations
import multidict._multidict
import typing

__all__ = [
    "CIMultiDict",
    "CIMultiDictProxy",
    "MultiDict",
    "MultiDictProxy",
    "getversion",
    "istr"
]


class CIMultiDict(MultiDict):
    """
    Dictionary with the support for duplicate case-insensitive keys.
    """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Return a copy of itself.
        """
    pass
class CIMultiDictProxy(MultiDictProxy):
    """
    Read-only proxy for CIMultiDict instance.
    """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Return copy of itself
        """
    __hash__ = None
    pass
class MultiDict():
    """
    Dictionary with the support for duplicate keys.
    """
    @staticmethod
    def add(*args, **kwargs) -> typing.Any: 
        """
        Add the key and value, not overwriting any previous value.
        """
    @staticmethod
    def clear(*args, **kwargs) -> typing.Any: 
        """
        Remove all items from MultiDict
        """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Return a copy of itself.
        """
    @staticmethod
    def extend(*args, **kwargs) -> typing.Any: 
        """
        Extend current MultiDict with more values.
        This method must be used instead of update.
        """
    @staticmethod
    def get(*args, **kwargs) -> typing.Any: 
        """
        Get first value matching the key.

        The method is alias for .getone().
        """
    @staticmethod
    def getall(*args, **kwargs) -> typing.Any: 
        """
        Return a list of all values matching the key.
        """
    @staticmethod
    def getone(*args, **kwargs) -> typing.Any: 
        """
        Get first value matching the key.
        """
    @staticmethod
    def items(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's items *(key, value) pairs).
        """
    @staticmethod
    def keys(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's keys.
        """
    @staticmethod
    def pop(*args, **kwargs) -> typing.Any: 
        """
        Remove the last occurrence of key and return the corresponding value.

        If key is not found, default is returned if given, otherwise KeyError is raised.
        """
    @staticmethod
    def popall(*args, **kwargs) -> typing.Any: 
        """
        Remove all occurrences of key and return the list of corresponding values.

        If key is not found, default is returned if given, otherwise KeyError is raised.
        """
    @staticmethod
    def popitem(*args, **kwargs) -> typing.Any: 
        """
        Remove and return an arbitrary (key, value) pair.
        """
    @staticmethod
    def popone(*args, **kwargs) -> typing.Any: 
        """
        Remove the last occurrence of key and return the corresponding value.

        If key is not found, default is returned if given, otherwise KeyError is raised.
        """
    @staticmethod
    def setdefault(*args, **kwargs) -> typing.Any: 
        """
        Return value for key, set value to default if key is not present.
        """
    @staticmethod
    def update(*args, **kwargs) -> typing.Any: 
        """
        Update the dictionary from *other*, overwriting existing keys.
        """
    @staticmethod
    def values(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's values.
        """
    __hash__ = None
    pass
class MultiDictProxy():
    """
    Read-only proxy for MultiDict instance.
    """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Return a copy of itself.
        """
    @staticmethod
    def get(*args, **kwargs) -> typing.Any: 
        """
        Get first value matching the key.

        The method is alias for .getone().
        """
    @staticmethod
    def getall(*args, **kwargs) -> typing.Any: 
        """
        Return a list of all values matching the key.
        """
    @staticmethod
    def getone(*args, **kwargs) -> typing.Any: 
        """
        Get first value matching the key.
        """
    @staticmethod
    def items(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's items *(key, value) pairs).
        """
    @staticmethod
    def keys(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's keys.
        """
    @staticmethod
    def values(*args, **kwargs) -> typing.Any: 
        """
        Return a new view of the dictionary's values.
        """
    __hash__ = None
    pass
class istr(str):
    """
    istr class implementation
    """
    pass
def getversion(*args, **kwargs) -> typing.Any:
    pass
