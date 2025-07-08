from __future__ import annotations
import aiohttp._http_parser
import typing
from aiohttp.http_exceptions import BadHttpMessage
from aiohttp.http_exceptions import BadHttpMethod
from aiohttp.http_exceptions import BadStatusLine
from aiohttp.http_exceptions import ContentLengthError
from aiohttp.http_exceptions import InvalidHeader
from aiohttp.http_exceptions import InvalidURLError
from aiohttp.http_exceptions import LineTooLong
from aiohttp.http_exceptions import PayloadEncodingError
from aiohttp.http_exceptions import TransferEncodingError
import _cython_3_0_11
import aiohttp.hdrs
import aiohttp.http_writer
import aiohttp.streams

__all__ = [
    "HttpRequestParser",
    "HttpResponseParser",
    "RawRequestMessage",
    "RawResponseMessage"
]


class HttpRequestParser(HttpParser):
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
class HttpResponseParser(HttpParser):
    __pyx_vtable__: typing.Any  # PyCapsule()
    pass
class RawRequestMessage():
    chunked: getset_descriptor # value = <attribute 'chunked' of 'aiohttp._http_parser.RawRequestMessage' objects>
    compression: getset_descriptor # value = <attribute 'compression' of 'aiohttp._http_parser.RawRequestMessage' objects>
    headers: getset_descriptor # value = <attribute 'headers' of 'aiohttp._http_parser.RawRequestMessage' objects>
    method: getset_descriptor # value = <attribute 'method' of 'aiohttp._http_parser.RawRequestMessage' objects>
    path: getset_descriptor # value = <attribute 'path' of 'aiohttp._http_parser.RawRequestMessage' objects>
    raw_headers: getset_descriptor # value = <attribute 'raw_headers' of 'aiohttp._http_parser.RawRequestMessage' objects>
    should_close: getset_descriptor # value = <attribute 'should_close' of 'aiohttp._http_parser.RawRequestMessage' objects>
    upgrade: getset_descriptor # value = <attribute 'upgrade' of 'aiohttp._http_parser.RawRequestMessage' objects>
    url: getset_descriptor # value = <attribute 'url' of 'aiohttp._http_parser.RawRequestMessage' objects>
    version: getset_descriptor # value = <attribute 'version' of 'aiohttp._http_parser.RawRequestMessage' objects>
    pass
class RawResponseMessage():
    chunked: getset_descriptor # value = <attribute 'chunked' of 'aiohttp._http_parser.RawResponseMessage' objects>
    code: getset_descriptor # value = <attribute 'code' of 'aiohttp._http_parser.RawResponseMessage' objects>
    compression: getset_descriptor # value = <attribute 'compression' of 'aiohttp._http_parser.RawResponseMessage' objects>
    headers: getset_descriptor # value = <attribute 'headers' of 'aiohttp._http_parser.RawResponseMessage' objects>
    raw_headers: getset_descriptor # value = <attribute 'raw_headers' of 'aiohttp._http_parser.RawResponseMessage' objects>
    reason: getset_descriptor # value = <attribute 'reason' of 'aiohttp._http_parser.RawResponseMessage' objects>
    should_close: getset_descriptor # value = <attribute 'should_close' of 'aiohttp._http_parser.RawResponseMessage' objects>
    upgrade: getset_descriptor # value = <attribute 'upgrade' of 'aiohttp._http_parser.RawResponseMessage' objects>
    version: getset_descriptor # value = <attribute 'version' of 'aiohttp._http_parser.RawResponseMessage' objects>
    pass
ALLOWED_UPGRADES: frozenset # value = frozenset({'websocket'})
DEBUG = False
_EMPTY_PAYLOAD: aiohttp.streams.EmptyStreamReader # value = <EmptyStreamReader>
_HttpVersion10 = HttpVersion(major=1, minor=0)
_HttpVersion11 = HttpVersion(major=1, minor=1)
__all__ = ('HttpRequestParser', 'HttpResponseParser', 'RawRequestMessage', 'RawResponseMessage')
__pyx_unpickle_RawRequestMessage: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_RawRequestMessage>
__pyx_unpickle_RawResponseMessage: _cython_3_0_11.cython_function_or_method # value = <cyfunction __pyx_unpickle_RawResponseMessage>
__reduce_cython__: _cython_3_0_11.cython_function_or_method # value = <cyfunction HttpResponseParser.__reduce_cython__>
__setstate_cython__: _cython_3_0_11.cython_function_or_method # value = <cyfunction HttpResponseParser.__setstate_cython__>
__test__ = {}
hdrs = aiohttp.hdrs
i = 45
_CIMultiDict = multidict._multidict.CIMultiDict
_CIMultiDictProxy = multidict._multidict.CIMultiDictProxy
_DeflateBuffer = aiohttp.http_parser.DeflateBuffer
_HttpVersion = aiohttp.http_writer.HttpVersion
_StreamReader = aiohttp.streams.StreamReader
_URL = yarl.URL
