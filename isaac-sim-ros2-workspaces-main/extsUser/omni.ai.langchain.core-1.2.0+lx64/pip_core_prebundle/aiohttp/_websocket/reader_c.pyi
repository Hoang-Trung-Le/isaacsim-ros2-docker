"""Reader for WebSocket protocol versions 13 and 8."""
from __future__ import annotations
import aiohttp._websocket.reader_c
import typing
from aiohttp.base_protocol import BaseProtocol
from aiohttp.streams import EofStream
from aiohttp._websocket.models import WSCloseCode
from aiohttp._websocket.models import WebSocketError
from aiohttp.compression_utils import ZLibDecompressor
from collections import deque
import _cython_3_0_11
import asyncio

__all__ = [
    "BaseProtocol",
    "Deque",
    "EofStream",
    "Final",
    "List",
    "Optional",
    "Set",
    "Tuple",
    "Union",
    "WSCloseCode",
    "WS_DEFLATE_TRAILING",
    "WebSocketDataQueue",
    "WebSocketError",
    "WebSocketReader",
    "ZLibDecompressor",
    "asyncio",
    "builtins",
    "deque",
    "int_",
    "set_exception"
]


class WebSocketDataQueue():
    """
    WebSocketDataQueue resumes and pauses an underlying stream.

        It is a destination for WebSocket data.
        
    """
    __pyx_vtable__: typing.Any  # PyCapsule()
    _buffer: getset_descriptor # value = <attribute '_buffer' of 'aiohttp._websocket.reader_c.WebSocketDataQueue' objects>
    _protocol: getset_descriptor # value = <attribute '_protocol' of 'aiohttp._websocket.reader_c.WebSocketDataQueue' objects>
    pass
class WebSocketReader():
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
Deque: typing._SpecialGenericAlias # value = typing.Deque
Final: typing._SpecialForm # value = typing.Final
List: typing._SpecialGenericAlias # value = typing.List
Optional: typing._SpecialForm # value = typing.Optional
Set: typing._SpecialGenericAlias # value = typing.Set
Tuple: typing._TupleType # value = typing.Tuple
Union: typing._SpecialForm # value = typing.Union
WS_DEFLATE_TRAILING: bytes # value = b'\x00\x00\xff\xff'
_EXC_SENTINEL: BaseException # value = BaseException()
__pyx_capi__: dict # value = {'READ_HEADER': <capsule object "unsigned int">, 'READ_PAYLOAD_LENGTH': <capsule object "unsigned int">, 'READ_PAYLOAD_MASK': <capsule object "unsigned int">, 'READ_PAYLOAD': <capsule object "unsigned int">, 'OP_CODE_CONTINUATION': <capsule object "unsigned int">, 'OP_CODE_TEXT': <capsule object "unsigned int">, 'OP_CODE_BINARY': <capsule object "unsigned int">, 'OP_CODE_CLOSE': <capsule object "unsigned int">, 'OP_CODE_PING': <capsule object "unsigned int">, 'OP_CODE_PONG': <capsule object "unsigned int">, 'UNPACK_LEN3': <capsule object "PyObject *">, 'UNPACK_CLOSE_CODE': <capsule object "PyObject *">, 'TUPLE_NEW': <capsule object "PyObject *">, 'WSMsgType': <capsule object "PyObject *">, 'WSMessage': <capsule object "PyObject *">, 'WS_MSG_TYPE_TEXT': <capsule object "PyObject *">, 'WS_MSG_TYPE_BINARY': <capsule object "PyObject *">, 'ALLOWED_CLOSE_CODES': <capsule object "PyObject *">, 'MESSAGE_TYPES_WITH_CONTENT': <capsule object "PyObject *">, 'EMPTY_FRAME': <capsule object "PyObject *">, 'EMPTY_FRAME_ERROR': <capsule object "PyObject *">}
__pyx_unpickle_WebSocketDataQueue: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_WebSocketDataQueue>
__pyx_unpickle_WebSocketReader: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_WebSocketReader>
__test__ = {}
_websocket_mask_cython: _cython_3_0_11.cython_function_or_method # value = <cyfunction _websocket_mask_cython>
asyncio = asyncio
builtins = builtins
int_ = int
