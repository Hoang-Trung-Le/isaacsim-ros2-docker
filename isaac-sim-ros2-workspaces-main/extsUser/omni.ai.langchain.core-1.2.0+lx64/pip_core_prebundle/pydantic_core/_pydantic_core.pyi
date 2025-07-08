from __future__ import annotations
import pydantic_core._pydantic_core
import typing
import datetime

__all__ = [
    "ArgsKwargs",
    "MultiHostUrl",
    "PydanticCustomError",
    "PydanticKnownError",
    "PydanticOmit",
    "PydanticSerializationError",
    "PydanticSerializationUnexpectedValue",
    "PydanticUndefined",
    "PydanticUndefinedType",
    "PydanticUseDefault",
    "SchemaError",
    "SchemaSerializer",
    "SchemaValidator",
    "Some",
    "TzInfo",
    "Url",
    "ValidationError",
    "__version__",
    "_recursion_limit",
    "build_info",
    "build_profile",
    "from_json",
    "list_all_errors",
    "to_json",
    "to_jsonable_python",
    "validate_core_schema"
]


class ArgsKwargs():
    __hash__ = None
    args: member_descriptor # value = <member 'args' of 'pydantic_core._pydantic_core.ArgsKwargs' objects>
    kwargs: getset_descriptor # value = <attribute 'kwargs' of 'pydantic_core._pydantic_core.ArgsKwargs' objects>
    pass
class MultiHostUrl():
    fragment: getset_descriptor # value = <attribute 'fragment' of 'pydantic_core._pydantic_core.MultiHostUrl' objects>
    path: getset_descriptor # value = <attribute 'path' of 'pydantic_core._pydantic_core.MultiHostUrl' objects>
    query: getset_descriptor # value = <attribute 'query' of 'pydantic_core._pydantic_core.MultiHostUrl' objects>
    scheme: getset_descriptor # value = <attribute 'scheme' of 'pydantic_core._pydantic_core.MultiHostUrl' objects>
    pass
class PydanticCustomError(ValueError, Exception, BaseException):
    context: getset_descriptor # value = <attribute 'context' of 'pydantic_core._pydantic_core.PydanticCustomError' objects>
    message_template: getset_descriptor # value = <attribute 'message_template' of 'pydantic_core._pydantic_core.PydanticCustomError' objects>
    type: getset_descriptor # value = <attribute 'type' of 'pydantic_core._pydantic_core.PydanticCustomError' objects>
    pass
class PydanticKnownError(ValueError, Exception, BaseException):
    context: getset_descriptor # value = <attribute 'context' of 'pydantic_core._pydantic_core.PydanticKnownError' objects>
    message_template: getset_descriptor # value = <attribute 'message_template' of 'pydantic_core._pydantic_core.PydanticKnownError' objects>
    type: getset_descriptor # value = <attribute 'type' of 'pydantic_core._pydantic_core.PydanticKnownError' objects>
    pass
class PydanticOmit(Exception, BaseException):
    pass
class PydanticSerializationError(ValueError, Exception, BaseException):
    pass
class PydanticSerializationUnexpectedValue(ValueError, Exception, BaseException):
    pass
class PydanticUndefinedType():
    pass
class PydanticUseDefault(Exception, BaseException):
    pass
class SchemaError(Exception, BaseException):
    pass
class SchemaSerializer():
    pass
class SchemaValidator():
    title: member_descriptor # value = <member 'title' of 'pydantic_core._pydantic_core.SchemaValidator' objects>
    pass
class Some():
    __match_args__ = ('value',)
    value: getset_descriptor # value = <attribute 'value' of 'pydantic_core._pydantic_core.Some' objects>
    pass
class TzInfo(datetime.tzinfo):
    pass
class Url():
    fragment: getset_descriptor # value = <attribute 'fragment' of 'pydantic_core._pydantic_core.Url' objects>
    host: getset_descriptor # value = <attribute 'host' of 'pydantic_core._pydantic_core.Url' objects>
    password: getset_descriptor # value = <attribute 'password' of 'pydantic_core._pydantic_core.Url' objects>
    path: getset_descriptor # value = <attribute 'path' of 'pydantic_core._pydantic_core.Url' objects>
    port: getset_descriptor # value = <attribute 'port' of 'pydantic_core._pydantic_core.Url' objects>
    query: getset_descriptor # value = <attribute 'query' of 'pydantic_core._pydantic_core.Url' objects>
    scheme: getset_descriptor # value = <attribute 'scheme' of 'pydantic_core._pydantic_core.Url' objects>
    username: getset_descriptor # value = <attribute 'username' of 'pydantic_core._pydantic_core.Url' objects>
    pass
class ValidationError(ValueError, Exception, BaseException):
    title: getset_descriptor # value = <attribute 'title' of 'pydantic_core._pydantic_core.ValidationError' objects>
    pass
PydanticUndefined: pydantic_core._pydantic_core.PydanticUndefinedType # value = PydanticUndefined
__all__ = ['__version__', 'build_profile', 'build_info', '_recursion_limit', 'PydanticUndefined', 'PydanticUndefinedType', 'Some', 'SchemaValidator', 'ValidationError', 'SchemaError', 'PydanticCustomError', 'PydanticKnownError', 'PydanticOmit', 'PydanticUseDefault', 'PydanticSerializationError', 'PydanticSerializationUnexpectedValue', 'Url', 'MultiHostUrl', 'ArgsKwargs', 'SchemaSerializer', 'TzInfo', 'to_json', 'from_json', 'to_jsonable_python', 'list_all_errors', 'validate_core_schema']
__version__ = '2.27.1'
_recursion_limit = 255
build_info = 'profile=release pgo=false'
build_profile = 'release'
